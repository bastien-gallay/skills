"""spec.json -> one self-contained HTML simulation. Nothing is written unless every check passes.

    python3 build.py path/to/spec.json [-o out.html] [--export WORKTREE]

Verdicts come from the spec's `oracle` (the repository's own code, run on a frozen
`git archive` of a ref) or, without one, from `port` (a JS port run by node).
Geometry comes from layout.py, next to this file. Python 3.9+, standard library only.

The build is a line of steps, each handing the next what it made:

    read -> validate -> scenarios (plain, or grid cells) -> verdicts -> templates
         -> checks C1..C15 -> page data -> page

The spec is read, never rewritten: what the page receives is built on purpose by
`page_data`, so nothing of the spec reaches it by accident.
"""
import argparse
import copy
import hashlib
import html
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field

SCRIPTS = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))
from layout import CHAR_W, layout  # noqa: E402

RUNTIME = SCRIPTS / "runtime.html"
WORKDIR = ".truepath"  # next to the spec: oracle snapshots and their in/out files
MAX_KINDS = 4
MIN_AIR = 8  # px a label must keep inside its box, both sides together (C6)


class UnreadableSpec(Exception):
    """The spec, or the logic it names, cannot be used: said in plain words, without a traceback."""


class ChecksFailed(Exception):
    """The spec is readable but breaks checks: `args[0]` lists the violations."""


# ---- reading the spec

class Problems(list):
    """Shape errors, gathered so that one run names them all."""

    def keys(self, obj, required, where):
        if not isinstance(obj, dict):
            self.append(f"{where}: expected an object")
            return False
        missing = [k for k in required if k not in obj]
        if missing:
            self.append(f"{where}: missing {', '.join(missing)}")
        return not missing

    def typed(self, obj, key, kind, where, name):
        """An optional key, when present, has the expected type."""
        if key in obj and not isinstance(obj[key], kind):
            self.append(f"{where}: `{key}` must be {name}")
            return False
        return key in obj

    def raise_if_any(self):
        if self:
            raise UnreadableSpec("\n".join(self))


def validate(spec, specdir, exporting=False):
    """What can be said before any logic runs. Reads the spec, changes nothing."""
    p = Problems()
    if not p.keys(spec, ["title", "nodes", "edges"], "spec"):
        p.raise_if_any()
    for key, kind, name in (("nodes", list, "a list"), ("edges", list, "a list"), ("kinds", dict, "an object"),
                            ("panel", list, "a list"), ("scenarios", list, "a list"), ("pairs", list, "a list"),
                            ("grid", dict, "an object"), ("oracle", dict, "an object"), ("export", dict, "an object")):
        p.typed(spec, key, kind, "spec", name)
    p.raise_if_any()

    p.typed(spec, "credit", bool, "spec", "true or false")
    if spec.get("lang", "en") not in ("en", "fr"):
        p.append(f"spec: lang is {spec['lang']!r}, expected en or fr")
    if "oracle" in spec:
        o = spec["oracle"]
        if p.keys(o, ["repo", "ref", "paths", "cwd", "cmd"], "oracle"):
            p.typed(o, "paths", list, "oracle", "a list")
            p.typed(o, "link", dict, "oracle", "an object {path in the snapshot: path in the repository}")
            p.typed(o, "files", dict, "oracle", "an object {path in the snapshot: file next to the spec}")
            for dest, src in (o.get("files") or {}).items() if isinstance(o.get("files"), dict) else ():
                if not (specdir / str(src)).is_file():
                    p.append(f"oracle.files: {src} not found next to the spec")
            validate_doubles(o, p)
    elif "port" in spec:
        if not (specdir / str(spec["port"])).is_file():
            p.append(f"port: {spec['port']} not found next to the spec")
    else:
        p.append("spec: neither `oracle` nor `port`, so nothing computes the verdicts")
    if exporting:
        if "export" not in spec:
            p.append("--export needs an `export` key in the spec: {dir, fixture, assert}")
        elif p.keys(spec["export"], ["dir", "fixture", "assert"], "export"):
            p.typed(spec["export"], "assert", list, "export", "a list of verdict fields")

    ids = []
    for i, n in enumerate(spec["nodes"]):
        if p.keys(n, ["id", "label"], f"nodes[{i}]"):
            if not isinstance(n["id"], str) or not isinstance(n["label"], str):
                p.append(f"nodes[{i}]: id and label must be text")
                continue
            ids.append(n["id"])
            if n.get("role") not in (None, "decision"):
                p.append(f"nodes[{i}]: role is {n['role']!r}; the only role to declare is \"decision\"")
    if not spec["nodes"]:
        p.append("nodes: at least one node is needed")
    for d in sorted({i for i in ids if ids.count(i) > 1}):
        p.append(f"nodes: id {d} is used twice")
    for i, e in enumerate(spec["edges"]):
        if not isinstance(e, list) or len(e) not in (2, 3) or not all(isinstance(x, str) for x in e):
            p.append(f"edges[{i}]: expected [from, to, label], all text")
            continue
        for end in e[:2]:
            if end not in ids:
                p.append(f"edges[{i}]: {end} is not a node")
    pairs = [tuple(e[:2]) for e in spec["edges"] if isinstance(e, list) and len(e) in (2, 3)]
    for a, b in sorted({x for x in pairs if pairs.count(x) > 1}):
        p.append(f"edges: {a} -> {b} is declared twice; one edge per pair of nodes, its label naming every case "
                 "(\"same or absent\")")
    for k, v in spec.get("kinds", {}).items():
        p.keys(v, ["label", "color"], f"kinds.{k}")
    for i, r in enumerate(spec.get("panel", [])):
        where = f"panel[{i}]"
        if p.keys(r, ["label", "value", "at"], where):
            if not isinstance(r["value"], str):
                p.append(f"{where}: `value` must be a path such as inputs.x or verdict.y")
            if r["at"] != "last" and not (isinstance(r["at"], int) and not isinstance(r["at"], bool) and r["at"] >= 0):
                p.append(f"{where}: `at` is {r['at']!r}, expected a step index or \"last\"")
            p.typed(r, "labels", dict, where, "an object {value: what to show}")
            p.typed(r, "digits", int, where, "a number of digits")
            p.typed(r, "series", bool, where, "true or false")

    scenarios = spec.get("scenarios", [])
    for i, s in enumerate(scenarios):
        if p.keys(s, ["id", "tab", "summary", "inputs", "steps"], f"scenarios[{i}]"):
            where = f"scenario {s['id']}"
            p.typed(s, "inputs", dict, where, "an object")
            p.typed(s, "expect", dict, where, "an object {verdict field: value}")
            validate_steps(s["steps"], where, p)
    seen = [s.get("id") for s in scenarios if isinstance(s, dict)]
    for d in sorted({str(i) for i in seen if i is not None and seen.count(i) > 1}):
        p.append(f"scenarios: id {d} is used twice")
    for i, pair in enumerate(spec.get("pairs", [])):
        p.keys(pair, ["before", "after", "tab", "summary"], f"pairs[{i}]")
    if "grid" in spec:
        if scenarios or spec.get("pairs"):
            p.append("spec: a grid page shows only its cells; move `scenarios` and `pairs` to another spec")
        validate_grid(spec["grid"], p)
    elif not scenarios:
        p.append("spec: no scenario and no grid, so there is nothing to play")
    validate_doubts(spec, p)
    p.raise_if_any()


DOUBLE_KINDS = ("stub", "fake", "mock")


def validate_doubles(o, p):
    """What the oracle runs is a unit, its collaborators replaced: the reader is told which ones.

    `files` brings code that is not the ref's; the spec says which collaborator each double
    stands in for, or `doubles: []` when the files only drive the run."""
    if "doubles" not in o:
        if o.get("files"):
            p.append("oracle.files brings code that is not the ref's: list in oracle.doubles the collaborators "
                     "it stands in for, as [{name, kind, replaces}], or [] if it only drives the run")
        return
    if not isinstance(o["doubles"], list):
        p.append("oracle.doubles: expected a list [{name, kind, replaces}]")
        return
    for i, d in enumerate(o["doubles"]):
        if p.keys(d, ["name", "kind", "replaces"], f"oracle.doubles[{i}]") and d["kind"] not in DOUBLE_KINDS:
            p.append(f"oracle.doubles[{i}]: kind is {d['kind']!r}, expected stub, fake or mock")


def validate_doubts(spec, p):
    if not p.typed(spec, "doubts", list, "spec", "a list [{id, question, scenarios, answer?, assumed?}]") or "doubts" not in spec:
        return
    for i, d in enumerate(spec["doubts"]):
        if p.keys(d, ["id", "question", "scenarios"], f"doubts[{i}]"):
            p.typed(d, "scenarios", list, f"doubt {d['id']}", "a list of scenario or case ids")


def validate_steps(steps, where, p):
    if not isinstance(steps, list):
        p.append(f"{where}: steps must be a list")
        return
    for i, st in enumerate(steps):
        if p.keys(st, ["hop", "message", "caption"], f"{where}, step {i}"):
            if not (isinstance(st["hop"], list) and len(st["hop"]) >= 2 and all(isinstance(h, str) for h in st["hop"])):
                p.append(f"{where}, step {i}: hop must be [from, to], two node ids, or [from, via…, to]")
            if not isinstance(st["message"], str) or not isinstance(st["caption"], str):
                p.append(f"{where}, step {i}: message and caption must be text")


def validate_grid(g, p):
    if not p.keys(g, ["baseline", "cases", "hover"], "grid"):
        return
    if not isinstance(g["hover"], list) or not isinstance(g["cases"], list):
        p.append("grid: `cases` and `hover` must be lists")
        return
    if "show" not in g and not g["hover"]:
        p.append("grid: name the panel row a cell shows (`show`), or at least one in `hover`")
    if "questions" in g:
        p.keys(g["baseline"], ["id", "label"], "grid.baseline")
        for i, q in enumerate(g["questions"] if isinstance(g["questions"], list) else []):
            if p.keys(q, ["id", "text", "options", "cases"], f"grid.questions[{i}]"):
                for j, o in enumerate(q["options"]):
                    p.keys(o, ["id", "label"], f"grid.questions[{i}].options[{j}]")
    elif "variants" in g:
        known = set()
        for i, v in enumerate(g["variants"] if isinstance(g["variants"], list) else []):
            if p.keys(v, ["id", "label"], f"grid.variants[{i}]"):
                known.add(v["id"])
        if not isinstance(g["baseline"], str) or g["baseline"] not in known:
            p.append("grid: with `variants`, `baseline` is the id of one of them")
    else:
        p.append("grid: neither `questions` nor `variants`")
    for i, c in enumerate(g["cases"]):
        if p.keys(c, ["id", "label", "summary", "origin", "inputs"], f"grid.cases[{i}]"):
            if "steps" not in c and "steps" not in g:
                p.append(f"grid case {c['id']}: no steps, and the grid shares none")
            validate_steps(c.get("steps") or g.get("steps") or [], f"grid case {c['id']}", p)


# ---- where verdicts come from

def git(repo, *args, text=True):
    run = subprocess.run(["git", "-C", str(repo), *args], check=False, capture_output=True, text=text)
    if run.returncode:
        err = run.stderr if text else run.stderr.decode(errors="replace")
        raise UnreadableSpec(f"oracle: git {args[0]} failed in {repo}:\n{err.strip()}")
    return run.stdout.strip() if text else run.stdout


def snapshot(o, workdir, specdir):
    """A frozen copy of the ref, never the live checkout: the branch may move during the build.

    `link` and `files` both read {path in the snapshot: where it comes from}."""
    repo = (specdir / o["repo"]).resolve()
    sha = git(repo, "rev-parse", "--short", o["ref"])
    what = hashlib.sha1(json.dumps([o["paths"], o.get("link", {})], sort_keys=True).encode()).hexdigest()[:8]
    snap = workdir / f"{sha}-{what}"  # other paths of the same commit are another snapshot
    if not snap.exists():
        archive = git(repo, "archive", sha, *o["paths"], text=False)
        snap.mkdir(parents=True)
        untar = subprocess.run(["tar", "-x", "-C", str(snap)], check=False, input=archive, capture_output=True)
        if untar.returncode:
            shutil.rmtree(snap, ignore_errors=True)
            raise UnreadableSpec("oracle: cannot unpack the snapshot:\n" + untar.stderr.decode(errors="replace").strip())
        for dest, src in o.get("link", {}).items():
            (snap / dest).symlink_to(repo / src)
    for dest, src in o.get("files", {}).items():
        (snap / dest).parent.mkdir(parents=True, exist_ok=True)
        (snap / dest).write_bytes((specdir / src).read_bytes())  # a lockfile, a binary fixture: copied as they are
    return sha, snap


def run_oracle(spec, scenarios, specdir):
    o = spec["oracle"]
    workdir = specdir / WORKDIR
    workdir.mkdir(exist_ok=True)
    sha, snap = snapshot(o, workdir, specdir)
    io_in, io_out = workdir / "in.json", workdir / "out.json"
    io_in.write_text(json.dumps([s["inputs"] for s in scenarios]), encoding="utf-8")
    io_out.unlink(missing_ok=True)
    try:
        # cmd runs without a shell: build.py itself puts the spec's folder where an argument names it
        cmd = [str(a).replace("$TRUEPATH_SPEC_DIR", str(specdir)) for a in o["cmd"]]
        run = subprocess.run(cmd, cwd=snap / o["cwd"], check=False, capture_output=True, text=True,
                             env={**os.environ, "TRUEPATH_ORACLE_IN": str(io_in), "TRUEPATH_ORACLE_OUT": str(io_out),
                                  "TRUEPATH_SPEC_DIR": str(specdir)})  # a dependency cache lives there, not in the snapshot
    except OSError as e:
        raise UnreadableSpec(f"oracle: cannot run {o['cmd']!r}: {e}") from e
    if run.returncode or not io_out.exists():
        raise UnreadableSpec("oracle failed:\n" + run.stdout[-3000:] + run.stderr[-3000:])
    return read_verdicts(io_out.read_text(encoding="utf-8"), "oracle"), oracle_label(o, sha, (specdir / o["repo"]).resolve(),
                                                                                    spec.get("lang", "en") == "en")


def oracle_label(o, sha, repo, en):
    """Whose code ran, at which commit, and what stood in for the rest.

    A repository made by fetch.py is an excerpt of another one: its `excerpt.json` names the
    origin, and the footer names that, not the local commit holding the copy."""
    excerpt = subprocess.run(["git", "-C", str(repo), "show", f"{sha}:excerpt.json"], check=False,
                             capture_output=True, text=True)
    if excerpt.returncode == 0:
        e = json.loads(excerpt.stdout)
        n = len([f for f in e["files"] if any(f == p.rstrip("/") or f.startswith(p.rstrip("/") + "/") for p in o["paths"])])
        # what the snapshot holds: files fetched only to be read are not what ran
        label = (f"code of {e['repo']} @ {e['sha'][:7]}, excerpt of {n} file{'s' * (n > 1)}" if en else
                 f"code de {e['repo']} @ {e['sha'][:7]}, extrait de {n} fichier{'s' * (n > 1)}")
    else:
        label = f"code of {o['ref']} @ {sha}" if en else f"code de {o['ref']} @ {sha}"
    if o.get("files"):  # what the spec brings is not the ref's code: the footer names it
        brought = ", ".join(sorted(str(src) for src in o["files"].values()))
        label += f" + from the spec: {brought}" if en else f" + apporté par le spec : {brought}"
    if o.get("doubles"):
        names = ", ".join(f"{d['name']} ({d['kind']})" for d in o["doubles"])
        label += f" · doubles: {names}" if en else f" · doublures : {names}"
    return label


def run_port(spec, scenarios, specdir):
    if not shutil.which("node"):
        raise UnreadableSpec("port: a JS port needs Node.js, and `node` is not on the PATH")
    script = ("const {decide}=require(process.argv[1]);"
              "const s=JSON.parse(require('fs').readFileSync(0,'utf8'));"
              "process.stdout.write(JSON.stringify(s.map(x=>decide(x))))")
    run = subprocess.run(["node", "-e", script, str(specdir / spec["port"])],
                         input=json.dumps([s["inputs"] for s in scenarios]),
                         check=False, capture_output=True, text=True)
    if run.returncode:
        raise UnreadableSpec(f"port: {spec['port']} failed:\n{run.stderr.strip()[-3000:]}")
    label = f"port {spec['port']}" if spec.get("lang", "en") == "en" else f"portage {spec['port']}"
    return read_verdicts(run.stdout, "port"), label


def read_verdicts(text, who):
    try:
        verdicts = json.loads(text)
    except json.JSONDecodeError as e:
        raise UnreadableSpec(f"{who}: the verdicts are not JSON ({e})") from e
    if not isinstance(verdicts, list) or not all(isinstance(v, dict) for v in verdicts):
        raise UnreadableSpec(f"{who}: expected a JSON array of verdict objects, one per scenario")
    return verdicts


def provenance(basis):
    """What a `basis` text claims: `code: …`, `port: …`, `double: …` (a stub or a fake answered), or anything else, a definition.

    The word before the colon decides, not a prefix: "code of conduct" is a definition."""
    m = re.match(r"\s*(code|port|double)\s*:", str(basis))
    return m.group(1) if m else "definition"


# ---- scenarios: the plain ones, or the cells of a grid

def answer_sets(questions, chosen=()):
    """Every coherent set of answers: a question asked only `if` earlier answers hold."""
    if not questions:
        yield list(chosen)
        return
    q, rest = questions[0], questions[1:]
    picked = {qq["id"]: o["id"] for qq, o in chosen}
    if all(picked.get(k) == v for k, v in q.get("if", {}).items()):
        for o in q["options"]:
            yield from answer_sets(rest, (*chosen, (q, o)))
    else:
        yield from answer_sets(rest, chosen)


def variants_from_questions(g):
    """Questions -> variants (one per coherent set of answers) and one matrix section per question."""
    base = g["baseline"]
    variants = [{"id": base["id"], "label": base["label"], "short": base.get("short", base["label"]),
                 "note": base.get("note"), "inputs": base.get("inputs", {}), "choice": {}}]
    for chosen in answer_sets(g["questions"]):
        inputs = {}
        for _, o in chosen:
            inputs.update(o.get("inputs", {}))
        variants.append({"id": "+".join(o["id"] for _, o in chosen), "short": " · ".join(o["id"] for _, o in chosen),
                         "label": " · ".join(f"{o['id']} {o['label']}" for _, o in chosen), "note": None,
                         "inputs": inputs, "choice": {q["id"]: o["id"] for q, o in chosen}})
    sections = []
    for q in g["questions"]:
        columns = [{"variant": base["id"], "head": base["label"], "short": base.get("short", base["label"]), "sameAnswer": []}]
        for o in q["options"]:
            same = [v["id"] for v in variants[1:] if v["choice"].get(q["id"]) == o["id"]]
            if not same:
                raise UnreadableSpec(f"grid: answer {o['id']} of {q['id']} is in no coherent set of answers")
            # the column plays the first such set: the other questions at their first answer
            columns.append({"variant": same[0], "head": f"{o['id']} · {o['label']}", "short": o["id"], "sameAnswer": same})
        sections.append({"id": q["id"], "text": q["text"], "columns": columns, "cases": q["cases"]})
    return base["id"], variants, sections


def expand_grid(g):
    """A grid is cases x variants (the rules compared); each cell is a scenario.

    Variants are either listed, or derived from `questions`: then each answer set is a variant
    and the matrix shows one section per question. Returns the grid as the build sees it,
    and its cells."""
    if "questions" in g:
        baseline, variants, sections = variants_from_questions(g)
    else:
        baseline = g["baseline"]
        variants = [{"id": v["id"], "label": v["label"], "short": v.get("short", v["label"].split(" ")[0]),
                     "note": v.get("note"), "inputs": v.get("inputs", {})} for v in g["variants"]]
        sections = [{"id": None, "text": None, "cases": [c["id"] for c in g["cases"]],
                     "columns": [{"variant": v["id"], "head": v["label"], "short": v["short"], "note": v["note"],
                                  "sameAnswer": []} for v in variants]}]
    grid = {"baseline": baseline, "variants": variants, "sections": sections, "cases": g["cases"],
            "show": g.get("show", g["hover"][0] if g["hover"] else None), "hover": g["hover"],
            "summary": g.get("summary", "")}
    cells = [{
        "id": f"{c['id']}/{v['id']}", "case": c["id"], "variant": v["id"], "answer": v["short"],
        "tab": c["label"], "summary": c["summary"], "origin": c["origin"],
        "inputs": {**c["inputs"], **v["inputs"]},
        "expect": g.get("expect", {}).get(c["id"], {}).get(v["id"], {}),
        "steps": copy.deepcopy(c.get("steps") or g["steps"]),
    } for c in g["cases"] for v in variants]
    return grid, cells


# ---- what a value looks like

def resolve(path, scenario):
    """inputs.a.b: a null on the way reads as null (shown "null"), a missing key is C9's to report."""
    cur = scenario
    for part in path.split("."):
        if cur is None:
            return None
        if not isinstance(cur, dict) or part not in cur:
            raise KeyError(path)
        cur = cur[part]
    return cur


def shown(row, value):
    """A value as the page shows it. The only place that decides: the page receives the result."""
    labels = row.get("labels", {})

    def one(x):
        text = json.dumps(x) if isinstance(x, bool) or x is None else str(x)  # true, false, null
        if row.get("digits") and text.isdigit():
            text = text.zfill(row["digits"])
        return str(labels.get(text, text))
    if isinstance(value, list):
        return " · ".join(map(one, value)) if value else str(labels.get("[]", "—"))
    return one(value)


def fill_templates(scenarios, panel):
    """Step text and hops may quote {inputs.x} or {verdict.y}: the verdict is known only after the logic ran.

    A quoted value is shown as the first panel row reading the same path shows it."""
    pat = re.compile(r"\{((?:inputs|verdict)\.[A-Za-z0-9_.]+)\}")
    row_reading = {}
    for row in panel:
        row_reading.setdefault(row["value"], row)
    for sc in scenarios:
        def as_shown(m, sc=sc):
            return shown(row_reading.get(m.group(1), {}), resolve(m.group(1), sc))

        def raw(m, sc=sc):
            return str(resolve(m.group(1), sc))
        try:
            for st in sc["steps"]:
                st["message"] = pat.sub(as_shown, st["message"])
                st["caption"] = pat.sub(as_shown, st["caption"])
                st["hop"] = [pat.sub(raw, h) for h in st["hop"]]
        except KeyError as e:
            raise UnreadableSpec(f"scenario {sc['id']}: a step quotes {{{e.args[0]}}}, which is missing") from e


def panel_rows(scenario, panel, in_grid):
    """The panel as one scenario fills it: each row already shown, with where its value comes from."""
    rows = []
    basis = scenario["verdict"].get("basis") if isinstance(scenario["verdict"].get("basis"), dict) else {}
    for row in panel:
        at = len(scenario["steps"]) - 1 if row["at"] == "last" else row["at"]  # "last": each scenario's own last step
        out = {"label": row["label"], "at": at, "compared": bool(row.get("compared"))}
        if in_grid and row["value"] == "answer":
            out["answer"] = True  # named by the page: an answer is called as the open question calls it
        else:
            try:
                value = resolve(row["value"], scenario)
                if row.get("series") and isinstance(value, list) and value:
                    out["series"] = [shown(row, v) for v in value]  # one value per step from `at`, the last one stays
                    out["shown"] = out["series"][-1]
                else:
                    out["shown"] = None if row.get("series") else shown(row, value)  # C9 says so
            except KeyError:
                out["shown"] = None  # C9 says so
            head, _, rest = row["value"].partition(".")
            said = basis.get(rest.split(".")[0]) if head == "verdict" else None
            if said:
                out["provenance"] = {"kind": provenance(said), "text": str(said)}
        rows.append(out)
    return rows


# ---- checks

@dataclass
class Subject:
    """What the checks look at: the spec as written, its scenarios with their verdicts and rows, the geometry."""
    spec: dict
    scenarios: list
    grid: dict
    geo: dict
    edges: set = field(init=False)
    sources: set = field(init=False)
    by_id: dict = field(init=False)

    def __post_init__(self):
        self.edges = {(e[0], e[1]) for e in self.spec["edges"]}
        self.sources = {n["id"] for n in self.spec["nodes"]} - {b for _, b in self.edges}
        self.by_id = {s["id"]: s for s in self.scenarios}

    @property
    def panel(self):
        return self.spec.get("panel", [])

    def hops(self, s):
        """Every edge the path takes, in order: a step through [a, b, c] takes a->b, then b->c."""
        return [(h[k], h[k + 1]) for st in s["steps"] for h in [st["hop"]] for k in range(len(h) - 1)]


def c1_hops_are_edges(b):
    for s in b.scenarios:
        for h in b.hops(s):
            if h not in b.edges:
                yield f"{s['id']}: hop {h} is not an edge"


def c2_path_is_unbroken_from_a_source(b):
    for s in b.scenarios:
        hops = b.hops(s)
        if not hops:
            yield f"{s['id']}: no step, so there is no path to play"
            continue
        for (a, x), (y, d) in zip(hops, hops[1:]):
            if x != y:
                yield f"{s['id']}: path breaks between {a}->{x} and {y}->{d}"
        if hops[0][0] not in b.sources:
            yield f"{s['id']}: path starts at {hops[0][0]}, not at a source"


def c3_expect_is_what_the_logic_gives(b):
    for s in b.scenarios:
        for key, want in s.get("expect", {}).items():
            if s["verdict"].get(key) != want:
                yield f"{s['id']}: the logic gives {key}={s['verdict'].get(key)!r}, the scenario declares {want!r}"


def c4_path_ends_at_the_outcome(b):
    for s in b.scenarios:
        hops = b.hops(s)
        if "outcome" not in s["verdict"]:
            yield f"{s['id']}: the logic gives no `outcome`, so nothing ties the path to it"
        elif hops and hops[-1][1] != s["verdict"]["outcome"]:
            yield f"{s['id']}: path ends at {hops[-1][1]}, the logic ends at {s['verdict']['outcome']}"


def c5_colour_means_an_outcome_kind(b):
    kinds = b.spec.get("kinds", {})
    used = {n["kind"] for n in b.spec["nodes"] if "kind" in n}
    if not used <= set(kinds):
        yield f"kinds without a legend entry: {sorted(used - set(kinds))}"
    if len(kinds) > MAX_KINDS:
        yield f"{len(kinds)} colour kinds > {MAX_KINDS}"
    for n in b.spec["nodes"]:
        if not any(a == n["id"] for a, _ in b.edges) and "kind" not in n:
            yield f"outcome {n['id']} has no kind, so its colour means nothing"


def c6_labels_fit_their_box(b):
    for nid, g in b.geo["nodes"].items():
        for line in g["labelLines"]:
            if len(line) * CHAR_W > g["w"] - MIN_AIR:
                yield f"label of {nid} overflows: {line!r} needs {len(line) * CHAR_W:.0f}px in {g['w']}px"


def c7_scenarios_say_where_they_come_from(b):
    for s in b.scenarios:
        o = s.get("origin") if isinstance(s.get("origin"), dict) else {}
        if o.get("kind") not in ("real", "illustrative") or not str(o.get("text", "")).strip():
            yield f"{s['id']}: origin must say real or illustrative, and where it comes from"


def c8_pairs_name_known_scenarios(b):
    """A pair may differ in length: the page keeps the side that has arrived on its outcome."""
    for p in b.spec.get("pairs", []):
        for side in ("before", "after"):
            if p[side] not in b.by_id:
                yield f"pair {p['tab']}: {side} names unknown scenario {p[side]}"


def c9_panel_rows_resolve(b):
    for s in b.scenarios:
        for row, filled in zip(b.panel, s["rows"]):
            if "answer" not in filled and filled["shown"] is None:
                yield f"{s['id']}: panel row {row['label']!r} reads {row['value']}, which is " \
                      + ("not a list with one value per step" if row.get("series") else "missing")


def c10_matrix_shows_panel_rows(b):
    if b.grid:
        labels = {r["label"] for r in b.panel}
        for name in dict.fromkeys([b.grid["show"], *b.grid["hover"]]):
            if name not in labels:
                yield f"matrix cell {name!r} is not a panel row label"


def c11_a_section_depends_on_its_question_only(b):
    if not b.grid:
        return
    known = {c["id"] for c in b.grid["cases"]}

    def cell_shows(case, variant):
        return next((r.get("shown") for r in b.by_id[f"{case}/{variant}"]["rows"] if r["label"] == b.grid["show"]), None)
    for sec in b.grid["sections"]:
        for case in sec["cases"]:
            for col in sec["columns"] if case in known else ():
                values = {v: cell_shows(case, v) for v in col["sameAnswer"]}
                if len(set(values.values())) > 1:
                    yield f"{sec['id']} · {case}: {b.grid['show']!r} depends on another question {values}; show this case under that question"


def c12_every_case_is_in_the_matrix(b):
    if not b.grid:
        return
    known = {c["id"] for c in b.grid["cases"]}
    for sec in b.grid["sections"]:
        for case in sec["cases"]:
            if case not in known:
                yield f"section {sec['id']}: unknown case {case}"
    for case in b.grid["cases"]:
        if not any(case["id"] in sec["cases"] for sec in b.grid["sections"]):
            yield f"case {case['id']} is in no matrix section"


def c13_panel_rows_appear_at_a_real_step(b):
    for s in b.scenarios:
        n = len(s["steps"])
        for row, filled in zip(b.panel, s["rows"]):
            last = filled["at"] + len(filled.get("series", [None])) - 1
            if n and last >= n:
                yield f"{s['id']}: panel row {row['label']!r} appears at step {last}, the scenario has {n}"


# What a text may say at most, in characters: the motion carries the explanation, the text labels it.
TEXT_BUDGET = {"title": 60, "subtitle": 90, "summary": 110, "question": 90, "origin": 110, "caption": 70, "message": 40}


def c14_texts_stay_within_their_budget(b):
    """A reader projected on a wall reads a sentence, not a paragraph; a longer text also takes longer to write."""
    def over(kind, where, text):
        n = len(str(text or "").replace("`", ""))
        if n > TEXT_BUDGET[kind]:
            return f"{where}: {kind} is {n} characters, at most {TEXT_BUDGET[kind]}"
        return None
    spec, grid = b.spec, b.spec.get("grid") or {}
    texts = [("title", "title", spec.get("title")), ("subtitle", "subtitle", spec.get("subtitle")),
             ("summary", "grid", grid.get("summary"))]
    texts += [("question", f"question {q.get('id')}", q.get("text")) for q in grid.get("questions", [])]
    for c in grid.get("cases", []):
        texts += [("summary", f"case {c.get('id')}", c.get("summary")),
                  ("origin", f"case {c.get('id')}", (c.get("origin") or {}).get("text"))]
    texts += [("summary", f"pair {p.get('tab')}", p.get("summary")) for p in spec.get("pairs", [])]
    seen = set()
    for s in b.scenarios:
        if not grid:
            texts += [("summary", s["id"], s.get("summary")),
                      ("origin", s["id"], (s.get("origin") or {}).get("text"))]
        for i, step in enumerate(s["steps"]):
            for kind in ("caption", "message"):
                if (kind, step.get(kind)) not in seen:
                    seen.add((kind, step.get(kind)))
                    texts.append((kind, f"{s['id']} step {i}", step.get(kind)))
    for kind, where, text in texts:
        said = over(kind, where, text)
        if said:
            yield said


def c15_no_case_rests_on_an_open_doubt(b):
    """A doubt is asked before the page is built: its answer shapes the case, or the case says it is undecided."""
    known = {s["id"] for s in b.scenarios} | {s.get("case") for s in b.scenarios}
    for d in b.spec.get("doubts", []):
        for sid in d["scenarios"]:
            if sid not in known:
                yield f"doubt {d['id']} names {sid}, which is no scenario or case"
        if d.get("answer") in (None, "") and d.get("assumed") in (None, ""):
            open_cases = [s["id"] for s in b.scenarios
                          if (s["id"] in d["scenarios"] or s.get("case") in d["scenarios"]) and not s.get("undecided")]
            if open_cases:
                yield f"doubt {d['id']} is not answered, and {', '.join(open_cases)} rests on it: " \
                      f"ask \"{d['question']}\", write the answer, write what you assumed, or mark the scenario undecided"


# The ids are the handles SKILL.md documents: stable, never renumbered.
CHECKS = [
    ("C1", c1_hops_are_edges), ("C2", c2_path_is_unbroken_from_a_source), ("C3", c3_expect_is_what_the_logic_gives),
    ("C4", c4_path_ends_at_the_outcome), ("C5", c5_colour_means_an_outcome_kind), ("C6", c6_labels_fit_their_box),
    ("C7", c7_scenarios_say_where_they_come_from), ("C8", c8_pairs_name_known_scenarios), ("C9", c9_panel_rows_resolve),
    ("C10", c10_matrix_shows_panel_rows), ("C11", c11_a_section_depends_on_its_question_only),
    ("C12", c12_every_case_is_in_the_matrix), ("C13", c13_panel_rows_appear_at_a_real_step),
    ("C14", c14_texts_stay_within_their_budget), ("C15", c15_no_case_rests_on_an_open_doubt),
]


# What the logic must have run for: a verdict to compare (C3, C4), panel rows filled from it (C9, C11, C13).
NEEDS_LOGIC = {"C3", "C4", "C9", "C11", "C13"}


def check(subject, without_logic=False):
    return [f"{cid} {said}" for cid, rule in CHECKS if not (without_logic and cid in NEEDS_LOGIC) for said in rule(subject)]


# ---- output

def export_fixture(spec, scenarios, from_code):
    """The scenarios as a regression table: only values that real code computed are asserted.

    A field without a `basis` counts as code under an oracle, and as ported under a JS port."""
    default = "code:" if from_code else "port:"
    cases = []
    for s in scenarios:
        v = s["verdict"]
        basis = v.get("basis") if isinstance(v.get("basis"), dict) else {}
        expected = {k: v[k] for k in spec["export"]["assert"] if k in v and provenance(basis.get(k, default)) == "code"}
        cases.append({"name": s.get("caseName") or s["id"], "inputs": s["inputs"], "expected": expected})
    return json.dumps({"cases": cases}, ensure_ascii=False, indent=2) + "\n", len(cases)


def default_out(specpath):
    """x.spec.json -> x.sim.html, spec.json -> sim.html, anything else keeps its name."""
    stem = specpath.stem
    name = "sim" if stem == "spec" else stem[:-len(".spec")] + ".sim" if stem.endswith(".spec") else stem
    return specpath.with_name(name + ".html")


def page_data(spec, scenarios, grid, geo, verdict_source):
    """Everything the page receives, and nothing else: no inputs, no expectations, no oracle settings."""
    entered = {e[1] for e in spec["edges"]}
    page = {
        "title": spec["title"], "subtitle": spec.get("subtitle", ""), "source": spec.get("source", ""),
        "lang": spec.get("lang", "en"), "verdictSource": verdict_source, "credit": spec.get("credit", True),
        "kinds": {k: {"label": v["label"], "color": v["color"]} for k, v in spec.get("kinds", {}).items()},
        "nodes": {n["id"]: {"label": n["label"], "kind": n.get("kind"),
                            "role": n.get("role") or ("start" if n["id"] not in entered else None)}
                  for n in spec["nodes"]},
        "scenarios": [{"id": s["id"], "tab": s["tab"], "summary": s["summary"], "origin": s["origin"],
                       "undecided": bool(s.get("undecided")), "case": s.get("case"), "variant": s.get("variant"),
                       "steps": [{"hop": st["hop"], "message": st["message"], "caption": st["caption"]} for st in s["steps"]],
                       "rows": s["rows"]} for s in scenarios],
        "pairs": [{k: p[k] for k in ("before", "after", "tab", "summary")} for p in spec.get("pairs", [])],
        "grid": grid and {
            "baseline": grid["baseline"], "show": grid["show"], "hover": grid["hover"], "summary": grid["summary"],
            "variants": [{k: v[k] for k in ("id", "label", "short", "note")} for v in grid["variants"]],
            "sections": [{"text": sec["text"], "cases": sec["cases"],
                          "columns": [{"variant": c["variant"], "head": c["head"], "short": c["short"], "note": c.get("note")}
                                      for c in sec["columns"]]} for sec in grid["sections"]],
            "cases": [{k: c[k] for k in ("id", "label", "summary", "origin")} for c in grid["cases"]],
        },
    }
    return {"page": page, "geo": geo}


def plain(text):
    """Spec text without its code marks, as the runtime's plain(): `x` -> x, \\` -> `, an open backtick kept."""
    out, buf, opened, i = [], "", False, 0
    while i < len(text):
        if text.startswith("\\`", i):
            buf, i = buf + "`", i + 2
            continue
        if text[i] == "`":
            out.append(buf)
            buf, opened = "", not opened
        else:
            buf += text[i]
        i += 1
    out.append("`" + buf if opened else buf)
    return "".join(out)


def render(data):
    """The runtime with the data in it. Spec text never reaches the page as markup: the title is
    escaped here, the data cannot close its <script>, and the runtime escapes what it inserts."""
    payload = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    shell = RUNTIME.read_text(encoding="utf-8").replace("__LANG__", data["page"]["lang"]).replace("__TITLE__", html.escape(plain(str(data["page"]["title"]))))
    return shell.replace("/*__DATA__*/null", payload, 1)


def build(specpath, out=None, export_to=None, check_only=False, dry_run=False):
    """Returns (page path, scenario count, verdict source, exported). Raises UnreadableSpec or ChecksFailed.

    `exported` is (fixture path, case count), or None without `export_to`. `check_only` runs the checks
    that need no verdict, without the logic, and writes nothing: the page path is then None. `dry_run`
    runs the logic and every check, and writes nothing either."""
    specpath = pathlib.Path(specpath).resolve()
    specdir = specpath.parent
    try:
        spec = json.loads(specpath.read_text(encoding="utf-8"))
    except OSError as e:
        raise UnreadableSpec(f"cannot read {specpath}: {e.strerror}") from e
    except json.JSONDecodeError as e:
        raise UnreadableSpec(f"{specpath.name} is not JSON: {e}") from e
    validate(spec, specdir, exporting=bool(export_to))

    grid, scenarios = expand_grid(spec["grid"]) if "grid" in spec else (None, copy.deepcopy(spec["scenarios"]))
    edges = [[*e, ""][:3] for e in spec["edges"]]
    geo = layout(spec["nodes"], edges)
    if check_only:
        # a hop to {verdict.outcome} is known once the logic has run: its path is checked then
        known = [s for s in scenarios if not any("{" in h for st in s["steps"] for h in st["hop"])]
        paths = ("C1", "C2")
        violations = [v for v in check(Subject(spec, known, grid, geo), without_logic=True) if v.split()[0] in paths]
        violations += [v for v in check(Subject(spec, scenarios, grid, geo), without_logic=True) if v.split()[0] not in paths]
        if violations:
            raise ChecksFailed(violations)
        return None, len(scenarios), "not run", None
    from_code = "oracle" in spec
    verdicts, verdict_source = (run_oracle if from_code else run_port)(spec, scenarios, specdir)
    if len(verdicts) != len(scenarios):
        raise UnreadableSpec(f"the logic returned {len(verdicts)} verdicts for {len(scenarios)} scenarios")
    for s, v in zip(scenarios, verdicts):
        s["verdict"] = v
    fill_templates(scenarios, spec.get("panel", []))
    for s in scenarios:
        s["rows"] = panel_rows(s, spec.get("panel", []), in_grid=bool(grid))
    violations = check(Subject(spec, scenarios, grid, geo))
    if violations:
        raise ChecksFailed(violations)

    if dry_run:
        return None, len(scenarios), verdict_source, None
    # everything is computed before anything is written: a page without its fixture is not "or nothing"
    page = render(page_data(spec, scenarios, grid, geo, verdict_source))
    fixture = export_fixture(spec, scenarios, from_code) if export_to else None
    out = pathlib.Path(out) if out else default_out(specpath)
    out.write_text(page, encoding="utf-8")
    exported = None
    if fixture:
        dest = pathlib.Path(export_to) / spec["export"]["dir"]
        dest.mkdir(parents=True, exist_ok=True)
        (dest / spec["export"]["fixture"]).write_text(fixture[0], encoding="utf-8")
        exported = (dest / spec["export"]["fixture"], fixture[1])
    return out, len(scenarios), verdict_source, exported


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build one self-contained HTML simulation from a spec, or nothing.")
    ap.add_argument("spec")
    ap.add_argument("-o", "--out")
    ap.add_argument("--export", metavar="WORKTREE")
    ap.add_argument("--check", action="store_true",
                    help="run the checks that need no verdict, without the logic, and write nothing")
    ap.add_argument("--dry-run", action="store_true", help="run the logic and every check, and write nothing")
    args = ap.parse_args(argv)
    asks = []
    try:
        try:
            out, n, verdict_source, exported = build(args.spec, args.out, args.export, check_only=args.check,
                                                     dry_run=args.dry_run)
        except ChecksFailed as e:
            # before the first build, an open doubt is a question to ask, not a mistake in the spec
            asks = [v for v in e.args[0] if args.check and v.startswith("C15 ") and " is not answered" in v]
            if len(asks) < len(e.args[0]):
                raise ChecksFailed([v for v in e.args[0] if v not in asks]) from e
            n = None
    except UnreadableSpec as e:
        sys.exit(f"✗ {e}\nnothing written")
    except ChecksFailed as e:
        for line in e.args[0]:
            print("✗", line)
        sys.exit(f"{len(e.args[0])} violation(s), nothing written")
    if args.check:
        for a in asks:
            print("?", a[len("C15 "):])
        print(f"✓ 0 violation without the logic · "
              f"{', '.join(sorted(NEEDS_LOGIC, key=lambda c: int(c[1:])))} wait for it"
              f"{f' · {len(asks)} question(s) to ask before building' if asks else ''} · nothing written")
        return
    if args.dry_run:
        print(f"✓ 0 violation · {n} scenarios · logic: {verdict_source} · dry run, nothing written")
        return
    if exported:
        print(f"✓ exported {exported[1]} cases to {exported[0]}")
    print(f"✓ 0 violation · {n} scenarios · logic: {verdict_source} · wrote {out}")


if __name__ == "__main__":
    main()
