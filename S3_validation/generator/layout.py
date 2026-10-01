"""Layout description for the S3 board (board-local mm, origin = top-left corner of Edge.Cuts,
x to the right, y down). Rotation in degrees, KiCad convention (CCW positive)."""

OX, OY = 100.0, 100.0            # Edge.Cuts top-left corner in KiCad page coordinates
W, H = 39.0, 26.7                # board size (mm)
CORNER_R = 0.0

# ---------------- rules ----------------
MIN_CLEARANCE = 0.20             # REQUISITO DOCENTE
MIN_TRACK_WIDTH = 0.25           # REQUISITO DOCENTE
TRACK_TO_TRACK = 0.25            # REQUISITO DOCENTE (custom rule in .kicad_dru)
PREDEF_TRACKS = [0.25, 0.6, 1.3]
PREDEF_VIAS = [(0.6, 0.3), (0.8, 0.4)]
NETCLASSES = {     # W_GND > 2*W_POWER > 2*W_SIGNAL (course slide): 1.3 > 1.2 ; 0.6 > 0.5
    "Default": dict(clearance=0.2, track=0.25, via=0.6, drill=0.3),
    "GND": dict(clearance=0.2, track=1.3, via=0.8, drill=0.4, descr="Ground"),
    "POWER": dict(clearance=0.2, track=0.6, via=0.8, drill=0.4, descr="VIN and 3V3 supply"),
    "SIGNAL": dict(clearance=0.2, track=0.25, via=0.6, drill=0.3, descr="Analog/digital signals"),
}
NETCLASS_PATTERNS = [
    ("GND", "GND"),
    ("*VIN", "POWER"),
    ("*3V3", "POWER"),
    ("*AIN*", "SIGNAL"),
    ("*NRST", "SIGNAL"),
    ("*OUT1", "SIGNAL"),
    ("*SWCLK", "SIGNAL"),
    ("*SWDIO", "SIGNAL"),
]

# ---------------- placement ----------------
MX, MY = 28.6, 11.5              # U301 centre
YROW = 18.7 + 0.9                      # RC filter cell row (centre); JY = YROW + 3.75
JY = YROW + 3.75                       # J301 pin row
JY_X0 = 18.49                    # J301 pin 1 x
PLACEMENT = {
    # ---- power zone (top-left) ----
    "J101": (6.05, 3.5, 270),    # pin1 VIN top, pin2 GND below, wire entry towards the left edge
    "C201": (11.8, 4.538, 270),  # LDO input cap: pad1 VIN on the VIN line, pad2 GND below
    "C202": (11.8, 8.9, 90),     # LDO output cap (tantalum): pad1(+) bottom
    "U201": (16.6, 6.65, 270),   # pins up (VIN, VOUT, GND), tab (VOUT) down
    # ---- test points (lower-left, grouped VIN / GND / 3V3) ----
    "TP201": (3.2, 15.65, 0),
    "TP203": (7.4, 15.65, 0),
    "TP202": (11.8, 15.65, 0),
    # ---- MCU zone ----
    "U301": (MX, MY, 0),
    "C302": (MX - 6.9, MY - 0.95, 270),   # 100nF: pad1 3V3 -> pin4, pad2 GND -> pin5
    "C303": (MX - 6.9, MY - 4.9, 90),     # 4.7uF bulk: pad1 3V3 bottom, pad2 GND top
    "C301": (18.7, 12.2, 180),            # NRST cap: pad1 NRST right
    "J302": (MX + 8.2, 5.36, 0),          # SWD, pins 1..5 top->bottom
    # ---- analog zone (bottom): cells [C401|R401] [R501|C501] [C601|R601] ----
    "C401": (14.66, YROW, 270), "R401": (16.81, YROW, 90),
    "R501": (21.03, YROW, 90), "C501": (23.18, YROW, 270),
    "C601": (25.25, YROW, 270), "R601": (27.4, YROW, 90),
    "J301": (18.49, JY, 90),              # pins 1..6 left->right
}

REF_SIZE, REF_THICK = 0.8, 0.15
REF_TEXT = {        # ref -> (u, v, angle) board-local, or None to hide; others are auto-placed
    "J101": (5.5, 12.1, 0), "C202": (11.8, 12.1, 0),
    "TP201": (3.2, 19.1, 0), "TP203": (7.4, 19.1, 0), "TP202": (11.8, 19.1, 0),
    # filter row: horizontal legends, staggered on two levels, centred over each part
    "C401": (14.66, YROW + 2.4, 0), "R401": (16.81, YROW - 2.3, 0), "R501": (21.03, YROW - 2.3, 0),
    "C501": (23.18, YROW - 3.5, 0), "C601": (25.5, YROW - 2.3, 0),
    "C301": (18.7, 13.75, 0), "C302": (22.0, 13.0, 0), "C303": (23.3, 4.25, 0),
    "U301": (MX, 4.45, 0), "J301": (14.9, JY + 0.95, 0),
}
REF_ORDER = ["U301", "U201", "J101", "J302", "J301", "TP201", "TP203", "TP202",
             "C202", "C201", "C302", "C303", "C301", "R601", "C601", "C501", "R501", "R401", "C401"]
TITLE, REV, DATE, COMPANY = "Sesion2_Izan - DEE Sesion 3 (PCB)", "A", "2026-10-01", "UPNA - Desarrollo de Equipos Electronicos"
T8, T6 = (0.8, 0.12), (0.8, 0.12)
TEXTS = [
    # board identification (lower-left free area)
    ("DEE Sesion 3", 0.9, 20.6, 1.0, 0.15, 5, 0, "left"),
    ("Izan  -  Rev A", 0.9, 22.1, 0.8, 0.15, 5, 0, "left"),
    ("2026-10  UPNA", 0.9, 23.4, 0.8, 0.15, 5, 0, "left"),
    # test point labels
    ("VIN", 3.2, 17.9, 0.8, 0.15, 5), ("GND", 7.4, 17.9, 0.8, 0.15, 5), ("3V3", 11.8, 17.9, 0.8, 0.15, 5),
    # J101 pinout (pin 1 = square pad + footprint triangle)
    ("1:VIN 2:GND", 5.5, 13.25, 0.8, 0.15, 5),
    # J301 (E/S) pin names under the header
    ("3V3", JY_X0 + 0.0, JY + 2.35, 0.8, 0.15, 5), ("A1", JY_X0 + 2.54, JY + 2.35, 0.8, 0.15, 5),
    ("A2", JY_X0 + 5.08, JY + 2.35, 0.8, 0.15, 5), ("A3", JY_X0 + 7.62, JY + 2.35, 0.8, 0.15, 5),
    ("OUT", JY_X0 + 10.16 - 0.25, JY + 2.35, 0.8, 0.15, 5), ("GND", JY_X0 + 12.7 + 0.35, JY + 2.35, 0.8, 0.15, 5),
    # J302 (SWD) pin names, vertical, between U301 and the header
    ("3V3", 34.45, 5.36, 0.8, 0.15, 5, 90), ("CLK", 34.45, 7.9, 0.8, 0.15, 5, 90),
    ("GND", 34.45, 10.44, 0.8, 0.15, 5, 90), ("DIO", 34.45, 12.98, 0.8, 0.15, 5, 90),
    ("RST", 34.45, 15.52, 0.8, 0.15, 5, 90),
]

# ---------------- routing ----------------
# ("track", net, layer, width, [points])   points: (u, v) or ("pad", REF, number[, index])
# ("via", net, (u, v), diameter, drill)
VIN, V33, GND = "/Alimentacion/VIN", "/Microcontrolador/3V3", "GND"
NET = lambda n: "/Microcontrolador/" + n
PW, SW, GW = 0.6, 0.25, 0.5      # POWER / SIGNAL widths; GW = local GND neck width at fine-pitch pads
ROUTES = [
    # ---- VIN: J101.1 -> C201.1 -> U201.3 (straight), branch to TP201 ----
    ("track", VIN, "F", PW, [("pad", "J101", 1), ("pad", "C201", 1), ("pad", "U201", 3)]),
    ("track", VIN, "F", PW, [("pad", "J101", 1), (3.7, 3.5), (3.2, 4.0), ("pad", "TP201", 1)]),
    # ---- 3V3 ----
    ("track", V33, "F", PW, [("pad", "U201", 2, 0), ("pad", "U201", 2, 1)]),            # top pin 2 <-> tab
    ("track", V33, "F", PW, [("pad", "U201", 2, 1), (18.6, 9.8), (20.7625, 7.6375), ("pad", "C303", 1)]),  # tab -> C303 (enters from the left)
    ("track", V33, "F", PW, [("pad", "C303", 1), ("pad", "C302", 1)]),                     # C303 -> C302
    ("track", V33, "F", PW, [("pad", "C302", 1), (23.287, 11.1), ("pad", "U301", 4)]),    # C302 -> VDD
    ("track", V33, "F", PW, [("pad", "U201", 2, 1), (12.252, 9.8), ("pad", "C202", 1)]),  # tab -> C202
    ("track", V33, "F", PW, [("pad", "C202", 1), ("pad", "TP202", 1)]),
    ("track", V33, "F", PW, [("pad", "TP202", 1), (11.8, JY - 0.5), (12.3, JY), ("pad", "J301", 1)]),
    ("track", V33, "F", PW, [("pad", "C303", 1), (22.9, 7.6375), (25.1775, 5.36), ("pad", "J302", 1)]),
    # ---- analog filters ----
    ("track", NET("AIN1"), "F", SW, [(14.66, YROW - 1.0), ("pad", "R401", 2)]),
    ("track", NET("AIN1"), "F", SW, [("pad", "R401", 2), (16.81, 14.0), (17.31, 13.5), ("pad", "U301", 7)]),
    ("track", NET("AIN2"), "F", SW, [("pad", "R501", 2), (23.18, YROW - 1.0)]),
    ("track", NET("AIN2"), "F", SW, [(23.18, YROW - 1.0), (23.18, 14.8), (23.68, 14.3), ("pad", "U301", 8)]),
    ("track", NET("AIN3"), "F", SW, [(25.25, YROW - 1.0), ("pad", "R601", 2)]),
    ("track", NET("AIN3"), "F", SW, [("pad", "R601", 2), ("pad", "U301", 11)]),
    ("track", NET("AIN1_EXT"), "F", SW, [("pad", "J301", 2), (21.03, JY - 0.82), (20.63, JY - 1.22), (17.21, JY - 1.22), (16.81, JY - 1.62), ("pad", "R401", 1)]),
    ("track", NET("AIN2_EXT"), "F", SW, [("pad", "J301", 3), (23.57, JY - 1.35), (23.17, JY - 1.75), (21.43, JY - 1.75), (21.03, JY - 2.15), ("pad", "R501", 1)]),
    ("track", NET("AIN3_EXT"), "F", SW, [("pad", "J301", 4), (27.4, JY - 1.29), ("pad", "R601", 1)]),
    ("track", NET("OUT1"), "F", SW, [("pad", "U301", 12), (28.2, 16.6), (28.95, 17.35), (28.95, JY - 0.3), ("pad", "J301", 5)]),
    # ---- SWD ----
    ("track", NET("SWCLK"), "F", SW, [("pad", "U301", 25), (31.4, 6.7), (31.9, 6.2), (34.9, 6.2), (36.6, 7.9), ("pad", "J302", 2)]),
    ("track", NET("SWDIO"), "F", SW, [("pad", "U301", 24), (34.1, 8.7), (34.6, 9.2), (34.6, 10.78), ("pad", "J302", 4)]),
    # ---- NRST: C301 on F.Cu, then one via under U301 and B.Cu to the THT pad J302.5 ----
    ("track", NET("NRST"), "F", SW, [("pad", "U301", 6), (20.237, 12.7), ("pad", "C301", 1)]),
    ("track", NET("NRST"), "F", SW, [("pad", "U301", 6), (26.0, 12.7), (26.6, 13.3)]),
    ("via", NET("NRST"), (26.6, 13.3), 0.6, 0.3),
    ("track", NET("NRST"), "B", SW, [(26.6, 13.3), (34.58, 13.3), ("pad", "J302", 5)]),
    # ---- GND local connections (the rest is done by the copper pours) ----
    ("track", GND, "F", GW, [(21.7, 11.95), (24.425, 11.95)]),                 # C302.2 -> VSS
    ("track", GND, "F", 0.4, [("pad", "U301", 5), (26.0, 11.9)]),               # VSS -> via (under U301)
    ("via", GND, (26.0, 11.9), 0.8, 0.4),
    ("track", GND, "F", 1.3, [("pad", "U201", 1), (20.75, 3.5)]),                 # LDO GND -> via
    ("track", GND, "F", 1.3, [("pad", "C303", 2), (20.75, 4.6125), (20.75, 3.5)]),  # C303 GND -> via
    ("via", GND, (20.75, 3.5), 0.8, 0.4),
    ("track", GND, "F", 1.3, [("pad", "C301", 2), (16.0, 12.2)]),                  # NRST cap GND -> via
    ("via", GND, (16.0, 12.2), 0.8, 0.4),
    ("track", GND, "F", 1.0, [("pad", "C501", 2), ("pad", "C601", 2)]),           # filter caps GND bridge
    ("track", GND, "F", 1.0, [("pad", "C601", 2), (25.25, JY - 1.5)]),
    ("via", GND, (25.25, JY - 1.5), 0.8, 0.4),
    # LDO input/output caps: GND pads tied together and to an adjacent via (slide 11) -> short return to U201.1
    ("track", GND, "F", 1.3, [("pad", "C201", 2), ("pad", "C202", 2)]),
    ("track", GND, "F", 1.3, [(11.8, 6.56), (13.75, 6.56)]),
    ("via", GND, (13.75, 6.56), 0.8, 0.4),
]

ZONE_DEF = dict(net=GND, clearance=0.3, min_thickness=0.25, thermal_gap=0.3, spoke=0.4,
                outline=[(0, 0), (W, 0), (W, H), (0, H)])
ZONES = [
    dict(ZONE_DEF, name="GND_F", layer="F", priority=0),
    dict(ZONE_DEF, name="GND_B", layer="B", priority=0),
]
