"""Automatic reference-designator placement on F.Silkscreen.

For each footprint, candidate positions around its courtyard are tried (horizontal text first,
then vertical) and the first one that keeps clear of pads (copper), silkscreen graphics, already
placed texts and the board edge is used.  Manual overrides in layout.REF_TEXT win."""
import math
import pcbnew

MM = pcbnew.FromMM
ToMM = pcbnew.ToMM
PAD_GAP = 0.15     # silk to copper (pads)
SILK_GAP = 0.12    # silk to silk
EDGE_GAP = 0.3     # silk to board edge


def _rect(bb, grow=0.0):
    return (ToMM(bb.GetLeft()) - grow, ToMM(bb.GetTop()) - grow, ToMM(bb.GetRight()) + grow, ToMM(bb.GetBottom()) + grow)


def _rect_overlap(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def _pt_seg(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L2))
    cx, cy = ax + t * dx, ay + t * dy
    return math.hypot(px - cx, py - cy)


def _seg_rect_dist(seg, r):
    (ax, ay, bx, by) = seg
    # inside test / intersection: sample-free exact test via separating distances
    if r[0] <= ax <= r[2] and r[1] <= ay <= r[3]:
        return 0.0
    if r[0] <= bx <= r[2] and r[1] <= by <= r[3]:
        return 0.0
    edges = [(r[0], r[1], r[2], r[1]), (r[2], r[1], r[2], r[3]), (r[2], r[3], r[0], r[3]), (r[0], r[3], r[0], r[1])]
    def inter(p, q):
        def orient(a, b, c):
            return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        p1, p2, q1, q2 = (p[0], p[1]), (p[2], p[3]), (q[0], q[1]), (q[2], q[3])
        d1, d2 = orient(q1, q2, p1), orient(q1, q2, p2)
        d3, d4 = orient(p1, p2, q1), orient(p1, p2, q2)
        return (d1 * d2 < 0) and (d3 * d4 < 0)
    for e in edges:
        if inter(seg, e):
            return 0.0
    d = min(_pt_seg(cx, cy, ax, ay, bx, by) for cx, cy in ((r[0], r[1]), (r[2], r[1]), (r[2], r[3]), (r[0], r[3])))
    d = min(d, min(_pt_seg(px, py, *e) for px, py in ((ax, ay), (bx, by)) for e in edges))
    return d


def collect_obstacles(board):
    pads, segs, rects = [], [], []
    for fp in board.Footprints():
        for p in fp.Pads():
            if p.IsOnLayer(pcbnew.F_Cu) or p.GetAttribute() == pcbnew.PAD_ATTRIB_PTH:
                pads.append(_rect(p.GetBoundingBox()))
        for g in fp.GraphicalItems():
            if g.GetLayer() != pcbnew.F_SilkS or not isinstance(g, pcbnew.PCB_SHAPE):
                continue
            w = ToMM(g.GetWidth()) / 2
            st = g.GetShape()
            if st == pcbnew.SHAPE_T_SEGMENT:
                a, b = g.GetStart(), g.GetEnd()
                segs.append(((ToMM(a.x), ToMM(a.y), ToMM(b.x), ToMM(b.y)), w))
            elif st == pcbnew.SHAPE_T_CIRCLE:
                c = g.GetCenter(); R = ToMM(g.GetRadius()); cx, cy = ToMM(c.x), ToMM(c.y)
                n = 24
                for i in range(n):
                    a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
                    segs.append(((cx + R * math.cos(a0), cy + R * math.sin(a0), cx + R * math.cos(a1), cy + R * math.sin(a1)), w))
            elif st in (pcbnew.SHAPE_T_RECT, pcbnew.SHAPE_T_RECTANGLE):
                cs = [ToMM(v) for pt in g.GetRectCorners() for v in (pt.x, pt.y)] if hasattr(g, "GetRectCorners") else None
                bb = g.GetBoundingBox()
                l, t, r_, b_ = _rect(bb)
                for e in ((l, t, r_, t), (r_, t, r_, b_), (r_, b_, l, b_), (l, b_, l, t)):
                    segs.append((e, w))
            else:
                rects.append(_rect(g.GetBoundingBox(), w))
    return pads, segs, rects


def text_rect(field):
    return _rect(field.GetBoundingBox())


def fits(r, obst, placed, board_rect):
    pads, segs, rects = obst
    if r[0] < board_rect[0] + EDGE_GAP or r[1] < board_rect[1] + EDGE_GAP or r[2] > board_rect[2] - EDGE_GAP or r[3] > board_rect[3] - EDGE_GAP:
        return False
    for p in pads:
        if _rect_overlap((r[0] - PAD_GAP, r[1] - PAD_GAP, r[2] + PAD_GAP, r[3] + PAD_GAP), p):
            return False
    for s, w in segs:
        if _seg_rect_dist(s, r) < w + SILK_GAP:
            return False
    for q in rects + placed:
        if _rect_overlap((r[0] - SILK_GAP, r[1] - SILK_GAP, r[2] + SILK_GAP, r[3] + SILK_GAP), q):
            return False
    return True


def autoplace(board, fps, size, thick, board_rect, overrides, order, extra_placed=None):
    obst = collect_obstacles(board)
    placed = list(extra_placed or [])
    report = {}
    for ref in order:
        fp = fps[ref]
        f = fp.Reference()
        f.SetTextSize(pcbnew.VECTOR2I(MM(size), MM(size)))
        f.SetTextThickness(MM(thick))
        f.SetKeepUpright(True) if hasattr(f, "SetKeepUpright") else None
        if ref in overrides:
            spec = overrides[ref]
            if spec is None:
                f.SetVisible(False)
                report[ref] = "hidden"
                continue
            u, v, ang = spec
            f.SetTextAngleDegrees(ang)
            f.SetTextPos(pcbnew.VECTOR2I(MM(u), MM(v)))
            placed.append(text_rect(f))
            report[ref] = "manual"
            continue
        cy = fp.GetCourtyard(pcbnew.F_CrtYd).BBox()
        l, t, r, b = ToMM(cy.GetLeft()), ToMM(cy.GetTop()), ToMM(cy.GetRight()), ToMM(cy.GetBottom())
        cx, cyy = (l + r) / 2, (t + b) / 2
        g = 0.15 + size / 2
        cands = []
        for ang in (0, 90):
            half_w_guess = 0  # computed from the real bbox below
            cands += [(ang, "top", cx, t - g), (ang, "bottom", cx, b + g), (ang, "left", l - g, cyy), (ang, "right", r + g, cyy),
                      (ang, "tl", l, t - g), (ang, "tr", r, t - g), (ang, "bl", l, b + g), (ang, "br", r, b + g)]
        best = None
        for ang, where, x, y in cands:
            f.SetTextAngleDegrees(ang)
            f.SetTextPos(pcbnew.VECTOR2I(MM(x), MM(y)))
            rr = text_rect(f)
            w, h = rr[2] - rr[0], rr[3] - rr[1]
            # push the text out so its bbox just clears the courtyard on the chosen side
            if where == "top" or where in ("tl", "tr"):
                y = t - 0.1 - h / 2
            if where == "bottom" or where in ("bl", "br"):
                y = b + 0.1 + h / 2
            if where == "left":
                x = l - 0.1 - w / 2
            if where == "right":
                x = r + 0.1 + w / 2
            if where in ("tl", "bl"):
                x = l + w / 2
            if where in ("tr", "br"):
                x = r - w / 2
            for dx, dy in ((0, 0), (0.6, 0), (-0.6, 0), (0, 0.6), (0, -0.6), (1.2, 0), (-1.2, 0)):
                f.SetTextPos(pcbnew.VECTOR2I(MM(x + dx), MM(y + dy)))
                rr = text_rect(f)
                if fits(rr, obst, placed, board_rect):
                    best = (ang, where, x + dx, y + dy, rr)
                    break
            if best:
                break
        if best:
            ang, where, x, y, rr = best
            f.SetTextAngleDegrees(ang)
            f.SetTextPos(pcbnew.VECTOR2I(MM(x), MM(y)))
            placed.append(rr)
            report[ref] = "%s/%d at (%.2f, %.2f)" % (where, ang, x, y)
        else:
            f.SetTextAngleDegrees(0)
            f.SetTextPos(pcbnew.VECTOR2I(MM(cx), MM(t - g)))
            report[ref] = "NO FIT"
    return report
