# S3_validation — artefactos de validación de la Sesión 3

Generados el 2026‑10‑01 con KiCad 10.0.6 (`kicad-cli`) sobre los ficheros versionados en `Sesion2_Izan/`. El informe completo está en [`../S3_AUTONOMOUS_REPORT.md`](../S3_AUTONOMOUS_REPORT.md).

| Fichero | Contenido | Cómo se generó |
|---|---|---|
| `ERC_report.rpt` / `.json` | ERC del esquema completo: 0 errores, 0 avisos | `kicad-cli sch erc --severity-all --exit-code-violations` |
| `DRC_report.rpt` / `.json` | DRC del PCB: 0 violaciones, 0 conexiones pendientes, 0 problemas de paridad | `kicad-cli pcb drc --refill-zones --schematic-parity --severity-all --exit-code-violations` |
| `board_stats.txt` | Tamaño, áreas de cobre, pads, vías, taladros, componentes | `kicad-cli pcb export stats` |
| `audit_geometry.txt` | Auditoría propia, independiente del DRC: clase y anchos por red, vías, distancias mínimas (pista‑pista, pista‑pad, pista‑vía), ángulos en todas las uniones (también de 3 brazos y en T), zonas, reglas, serigrafía frente a aperturas de máscara, a otras leyendas y a la serigrafía de las huellas, y taladros bajo serigrafía | `generator/audit.py` (API Python de KiCad) |
| `renders/render_3d_top.jpg`, `render_3d_bottom.jpg`, `render_3d_iso.jpg` | Vistas 3D superior, inferior e isométrica | `kicad-cli pcb render --quality high` |
| `renders/layer_Fcu_silk.png` | F.Cu + serigrafía + contorno | `kicad-cli pcb export pdf` → PNG |
| `renders/layer_Bcu.png` | B.Cu (plano GND y tramo NRST), vista desde arriba | ídem |
| `renders/layer_fab_courtyard.png` | F.Fab + courtyards (pads en contorno) | ídem |
| `renders/layer_Fmask.png` | Aperturas de máscara + serigrafía | ídem |
| `generator/` | Scripts con los que se construyó el PCB (sin GUI) y `regenerate.sh` para reproducirlo fuera del repo | ver `generator/README.md` |
| `review/ADVERSARIAL_REVIEW.md` | Revisión adversarial independiente (4 lentes + escépticos) y dos rondas de verificación (revisiones 2 y 3 del PCB; la 4, commiteada, solo mueve dos textos) | workflows de revisión con agentes independientes |
