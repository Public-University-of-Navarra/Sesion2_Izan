import json, sys, collections
d = json.load(open(sys.argv[1], encoding="utf-8"))
viol = d.get("violations", [])
unc = d.get("unconnected_items", [])
par = d.get("schematic_parity", [])
print("DRC: violations=%d unconnected=%d parity=%d" % (len(viol), len(unc), len(par)))
cnt = collections.Counter((v["severity"], v["type"]) for v in viol)
for (sev, typ), n in sorted(cnt.items()):
    print("   %-8s %-32s x%d" % (sev, typ, n))
full = "--all" in sys.argv
for v in (viol if full else viol[:40]):
    items = "; ".join(i.get("description", "")[:70] for i in v.get("items", []))
    print("  [%s] %s :: %s" % (v["type"], v["description"][:60], items))
for v in unc[:30]:
    items = "; ".join(i.get("description", "")[:70] for i in v.get("items", []))
    print("  [unconnected] %s" % items)
for v in par[:30]:
    items = "; ".join(i.get("description", "")[:70] for i in v.get("items", []))
    print("  [parity:%s] %s :: %s" % (v["type"], v["description"][:80], items))
