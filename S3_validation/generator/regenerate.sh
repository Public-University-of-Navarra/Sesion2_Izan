#!/bin/sh
# Rebuild the S3 board from the schematic into a scratch copy and run the checks.
# It never writes into the repository: the result is left in $OUT (default: $TMPDIR/s3_regen_out, outside the repo).
#
#   usage:  sh S3_validation/generator/regenerate.sh [OUT_DIR]
#
# Requires KiCad 10.0.x (kicad-cli + bundled python with pcbnew). Optional: system python with
# pymupdf for the PNG previews.
set -e
export PYTHONDONTWRITEBYTECODE=1   # no __pycache__ next to the scripts in the repo
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
PROJ="$REPO/Sesion2_Izan"
OUT="${1:-${TMPDIR:-/tmp}/s3_regen_out}"
KICAD_BIN="${KICAD_BIN:-/c/Program Files/KiCad/10.0/bin}"
K="$KICAD_BIN/kicad-cli.exe"
KP="$KICAD_BIN/python.exe"

mkdir -p "${OUT:?}"
cp "$PROJ"/*.kicad_sch "$PROJ"/Sesion2_Izan.kicad_pro "$PROJ"/Sesion2_Izan.kicad_dru "$OUT/"
printf '(kicad_pcb (version 20260206) (generator "pcbnew") (generator_version "10.0")\n)\n' > "$OUT/Sesion2_Izan.kicad_pcb"
"$K" sch export netlist -o "$OUT/S3.net" "$OUT/Sesion2_Izan.kicad_sch"
"$KP" "$HERE/build_pcb.py" "$OUT" "$OUT/S3.net"
# KiCad refills the copper zones itself and saves; then the full DRC with schematic parity
"$K" pcb drc --refill-zones --save-board --schematic-parity --severity-all --exit-code-violations \
    --format json -o "$OUT/drc.json" "$OUT/Sesion2_Izan.kicad_pcb" || true
"$KP" "$HERE/drc_summary.py" "$OUT/drc.json"
"$KP" "$HERE/audit.py" "$OUT/Sesion2_Izan.kicad_pcb"
# geometric comparison with the versioned board (a copy of it, so pcbnew never opens the repo file)
mkdir -p "$OUT/versioned"
cp "$PROJ/Sesion2_Izan.kicad_pcb" "$PROJ/Sesion2_Izan.kicad_pro" "$PROJ/Sesion2_Izan.kicad_dru" "$OUT/versioned/"
"$KP" "$HERE/compare_boards.py" "$OUT/versioned/Sesion2_Izan.kicad_pcb" "$OUT/Sesion2_Izan.kicad_pcb"
