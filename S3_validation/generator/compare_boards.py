"""Compare two boards geometrically (footprints, fields, tracks, vias, zones, drawings)."""
import sys, pcbnew
def sig(path):
    b = pcbnew.LoadBoard(path)
    fps = sorted((f.GetReference(), f.GetValue(), f.GetFPIDAsString(), f.GetPosition().x, f.GetPosition().y,
                  round(f.GetOrientationDegrees(), 3), f.GetLayer(), f.GetPath().AsString(),
                  tuple(sorted((p.GetNumber(), p.GetNetname(), p.GetPosition().x, p.GetPosition().y) for p in f.Pads())),
                  tuple(sorted((fl.GetName(), fl.GetText(), fl.IsVisible()) for fl in f.GetFields())),
                  (f.Reference().GetPosition().x, f.Reference().GetPosition().y, round(f.Reference().GetTextAngleDegrees(), 3), f.Reference().GetLayer()))
                 for f in b.GetFootprints())
    trk = sorted((t.GetClass(), t.GetLayer(), t.GetNetname(), t.GetStart().x, t.GetStart().y, t.GetEnd().x, t.GetEnd().y, t.GetWidth(pcbnew.F_Cu) if t.GetClass() == 'PCB_VIA' else t.GetWidth(), t.GetDrillValue() if t.GetClass() == 'PCB_VIA' else 0)
                 for t in b.GetTracks())
    zones = sorted((z.GetZoneName(), z.GetLayer(), z.GetNetname(), round(z.GetFilledArea() / 1e12, 3)) for z in b.Zones())
    drw = sorted((d.GetClass(), d.GetLayer(), getattr(d, "GetText", lambda: "")(), d.GetPosition().x, d.GetPosition().y) for d in b.GetDrawings())
    ds = b.GetDesignSettings()
    rules = (ds.m_MinClearance, ds.m_TrackMinWidth, ds.m_HasStackup, ds.GetBoardThickness())
    return dict(footprints=fps, tracks=trk, zones=zones, drawings=drw, rules=rules)
a, c = sig(sys.argv[1]), sig(sys.argv[2])
same = True
for k in a:
    eq = a[k] == c[k]
    same &= eq
    print("%-10s %s (%d items)" % (k, "IDENTICAL" if eq else "DIFFERENT", len(a[k]) if isinstance(a[k], list) else 1))
    if not eq and isinstance(a[k], list):
        sa, sc = set(a[k]), set(c[k])
        for x in list(sa - sc)[:5]: print("   only A:", x)
        for x in list(sc - sa)[:5]: print("   only B:", x)
print("GEOMETRY", "IDENTICAL" if same else "DIFFERENT")
