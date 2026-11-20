"""Top-down layered layout of a process graph: boxes sized to their label, orthogonal edges.

    layout(nodes, edges, across=False) -> {width, height, lineHeight,
                                           nodes: {id: {x, y, w, h, labelLines}},
                                           edges: [{from, to, d, label, labelPos, pass}]}

A node's rank is its longest path from the sources; a rank is drawn as one layer. An edge that
climbs back (a loop) runs in a lane of its own to the right of every box; when other boxes
stand beside its source, it first runs under their row in a corridor of its own. An edge that would
cross a box on its way down steps aside just past the boxes in its way, on the nearer side:
sent around the whole drawing, it was the longest line on the page and widened it for nothing.
`pass` is where the page writes, along an edge, which visits of a node revisited by a loop left
by it: [x, y, side], the badges laid from (x, y) towards side (-1 left, 1 right). A labelled
edge has them right after its label, which already names the branch ("no 1 2", "yes 3"); an
unlabelled one, on a stretch of the edge no other edge leaving the same node shares.
`across` lays the ranks out left to right instead (see `across`): the same layout, run on boxes
turned a quarter, then turned back, its labels set again since text does not turn.
Pure stdlib, deterministic: the same graph gives the same file.

The page draws with the fonts these widths assume: node labels in 13px monospace, edge
labels in 11px sans (see `.node text` and `.elabel` in runtime.html).
"""
import math
import re

CHAR_W = 7.85       # advance of a 13px ui-monospace glyph, measured in Chrome on macOS (7.84 max)
EDGE_CHAR_W = 6.2   # mean advance of an 11px sans glyph: an estimate, edge labels are short
WRAP = 30           # characters per label line
LINE_H = 16         # between two lines of a label; the page reads it from the geometry
PAD_X = 20          # between a label and each side of its box
MIN_W = 120         # a short label still gets a box wide enough to aim at
BOX_H = 44          # a one-line box
GRID = 8            # the gaps around boxes are multiples of it
GAP_X = 4 * GRID    # between two boxes of a layer
GAP_Y = 8 * GRID    # between two layers; rails run in the middle of it
MARGIN = 4 * GRID   # around the drawing
LANE = 2 * GRID     # between two lanes, and between the boxes and the first lane
STUB = 4            # an edge stops this short of the box it enters, so the arrowhead does not pierce it
LABEL_GAP = 4       # between an edge and its label
CLEARANCE = 6       # how near a box side an edge may pass before it is sent around
PASS_ROOM = 3       # between an edge label and the first pass badge after it
PASS_W = 19         # a pass badge and the gap after it, in the page's units (runtime.html PASS_R, PASS_GAP)


def wrap(label):
    lines, cur = [], ""
    for word in label.split():
        if cur and len(cur) + 1 + len(word) > WRAP:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}" if cur else word
    return lines + [cur] if cur else [""]


def box_size(node):
    lines = wrap(node["label"])
    w = max(MIN_W, math.ceil(max(map(len, lines)) * CHAR_W) + 2 * PAD_X)
    return lines, w, BOX_H + LINE_H * (len(lines) - 1)


def rank_nodes(ids, edges):
    """Each node's longest path from the sources, over the graph without its back edges."""
    succ = {i: [] for i in ids}
    for a, b in edges:
        succ[a].append(b)
    state, back = {}, set()

    def visit(n):
        state[n] = "open"
        for m in succ[n]:
            if state.get(m) == "open":
                back.add((n, m))
            elif m not in state:
                visit(m)
        state[n] = "done"

    entered = {b for _, b in edges}
    for i in [i for i in ids if i not in entered] + ids:  # from the sources, whatever the declaration order
        if i not in state:
            visit(i)
    forward = [(a, b) for a, b in edges if (a, b) not in back]
    rank = {i: 0 for i in ids}
    for _ in ids:  # relax: at most len(ids) rounds on a DAG
        for a, b in forward:
            rank[b] = max(rank[b], rank[a] + 1)
    return rank, back


def order_layers(layers, parents):
    """One top-down pass: each node sits under the mean position of its parents in the layer above.

    The first layer keeps its declaration order, and every later node has a parent just above it
    (that is what its rank means), so a second pass would change nothing."""
    for r in range(1, len(layers)):
        pos = {n: k for k, n in enumerate(layers[r - 1])}

        def mean_parent(n, pos=pos):
            above = [pos[p] for p in parents[n] if p in pos]
            return sum(above) / len(above)
        layers[r].sort(key=mean_parent)
    return layers


def place_layer(layer, box, want):
    """Left to right at the wanted centres, pushed apart, then shifted back to the wanted mean."""
    xs, right = [], -math.inf
    for n in layer:
        x = max(want[n] - box[n]["w"] / 2, right + GAP_X)
        xs.append(x)
        right = x + box[n]["w"]
    shift = sum(want[n] - (x + box[n]["w"] / 2) for n, x in zip(layer, xs)) / len(layer)
    for n, x in zip(layer, xs):
        box[n]["x"] = x + shift


def detour(tx, passed, taken):
    """The x of a vertical that clears every box between two layers, nearest to tx, and the side it lies on.

    `taken` holds the detours already drawn, so two of them never share a vertical."""
    def clear(x):
        return not any(o["x"] - CLEARANCE <= x <= o["x"] + o["w"] + CLEARANCE for o in passed) \
            and all(abs(x - u) >= LANE for u in taken)

    def walk(x, step):
        for _ in range(len(passed) + len(taken) + 2):
            if clear(x):
                return x
            hit = [o for o in passed if o["x"] - CLEARANCE <= x <= o["x"] + o["w"] + CLEARANCE]
            if hit:
                x = (max(o["x"] + o["w"] for o in hit) + LANE) if step > 0 else (min(o["x"] for o in hit) - LANE)
            else:
                x += step * LANE
        return x
    right, left = walk(tx, 1), walk(tx, -1)
    if left >= MARGIN and tx - left < right - tx:
        return left, -1
    return right, 1


def loop_lanes(loops, ids, box, rank, right, gaps):
    """Where each loop climbs, and the corridor it takes past the boxes beside its two ends.

    A loop leaves its source's side and enters its target's side. When another box of the same
    row stands further right, a line at mid-height would run through it and seem to chain the
    boxes together, so the loop drops into the gap beside its source and runs under the row
    (or above the target's row) in a corridor of its own. The shortest loops climb nearest the
    boxes, and under one row the outer lane takes the lower corridor, so no two loops cross."""
    def mid(n):
        return box[n]["y"] + box[n]["h"] / 2

    def gap_right(n):
        """The middle of the gap after n in its row, or None when n is the last of its row."""
        after = [box[m]["x"] for m in ids if rank[m] == rank[n] and box[m]["x"] > box[n]["x"]]
        return (box[n]["x"] + box[n]["w"] + min(after)) / 2 if after else None

    order = sorted(loops, key=lambda e: (mid(e[0]) - mid(e[1]), -box[e[0]]["x"]))
    lane = {e: right + LANE * (k + 1) for k, e in enumerate(order)}
    under, over = {}, {}
    for e in order:  # inner lane first: nearest the row
        if gap_right(e[0]) is not None:
            under.setdefault(rank[e[0]], []).append(e)
        if gap_right(e[1]) is not None:
            over.setdefault(rank[e[1]], []).append(e)
    corridor = {}
    for r, es in under.items():
        bottom = max(box[n]["y"] + box[n]["h"] for n in ids if rank[n] == r)
        for k, e in enumerate(es):  # between the row and its rail
            corridor[e, "under"] = round(bottom + (k + 1) * gaps[r] / 2 / (len(es) + 1))
    for r, es in over.items():
        top = min(box[n]["y"] for n in ids if rank[n] == r)
        for k, e in enumerate(es):
            corridor[e, "over"] = round(top - (k + 1) * gaps[r - 1] / 2 / (len(es) + 1))

    paths = {}
    for e in order:
        a, b = e
        s, t, x = box[a], box[b], round(lane[e])
        sy, ty = round(mid(a)), round(mid(b))
        if (e, "under") in corridor:
            out = f"M{s['x'] + s['w']:.0f} {sy} H{gap_right(a):.0f} V{corridor[e, 'under']} H{x}"
            low = corridor[e, "under"]
        else:
            out, low = f"M{s['x'] + s['w']:.0f} {sy} H{x}", sy
        if (e, "over") in corridor:
            back_in = f" V{corridor[e, 'over']} H{gap_right(b):.0f} V{ty} H{t['x'] + t['w'] + STUB:.0f}"
            high = corridor[e, "over"]
        else:
            back_in, high = f" V{ty} H{t['x'] + t['w'] + STUB:.0f}", ty
        paths[e] = (out + back_in, x, (low + high) / 2, low)
    return paths


def route(edges, ids, box, rank, back, gaps, near=False):
    """One orthogonal path per edge, and how far right the drawing now reaches.

    `gaps[r]` is the gap after rank r. The rail an edge leaves on runs in the middle of it, or,
    `near`, close to the source: the rest of the gap is the run entering the target, where a
    left-to-right drawing writes the branch's name."""
    def cx(n):
        return box[n]["x"] + box[n]["w"] / 2

    right = max(b["x"] + b["w"] for b in box.values())
    loops = loop_lanes([(a, b) for a, b, _ in edges if (a, b) in back], ids, box, rank, right, gaps)
    out, reach, taken = [], right, []
    for a, b, label in edges:
        s, t = box[a], box[b]
        sx, tx = round(cx(a)), round(cx(b))
        y1, y2 = round(s["y"] + s["h"]), round(t["y"] - STUB)
        rail = round(y1 + (LANE if near else gaps[rank[a]] / 2))
        passed = [box[n] for n in ids if rank[a] < rank[n] < rank[b]]
        lane = None
        if (a, b) in back:  # out of the source's side, up its lane, into the target's side
            d, lane, climb, low = loops[a, b]
            pos = [lane + LABEL_GAP, climb]
            badge = [lane + PASS_ROOM * 2, low - LANE, 1]  # at the foot of its own lane, which no other edge climbs
        elif any(o["x"] - CLEARANCE <= tx <= o["x"] + o["w"] + CLEARANCE for o in passed):  # a box is in the way
            lane, side = detour(tx, passed, taken)
            lane = round(lane)
            taken.append(lane)
            before = gaps[rank[b] - 1]
            low = round(t["y"] - (before - LANE if near else before / 2))
            d = f"M{sx} {y1} V{rail} H{lane} V{low} H{tx} V{y2}"
            badge = [tx - PASS_ROOM * 2, (low + y2) / 2, -1]
            # the label sits on the outer side of the detour, away from the boxes it steps around
            pos = [lane + LABEL_GAP if side > 0 else lane - LABEL_GAP - len(label) * EDGE_CHAR_W, (rail + low) / 2]
        elif sx == tx:
            d = f"M{sx} {y1} V{y2}"
            badge = [sx - PASS_ROOM * 2, (rail + y2) / 2, -1]  # past the rail: above it, the stub is shared with the source's other edges
            # below the rail: above it, the stub is shared with the source's other edges, and a label there names them all
            pos = [sx + CLEARANCE, (rail + y2) / 2 + LABEL_GAP]
        else:
            d = f"M{sx} {y1} V{rail} H{tx} V{y2}"
            badge = [tx - PASS_ROOM * 2, (rail + y2) / 2, -1]
            pos = [(sx + tx) / 2 - len(label) * EDGE_CHAR_W / 2, rail - LABEL_GAP]  # centred on the rail
        if label:  # after the branch's name, on its baseline's middle: the badges read as part of the label
            badge = [pos[0] + len(label) * EDGE_CHAR_W + PASS_ROOM, pos[1] - 4, 1]
        if lane is not None:
            reach = max(reach, lane, lane + LABEL_GAP + len(label) * EDGE_CHAR_W + 3 * PASS_W if label else lane)
        out.append({"from": a, "to": b, "d": d, "label": label or None, "pass": [round(badge[0], 1), round(badge[1], 1), badge[2]],
                    "labelPos": [round(pos[0], 1), round(pos[1], 1)] if label else None})
    return out, reach


def layout(nodes, edges, across=False):
    ids = [n["id"] for n in nodes]
    pairs = [(a, b) for a, b, _ in edges]
    rank, back = rank_nodes(ids, pairs)
    box = {}
    for n in nodes:
        lines, w, h = box_size(n)
        box[n["id"]] = {"w": h, "h": w, "labelLines": lines} if across else {"w": w, "h": h, "labelLines": lines}
    layers = [[i for i in ids if rank[i] == r] for r in range(max(rank.values()) + 1)]
    parents = {i: [a for a, b in pairs if b == i and (a, b) not in back] for i in ids}
    layers = order_layers(layers, parents)
    gaps = across_gaps(edges, rank, back, len(layers)) if across else [GAP_Y] * len(layers)

    y = MARGIN
    for r, layer in enumerate(layers):
        h = max(box[n]["h"] for n in layer)
        for n in layer:
            box[n]["y"] = y + (h - box[n]["h"]) / 2
        y += h + gaps[r]

    def cx(n):
        return box[n]["x"] + box[n]["w"] / 2
    place_layer(layers[0], box, {n: 0 for n in layers[0]})
    for layer in layers[1:]:
        place_layer(layer, box, {n: sum(cx(p) for p in parents[n]) / len(parents[n]) for n in layer})

    left = min(b["x"] for b in box.values())
    for b in box.values():
        b["x"] = round(b["x"] - left + MARGIN, 1)
        b["y"] = round(b["y"], 1)

    routed, reach = route(edges, ids, box, rank, back, gaps, near=across)
    height = max(b["y"] + b["h"] for b in box.values()) + MARGIN + LANE  # the last layer gets a little more room below
    geo = {"width": round(reach + MARGIN), "height": round(height), "lineHeight": LINE_H, "nodes": box, "edges": routed}
    return turn(geo, back) if across else geo


def in_loop(edges, back):
    """The nodes a loop comes back through: only their edges ever carry pass badges."""
    succ = {}
    for a, b, _ in edges:
        succ.setdefault(a, []).append(b)
    looped = set()
    for a, b in back:  # b ... a, then a -> b: every node on a way from b to a is in the loop
        reach, todo = {b}, [b]
        while todo:
            for m in succ.get(todo.pop(), []):
                if m not in reach:
                    reach.add(m)
                    todo.append(m)
        looped |= {n for n in reach if n == a or a in walk(succ, n)}
    return looped


def walk(succ, n):
    seen, todo = {n}, [n]
    while todo:
        for m in succ.get(todo.pop(), []):
            if m not in seen:
                seen.add(m)
                todo.append(m)
    return seen


def across_gaps(edges, rank, back, n):
    """Left to right, a branch's name is written on the run entering its target, after a rail kept
    close to the source: the gap before a rank holds the longest name entering it, and the pass
    badges after it when its source is in a loop."""
    looped = in_loop(edges, back)
    gaps = [GAP_Y] * n
    for a, b, label in edges:
        if (a, b) in back:
            continue
        need = LANE + LABEL_GAP + len(label or "") * EDGE_CHAR_W + PASS_ROOM + \
            (3 * PASS_W if a in looped else 0) + STUB + GRID
        gaps[rank[b] - 1] = max(gaps[rank[b] - 1], GRID * math.ceil(need / GRID))
    return gaps


def turned_path(d):
    """M x y → M y x, and every horizontal run becomes a vertical one: the drawing mirrored on its diagonal."""
    return re.sub(r"([MHV])(-?[\d.]+)(?: (-?[\d.]+))?",
                  lambda m: f"M{m[3]} {m[2]}" if m[1] == "M" else ("V" if m[1] == "H" else "H") + m[2], d)


def points(d):
    """The corners of an orthogonal path, in order."""
    pts = []
    for cmd, a, b in re.findall(r"([MHV])(-?[\d.]+)(?: (-?[\d.]+))?", d):
        x, y = pts[-1] if pts else (0, 0)
        pts.append((float(a), float(b)) if cmd == "M" else (float(a), y) if cmd == "H" else (x, float(a)))
    return pts


def turn(geo, back):
    """The top-down layout of quarter-turned boxes, mirrored on its diagonal: ranks now run left to right.

    Each edge's name is set again, horizontal: on the stretch entering its target, above it, the
    pass badges after it. A loop, which ran up a lane right of the drawing, now runs under it:
    its name sits above its lane's long run, which no other edge shares."""
    nodes = {i: {**b, "x": b["y"], "y": b["x"], "w": b["h"], "h": b["w"]} for i, b in geo["nodes"].items()}
    edges, bottom, right = [], geo["width"], geo["height"]
    for e in geo["edges"]:
        d = turned_path(e["d"])
        pts = points(d)
        w = len(e["label"] or "") * EDGE_CHAR_W
        if (e["from"], e["to"]) in back:
            (x1, y), (x2, _) = max(zip(pts, pts[1:]), key=lambda s: abs(s[1][0] - s[0][0]) if s[0][1] == s[1][1] else -1)
            pos = [min(x1, x2) + (abs(x2 - x1) - w) / 2, y - LABEL_GAP]
        else:
            (x1, y), _ = pts[-2], pts[-1]  # the run entering the target
            if len(pts) == 2:  # a straight edge: its source's other branches leave on a rail just past it
                x1 += LANE
            pos = [x1 + LABEL_GAP, y - LABEL_GAP]
        badge = [pos[0] + w + PASS_ROOM, pos[1] - 4, 1] if e["label"] else [pos[0], y - 10, 1]
        bottom = max(bottom, max(p[1] for p in pts) + MARGIN)
        right = max(right, max(p[0] for p in pts) + MARGIN)  # a corridor under the last rank runs past its boxes
        edges.append({**e, "d": d, "pass": [round(badge[0], 1), round(badge[1], 1), 1],
                      "labelPos": [round(pos[0], 1), round(pos[1], 1)] if e["label"] else None})
    return {"width": round(right), "height": round(bottom), "lineHeight": geo["lineHeight"], "nodes": nodes, "edges": edges,
            "across": True}
