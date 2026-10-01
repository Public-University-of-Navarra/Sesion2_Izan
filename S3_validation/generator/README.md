# Generador del PCB de S3 (trazabilidad)

El PCB de la Sesión 3 se hizo en una sesión **sin interfaz gráfica de KiCad**. Por eso se construyó con la **API Python oficial de KiCad 10 (`pcbnew`)** y se validó con **`kicad-cli`**, que usa el mismo parser y el mismo DRC que la GUI. Estos scripts documentan exactamente cómo se obtuvo `Sesion2_Izan/Sesion2_Izan.kicad_pcb`.

**No es un autorouter.** Cada huella tiene una posición y un giro decididos a mano, y cada pista y cada vía están escritas una a una, con su justificación, en `layout.py`. El script solo las vuelca a KiCad.

| Fichero | Qué hace |
|---|---|
| `layout.py` | **El diseño.** Tamaño de placa, reglas, net classes, placement, cada pista y vía (coordenadas en mm respecto a la esquina superior izquierda de Edge.Cuts; en KiCad son +100/+100), zonas GND y serigrafía |
| `build_pcb.py` | Lee el netlist de `kicad-cli sch export netlist` y replica "Update PCB from Schematic": huella de librería, ruta jerárquica, campos, sheetname/sheetfile, red y función de cada pad. Después aplica reglas y net classes, coloca, enruta, rellena zonas, añade el stackup 2 capas FR4 1 oz y guarda con `pcbnew.SaveBoard` |
| `netlist.py`, `sexpr.py` | Lectura del netlist (S‑expressions) |
| `silk.py` | Colocación automática de las referencias que no tienen posición fija en `layout.py` |
| `audit.py` | Auditoría geométrica independiente del DRC. Comprueba clases y anchos por red, vías, distancias mínimas (pista‑pista, pista‑pad, pista‑vía), ángulos, zonas, reglas y distancia de la serigrafía a las aperturas de máscara |
| `compare_boards.py` | Compara dos placas: huellas (posición, giro, pads, redes, campos, ruta jerárquica), pistas, vías, zonas, dibujos y reglas |
| `drc_summary.py`, `rasterize.py` | Resumen del JSON de DRC; PNG de una exportación PDF (este último necesita `pymupdf`) |
| `regenerate.sh` | Reconstruye la placa desde el esquema **en una carpeta temporal fuera del repo**, pasa DRC y auditoría, y la compara con la placa versionada |

Reproducir (Git Bash, KiCad 10.0.x instalado en la ruta por defecto):

```sh
sh S3_validation/generator/regenerate.sh            # salida en $TMPDIR/s3_regen_out
```

Al final debe salir `DRC: violations=0 unconnected=0 parity=0` y `GEOMETRY IDENTICAL`. Esto se comprobó el 2026‑10‑01: la placa regenerada coincide con la versionada en huellas, pads, redes, campos, pistas, vías, zonas rellenas, dibujos y reglas. Los UUID internos cambian en cada ejecución, así que el fichero no es idéntico byte a byte. **La fuente de verdad es el `.kicad_pcb` versionado**, y a partir de ahora se puede editar con normalidad en la GUI de KiCad. Si se edita en la GUI, `layout.py` deja de describir la placa: queda como registro de cómo se hizo la revisión commiteada.

El script exporta `PYTHONDONTWRITEBYTECODE=1` para no dejar `__pycache__` en el repo (también está en `S3_validation/.gitignore`).
