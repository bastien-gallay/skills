"""Every check bites, and a spec that cannot be read says so in one line.

    python3 -m unittest discover -s tests
"""
import contextlib
import copy
import io
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "skills/truepath/examples/refund-window"
sys.path.insert(0, str(ROOT / "skills/truepath/scripts"))
import build  # noqa: E402

BASE = json.loads((EXAMPLE / "spec.json").read_text(encoding="utf-8"))
DECIDE = (EXAMPLE / "decide.js").read_text(encoding="utf-8")

GRID = {
    "baseline": {"id": "today", "label": "today", "inputs": {"fix": False}},
    "questions": [{"id": "Q1", "text": "Does day 30 count?", "cases": ["d30", "d31"],
                   "options": [{"id": "1A", "label": "yes", "inputs": {"fix": True}},
                               {"id": "1B", "label": "no", "inputs": {"fix": False}}]}],
    "cases": [
        {"id": "d30", "label": "day 30", "summary": "last day",
         "origin": {"kind": "illustrative", "text": "test"}, "inputs": {"days": 30}},
        {"id": "d31", "label": "day 31", "summary": "one day late",
         "origin": {"kind": "illustrative", "text": "test"}, "inputs": {"days": 31}}],
    "steps": [{"hop": ["REQ", "AGE"], "message": "{inputs.days} days", "caption": "asked"},
              {"hop": ["AGE", "D"], "message": "in window: {verdict.inWindow}", "caption": "checked"},
              {"hop": ["D", "{verdict.outcome}"], "message": "done", "caption": "decided"}],
    "expect": {"d30": {"1A": {"outcome": "REFUND"}, "today": {"outcome": "CREDIT"}}},
    "hover": ["In the window"],
}


class Case(unittest.TestCase):
    def setUp(self):
        self.dir = pathlib.Path(tempfile.mkdtemp(prefix="truepath-test-"))
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)
        (self.dir / "decide.js").write_text(DECIDE, encoding="utf-8")

    def spec(self, change=None):
        s = copy.deepcopy(BASE)
        if change:
            change(s)
        return s

    def build(self, spec, name="case.spec.json", **kw):
        path = self.dir / name
        path.write_text(json.dumps(spec), encoding="utf-8")
        return build.build(path, **kw)

    def refused(self, change, check):
        """The build refuses, names the check, and writes no page."""
        with self.assertRaises(build.ChecksFailed) as cm:
            self.build(self.spec(change))
        self.assertTrue(any(e.startswith(check + " ") for e in cm.exception.args[0]), cm.exception.args[0])
        self.assertEqual(list(self.dir.glob("*.html")), [])

    def unreadable(self, change, words):
        with self.assertRaises(build.UnreadableSpec) as cm:
            self.build(self.spec(change))
        self.assertIn(words, str(cm.exception))
        self.assertEqual(list(self.dir.glob("*.html")), [])


class Example(Case):
    def test_committed_page_is_what_the_build_writes(self):
        out, n, logic, _ = self.build(self.spec(), name="spec.json")
        self.assertEqual((out.name, n, logic), ("sim.html", 2, "port decide.js"))
        self.assertEqual(out.read_bytes(), (EXAMPLE / "sim.html").read_bytes())

    def test_a_port_leaves_no_work_directory(self):
        self.build(self.spec())
        self.assertFalse((self.dir / build.WORKDIR).exists())


class Examples(unittest.TestCase):
    """The other examples, built where a copy of them lives."""

    def copy(self, name):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="truepath-test-"))
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        src = EXAMPLE.parent / name
        shutil.copytree(src, tmp / name, ignore=shutil.ignore_patterns(build.WORKDIR))
        return src, tmp / name

    def test_the_grid_example_rebuilds_into_its_committed_page(self):
        src, work = self.copy("free-shipping")
        out, n, _, _ = build.build(work / "spec.json", out=work / "built.html")
        self.assertEqual(n, 15)  # 3 cases x (today + 4 sets of answers)
        self.assertEqual(out.read_bytes(), (src / "sim.html").read_bytes())
        played = json.loads(subprocess.run(["node", str(ROOT / "tests/play_page.js"), str(out)],
                                           capture_output=True, text=True, check=True).stdout)
        self.assertEqual(played["tabs"], 4)  # the matrix, then one per case

    def test_the_oracle_example_runs_its_committed_code_and_exports_its_fixture(self):
        src, work = self.copy("loyalty-tier")

        def git(*args):
            subprocess.run(["git", "-C", str(work), *args], check=True, capture_output=True)
        git("init", "-q")
        git("add", "spec.json", "src")
        git("-c", "user.name=t", "-c", "user.email=t@example.invalid", "-c", "commit.gpgsign=false", "commit", "-qm", "example")
        (work / "cases.json").unlink()
        _, n, source, exported = build.build(work / "spec.json", export_to=work)
        self.assertEqual((n, exported[1]), (3, 3))
        self.assertTrue(source.startswith("code of HEAD @ "))
        self.assertEqual(exported[0].read_text(encoding="utf-8"), (src / "cases.json").read_text(encoding="utf-8"))
        replay = subprocess.run(["node", "src/oracle.js"], cwd=work, capture_output=True, text=True)
        self.assertEqual((replay.returncode, replay.stdout.strip()), (0, "3 cases hold"), replay.stderr)


class Checks(Case):
    def test_c1_hop_off_the_edges(self):
        self.refused(lambda s: s["scenarios"][0]["steps"][1].update(hop=["AGE", "REFUND"]), "C1")

    def test_c2_broken_path(self):
        self.refused(lambda s: s["scenarios"][0]["steps"].pop(1), "C2")

    def test_c2_path_not_from_a_source(self):
        self.refused(lambda s: s["scenarios"][0]["steps"].pop(0), "C2")

    def test_c2_scenario_without_steps(self):
        def change(s):
            s["scenarios"][0]["steps"] = []
            s["pairs"] = []
        self.refused(change, "C2")

    def test_c3_expect_contradicted(self):
        self.refused(lambda s: s["scenarios"][0]["expect"].update(inWindow=True), "C3")

    def test_c4_path_ends_elsewhere(self):
        def change(s):
            s["scenarios"][0]["expect"] = {}
            s["scenarios"][0]["steps"][2]["hop"] = ["D", "REFUND"]
        self.refused(change, "C4")

    def test_c4_logic_without_outcome(self):
        """Without an outcome nothing ties the path to the logic: the build must not pass by default."""
        (self.dir / "decide.js").write_text("module.exports={decide:()=>({inWindow:true})};", encoding="utf-8")

        def change(s):
            for sc in s["scenarios"]:
                sc["expect"] = {}
        self.refused(change, "C4")

    def test_c5_outcome_without_kind(self):
        self.refused(lambda s: s["nodes"][3].pop("kind"), "C5")

    def test_c5_kind_without_legend(self):
        self.refused(lambda s: s["kinds"].pop("ok"), "C5")

    def test_c5_too_many_kinds(self):
        self.refused(lambda s: s["kinds"].update({k: {"label": k, "color": "#000"} for k in "abc"}), "C5")

    def test_c6_label_wider_than_its_box(self):
        """layout.py sizes each box to its label, so C6 guards the layout itself: narrow a box by hand."""
        s = self.spec()
        geo = build.layout(s["nodes"], s["edges"])
        subject = build.Subject(s, [], None, geo)
        self.assertEqual(list(build.c6_labels_fit_their_box(subject)), [])
        geo["nodes"]["AGE"]["w"] = 60
        self.assertEqual(len(list(build.c6_labels_fit_their_box(subject))), 1)

    def test_c7_origin_missing(self):
        self.refused(lambda s: s["scenarios"][0].pop("origin"), "C7")

    def test_c8_pair_out_of_step(self):
        def change(s):
            s["edges"].append(["REFUND", "DONE", ""])
            s["nodes"][3].pop("kind")
            s["nodes"].append({"id": "DONE", "label": "done", "kind": "ok"})
            s["scenarios"][1]["steps"].append({"hop": ["REFUND", "DONE"], "message": "m", "caption": "c"})
            s["scenarios"][1]["expect"] = {}
        (self.dir / "decide.js").write_text(
            "module.exports={decide:({fix})=>({inWindow:fix,outcome:fix?'DONE':'CREDIT'})};", encoding="utf-8")
        self.refused(change, "C8")

    def test_c8_pair_names_unknown_scenario(self):
        self.refused(lambda s: s["pairs"][0].update(after="nope"), "C8")

    def test_c9_panel_reads_missing_field(self):
        self.refused(lambda s: s["panel"][2].update(value="verdict.nope"), "C9")

    def test_c13_panel_row_after_the_last_step(self):
        self.refused(lambda s: s["panel"][2].update(at=7), "C13")


class Grid(Case):
    def grid(self, change=None):
        def apply(s):
            s.pop("scenarios"), s.pop("pairs")
            s["panel"] = [r for r in s["panel"] if r["value"] != "inputs.fix"]
            s["grid"] = copy.deepcopy(GRID)
            if change:
                change(s)
        return apply

    def test_questions_become_cells(self):
        out, n, _, _ = self.build(self.spec(self.grid()))
        self.assertEqual(n, 6)  # 2 cases x (today, 1A, 1B)
        self.assertIn("in window: yes", out.read_text(encoding="utf-8"))

    def test_c3_in_a_cell(self):
        self.refused(self.grid(lambda s: s["grid"]["expect"]["d30"].update({"1A": {"outcome": "CREDIT"}})), "C3")

    def test_c10_cell_is_not_a_panel_row(self):
        self.refused(self.grid(lambda s: s["grid"].update(hover=["Nope"])), "C10")

    def test_c11_cell_depends_on_another_question(self):
        def change(s):
            s["grid"]["questions"].append({"id": "Q2", "text": "Shift the window?", "cases": ["d31"], "options": [
                {"id": "2A", "label": "no", "inputs": {}}, {"id": "2B", "label": "by a day", "inputs": {"days": 29}}]})
        self.refused(self.grid(change), "C11")

    def test_c12_case_in_no_section(self):
        self.refused(self.grid(lambda s: s["grid"]["questions"][0].update(cases=["d30"])), "C12")

    def test_c12_section_names_unknown_case(self):
        self.refused(self.grid(lambda s: s["grid"]["questions"][0]["cases"].append("nope")), "C12")


class Contract(Case):
    def test_the_checks_are_the_ones_skill_md_documents(self):
        import re
        skill = (ROOT / "skills/truepath/SKILL.md").read_text(encoding="utf-8")
        documented = re.findall(r"^\| (C\d+) \|", skill, flags=re.M)
        self.assertEqual(documented, [cid for cid, _ in build.CHECKS])

    def page(self, out):
        text = out.read_text(encoding="utf-8")
        start = text.index("const DATA=") + len("const DATA=")
        return json.loads(text[start:text.index(";\n", start)])["page"]

    def test_the_page_receives_what_it_shows_and_nothing_else(self):
        page = self.page(self.build(self.spec())[0])
        self.assertEqual(sorted(page), ["grid", "kinds", "lang", "nodes", "pairs", "scenarios", "source",
                                        "subtitle", "title", "verdictSource"])
        self.assertEqual(sorted(page["scenarios"][0]),
                         ["case", "id", "origin", "rows", "steps", "summary", "tab", "undecided", "variant"])

    def test_a_row_is_shown_once_with_where_it_comes_from(self):
        rows = self.page(self.build(self.spec())[0])["scenarios"][0]["rows"]
        self.assertEqual(rows[0], {"label": "Fix", "at": 0, "compared": True, "shown": "no"})
        self.assertEqual(rows[2], {"label": "In the window", "at": 2, "compared": False, "shown": "no",
                                   "provenance": {"kind": "port", "text": "port: decide.js"}})

    def test_where_a_path_starts_is_derived_and_a_decision_declared(self):
        nodes = self.page(self.build(self.spec())[0])["nodes"]
        self.assertEqual({k: v["role"] for k, v in nodes.items()},
                         {"REQ": "start", "AGE": None, "D": "decision", "REFUND": None, "CREDIT": None})


class Layout(unittest.TestCase):
    def test_edges_sent_around_boxes_each_get_a_lane(self):
        nodes = [{"id": i, "label": i} for i in "ABCD"]
        edges = [["A", "B", ""], ["B", "C", ""], ["C", "D", ""], ["A", "C", ""], ["A", "D", ""], ["B", "D", ""]]
        geo = build.layout(nodes, edges)
        lanes = [e["d"].split(" H")[1].split(" ")[0] for e in geo["edges"][3:]]
        self.assertEqual(len(set(lanes)), 3, lanes)
        self.assertGreater(geo["width"], max(map(float, lanes)))

    def test_a_loop_label_stays_inside_the_drawing(self):
        import layout
        label = "try again later"
        geo = build.layout([{"id": i, "label": i} for i in "AB"], [["A", "B", ""], ["B", "A", label]])
        loop = geo["edges"][1]
        self.assertLessEqual(loop["labelPos"][0] + len(label) * layout.EDGE_CHAR_W, geo["width"])

    def test_a_loop_is_found_from_the_sources_whatever_the_declaration_order(self):
        edges = [["A", "B", ""], ["B", "C", ""], ["C", "B", "again"]]
        tops = set()
        for order in ("ABC", "CAB", "BCA"):
            geo = build.layout([{"id": i, "label": i} for i in order], edges)
            ys = {i: geo["nodes"][i]["y"] for i in "ABC"}
            self.assertLess(ys["A"], ys["B"], order)
            self.assertLess(ys["B"], ys["C"], order)
            tops.add(min(ys, key=ys.get))
        self.assertEqual(tops, {"A"})


class Unreadable(Case):
    def test_edge_to_unknown_node(self):
        self.unreadable(lambda s: s["edges"].append(["D", "NOPE", "x"]), "NOPE is not a node")

    def test_missing_nodes(self):
        self.unreadable(lambda s: s.pop("nodes"), "missing nodes")

    def test_no_logic_source(self):
        self.unreadable(lambda s: s.pop("port"), "neither `oracle` nor `port`")

    def test_logic_file_absent(self):
        self.unreadable(lambda s: s.update(port="gone.js"), "gone.js not found")

    def test_port_that_throws(self):
        (self.dir / "decide.js").write_text("module.exports={decide:()=>{throw new Error('boom')}};", encoding="utf-8")
        self.unreadable(None, "boom")

    def test_port_that_returns_no_object(self):
        (self.dir / "decide.js").write_text("module.exports={decide:()=>1};", encoding="utf-8")
        self.unreadable(None, "verdict objects")

    def test_template_quotes_missing_field(self):
        self.unreadable(lambda s: s["scenarios"][0]["steps"][0].update(message="{verdict.nope}"), "{verdict.nope}")

    def test_values_of_the_wrong_type(self):
        self.unreadable(lambda s: s.update(kinds=[]), "`kinds` must be an object")
        self.unreadable(lambda s: s["scenarios"][0].update(expect=["x"]), "`expect` must be an object")
        self.unreadable(lambda s: s["scenarios"][0]["steps"][0].update(hop=["REQ", 3]), "two node ids")
        self.unreadable(lambda s: s["nodes"][0].update(label=3), "id and label must be text")
        self.unreadable(lambda s: s["nodes"][0].update(role="pill"), "the only role to declare")

    def test_a_grid_page_takes_no_plain_scenario(self):
        self.unreadable(lambda s: s.update(grid=copy.deepcopy(GRID)), "a grid page shows only its cells")

    def test_not_json(self):
        path = self.dir / "bad.spec.json"
        path.write_text("{", encoding="utf-8")
        with self.assertRaises(build.UnreadableSpec):
            build.build(path)

    def test_cli_says_it_without_a_traceback(self):
        path = self.dir / "case.spec.json"
        path.write_text(json.dumps(self.spec(lambda s: s.pop("nodes"))), encoding="utf-8")
        with self.assertRaises(SystemExit) as cm, contextlib.redirect_stdout(io.StringIO()):
            build.main([str(path)])
        self.assertIn("nothing written", str(cm.exception.code))

    def test_missing_kinds_is_a_violation_not_a_crash(self):
        self.refused(lambda s: s.pop("kinds"), "C5")


class Page(Case):
    def test_spec_text_cannot_close_the_script_or_the_title(self):
        hostile = "x</script><script>alert(1)</script>"
        out, *_ = self.build(self.spec(lambda s: s.update(title=hostile, sub=hostile)))
        text = out.read_text(encoding="utf-8")
        self.assertNotIn("<script>alert", text)
        self.assertEqual(text.count("</script>"), 1)
        self.assertIn("<title>x&lt;/script&gt;", text)

    def play(self, out, *mode):
        """Every tab and step of a built page, on a stand-in DOM (see play_page.js)."""
        run = subprocess.run(["node", str(ROOT / "tests/play_page.js"), str(out), *mode], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr[-2000:])
        return json.loads(run.stdout)

    def test_the_example_plays_through(self):
        played = self.play(EXAMPLE / "sim.html")
        self.assertEqual(played["tabs"], 3)
        self.assertTrue(any("30 &lt; 30" in h for h in played["html"]))

    def test_reduced_motion_does_not_autoplay(self):
        self.assertTrue(self.play(EXAMPLE / "sim.html")["playingOnLoad"])
        self.assertFalse(self.play(EXAMPLE / "sim.html", "reduced")["playingOnLoad"])

    def test_hostile_spec_text_stays_text(self):
        tag = "<img src=x onerror=alert(1)>"

        def change(s):
            s["subtitle"] = tag
            s["kinds"]["ok"]["label"] = tag
            for r in s["panel"]:
                r["labels"] = {"true": tag, "false": tag + "!", "30": tag}
            for i, sc in enumerate(s["scenarios"]):
                sc["summary"] = tag
                sc["origin"]["text"] = tag
                for st in sc["steps"]:
                    st["message"] = f"{tag}{i}"
                    st["caption"] = f"{tag}{i}"
            s["pairs"][0]["summary"] = tag
        played = self.play(self.build(self.spec(change))[0])
        self.assertTrue(any("&lt;img" in h for h in played["html"]))
        for h in played["html"]:
            self.assertNotIn("<img", h)

    def test_a_grid_plays_through_in_french(self):
        tag = "<img src=x onerror=alert(1)>"

        def change(s):
            s.pop("scenarios"), s.pop("pairs")
            s["lang"] = "fr"
            s["grid"] = copy.deepcopy(GRID)
            s["grid"]["summary"] = tag
            s["grid"]["questions"][0]["text"] = tag
            s["grid"]["questions"][0]["options"][0]["label"] = tag
            for c in s["grid"]["cases"]:
                c["label"] = c["summary"] = tag
                c["origin"]["text"] = tag
            s["panel"] = [r for r in s["panel"] if r["value"] != "inputs.fix"]
            s["panel"].append({"label": "Answer", "value": "answer", "at": 0, "compared": True})
        played = self.play(self.build(self.spec(change))[0])
        self.assertEqual(played["tabs"], 3)  # the matrix, then one per case
        for h in played["html"]:
            self.assertNotIn("<img", h)

    def test_output_names(self):
        for spec, page in (("spec.json", "sim.html"), ("a.spec.json", "a.sim.html"),
                           ("inspection.spec.json", "inspection.sim.html"), ("process.json", "process.html")):
            self.assertEqual(build.default_out(pathlib.Path(spec)).name, page)


@unittest.skipUnless(shutil.which("git"), "needs git")
class Oracle(Case):
    def setUp(self):
        super().setUp()
        self.repo = self.dir / "repo"
        (self.repo / "src").mkdir(parents=True)
        (self.repo / "src/rule.js").write_text("module.exports=d=>d<=30;", encoding="utf-8")
        (self.repo / "src/run.js").write_text(
            "const fs=require('fs'),rule=require('./rule.js');"
            "const i=JSON.parse(fs.readFileSync(process.env.TRUEPATH_ORACLE_IN));"
            "fs.writeFileSync(process.env.TRUEPATH_ORACLE_OUT,JSON.stringify(i.map(x=>{const w=rule(x.days);"
            "return {inWindow:w,note:'n',outcome:w?'REFUND':'CREDIT',basis:{note:'defined here'}}})));", encoding="utf-8")
        self.git("init", "-q")
        self.commit("rule")

    def git(self, *args):
        subprocess.run(["git", "-C", str(self.repo), *args], check=True, capture_output=True)

    def commit(self, msg):
        self.git("add", "-A")
        self.git("-c", "user.name=t", "-c", "user.email=t@example.invalid", "-c", "commit.gpgsign=false", "commit", "-qm", msg)

    def oracle(self, s):
        s.pop("port")
        s["oracle"] = {"repo": "repo", "ref": "HEAD", "paths": ["src"], "cwd": "src", "cmd": ["node", "run.js"]}
        s["scenarios"] = [s["scenarios"][1]]
        s["pairs"] = []
        s["export"] = {"dir": "fx", "fixture": "cases.json", "assert": ["inWindow", "note", "outcome"]}

    def test_verdicts_come_from_the_ref_not_the_checkout(self):
        (self.repo / "src/rule.js").write_text("module.exports=d=>d<30;", encoding="utf-8")  # uncommitted
        out, n, logic, _ = self.build(self.spec(self.oracle))
        self.assertTrue(logic.startswith("code of HEAD @ "))
        out.unlink()
        self.commit("regression")
        self.refused(self.oracle, "C3")

    def test_files_land_in_the_snapshot_at_the_path_they_name(self):
        (self.dir / "extra.json").write_text("{}", encoding="utf-8")

        def change(s):
            self.oracle(s)
            s["oracle"]["files"] = {"src/given/extra.json": "extra.json"}
            s["oracle"]["cmd"] = ["node", "-e", "require('./given/extra.json');require('./run.js')"]
        self.build(self.spec(change))

    def test_export_asserts_only_what_code_computed(self):
        *_, note = self.build(self.spec(self.oracle), export_to=self.dir / "wt")
        case = json.loads(note[0].read_text(encoding="utf-8"))["cases"][0]
        self.assertEqual(case["expected"], {"inWindow": True, "outcome": "REFUND"})

    def test_export_without_its_block_writes_no_page(self):
        with self.assertRaises(build.UnreadableSpec):
            self.build(self.spec(), export_to=self.dir / "wt")
        self.assertEqual(list(self.dir.glob("*.html")), [])

    def test_a_definition_starting_with_code_is_not_exported(self):
        (self.dir / "decide.js").write_text(
            "module.exports={decide:()=>({inWindow:true,outcome:'REFUND',"
            "basis:{inWindow:'code of conduct says so',outcome:'code: rule.js'}})};", encoding="utf-8")

        def change(s):
            s["scenarios"], s["pairs"] = [s["scenarios"][1]], []
            s["export"] = {"dir": ".", "fixture": "cases.json", "assert": ["inWindow", "outcome"]}
        *_, note = self.build(self.spec(change), export_to=self.dir / "wt")
        self.assertEqual(json.loads(note[0].read_text(encoding="utf-8"))["cases"][0]["expected"], {"outcome": "REFUND"})

    def test_export_from_a_port_asserts_nothing_unmarked(self):
        def change(s):
            s["export"] = {"dir": ".", "fixture": "cases.json", "assert": ["inWindow", "outcome"]}
        *_, note = self.build(self.spec(change), export_to=self.dir / "wt")
        self.assertEqual(json.loads(note[0].read_text(encoding="utf-8"))["cases"][0]["expected"], {})


if __name__ == "__main__":
    unittest.main()
