"""Read a KiCad s-expression netlist (kicad-cli sch export netlist) into plain dicts."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sexpr import load, find, find1, val


def read_netlist(path):
    net = load(path)
    comps = []
    for c in find(find1(net, "components"), "comp"):
        fields = []  # ordered (name, value) as in the symbol
        fs = find1(c, "fields")
        if fs:
            for f in find(fs, "field"):
                name = val(f, "name")
                value = f[2] if len(f) > 2 and not isinstance(f[2], list) else ""
                fields.append((name, str(value)))
        props = {val(p, "name"): (val(p, "value") or "") for p in find(c, "property")}
        sp = find1(c, "sheetpath")
        comps.append(dict(
            ref=str(val(c, "ref")), value=str(val(c, "value")), footprint=str(val(c, "footprint")),
            fields=fields, props=props,
            sheet_names=str(val(sp, "names")), sheet_tstamps=str(val(sp, "tstamps")),
            tstamp=str(val(c, "tstamps")),
        ))
    nets = []
    for n in find(find1(net, "nets"), "net"):
        nodes = [dict(ref=str(val(nd, "ref")), pin=str(val(nd, "pin")),
                      pinfunction=str(val(nd, "pinfunction") or ""), pintype=str(val(nd, "pintype") or ""))
                 for nd in find(n, "node")]
        nets.append(dict(code=int(val(n, "code")), name=str(val(n, "name")), nodes=nodes))
    return comps, nets
