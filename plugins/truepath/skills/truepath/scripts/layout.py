"""Top-down layered layout of a process graph: boxes sized to their label, orthogonal edges.

    layout(nodes, edges) -> {width, height, lineHeight,
                             nodes: {id: {x, y, w, h, labelLines}},
                             edges: [{from, to, d, label, labelPos}]}

A node's rank is its longest path from the sources; a rank is drawn as one layer. An edge that
climbs back (a loop) runs in a lane of its own to the right of every box. An edge that would
cross a box on its way down steps aside just past the boxes in its way, on the nearer side:
sent around the whole drawing, it was the longest line on the page and widened it for nothing.
Pure stdlib, deterministic: the same graph gives the same file.

The page draws with the fonts these widths assume: node labels in 13px monospace, edge
labels in 11px sans (see `.node text` and `.elabel` in runtime.html).
"""
import math

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


def route(edges, ids, box, rank, back):
    """One orthogonal path per edge, and how far right the drawing now reaches."""
    def cx(n):
        return box[n]["x"] + box[n]["w"] / 2

    right = max(b["x"] + b["w"] for b in box.values())
    out, lanes, reach, taken = [], 0, right, []
    for a, b, label in edges:
        s, t = box[a], box[b]
        sx, tx = round(cx(a)), round(cx(b))
        y1, y2 = round(s["y"] + s["h"]), round(t["y"] - STUB)
        rail = round(y1 + GAP_Y / 2)
        passed = [box[n] for n in ids if rank[a] < rank[n] < rank[b]]
        lane = None
        if (a, b) in back:  # out of the source's side, up the lane, into the target's side
            lanes += 1
            lane = right + LANE * lanes
            sy, ty = round(s["y"] + s["h"] / 2), round(t["y"] + t["h"] / 2)
            d = f"M{s['x'] + s['w']:.0f} {sy} H{lane:.0f} V{ty} H{t['x'] + t['w'] + STUB:.0f}"
            pos = [lane + LABEL_GAP, (sy + ty) / 2]
        elif any(o["x"] - CLEARANCE <= tx <= o["x"] + o["w"] + CLEARANCE for o in passed):  # a box is in the way
            lane, side = detour(tx, passed, taken)
            lane = round(lane)
            taken.append(lane)
            low = round(t["y"] - GAP_Y / 2)
            d = f"M{sx} {y1} V{rail} H{lane} V{low} H{tx} V{y2}"
            # the label sits on the outer side of the detour, away from the boxes it steps around
            pos = [lane + LABEL_GAP if side > 0 else lane - LABEL_GAP - len(label) * EDGE_CHAR_W, (rail + low) / 2]
        elif sx == tx:
            d = f"M{sx} {y1} V{y2}"
            # below the rail: above it, the stub is shared with the source's other edges, and a label there names them all
            pos = [sx + CLEARANCE, (rail + y2) / 2 + LABEL_GAP]
        else:
            d = f"M{sx} {y1} V{rail} H{tx} V{y2}"
            pos = [(sx + tx) / 2 - len(label) * EDGE_CHAR_W / 2, rail - LABEL_GAP]  # centred on the rail
        if lane is not None:
            reach = max(reach, lane, lane + LABEL_GAP + len(label) * EDGE_CHAR_W if label else lane)
        out.append({"from": a, "to": b, "d": d, "label": label or None,
                    "labelPos": [round(pos[0], 1), round(pos[1], 1)] if label else None})
    return out, reach


def layout(nodes, edges):
    ids = [n["id"] for n in nodes]
    pairs = [(a, b) for a, b, _ in edges]
    rank, back = rank_nodes(ids, pairs)
    box = {}
    for n in nodes:
        lines, w, h = box_size(n)
        box[n["id"]] = {"w": w, "h": h, "labelLines": lines}
    layers = [[i for i in ids if rank[i] == r] for r in range(max(rank.values()) + 1)]
    parents = {i: [a for a, b in pairs if b == i and (a, b) not in back] for i in ids}
    layers = order_layers(layers, parents)

    y = MARGIN
    for layer in layers:
        h = max(box[n]["h"] for n in layer)
        for n in layer:
            box[n]["y"] = y + (h - box[n]["h"]) / 2
        y += h + GAP_Y

    def cx(n):
        return box[n]["x"] + box[n]["w"] / 2
    place_layer(layers[0], box, {n: 0 for n in layers[0]})
    for layer in layers[1:]:
        place_layer(layer, box, {n: sum(cx(p) for p in parents[n]) / len(parents[n]) for n in layer})

    left = min(b["x"] for b in box.values())
    for b in box.values():
        b["x"] = round(b["x"] - left + MARGIN, 1)
        b["y"] = round(b["y"], 1)

    routed, reach = route(edges, ids, box, rank, back)
    height = max(b["y"] + b["h"] for b in box.values()) + MARGIN + LANE  # the last layer gets a little more room below
    return {"width": round(reach + MARGIN), "height": round(height), "lineHeight": LINE_H, "nodes": box, "edges": routed}
