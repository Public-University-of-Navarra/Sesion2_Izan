"""Rasterize the board area of a kicad-cli PDF export (crop to Edge.Cuts bbox + margin).
usage: python rasterize.py in.pdf out.png [px_per_mm]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layout as L
import pymupdf

src, dst = sys.argv[1], sys.argv[2]
px_per_mm = float(sys.argv[3]) if len(sys.argv) > 3 else 25.0
d = pymupdf.open(src)
p = d[0]
pt = 72 / 25.4                       # PDF points per mm
m = 1.5                              # margin around the board (mm)
clip = pymupdf.Rect((L.OX - m) * pt, (L.OY - m) * pt, (L.OX + L.W + m) * pt, (L.OY + L.H + m) * pt)
s = px_per_mm / pt
pix = p.get_pixmap(matrix=pymupdf.Matrix(s, s), clip=clip)
pix.save(dst)
print("png", dst, pix.width, pix.height)
