"""A few files of a GitHub repository, frozen at one commit, without cloning or building it.

    python3 fetch.py tree OWNER/REPO [--ref REF] [--grep REGEX]
    python3 fetch.py get  OWNER/REPO PATH... --into DIR [--ref REF]

`tree` lists the repository's paths, to find the part worth showing. `get` resolves the ref to
one commit, downloads the paths at that commit, unchanged, and commits them in DIR, a git
repository it creates if needed. DIR then serves as an oracle's `repo`: build.py reads the
`excerpt.json` committed beside the files and names the origin in the page's footer
(`code of OWNER/REPO @ sha, excerpt`), not the local commit. A second `get` into the same DIR
adds files, and refuses another commit of the same repository: an excerpt is one snapshot.

Downloads go through `curl`, which honours the system's certificates where some tools do not.
TRUEPATH_GITHUB_API and TRUEPATH_GITHUB_RAW replace the two base URLs (a mirror, a test).
"""
import argparse
import json
import os
import pathlib
import re
import subprocess
import sys

API = os.environ.get("TRUEPATH_GITHUB_API", "https://api.github.com")
RAW = os.environ.get("TRUEPATH_GITHUB_RAW", "https://raw.githubusercontent.com")
EXCERPT = "excerpt.json"


class FetchFailed(Exception):
    """Said in plain words, without a traceback."""


def download(url):
    run = subprocess.run(["curl", "-sSfL", url], check=False, capture_output=True)
    if run.returncode:
        raise FetchFailed(f"cannot download {url}: {run.stderr.decode(errors='replace').strip()}")
    return run.stdout


def resolve(repo, ref):
    """The full sha the ref names now: everything after is read at that commit."""
    data = json.loads(download(f"{API}/repos/{repo}/commits/{ref}"))
    return data["sha"]


def tree(repo, ref, grep=None):
    sha = resolve(repo, ref)
    data = json.loads(download(f"{API}/repos/{repo}/git/trees/{sha}?recursive=1"))
    paths = [t["path"] for t in data["tree"] if t["type"] == "blob"]
    if data.get("truncated"):
        print("warning: the listing is truncated by GitHub; narrow it with --grep", file=sys.stderr)
    return sha, [p for p in paths if not grep or re.search(grep, p)]


def git(into, *args):
    run = subprocess.run(["git", "-C", str(into), *args], check=False, capture_output=True, text=True)
    if run.returncode:
        raise FetchFailed(f"git {args[0]} failed in {into}: {run.stderr.strip()}")
    return run.stdout.strip()


def get(repo, ref, paths, into):
    into = pathlib.Path(into)
    into.mkdir(parents=True, exist_ok=True)
    if not (into / ".git").exists():
        git(into, "init", "-q")
    record = into / EXCERPT
    excerpt = json.loads(record.read_text()) if record.exists() else {"repo": repo, "sha": None, "files": []}
    if excerpt["repo"] != repo:
        raise FetchFailed(f"{into} holds an excerpt of {excerpt['repo']}, not {repo}")
    sha = excerpt["sha"] or resolve(repo, ref)
    if excerpt["sha"] and ref not in (sha, sha[:len(ref)]) and resolve(repo, ref) != sha:
        raise FetchFailed(f"{into} is an excerpt of {repo} @ {sha[:7]}; {ref} names another commit. "
                          "Use another directory, or --ref " + sha[:7])
    for path in paths:
        dest = into / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(download(f"{RAW}/{repo}/{sha}/{path}"))
    excerpt.update(sha=sha, files=sorted(set(excerpt["files"]) | set(paths)))
    record.write_text(json.dumps(excerpt, indent=2) + "\n")
    git(into, "add", "--", EXCERPT, *paths)
    git(into, "-c", "user.name=truepath", "-c", "user.email=truepath@localhost", "-c", "commit.gpgsign=false",
        "commit", "-q", "--allow-empty", "-m", f"{len(paths)} file(s) of {repo} @ {sha[:7]}, unchanged")
    return sha


def main(argv=None):
    ap = argparse.ArgumentParser(description="A few files of a GitHub repository, frozen at one commit.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("tree", help="list the repository's paths")
    t.add_argument("repo")
    t.add_argument("--ref", default="HEAD")
    t.add_argument("--grep")
    g = sub.add_parser("get", help="download paths at one commit into a local git repository")
    g.add_argument("repo")
    g.add_argument("paths", nargs="+")
    g.add_argument("--into", required=True)
    g.add_argument("--ref", default="HEAD")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "tree":
            sha, paths = tree(args.repo, args.ref, args.grep)
            print(f"# {args.repo} @ {sha[:7]}, {len(paths)} path(s)")
            print("\n".join(paths))
        else:
            sha = get(args.repo, args.ref, args.paths, args.into)
            print(f"✓ {len(args.paths)} file(s) of {args.repo} @ {sha[:7]} in {args.into}")
    except FetchFailed as e:
        print(f"✗ {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
