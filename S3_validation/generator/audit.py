"""Independent geometric/electrical audit of the generated board (KiCad python)."""
import sys, math, collections, itertools
import pcbnew

b = pcbnew.LoadBoard(sys.argv[1])
mm = pcbnew.ToMM
OX, OY = 100.0, 100.0
out = []
P = lambda *a: out.append(" ".join(str(x) for x in a))

# ---------- board outline ----------
edges = [d for d in b.GetDrawings() if d.GetLayer() == pcbnew.Edge_Cuts]
bb = b.GetBoardEdgesBoundingBox()
P("EDGE.CUTS items:", len(edges), [e.SHAPE_T_asString() if hasattr(e, "SHAPE_T_asString") else e.GetShape() for e in edges])
P("BOARD SIZE: %.2f x %.2f mm (bbox of Edge.Cuts)" % (mm(bb.GetWidth()), mm(bb.GetHeight())))
outline = pcbnew.SHAPE_POLY_SET()
ok = b.GetBoardPolygonOutlines(outline, True) if hasattr(b, "GetBoardPolygonOutlines") else None
P("closed outline polygon:", ok, "outlines:", outline.OutlineCount())

# ---------- footprints inside board ----------
for fp in b.Footprints():
    cy = fp.GetCourtyard(pcbnew.F_CrtYd).BBox()
    inside = (cy.GetLeft() >= bb.GetLeft() and cy.GetRight() <= bb.GetRight() and cy.GetTop() >= bb.GetTop() and cy.GetBottom() <= bb.GetBottom())
    if not inside:
        P("COURTYARD OUTSIDE BOARD:", fp.GetReference())
P("footprints:", len(list(b.Footprints())), "all on F.Cu:", all(fp.GetLayer() == pcbnew.F_Cu for fp in b.Footprints()))

# ---------- nets / classes / widths ----------
tracks = [t for t in b.GetTracks() if t.Type() == pcbnew.PCB_TRACE_T]
vias = [t for t in b.GetTracks() if t.Type() == pcbnew.PCB_VIA_T]
bynet = collections.defaultdict(list)
for t in tracks:
    bynet[t.GetNetname()].append(t)
P("\nNET | class | widths used (mm) | F.Cu len | B.Cu len | segments")
for ni in b.GetNetInfo().NetsByName().values() if hasattr(b.GetNetInfo(), "NetsByName") else []:
    pass
names = sorted(set(p.GetNetname() for fp in b.Footprints() for p in fp.Pads()))
for n in names:
    if n.startswith("unconnected") or n == "":
        continue
    net = b.FindNet(n)
    cls = net.GetNetClassName() if net else "?"
    ts = bynet.get(n, [])
    ws = sorted(set(round(mm(t.GetWidth()), 3) for t in ts))
    lf = sum(mm(t.GetLength()) for t in ts if t.GetLayer() == pcbnew.F_Cu)
    lb = sum(mm(t.GetLength()) for t in ts if t.GetLayer() == pcbnew.B_Cu)
    P("%-28s %-7s %-22s %6.2f %6.2f %3d" % (n, cls, ws, lf, lb, len(ts)))
unc = sorted(set(p.GetNetname() for fp in b.Footprints() for p in fp.Pads() if p.GetNetname().startswith("unconnected")))
P("single-pad 'unconnected-*' nets (MCU NC pins):", len(unc), "-> class", set(b.FindNet(n).GetNetClassName() for n in unc))

# ---------- vias ----------
P("\nVIAS:", len(vias))
for v in vias:
    pos = v.GetPosition()
    P("  via net=%-26s at (%.2f, %.2f) dia %.2f drill %.2f type %s" % (v.GetNetname(), mm(pos.x) - OX, mm(pos.y) - OY, mm(v.GetWidth(pcbnew.F_Cu)), mm(v.GetDrillValue()), v.GetViaType()))

# ---------- min distances between copper of different nets (tracks vs tracks/pads/vias) ----------
def seg(t):
    s, e = t.GetStart(), t.GetEnd()
    return (mm(s.x), mm(s.y), mm(e.x), mm(e.y))

def segseg(a, c):
    def pt(px, py, ax, ay, bx, by):
        dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy
        t = 0 if L2 == 0 else max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L2))
        return math.hypot(px - ax - t * dx, py - ay - t * dy)
    def inter(a, c):
        def o(p, q, r): return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
        p1, p2, q1, q2 = a[:2], a[2:], c[:2], c[2:]
        return o(q1, q2, p1) * o(q1, q2, p2) < 0 and o(p1, p2, q1) * o(p1, p2, q2) < 0
    if inter(a, c): return 0.0
    return min(pt(a[0], a[1], *c), pt(a[2], a[3], *c), pt(c[0], c[1], *a), pt(c[2], c[3], *a))

mind = (9e9, None)
for t1, t2 in itertools.combinations(tracks, 2):
    if t1.GetLayer() != t2.GetLayer() or t1.GetNetCode() == t2.GetNetCode():
        continue
    d = segseg(seg(t1), seg(t2)) - mm(t1.GetWidth()) / 2 - mm(t2.GetWidth()) / 2
    if d < mind[0]:
        mind = (d, (t1.GetNetname(), t2.GetNetname()))
P("\nMIN track-track edge distance (different nets, same layer): %.3f mm %s" % mind)

# track to pad: use KiCad's own geometry (pad effective shape)
mintp = (9e9, None)
for t in tracks:
    for fp in b.Footprints():
        for p in fp.Pads():
            if p.GetNetCode() == t.GetNetCode() or not p.IsOnLayer(t.GetLayer()):
                continue
            sh = p.GetEffectiveShape(t.GetLayer())
            d = mm(sh.GetClearance(t.GetEffectiveShape())) if hasattr(sh, "GetClearance") else None
            if d is None:
                continue
            if d < mintp[0]:
                mintp = (d, (t.GetNetname(), fp.GetReference() + "." + p.GetNumber()))
P("MIN track-pad distance (different nets): %.3f mm %s" % mintp)

# track to via (different nets): via copper on the track's layer
mintv = (9e9, None)
for t in tracks:
    for v in vias:
        if v.GetNetCode() == t.GetNetCode():
            continue
        d = mm(v.GetEffectiveShape(t.GetLayer()).GetClearance(t.GetEffectiveShape()))
        if d < mintv[0]:
            mintv = (d, (t.GetNetname(), v.GetNetname()))
P("MIN track-via distance (different nets): %.3f mm %s" % mintv)

# ---------- angles at track joints ----------
joints = collections.defaultdict(list)
for t in tracks:
    s, e = t.GetStart(), t.GetEnd()
    joints[(t.GetNetCode(), t.GetLayer(), s.x, s.y)].append((t, e))
    joints[(t.GetNetCode(), t.GetLayer(), e.x, e.y)].append((t, s))
angles = collections.Counter()
acute = []
for k, lst in joints.items():
    if len(lst) != 2:
        continue
    (_, _, x, y) = k
    (t1, o1), (t2, o2) = lst
    v1 = (o1.x - x, o1.y - y); v2 = (o2.x - x, o2.y - y)
    n1, n2 = math.hypot(*v1), math.hypot(*v2)
    if n1 == 0 or n2 == 0:
        continue
    ang = math.degrees(math.acos(max(-1, min(1, (v1[0] * v2[0] + v1[1] * v2[1]) / (n1 * n2)))))
    angles[round(ang)] += 1
    if ang < 90 - 1e-6:
        acute.append((t1.GetNetname(), round(mm(x) - OX, 2), round(mm(y) - OY, 2), round(ang, 1)))
P("\nInterior angles at 2-segment joints (180 = straight):", dict(sorted(angles.items())))
P("ACUTE joints (<90 deg):", acute)

# ---------- every junction, including 3-way and T (track end on another track's interior) ----------
def _arms(P, net, layer):
    """unit direction + half width of every copper arm leaving point P on (net, layer)"""
    out = []
    for t in tracks:
        if t.GetNetCode() != net or t.GetLayer() != layer:
            continue
        a, c = t.GetStart(), t.GetEnd()
        hw = t.GetWidth() / 2.0
        L = math.hypot(c.x - a.x, c.y - a.y)
        if L == 0:
            continue
        ux, uy = (c.x - a.x) / L, (c.y - a.y) / L
        if (a.x, a.y) == (P.x, P.y):
            out.append((ux, uy, hw))
        elif (c.x, c.y) == (P.x, P.y):
            out.append((-ux, -uy, hw))
        else:
            tt = ((P.x - a.x) * ux + (P.y - a.y) * uy)
            if 0 < tt < L and abs((P.x - a.x) * uy - (P.y - a.y) * ux) < 2:   # P on the segment interior (2 nm)
                out.append((ux, uy, hw)); out.append((-ux, -uy, hw))
    return out

def _inner_corner(P, a1, a2):
    """intersection of the facing copper edges of two arms (a = (ux, uy, half_width))"""
    (u1x, u1y, w1), (u2x, u2y, w2) = a1, a2
    cross = u1x * u2y - u1y * u2x
    if abs(cross) < 1e-9:
        return None
    s1 = 1 if cross > 0 else -1        # normal of arm 1 pointing towards arm 2
    n1 = (-u1y * s1, u1x * s1); n2 = (u2y * s1, -u2x * s1)
    # P + n1*w1 + t*u1 = P + n2*w2 + s*u2
    bx, by = n2[0] * w2 - n1[0] * w1, n2[1] * w2 - n1[1] * w1
    det = u1x * (-u2y) - (-u2x) * u1y
    tpar = (bx * (-u2y) - (-u2x) * by) / det
    return (P.x + n1[0] * w1 + tpar * u1x, P.y + n1[1] * w1 + tpar * u1y)

seen = set(); multi = 0; acute_all = []
for t in tracks:
    for Q in (t.GetStart(), t.GetEnd()):
        key = (t.GetNetCode(), t.GetLayer(), Q.x, Q.y)
        if key in seen:
            continue
        seen.add(key)
        arms = _arms(Q, t.GetNetCode(), t.GetLayer())
        if len(arms) < 2:
            continue
        if len(arms) >= 3:
            multi += 1
        arms.sort(key=lambda a: math.atan2(a[1], a[0]))
        for i in range(len(arms)):
            a1, a2 = arms[i], arms[(i + 1) % len(arms)]
            g = (math.degrees(math.atan2(a2[1], a2[0]) - math.atan2(a1[1], a1[0]))) % 360
            if g < 89.5 and len(arms) > 1:
                c = _inner_corner(Q, a1, a2)
                inside = False
                if c is not None:
                    cp = pcbnew.VECTOR2I(int(round(c[0])), int(round(c[1])))
                    for f in b.GetFootprints():
                        for pd in f.Pads():
                            if pd.GetNetCode() == t.GetNetCode() and pd.IsOnLayer(t.GetLayer()) and pd.GetEffectiveShape(t.GetLayer()).Collide(cp, 0):
                                inside = True
                acute_all.append((t.GetNetname(), b.GetLayerName(t.GetLayer()), round(mm(Q.x) - OX, 3), round(mm(Q.y) - OY, 3), round(g, 1),
                                  "inner corner inside a pad" if inside else "INNER CORNER ON BARE LAMINATE"))
P("Junctions with 3 or more arms (incl. T on a track interior):", multi)
P("ACUTE angles between adjacent arms at any junction:", acute_all if acute_all else "none")

# ---------- zones ----------
for z in b.Zones():
    P("ZONE", z.GetZoneName(), b.GetLayerName(z.GetLayer()), z.GetNetname(), "filled:", z.IsFilled(), "area %.1f mm2" % (z.GetFilledArea() / 1e12 if hasattr(z, "GetFilledArea") else -1),
      "clearance", mm(z.GetLocalClearance()) if not callable(getattr(z.GetLocalClearance(), "value", None)) else mm(z.GetLocalClearance().value()),
      "thermal gap", mm(z.GetThermalReliefGap()), "spoke", mm(z.GetThermalReliefSpokeWidth()))

# ---------- design settings ----------
ds = b.GetDesignSettings()
P("\nRULES: min clearance %.3f, min track %.3f, min via %.3f, min drill %.3f, edge clearance %.3f, board thickness %.3f, copper layers %d, has stackup %s" % (
    mm(ds.m_MinClearance), mm(ds.m_TrackMinWidth), mm(ds.m_ViasMinSize), mm(ds.m_MinThroughDrill), mm(ds.m_CopperEdgeClearance), mm(ds.GetBoardThickness()), b.GetCopperLayerCount(), ds.m_HasStackup))
ns = ds.m_NetSettings
for name in ("Default", "GND", "POWER", "SIGNAL"):
    nc = ns.GetDefaultNetclass() if name == "Default" else ns.GetNetClassByName(name)
    P("NETCLASS %-8s clearance %.2f track %.2f via %.2f/%.2f priority %s" % (name, mm(nc.GetClearance()), mm(nc.GetTrackWidth()), mm(nc.GetViaDiameter()), mm(nc.GetViaDrill()), nc.GetPriority()))
print("\n".join(out))
_printed = len(out)   # everything appended after this point is printed at the end

# ---------- silkscreen legends vs pad mask openings and vs other legends ----------
texts = [(t.GetText(), t) for t in b.GetDrawings() if t.Type() == pcbnew.PCB_TEXT_T and t.GetLayer() == pcbnew.F_SilkS]
texts += [(fp.GetReference(), fp.Reference()) for fp in b.Footprints() if fp.Reference().IsVisible() and fp.Reference().GetLayer() == pcbnew.F_SilkS]
pads = [(fp.GetReference() + "." + p.GetNumber(), p) for fp in b.Footprints() for p in fp.Pads()]
low = []
for name, t in texts:
    ts = t.GetEffectiveTextShape()
    best = (9e9, None)
    for pn, p in pads:
        if not (p.IsOnLayer(pcbnew.F_Mask)):
            continue
        d = mm(p.GetEffectiveShape(pcbnew.F_Cu).GetClearance(ts))
        if d < best[0]:
            best = (d, pn)
    if best[0] < 0.15:
        low.append((name, round(best[0], 3), best[1]))
P("\nSILK legends closer than 0.15 mm to a mask opening:", low if low else "none")
lowtt = []
for (n1, t1), (n2, t2) in itertools.combinations(texts, 2):
    d = mm(t1.GetEffectiveTextShape().GetClearance(t2.GetEffectiveTextShape()))
    if d < 0.2:
        lowtt.append((n1, n2, round(d, 3)))
P("SILK legend pairs closer than 0.2 mm:", lowtt if lowtt else "none")
# legends vs footprint silkscreen graphics (outlines, rings, pin-1 marks) and vs via drills.
# Computed geometrically (text polygon points against segments / circles / polygons), because
# SHAPE.GetClearance() is not reliable for every pair of shape types through the Python bindings.
def _text_pts(t):
    ps = pcbnew.SHAPE_POLY_SET()
    t.TransformTextToPolySet(ps, 0, pcbnew.FromMM(0.005), pcbnew.ERROR_INSIDE)
    pts = []
    for i in range(ps.OutlineCount()):
        ol = ps.Outline(i); n = ol.PointCount()
        for k in range(n):
            a, c = ol.CPoint(k), ol.CPoint((k + 1) % n)
            for q in range(4):
                pts.append((a.x + (c.x - a.x) * q / 4.0, a.y + (c.y - a.y) * q / 4.0))
    return pts, ps
def _seg_d(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    u = 0 if L2 == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L2))
    return math.hypot(px - (ax + u * dx), py - (ay + u * dy))
def _graphic_gap(pts, g):
    w = g.GetWidth() / 2.0
    st = g.GetShape()
    if st == pcbnew.SHAPE_T_CIRCLE and not g.IsSolidFill():
        c = g.GetCenter(); R = g.GetRadius()
        return min(abs(math.hypot(x - c.x, y - c.y) - R) for x, y in pts) - w
    if st == pcbnew.SHAPE_T_SEGMENT:
        a, c = g.GetStart(), g.GetEnd()
        return min(_seg_d(x, y, a.x, a.y, c.x, c.y) for x, y in pts) - w
    gp = pcbnew.SHAPE_POLY_SET()
    g.TransformShapeToPolygon(gp, g.GetLayer(), 0, pcbnew.FromMM(0.005), pcbnew.ERROR_INSIDE)
    best = 9e18
    for i in range(gp.OutlineCount()):
        ol = gp.Outline(i); n = ol.PointCount()
        for k in range(n):
            a, c = ol.CPoint(k), ol.CPoint((k + 1) % n)
            best = min(best, min(_seg_d(x, y, a.x, a.y, c.x, c.y) for x, y in pts))
    if any(gp.Contains(pcbnew.VECTOR2I(int(x), int(y))) for x, y in pts[::7]):
        best = 0
    return best
silk_g = [(fp.GetReference(), g) for fp in b.Footprints() for g in fp.GraphicalItems()
          if g.GetLayer() == pcbnew.F_SilkS and g.GetClass() == "PCB_SHAPE"]
worst = []
for name, t in texts:
    pts, _ = _text_pts(t)
    tb = t.GetEffectiveTextShape().BBox()
    best = (9e18, None)
    for r, g in silk_g:
        gb = g.GetBoundingBox()
        if gb.GetLeft() > tb.GetRight() + 1000000 or gb.GetRight() < tb.GetLeft() - 1000000 or gb.GetTop() > tb.GetBottom() + 1000000 or gb.GetBottom() < tb.GetTop() - 1000000:
            continue
        d = _graphic_gap(pts, g)
        if d < best[0]:
            best = (d, r)
    if best[1] is not None:
        worst.append((round(mm(best[0]), 3), name, best[1]))
worst.sort()
P("SILK legend -> nearest footprint silkscreen graphic (5 smallest):", worst[:5])
dr = []
for v in vias:
    c = v.GetPosition(); rh = v.GetDrillValue() / 2.0
    for r, g in silk_g:
        if g.GetShape() == pcbnew.SHAPE_T_SEGMENT:
            a, e = g.GetStart(), g.GetEnd()
            d = _seg_d(c.x, c.y, a.x, a.y, e.x, e.y) - g.GetWidth() / 2.0 - rh
        elif g.GetShape() == pcbnew.SHAPE_T_CIRCLE:
            d = abs(math.hypot(c.x - g.GetCenter().x, c.y - g.GetCenter().y) - g.GetRadius()) - g.GetWidth() / 2.0 - rh
        else:
            gp = pcbnew.SHAPE_POLY_SET()
            g.TransformShapeToPolygon(gp, g.GetLayer(), 0, pcbnew.FromMM(0.005), pcbnew.ERROR_INSIDE)
            d = 9e18
            for i in range(gp.OutlineCount()):
                ol = gp.Outline(i); n = ol.PointCount()
                for k in range(n):
                    a, e = ol.CPoint(k), ol.CPoint((k + 1) % n)
                    d = min(d, _seg_d(c.x, c.y, a.x, a.y, e.x, e.y) - rh)
        if d < 0.1e6:
            dr.append((v.GetNetname(), round(mm(c.x) - OX, 2), round(mm(c.y) - OY, 2), r, round(mm(d), 3)))
P("VIA drills closer than 0.1 mm to footprint silkscreen (fab clips the silk there):", dr if dr else "none")
P("SILK legend sizes:", sorted(set((round(mm(t.GetTextHeight()), 2), round(mm(t.GetTextThickness()), 2)) for _, t in texts)))
print("\n".join(out[_printed:]))
