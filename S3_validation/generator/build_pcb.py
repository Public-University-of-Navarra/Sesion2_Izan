"""DEE Session 3 - board generator for Sesion2_Izan (KiCad 10, pcbnew Python API).

Reproduces "Update PCB from Schematic" from the kicad-cli netlist (same footprint path, fields,
sheet name/file, filters, pad nets, pin function/type), then applies board setup (rules, net
classes), placement, Edge.Cuts, routing and copper zones described in layout.py.

usage: python.exe build_pcb.py <kicad_project_dir> <netlist.net> [--no-route] [--no-zones]
"""
import os, sys, math
import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from netlist import read_netlist
import layout as L
import silk

FPDIR = os.environ.get("KICAD10_FOOTPRINT_DIR", r"C:/Program Files/KiCad/10.0/share/kicad/footprints")
MM = pcbnew.FromMM
ToMM = pcbnew.ToMM


def P(u, v):
    """board-local (u, v) mm  ->  KiCad internal coordinates"""
    return pcbnew.VECTOR2I(MM(L.OX + u), MM(L.OY + v))


def clear_board(board):
    for it in list(board.Footprints()):
        board.Remove(it)
    for it in list(board.GetTracks()):
        board.Remove(it)
    for it in list(board.Zones()):
        board.Remove(it)
    for it in list(board.GetDrawings()):
        board.Remove(it)


def setup_rules(board):
    ds = board.GetDesignSettings()
    # --- constraints (Board Setup > Design Rules > Constraints) ---
    ds.m_MinClearance = MM(L.MIN_CLEARANCE)      # REQUISITO: clearance 0.20 mm
    ds.m_TrackMinWidth = MM(L.MIN_TRACK_WIDTH)   # REQUISITO: track width >= 0.25 mm
    # other constraints are left at KiCad 10 defaults (same values as the course slide)
    # --- predefined sizes (Board Setup > Design Rules > Pre-defined Sizes) ---
    tw = ds.m_TrackWidthList
    tw.clear()
    tw.append(0)  # index 0 = "use netclass"
    for w in L.PREDEF_TRACKS:
        tw.append(MM(w))
    vl = ds.m_ViasDimensionsList
    vl.clear()
    vl.append(pcbnew.VIA_DIMENSION(0, 0))
    for d, h in L.PREDEF_VIAS:
        vl.append(pcbnew.VIA_DIMENSION(MM(d), MM(h)))
    # --- net classes (Board Setup > Design Rules > Net Classes) ---
    ns = ds.m_NetSettings
    dflt = ns.GetDefaultNetclass()
    c = L.NETCLASSES["Default"]
    dflt.SetClearance(MM(c["clearance"]))
    dflt.SetTrackWidth(MM(c["track"]))
    dflt.SetViaDiameter(MM(c["via"]))
    dflt.SetViaDrill(MM(c["drill"]))
    ns.ClearNetclasses()
    prio = 0
    for name, c in L.NETCLASSES.items():
        if name == "Default":
            continue
        nc = pcbnew.NETCLASS(name)
        nc.SetPriority(prio)
        prio += 1
        nc.SetClearance(MM(c["clearance"]))
        nc.SetTrackWidth(MM(c["track"]))
        nc.SetViaDiameter(MM(c["via"]))
        nc.SetViaDrill(MM(c["drill"]))
        nc.SetDescription(c.get("descr", ""))
        ns.SetNetclass(name, nc)
    ns.ClearNetclassPatternAssignments()
    for pattern, cls in L.NETCLASS_PATTERNS:
        ns.SetNetclassPatternAssignment(pattern, cls)
    ns.ClearAllCaches()


def add_footprints(board, comps, nets):
    netinfo = {}
    for n in nets:
        ni = pcbnew.NETINFO_ITEM(board, n["name"])
        board.Add(ni)
        netinfo[n["name"]] = ni
    pin_net = {}
    for n in nets:
        for nd in n["nodes"]:
            pin_net[(nd["ref"], nd["pin"])] = (n["name"], nd["pinfunction"], nd["pintype"])
    fps = {}
    for c in comps:
        lib, name = c["footprint"].split(":", 1)
        fp = pcbnew.FootprintLoad(f"{FPDIR}/{lib}.pretty", name)
        assert fp is not None, c["footprint"]
        fp.SetFPID(pcbnew.LIB_ID(lib, name))
        fp.SetReference(c["ref"])
        fp.SetValue(c["value"])
        fp.SetPath(pcbnew.KIID_PATH(c["sheet_tstamps"] + c["tstamp"]))
        fp.SetSheetname(c["sheet_names"])
        fp.SetSheetfile(c["props"].get("Sheetfile", ""))
        fp.SetFilters(c["props"].get("ki_fp_filters", ""))
        # symbol fields -> footprint fields (hidden, on F.Fab), exactly like the netlist updater
        sym_fields = [(k, v) for (k, v) in c["fields"] if k not in ("Reference", "Value", "Footprint")]
        names = set(k for k, _ in sym_fields)
        for f in list(fp.GetFields()):
            if not f.IsMandatory() and f.GetName() not in names:
                fp.Remove(f)
        for k, v in sym_fields:
            existed = fp.HasField(k)
            fp.SetField(k, v)
            f = fp.GetField(k)
            if not existed:
                f.SetVisible(False)
                f.SetLayer(pcbnew.F_Fab)
                f.SetFPRelativePosition(pcbnew.VECTOR2I(0, 0))
        board.Add(fp)
        for pad in fp.Pads():
            key = (c["ref"], pad.GetNumber())
            if key in pin_net:
                nname, pfun, ptype = pin_net[key]
                pad.SetNet(netinfo[nname])
                pad.SetPinFunction(pfun)
                pad.SetPinType(ptype)
        fps[c["ref"]] = fp
    return fps, netinfo


def place(fps):
    for ref, (u, v, rot) in L.PLACEMENT.items():
        fp = fps[ref]
        fp.SetPosition(P(u, v))
        fp.SetOrientationDegrees(rot)
    for ref, fp in fps.items():
        assert ref in L.PLACEMENT, "unplaced " + ref


def set_texts(fps):
    """Reference designator placement on F.Silkscreen (relative to footprint, board coordinates)."""
    for ref, spec in L.REF_TEXT.items():
        fp = fps[ref]
        f = fp.Reference()
        if spec is None:
            f.SetVisible(False)
            continue
        du, dv, ang = spec
        pos = fp.GetPosition()
        f.SetTextPos(pcbnew.VECTOR2I(pos.x + MM(du), pos.y + MM(dv)))
        f.SetTextAngleDegrees(ang)
        f.SetTextSize(pcbnew.VECTOR2I(MM(L.REF_SIZE), MM(L.REF_SIZE)))
        f.SetTextThickness(MM(L.REF_THICK))


def add_edge(board):
    s = pcbnew.PCB_SHAPE(board, pcbnew.SHAPE_T_RECTANGLE)
    s.SetStart(P(0, 0))
    s.SetEnd(P(L.W, L.H))
    s.SetLayer(pcbnew.Edge_Cuts)
    s.SetWidth(MM(0.05))
    if L.CORNER_R:
        s.SetCornerRadius(MM(L.CORNER_R))
    board.Add(s)


def add_text(board, text, u, v, size, thick, layer=pcbnew.F_SilkS, angle=0, justify=None, mirror=False):
    t = pcbnew.PCB_TEXT(board)
    t.SetText(text)
    t.SetPosition(P(u, v))
    t.SetLayer(layer)
    t.SetTextSize(pcbnew.VECTOR2I(MM(size), MM(size)))
    t.SetTextThickness(MM(thick))
    t.SetTextAngleDegrees(angle)
    if justify == "left":
        t.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_LEFT)
    elif justify == "right":
        t.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_RIGHT)
    if mirror:
        t.SetMirrored(True)
    board.Add(t)
    return t


def pad_pos(fps, ref, num, which=0):
    pads = [p for p in fps[ref].Pads() if p.GetNumber() == str(num)]
    p = pads[which].GetPosition()
    return (ToMM(p.x) - L.OX, ToMM(p.y) - L.OY)


def add_tracks(board, fps, netinfo):
    resolve = lambda pt: pad_pos(fps, pt[1], pt[2], pt[3] if len(pt) > 3 else 0) if isinstance(pt, tuple) and pt and pt[0] == "pad" else pt
    nvia = 0
    for item in L.ROUTES:
        kind = item[0]
        if kind == "track":
            _, net, layer, width, pts = item
            pts = [resolve(p) for p in pts]
            for a, b in zip(pts[:-1], pts[1:]):
                t = pcbnew.PCB_TRACK(board)
                t.SetStart(P(*a))
                t.SetEnd(P(*b))
                t.SetWidth(MM(width))
                t.SetLayer(pcbnew.F_Cu if layer == "F" else pcbnew.B_Cu)
                t.SetNet(netinfo[net])
                board.Add(t)
        elif kind == "via":
            _, net, pos, dia, drill = item
            pos = resolve(pos)
            v = pcbnew.PCB_VIA(board)
            v.SetPosition(P(*pos))
            v.SetViaType(pcbnew.VIATYPE_THROUGH)
            v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
            v.SetWidth(MM(dia))
            v.SetDrill(MM(drill))
            v.SetNet(netinfo[net])
            board.Add(v)
            nvia += 1
    return nvia


def add_zones(board, netinfo):
    for z in L.ZONES:
        zone = pcbnew.ZONE(board)
        zone.SetLayer(pcbnew.F_Cu if z["layer"] == "F" else pcbnew.B_Cu)
        zone.SetNet(netinfo[z["net"]])
        zone.SetZoneName(z["name"])
        zone.SetAssignedPriority(z.get("priority", 0))
        zone.SetLocalClearance(MM(z["clearance"]))
        zone.SetMinThickness(MM(z["min_thickness"]))
        zone.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
        zone.SetThermalReliefGap(MM(z["thermal_gap"]))
        zone.SetThermalReliefSpokeWidth(MM(z["spoke"]))
        zone.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
        ol = zone.Outline()
        ol.NewOutline()
        for (u, v) in z["outline"]:
            ol.Append(MM(L.OX + u), MM(L.OY + v))
        board.Add(zone)
    board.BuildConnectivity()          # island removal needs up-to-date connectivity
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())


STACKUP = """(stackup
			(layer "F.SilkS"
				(type "Top Silk Screen")
			)
			(layer "F.Paste"
				(type "Top Solder Paste")
			)
			(layer "F.Mask"
				(type "Top Solder Mask")
				(thickness 0.01)
			)
			(layer "F.Cu"
				(type "copper")
				(thickness 0.035)
			)
			(layer "dielectric 1"
				(type "core")
				(thickness 1.51)
				(material "FR4")
				(epsilon_r 4.5)
				(loss_tangent 0.02)
			)
			(layer "B.Cu"
				(type "copper")
				(thickness 0.035)
			)
			(layer "B.Mask"
				(type "Bottom Solder Mask")
				(thickness 0.01)
			)
			(layer "B.Paste"
				(type "Bottom Solder Paste")
			)
			(layer "B.SilkS"
				(type "Bottom Silk Screen")
			)
			(copper_finish "None")
			(dielectric_constraints no)
		)"""


def add_stackup(pcb_path):
    """2-layer FR4 stackup, 35 um (1 oz/ft2) copper. Written in KiCad's own format, then the board is
    re-loaded and re-saved by pcbnew so the final text is KiCad's canonical serialisation."""
    CRLF, LF, TAB = chr(13) + chr(10), chr(10), chr(9)
    raw = open(pcb_path, encoding="utf-8", newline="").read()
    eol = CRLF if CRLF in raw else LF
    t = raw.replace(CRLF, LF)
    assert "(stackup" not in t
    anchor = TAB + "(setup" + LF
    i = t.index(anchor) + len(anchor)
    t = t[:i] + TAB + TAB + STACKUP + LF + t[i:]
    with open(pcb_path, "w", encoding="utf-8", newline=eol) as fh:
        fh.write(t)
    b = pcbnew.LoadBoard(pcb_path)
    assert b.GetDesignSettings().m_HasStackup, "stackup not parsed"
    pcbnew.SaveBoard(pcb_path, b)
    t2 = open(pcb_path, encoding="utf-8").read()
    assert '(material "FR4")' in t2 and "(thickness 0.035)" in t2, "stackup lost on re-save"


def main():
    proj = sys.argv[1]
    netl = sys.argv[2]
    no_route = "--no-route" in sys.argv
    no_zones = "--no-zones" in sys.argv
    pcb_path = os.path.join(proj, "Sesion2_Izan.kicad_pcb")
    board = pcbnew.LoadBoard(pcb_path)
    clear_board(board)
    board.SetCopperLayerCount(2)
    setup_rules(board)
    comps, nets = read_netlist(netl)
    fps, netinfo = add_footprints(board, comps, nets)
    place(fps)
    add_edge(board)
    text_rects = []
    for spec in L.TEXTS:
        t = add_text(board, *spec)
        text_rects.append(silk.text_rect(t))
    nvia = 0
    if not no_route:
        nvia = add_tracks(board, fps, netinfo)
    overrides = {r: (None if v is None else (L.OX + v[0], L.OY + v[1], v[2])) for r, v in L.REF_TEXT.items()}
    rep = silk.autoplace(board, fps, L.REF_SIZE, L.REF_THICK, (L.OX, L.OY, L.OX + L.W, L.OY + L.H),
                         overrides, L.REF_ORDER, text_rects)
    for r in L.REF_ORDER:
        print("   ref", r, rep.get(r))
    if not no_zones and not no_route:
        add_zones(board, netinfo)
    tb = board.GetTitleBlock()
    tb.SetTitle(L.TITLE)
    tb.SetRevision(L.REV)
    tb.SetDate(L.DATE)
    tb.SetCompany(L.COMPANY)
    board.BuildConnectivity()
    pcbnew.SaveBoard(pcb_path, board)
    add_stackup(pcb_path)
    print("saved", pcb_path, "footprints", len(fps), "vias", nvia,
          "tracks", len([t for t in board.GetTracks() if t.Type() == pcbnew.PCB_TRACE_T]))


if __name__ == "__main__":
    main()
