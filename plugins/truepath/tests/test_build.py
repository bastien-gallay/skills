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

    def page(self, out):
        text = out.read_text(encoding="utf-8")
        start = text.index("const DATA=") + len("const DATA=")
        return json.loads(text[start:text.index(";\n", start)])["page"]

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
        replay = subprocess.run(["node", "src/oracle.js"], cwd=work, check=False, capture_output=True, text=True)
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

    def test_c8_pair_names_unknown_scenario(self):
        self.refused(lambda s: s["pairs"][0].update(after="nope"), "C8")
        self.refused(lambda s: s["pairs"][0].update(before="nope"), "C8")

    def test_c9_panel_reads_missing_field(self):
        self.refused(lambda s: s["panel"][2].update(value="verdict.nope"), "C9")

    def test_c13_panel_row_after_the_last_step(self):
        self.refused(lambda s: s["panel"][2].update(at=7), "C13")

    def test_c14_text_over_its_budget(self):
        self.refused(lambda s: s.update(subtitle="x" * 91), "C14")
        self.refused(lambda s: s["scenarios"][0].update(summary="x" * 111), "C14")
        self.refused(lambda s: s["scenarios"][0]["steps"][0].update(caption="x" * 71), "C14")
        self.refused(lambda s: s["scenarios"][0]["steps"][0].update(message="x" * 41), "C14")

    def test_c14_backticks_cost_nothing(self):
        out, _, _, _ = self.build(self.spec(lambda s: s.update(subtitle="`x`" * 45)))
        self.assertTrue(out.exists())


class Doubts(Case):
    def doubt(self, answer=None, undecided=False, names=None):
        def change(s):
            sid = s["scenarios"][0]["id"]
            s["doubts"] = [{"id": "D1", "question": "Does the clock count the last day?",
                            "scenarios": names or [sid], **({"answer": answer} if answer else {})}]
            s["scenarios"][0]["undecided"] = undecided
        return change

    def test_c15_an_open_doubt_stops_the_build_and_says_what_to_ask(self):
        with self.assertRaises(build.ChecksFailed) as cm:
            self.build(self.spec(self.doubt()))
        self.assertTrue(any("C15" in e and "Does the clock count the last day?" in e for e in cm.exception.args[0]))

    def test_an_answered_doubt_builds(self):
        self.build(self.spec(self.doubt(answer="yes, said the product owner on 2026-11-20")))

    def test_an_open_doubt_on_an_undecided_case_builds(self):
        self.build(self.spec(self.doubt(undecided=True)))

    def test_c15_a_doubt_names_a_known_case(self):
        self.refused(self.doubt(answer="yes", names=["nowhere"]), "C15")


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
        documented = re.findall(r"^\| (C\d+) \|", skill, flags=re.MULTILINE)
        self.assertEqual(documented, [cid for cid, _ in build.CHECKS])

    def test_the_page_receives_what_it_shows_and_nothing_else(self):
        page = self.page(self.build(self.spec())[0])
        self.assertEqual(sorted(page), ["credit", "grid", "kinds", "lang", "nodes", "pairs", "scenarios", "source",
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

    def test_an_edge_steps_aside_beside_the_box_in_its_way_not_around_the_drawing(self):
        """S->T would cross M: it passes just beside M, inside the drawing, not past the wide X on the right."""
        nodes = [{"id": "S", "label": "S"}, {"id": "M", "label": "M"},
                 {"id": "X", "label": "a wide box on the right side"}, {"id": "T", "label": "T"}]
        edges = [["S", "M", ""], ["S", "X", ""], ["M", "T", ""], ["S", "T", "skip"]]
        geo = build.layout(nodes, edges)
        skip = geo["edges"][3]["d"]
        lane = float(skip.split(" H")[1].split(" ")[0])
        x = geo["nodes"]["X"]
        self.assertLess(lane, x["x"] + x["w"], skip)
        m = geo["nodes"]["M"]
        self.assertFalse(m["x"] <= lane <= m["x"] + m["w"], skip)

    def test_a_loop_label_stays_inside_the_drawing(self):
        import layout
        label = "try again later"
        geo = build.layout([{"id": i, "label": i} for i in "AB"], [["A", "B", ""], ["B", "A", label]])
        loop = geo["edges"][1]
        self.assertLessEqual(loop["labelPos"][0] + len(label) * layout.EDGE_CHAR_W, geo["width"])

    def test_loops_out_of_a_row_cross_no_box_and_share_no_line(self):
        """A parser loop: four boxes of one row return to the decision above them, beside a fifth that does not."""
        ids = ["N", "W", "P", "E", "I", "F"]
        edges = [["N", i, i] for i in ids[1:]] + [[i, "N", ""] for i in "WPEI"]
        geo = build.layout([{"id": i, "label": f"box {i}"} for i in ids], edges)
        segs = []
        for e in geo["edges"][5:]:
            tok = e["d"].split()
            x, y = float(tok[0][1:]), float(tok[1])
            for raw in tok[2:]:
                nx, ny = (float(raw[1:]), y) if raw[0] == "H" else (x, float(raw[1:]))
                segs.append(((x, y), (nx, ny), e["from"]))
                x, y = nx, ny
        for (x1, y1), (x2, y2), src in segs:
            for n, b in geo["nodes"].items():
                inside_x = min(x1, x2) < b["x"] + b["w"] and max(x1, x2) > b["x"]
                inside_y = min(y1, y2) < b["y"] + b["h"] and max(y1, y2) > b["y"]
                self.assertFalse(inside_x and inside_y and n != src, f"{src}->N crosses {n}")
        # before they meet at their target's side, no two loops run along the same stretch
        ends = {seg for seg in segs if seg[1][0] == geo["nodes"]["N"]["x"] + geo["nodes"]["N"]["w"] + 4}
        flats = [(y1, min(x1, x2), max(x1, x2), s) for (x1, y1), (x2, y2), s in segs
                 if y1 == y2 and ((x1, y1), (x2, y2), s) not in ends]
        for y, lo, hi, s in flats:
            for y_, lo_, hi_, s_ in flats:
                self.assertFalse(s != s_ and y == y_ and lo < hi_ and lo_ < hi, f"{s} and {s_} share y={y}")

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
        self.unreadable(lambda s: s.update(credit="no"), "`credit` must be true or false")

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
        run = subprocess.run(["node", str(ROOT / "tests/play_page.js"), str(out), *mode], check=False, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr[-2000:])
        return json.loads(run.stdout)

    def test_the_example_plays_through(self):
        played = self.play(EXAMPLE / "sim.html")
        self.assertEqual(played["tabs"], 1)  # the pair: its two scenarios get no tab of their own
        self.assertTrue(any("30 &lt; 30" in h for h in played["html"]))

    def test_the_page_opens_paused_with_play_marked(self):
        for mode in ((), ("reduced",)):
            played = self.play(EXAMPLE / "sim.html", *mode)
            self.assertEqual((played["playingOnLoad"], played["playMarkedOnLoad"]), (False, True), mode)

    def test_a_step_through_a_node_builds_and_plays_through(self):
        """A loop's return says nothing: the step runs on through the node it passes, without a stop of its own."""
        def change(s):
            for sc in s["scenarios"]:
                first, second = sc["steps"][:2]
                sc["steps"][:2] = [{**second, "hop": [first["hop"][0], *second["hop"]]}]
            for row in s.get("panel", []):
                row["at"] = max(0, row["at"] - 1)
        out, n, *_ = self.build(self.spec(change))
        self.assertEqual(n, 2)
        page = self.page(out)
        self.assertEqual(page["scenarios"][0]["steps"][0]["hop"], ["REQ", "AGE", "D"])
        self.play(out)

    def test_two_paths_that_part_mark_the_fork_even_when_no_value_differs(self):
        """The data the panel compares may differ only at the end, or not at all: the fork is a difference too."""
        def change(s):
            s["panel"] = [r for r in s["panel"] if r["label"] != "In the window"]
        out, *_ = self.build(self.spec(change))
        self.assertEqual(self.play(out)["parted"], {"step": 2, "node": "D"})

    def test_a_fork_inside_a_step_through_a_node_is_marked_on_the_node_both_share(self):
        """[A, D, X] against [A, D, Y]: the paths share D, so D is where they part, not A."""
        def change(s):
            for sc in s["scenarios"]:
                first, *rest = sc["steps"][1:]
                sc["steps"][1:] = [{**rest[0], "hop": [first["hop"][0], *rest[0]["hop"]]}]
            s["panel"] = [r for r in s["panel"] if r["at"] == 0]
        out, *_ = self.build(self.spec(change))
        self.assertEqual(self.play(out)["parted"], {"step": 1, "node": "D"})

    def test_a_series_row_changes_step_by_step_and_parts_where_it_first_differs(self):
        """A value built up across a loop: one value per step from `at`, the last one kept."""
        def change(s):
            s["panel"] = [s["panel"][0], {"label": "Log", "value": "inputs.log", "at": 0, "series": True}]
            s["scenarios"][0]["inputs"]["log"] = ["opened", "1 line"]
            s["scenarios"][1]["inputs"]["log"] = ["opened", "2 lines"]
        out, *_ = self.build(self.spec(change))
        row = self.page(out)["scenarios"][0]["rows"][1]
        self.assertEqual((row["series"], row["shown"]), (["opened", "1 line"], "1 line"))
        played = self.play(out)
        self.assertEqual(played["parted"], {"step": 1, "node": "AGE"})
        self.assertTrue(any("≠ " in h and "2 lines" in h for h in played["html"]))

    def test_a_compared_row_is_not_marked_as_a_change(self):
        """The row naming the fix differs on both sides by design: no ≠, which would point at it as an effect."""
        out, *_ = self.build(self.spec())
        html = self.play(out)["html"]
        self.assertTrue(any(">Fix<" in h for h in html))
        self.assertFalse(any("≠ Fix" in h for h in html))
        self.assertTrue(any("≠ In the window" in h for h in html))

    def test_c9_a_series_row_reads_a_list(self):
        self.refused(lambda s: s["panel"].append({"label": "Log", "value": "inputs.days", "at": 0, "series": True}), "C9")

    def test_c13_a_series_longer_than_the_steps(self):
        def change(s):
            s["panel"].append({"label": "Log", "value": "inputs.log", "at": 1, "series": True})
            for sc in s["scenarios"]:
                sc["inputs"]["log"] = ["a", "b", "c"]
        self.refused(change, "C13")

    def test_c1_a_step_through_a_node_takes_only_edges(self):
        self.refused(lambda s: s["scenarios"][0]["steps"].__setitem__(
            slice(0, 2), [{"hop": ["REQ", "D"], "message": "m", "caption": "c"}]), "C1")
        self.refused(lambda s: s["scenarios"][0]["steps"].__setitem__(
            slice(0, 2), [{"hop": ["REQ", "AGE", "REFUND"], "message": "m", "caption": "c"}]), "C1")

    def test_a_pair_of_unequal_length_builds_and_plays_through(self):
        """The shorter side stays on its outcome while the longer one goes on."""
        def change(s):
            s["edges"].append(["REFUND", "DONE", ""])
            s["nodes"][3].pop("kind")
            s["nodes"].append({"id": "DONE", "label": "done", "kind": "ok"})
            s["scenarios"][1]["steps"].append({"hop": ["REFUND", "DONE"], "message": "paid out", "caption": "c"})
            s["scenarios"][1]["expect"] = {}
        (self.dir / "decide.js").write_text(
            "module.exports={decide:({fix})=>({inWindow:fix,outcome:fix?'DONE':'CREDIT'})};", encoding="utf-8")
        out, n, *_ = self.build(self.spec(change))
        self.assertEqual(n, 2)
        played = self.play(out)
        self.assertEqual(played["pairSteps"], 4)  # the longer side's count
        self.assertTrue(any('data-i="3"><button type="button" aria-current="step">+ paid out</button></li>' in h for h in played["html"]))  # the arrived side says nothing

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

    def test_a_scenario_outside_any_pair_keeps_its_tab(self):
        def change(s):
            s["scenarios"].append({**copy.deepcopy(s["scenarios"][0]), "id": "alone", "tab": "Alone"})
        self.assertEqual(self.play(self.build(self.spec(change))[0])["tabs"], 2)  # the lone scenario, the pair

    def test_the_credit_is_shown_unless_the_spec_turns_it_off(self):
        link = '<a href="https://github.com/bastien-gallay/truepath" target="_blank" rel="noopener">'
        on = self.play(self.build(self.spec())[0])["html"]
        self.assertTrue(any(link + "made with truepath</a>" in h for h in on))
        off = self.play(self.build(self.spec(lambda s: s.update(credit=False)))[0])["html"]
        self.assertFalse(any("truepath</a>" in h for h in off))

    def test_backticks_are_code_in_text_and_dropped_in_tooltips(self):
        def change(s):
            s.pop("pairs")  # a paired scenario has no tab of its own: its summary would not show
            s["title"] = "uses `chardet`"
            s["scenarios"][0]["summary"] = "`<b>` and \\`tick\\` and `open"
            s["scenarios"][0]["origin"]["text"] = "from `ticket`"
        out, *_ = self.build(self.spec(change))
        self.assertIn("<title>uses chardet</title>", out.read_text(encoding="utf-8"))
        html = self.play(out)["html"]
        self.assertIn("<code>&lt;b&gt;</code> and `tick` and `open", "".join(html))
        self.assertTrue(any("from <code>ticket</code>" in h for h in html))
        self.assertFalse(any("<b>" in h for h in html))

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
        mx = next(h for h in played["html"] if 'class="mx"' in h)
        self.assertIn('<p class="hint">', mx)  # said before the table, not under it
        self.assertEqual(mx.count('<td tabindex="0" role="button"'), 6)  # every cell: 2 cases x (today, 1A, 1B)
        self.assertEqual(mx.count(' class="pulse hit"'), 1)  # one cell rings, the first where the answers disagree
        self.assertEqual(mx.count('<tr class="split">'), 1)  # day 30 splits the answers, day 31 does not
        self.assertEqual(mx.count('hit" aria-label'), 2)  # both answers of the split case are marked, not today
        self.assertEqual(mx.count('<span class="out">'), 6)  # every cell says how its case ends, then its value
        self.assertEqual(mx.count('scope="row"'), 2)  # a case heads its row for a screen reader
        self.assertIn('<p class="mxkey">', mx)  # the keys sit in one line of short items, not a paragraph
        minis = [h for h in played["html"] if 'class="mx mini"' in h]  # an open case keeps its row of the matrix
        marks = {h.count('aria-current="true"') for h in minis}
        self.assertEqual(marks, {1, 2})  # today alone marks one cell; a comparison marks two, − and +
        self.assertTrue(all('class="pickhint"' in h for h in minis))  # Shift is said on screen, not only on hover
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
        out, _, logic, _ = self.build(self.spec(self.oracle))
        self.assertTrue(logic.startswith("code of HEAD @ "))
        out.unlink()
        self.commit("regression")
        self.refused(self.oracle, "C3")

    def test_files_land_in_the_snapshot_at_the_path_they_name(self):
        (self.dir / "extra.json").write_text("{}", encoding="utf-8")

        def change(s):
            self.oracle(s)
            s["oracle"]["files"] = {"src/given/extra.json": "extra.json"}
            s["oracle"]["doubles"] = []
            s["oracle"]["cmd"] = ["node", "-e", "require('./given/extra.json');require('./run.js')"]
        *_, source, _ = self.build(self.spec(change))
        self.assertTrue(source.endswith(" + from the spec: extra.json"), source)  # not passed off as the ref's code

    def test_files_must_say_what_they_stand_in_for(self):
        (self.dir / "extra.json").write_text("{}", encoding="utf-8")

        def change(s):
            self.oracle(s)
            s["oracle"]["files"] = {"src/given/extra.json": "extra.json"}
        self.unreadable(change, "oracle.doubles")

    def test_a_double_has_a_known_kind(self):
        def change(s):
            self.oracle(s)
            s["oracle"]["doubles"] = [{"name": "clock", "kind": "spy-ish", "replaces": "the system clock"}]
        self.unreadable(change, "expected stub, fake or mock")

    def test_the_footer_names_the_doubles(self):
        def change(s):
            self.oracle(s)
            s["oracle"]["doubles"] = [{"name": "clock", "kind": "stub", "replaces": "the system clock"}]
        *_, source, _ = self.build(self.spec(change))
        self.assertTrue(source.endswith(" · doubles: clock (stub)"), source)

    def test_an_excerpt_is_named_by_its_origin_not_its_local_commit(self):
        (self.repo / "excerpt.json").write_text(json.dumps(
            {"repo": "someone/project", "sha": "0123456789abcdef", "files": ["src/rule.js", "src/run.js"]}), encoding="utf-8")
        self.commit("excerpt")
        *_, source, _ = self.build(self.spec(self.oracle))
        self.assertTrue(source.startswith("code of someone/project @ 0123456, excerpt of 2 files"), source)

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


class Fetch(unittest.TestCase):
    """fetch.py against a GitHub stand-in served from file:// URLs, through the same curl."""

    def setUp(self):
        self.dir = pathlib.Path(tempfile.mkdtemp(prefix="truepath-fetch-"))
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)
        api, raw = self.dir / "api/repos/o/r", self.dir / "raw/o/r"
        for sha in ("a" * 40, "b" * 40):
            (api / "commits").mkdir(parents=True, exist_ok=True)
            (raw / sha / "src").mkdir(parents=True)
            (raw / sha / "src/rule.rs").write_text(f"// at {sha[0]}\n", encoding="utf-8")
            (raw / sha / "src/other.rs").write_text("// other\n", encoding="utf-8")
        (api / "commits/main").write_text(json.dumps({"sha": "a" * 40}), encoding="utf-8")
        (api / "commits/next").write_text(json.dumps({"sha": "b" * 40}), encoding="utf-8")
        import fetch
        self.fetch = fetch
        self.urls = (fetch.API, fetch.RAW)
        fetch.API, fetch.RAW = f"file://{self.dir}/api", f"file://{self.dir}/raw"
        self.addCleanup(self.restore)

    def restore(self):
        self.fetch.API, self.fetch.RAW = self.urls

    def test_get_commits_the_files_unchanged_with_their_origin(self):
        into = self.dir / "excerpt"
        self.fetch.get("o/r", "main", ["src/rule.rs"], into)
        self.assertEqual((into / "src/rule.rs").read_text(encoding="utf-8"), "// at a\n")
        record = json.loads((into / "excerpt.json").read_text(encoding="utf-8"))
        self.assertEqual(record, {"repo": "o/r", "sha": "a" * 40, "files": ["src/rule.rs"]})
        tracked = subprocess.run(["git", "-C", str(into), "ls-files"], check=True, capture_output=True, text=True).stdout.split()
        self.assertEqual(sorted(tracked), ["excerpt.json", "src/rule.rs"])

    def test_a_second_get_adds_files_of_the_same_commit_only(self):
        into = self.dir / "excerpt"
        self.fetch.get("o/r", "main", ["src/rule.rs"], into)
        self.fetch.get("o/r", "main", ["src/other.rs"], into)
        self.assertEqual(json.loads((into / "excerpt.json").read_text())["files"], ["src/other.rs", "src/rule.rs"])
        with self.assertRaises(self.fetch.FetchFailed):
            self.fetch.get("o/r", "next", ["src/rule.rs"], into)


if __name__ == "__main__":
    unittest.main()
