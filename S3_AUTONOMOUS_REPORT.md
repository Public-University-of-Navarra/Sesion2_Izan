# DEE — SESIÓN 3 — AUTONOMOUS EXECUTION REPORT

Proyecto: `Sesion2_Izan` (KiCad 10.0.6) · Rama de trabajo: `sesion3-pcb` · Fecha de ejecución: 2026-10-01
Ámbito: Sesión 3 de Desarrollo de Equipos Electrónicos (layout, stackup, placement, reglas, net classes, routing, DRC, Git).

---

## 1. Resultado

**PARCIAL.**

El trabajo técnico de la Sesión 3 está terminado y validado con KiCad (ERC 0/0, DRC 0 violaciones, 0 conexiones pendientes, paridad esquema‑PCB 0). Queda **una cosa sin hacer**: **la rama no se ha podido subir a `origin`**. El servidor responde `403 Permission denied to IzanVoltis`: las únicas credenciales de git/gh en este equipo son de la cuenta del trabajo `IzanVoltis`, que no tiene acceso a la organización de la UPNA. No he tocado credenciales (ver §24 y §28). Según el criterio de éxito que se me dio ("rama subida a origin"), no puedo marcar el resultado como COMPLETADA.

Otros puntos abiertos, que no impiden el resultado técnico:
- Los teardrops no se pueden generar desde la CLI/API de KiCad 10; hay que hacerlos en la GUI (§28).
- Conviene revisar la placa en la GUI de KiCad (§27).
- **Antes de usar KiCad, hay que cerrar el KiCad que quedó abierto** con el proyecto cargado desde antes de S3, para que no sobrescriba los ajustes nuevos (§26.15, §27.2).

| Criterio | Estado |
|---|---|
| main preservada, baseline S2 registrado | ✅ `9509303` (main = origin/main, sin cambios) |
| Rama S3 creada | ✅ `sesion3-pcb` (local) |
| Fuentes leídas (PDF, ExplAIn, guía) | ✅ |
| Proyecto real auditado | ✅ |
| Datasheets reales revisados | ✅ STM32G030 (DS12991) y LD1117 |
| Desacoplos correctos | ✅ C302 100 nF + C303 4,7 µF en VDD (nuevos); C201/C202/C301 verificados |
| Test points razonables | ✅ TP201 VIN, TP202 3V3, TP203 GND |
| Manufacturer/MPN/footprints | ✅ en los 5 componentes nuevos |
| ERC correcto | ✅ 0 errores, 0 avisos |
| PCB sincronizado | ✅ 19/19 huellas, paridad 0 |
| Stackup 2 capas, FR4, 1 oz | ✅ en el `.kicad_pcb` |
| Edge.Cuts cerrado y dimensionado | ✅ 39,00 × 26,70 mm |
| Placement / conectores en bordes / desacoplo junto al CI | ✅ |
| Reglas 0,20 / 0,25 / 0,25 | ✅ (y comprobado que la regla 0,25 pista‑pista actúa) |
| Net classes GND/POWER/SIGNAL, todas las redes asignadas | ✅ |
| Routing terminado, vías minimizadas | ✅ 1 vía de señal + 5 de GND |
| Plano GND, zonas rellenas | ✅ F.Cu y B.Cu, rellenadas por kicad-cli |
| Serigrafía razonable | ✅ 0 avisos de serigrafía |
| DRC sin errores, sin pendientes, paridad | ✅ 0 / 0 / 0 |
| Revisión independiente del PCB | ✅ revisión adversarial (4 lentes + escépticos) y dos rondas de verificación, de las revisiones 2 y 3; la 4 solo mueve dos textos (§22) |
| BOM actualizada | ✅ |
| Commits coherentes | ✅ |
| **Rama subida a origin** | ❌ **BLOQUEADO** (credenciales) |
| main no tocada | ✅ |
| Informe generado | ✅ este documento |

---

## 2. Baseline Sesión 2

- **Rama:** `main`
- **SHA:** `95093034ed58d3fdfe4078ac2c028bbd6db632bf` — "Complete microcontroller schematic and BOM" (2026‑09‑28 12:38:32 +0200, Izan737)
- `origin/main` apuntaba al mismo SHA (después de `git fetch origin`). También `microcontrolador` y `origin/microcontrolador`. `alimentacion` = `d26830f`.
- **Etiqueta local** (no publicada): `S2_FINAL_BASELINE` → `9509303`.

**Estado inicial.** `main` tenía **3 ficheros modificados sin commit**:

| Fichero | Cambio |
|---|---|
| `FiltroRC.kicad_sch` | UUID de la hoja regenerado por KiCad al guardar |
| `Microcontrolador.kicad_sch` | Valor de C301 normalizado de `100 nF` a `100nF` |
| `Sesion2_Izan.kicad_pro` | Ajustes de exportación de BOM: columnas Manufacturer y MPN, nombre de fichero |

Procedencia: el historial local de KiCad (`.history`) registra un **"SCH Save" el 2026‑10‑01 a las 02:50:38**, posterior al commit de S2. Son ediciones del usuario en KiCad. Dato útil: la BOM de S2 que está en `main` ya agrupaba C201 y C301 como `100nF`, aunque el esquema de `main` todavía decía `100 nF`. El guardado pendiente corregía esa incoherencia.

**Protección antes de tocar nada.** No se borró nada, ni hubo reset ni clean:
1. Entrada de stash creada con `git stash create` + `git stash store`, sin tocar el working tree: `stash@{0}` = `96d71b69a164ab79cbfd6dd9a3e091c6b329aaf4` ("BACKUP pre-S3 …"). Sigue en el repo local; se puede borrar cuando quieras (`git stash drop`).
2. Patch y copia completa del working tree en el directorio temporal de la sesión. Puede borrarse con el tiempo; la copia que perdura es el stash.
3. Esos cambios **no** se commitearon en main: viajaron a la rama nueva y se commitearon allí por separado (`e417981`), para que su procedencia quede clara.

**Confirmación de main intacta** (auditoría final, §24): `main` = `origin/main` = `9509303…`. No se ha hecho commit, merge ni push sobre main.

---

## 3. Rama Sesión 3

- **Nombre:** `sesion3-pcb`, creada desde `main` (`9509303`). No existía ninguna rama `sesion3*` ni local ni remota.
- **Estado remoto:** **no publicada.** `git push -u origin sesion3-pcb` → `403 Permission to Public-University-of-Navarra/Sesion2_Izan.git denied to IzanVoltis`. En `git ls-remote` solo aparecen `main`, `alimentacion` y `microcontrolador`.

---

## 4. Fuentes utilizadas

**Material oficial**
- `Sesión+3+-+Fundamentos+de+Layout,+Placement+y+Stackup (1).pdf` (22 diapositivas), leído entero. Diapositivas clave:
  - 5: cobre 1 oz/ft² = 35 µm.
  - 10: orden de colocación; "diseña como lees".
  - 11: desacoplo. "Vía de VCC → pad del condensador → pin del IC (nunca del revés)"; GND del condensador al plano con vías adyacentes.
  - 12: práctica intermedia. 2 capas, FR4, 1 oz/ft²; placement; Edge.Cuts.
  - 14: net classes, W_GND > 2·W_POWER > 2·W_SIGNAL; enrutado manual; evitar ángulos agudos.
  - 15: teardrops, puntos de test, documentación.
  - 16: vías.
  - 17: plano de masa.
  - 18: copper pours y alivios térmicos.
  - 19: DRC (captura de restricciones).
  - **21: tarea de la sesión.** Rama + desacoplos según datasheet; placement mínimo con zonas, conectores en laterales, flujo lógico y puntos de test; **Clearance 0,2 mm y Track Width / Track Distance mínimos 0,25 mm**; net classes GND/POWER/SIGNAL con el mínimo de vías; DRC sin errores y actualizar el repositorio.

**ExplAIn**
- `CLASS_DIGEST_DEE_2026-09-24_S03_RECOVERED.md` (grabación `93efe8da-0bee-4bd3-a2fa-3a5f18ff85fc`), leído entero. Usado sobre todo:
  - §4: enumeración literal de la tarea, 1:16:39–1:18:37.
  - §6: procedimiento.
  - §7: valores.
  - §10–11: errores a evitar. Entre ellos: sin ángulos rectos, no enrutar GND/VCC si hay relleno, SMD en una cara, plano que cubra la placa.
  - §13.3: contradicciones. La anchura mínima 0,2 de la demo frente a 0,25 de la tarea, y la regla de anchuras dicha en clase.

**Datasheets** (st.com no respondía desde este equipo; se usaron copias de los mismos documentos ST):
- STM32G030x6/x8, **DS12991 Rev 3** (abril 2020), copia alojada por M5Stack. Datos usados:
  - §5.1.6 Fig. 9, p. 39: VDD/VDDA "1 x 100 nF + 1 x 4.7 µF" y la advertencia "must be decoupled with filtering ceramic capacitors … as close as possible to, or below, the appropriate pins".
  - "General PCB design guidelines", p. 70.
  - Fig. 19, p. 66: NRST con 0,1 µF "as close as possible to the device".
  - Fig. 4, p. 29: pinout LQFP32.
- LD1117, **ST Rev 19** (dic. 2005), copia alojada por Octopart. Datos usados:
  - Fig. 2: SOT‑223 con 1 = GND, 2 = VOUT (tab = VOUT), 3 = VIN.
  - Fig. 4: CIN 100 nF y COUT 10 µF.
  - Texto: "Only a very common 10 µF minimum capacitor is needed for stability".
- Fuente secundaria (no es datasheet): foro de ST, respuesta de un ingeniero de ST. Dice que el LD1117 necesita COUT ≥ 10 µF **y ESR ≥ 0,3 Ω**. Se usa solo para valorar el riesgo de §26.
- Fichas de distribuidor/fabricante, para confirmar que los MPN nuevos existen:
  - Samsung CL21B475KAFNNNE (4,7 µF 25 V X7R 0805).
  - Keystone 5000 rojo, 5001 negro y 5003 naranja (Miniature PC Test Point).

**Guía del compañero**
- `Sesión 3 Diseño PCB.html`, convertida a texto y leída entera. Es de otro proyecto (`Sesion2_Aser`: STM32G031 + MCP1703A). Solo se usó como lista de pasos y de menús. Las diferencias están en §6.

**Inferencia propia** (siempre señalada como decisión en §25)
- Valores de las net classes dentro de la regla del profesor.
- Interpretación de "Track Distance".
- Tamaño de placa, placement y ruteo.
- Tamaños de vía.
- Parámetros de zona.
- Colores de los test points.
- Serigrafía.

---

## 5. Proyecto real detectado

- **Raíz del repo:** `C:/Users/Propietario/Documents/GitHub/Sesion2_Izan`. Proyecto KiCad en `Sesion2_Izan/`.
- **Ficheros:** `Sesion2_Izan.kicad_pro`, `Sesion2_Izan.kicad_sch` (raíz), `Alimentacion.kicad_sch`, `Microcontrolador.kicad_sch`, `FiltroRC.kicad_sch` (instanciado 3 veces: FiltroRC_1/2/3), `Sesion2_Izan.kicad_pcb` (al empezar estaba **vacío**, 79 bytes), `Sesion2_Izan_BOM.csv` y `.gitignore` (`.history/`, `*.kicad_prl`, `~*.lck`, backups).
- **Archivo principal:** `Sesion2_Izan.kicad_sch`. Hoja raíz con J101 y PWR_FLAG, más las hojas Alimentacion y Microcontrolador.
- **MCU:** U301 STM32G030K8Tx, MPN **STM32G030K8T6**, LQFP‑32 7×7 mm, paso 0,8.
- **Regulador:** U201 **LD1117S33TR** (ST), SOT‑223‑3_TabPin2, salida fija de 3,3 V.
- **Conectores:**
  - J101: borna Phoenix 1935161 (PT 1,5/2‑5,0‑H). 1 = VIN, 2 = GND.
  - J301 "E/S": Samtec TSW‑106. 1 = 3V3, 2 = AIN1_EXT, 3 = AIN2_EXT, 4 = AIN3_EXT, 5 = OUT1, 6 = GND.
  - J302 "SWD": Samtec TSW‑105. 1 = 3V3, 2 = SWCLK, 3 = GND, 4 = SWDIO, 5 = NRST.
- **Filtros:** 3 RC paso bajo, R4x1 4,7 kΩ (Panasonic ERJ‑6ENF4701V) y C4x1 33 nF (KEMET C0805C333K5RACTU). Entran en PA0, PA1 y PA4 (pines 7, 8 y 11). fc ≈ 1 kHz.
- **Alimentaciones:** `/Alimentacion/VIN` (J101.1 → C201 → U201.3) y `/Microcontrolador/3V3` (U201 VOUT → C202, VDD, J301.1, J302.1). Masa: `GND`.
- **Otras señales:** `NRST` (C301 100 nF), `SWCLK` (PA14, pin 25), `SWDIO` (PA13, pin 24), `OUT1` (PA5, pin 12). 23 pines del MCU sin conectar, marcados con no‑connect.
- **Componentes:** 14 en S2 → **19 en S3**.

---

## 6. Diferencias respecto a la guía del compañero

| Tema | Guía del compañero (Sesion2_Aser) | Este proyecto (Izan) | Motivo |
|---|---|---|---|
| MCU | STM32G031 | **STM32G030K8T6** | Componente real del proyecto |
| LDO | MCP1703A (1 µF in / ≥1 µF out) | **LD1117S33TR** (100 nF in / 10 µF out) | Componente real; sus requisitos salen de su datasheet |
| Desacoplo VDD | C302 100 nF + C303 4,7 µF Murata GRM21BR71E475KA73L | C302 100 nF (mismo Samsung que C201/C301) + C303 4,7 µF **Samsung CL21B475KAFNNNE** | Mismo requisito ST (100 nF + 4,7 µF), pero MPN elegido de forma independiente y coherente con el fabricante ya usado |
| Conectores | J301 = SWD, J302 = E/S | **J301 = E/S, J302 = SWD** | Referencias reales del esquema de Izan |
| Valores (fase A de la guía) | Cambia valores a 1u/100n/1k, "VIN 9V", etc. | **No aplicado** | No pertenece a S3 ni al proyecto de Izan |
| Test points | 5000 rojo para VIN y 3V3, 5001 negro para GND; en el borde superior | 5003 **naranja** VIN, 5000 rojo 3V3, 5001 negro GND; agrupados abajo a la izquierda (VIN‑GND‑3V3) | Colores distintos para no confundir VIN con 3V3 al medir; la ubicación sale de este placement |
| Tamaño de placa | 45 × 35 mm (orientativo) | **39,00 × 26,70 mm** | Resultado de compactar este placement |
| Reglas | 0,2 / 0,25 y regla personalizada pista‑pista 0,25 | Igual en concepto. Además se comprueba con una prueba de violación inyectada que la regla actúa | Misma lectura del enunciado, verificada |
| Net classes | 0,25 / 0,6 / 1,3 | 0,25 / 0,6 / 1,3 | Coinciden porque ambos aplican la regla de la diapositiva con valores mínimos "redondos" (0,6 > 0,5; 1,3 > 1,2). No se copió sin contraste |
| Patrones de clase | `*VIN*`, `*AIN*`, `*SWD*`… | `GND`, `*VIN`, `*3V3`, `*AIN*`, `*NRST`, `*OUT1`, `*SWCLK`, `*SWDIO` | Comprobado red a red con pcbnew que cada red cae en su clase |
| Ruteo | Todo en F.Cu; vías donde haga falta | Todo en F.Cu salvo NRST (1 vía + B.Cu hasta el pad THT de J302.5). Análisis topológico en §18 | Pinout real del LQFP‑32 |
| Teardrops | Editar → Editar lágrimas | **No realizados** (sin CLI/API en KiCad 10) | §28 |
| Merge a main (paso G3 de la guía) | Sí | **No** | Instrucción explícita de no tocar main |
| Rama | `pcb` | `sesion3-pcb` | Nombre pedido en la instrucción |

---

## 7. Cambios de esquemático

Commit `a17f5f1` en la rama S3.

- **Microcontrolador.kicad_sch:**
  - **C302** (100 nF) y **C303** (4,7 µF), colgados de la línea 3V3 → VDD (pin 4) de U301, con sus símbolos GND (#PWR0305 y #PWR0306) y una unión.
  - Se dibujaron a la derecha de la línea VDD para no pisar los textos de U301.
- **Alimentacion.kicad_sch:**
  - **TP201** en el nodo VIN (entre la etiqueta jerárquica VIN y C201).
  - **TP202** en el nodo 3V3 (entre C202 y la etiqueta 3V3).
  - **TP203** a GND (#PWR0204).
  - Los cables existentes se partieron con unión, como lo haría el editor de KiCad. Se añadió el símbolo de librería `Connector:TestPoint`.
- **Sesion2_Izan.kicad_pro:** `used_designators` actualizado (C301‑303, #PWR201‑204, #PWR301‑306, TP201‑203).
- **Sesion2_Izan_BOM.csv:** regenerada (§10).

Cómo se editó. Se insertaron bloques S‑expression con el formato exacto de KiCad 10: grupos por tipo ordenados por UUID, CRLF como en los ficheros originales y UUID deterministas. Antes de aplicarlo al repo se validó en una copia: ERC, netlist y PDF del esquema. El diff contiene solo añadidos, más 2 líneas modificadas por partir los cables. Recomiendo abrir y guardar el esquema en la GUI de KiCad una vez (§27).

---

## 8. Desacoplo

| Ref | Valor | MPN | Footprint | Fuente | Justificación |
|---|---|---|---|---|---|
| **C302 (nuevo)** | 100nF, X7R 50 V | Samsung Electro‑Mechanics **CL21B104KBCNFNC** | Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder | DS12991 §5.1.6 Fig. 9 y p. 70 | Cerámico de 100 nF en VDD/VDDA. Pegado a los pines 4 y 5: pad 3V3 a **1,60 mm** de VDD y pad GND a **1,25 mm** de VSS, unido por una pista directa. Mismo MPN que C201/C301, así la BOM queda agrupada |
| **C303 (nuevo)** | 4.7uF, X7R 25 V | Samsung Electro‑Mechanics **CL21B475KAFNNNE** | Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder | DS12991 Fig. 9 ("+ 1 x 4.7 µF", "ceramic") | Reserva cerámica (bulk) junto a C302 (pad 3V3 a **3,04 mm** de VDD). Va antes que C302 en el camino 3V3. Su GND vuelve por la vía (20,75; 3,5) y el plano B.Cu (§26) |
| C301 (existente) | 100nF | Samsung CL21B104KBCNFNC | 0805 | DS12991 Fig. 19 (0,1 µF en NRST, lo más cerca posible) | Ya cumplía; en el PCB queda a **3,35 mm** del pin 6 (lo más cerca que permiten C302 y la pista AIN1) |
| C201 (existente) | 100nF | Samsung CL21B104KBCNFNC | 0805 | LD1117 Fig. 4 (CIN 100 nF) | Ya cumplía; en el PCB está sobre la línea VIN, a **1,02 mm** del pin 3 |
| C202 (existente) | 10uF tántalo 10 V | KEMET T495A106K010ATE1K8 (ESR máx. 1,8 Ω) | Capacitor_Tantalum_SMD:CP_EIA-3216-18_Kemet-A | LD1117 Fig. 4 y "10 µF minimum … for stability" | Ya cumplía; a **2,21 mm** del tab VOUT. Su ESR es coherente con el requisito ESR ≥ 0,3 Ω del foro de ST. Polaridad: pad 1 (+) en 3V3, comprobado en el PCB |

Las distancias son huecos de cobre pad‑pad medidos con pcbnew sobre la placa final. Los GND de C201 y C202 van juntos, con pista de 1,3 mm, a la vía (13,75; 6,56), bajo el cuerpo de U201. Así el retorno hasta el pin GND del LDO baja de ≈ 23 mm a ≈ 12 mm, medido por el eje de las pistas; es un hallazgo de la revisión adversarial (§22).

No se cambió ningún componente existente. Solo se añadieron los dos que faltaban: el MCU **no tenía ningún condensador en VDD** (C301 está en NRST, no en VDD).

---

## 9. Test points

- **Qué piden las fuentes.** El PDF (diap. 21) dice "añade puntos de test". ExplAIn: "algún punto de test", con el ejemplo de la tensión de salida del regulador (1:17:11–1:17:57). **No se fija un número.** La decisión de poner 3 es mía.
- **Implementación:**
  - **TP201** en VIN: Keystone **5003** (naranja).
  - **TP202** en 3V3: Keystone **5000** (rojo).
  - **TP203** en GND: Keystone **5001** (negro).
  - Footprint de los tres: `TestPoint:TestPoint_Keystone_5000-5004_Miniature` (pad THT Ø2,0, taladro 1,0).
- **Por qué THT de lazo:** permiten enganchar pinzas o sondas de polímetro sin pinchar patillas de integrados, que es lo que desaconsejó el profesor (1:00:24). Los colores separan las dos tensiones.
- **Ubicación:** agrupados abajo a la izquierda, en zona libre y accesible, con orden VIN · GND · 3V3 y serigrafía `VIN`/`GND`/`3V3` más su referencia. TP202 está en el propio corredor de 3V3. TP201 se alimenta con una pista VIN que baja bajo el cuerpo de J101. TP203 (GND) es THT y une los dos planos.

---

## 10. BOM

`Sesion2_Izan/Sesion2_Izan_BOM.csv` se regeneró con kicad-cli usando las **mismas columnas, agrupación y orden** que la BOM de S2. Se comprobó que el mismo comando reproduce **byte a byte** la BOM de S2 sobre el esquema anterior. 14 filas, 19 componentes:

- Fila 100nF: `C201,C301,C302` (3 unidades, CL21B104KBCNFNC).
- Fila nueva: `C303` 4.7uF (CL21B475KAFNNNE).
- Filas nuevas: `TP201` VIN (5003), `TP202` 3V3 (5000), `TP203` GND (5001).
- El resto, idéntico a S2.

Nota heredada de S2: la columna "Exclude from Position Files" sale con el texto literal `${EXCLUDE_FROM_POS_FILES}`. Es un comportamiento de KiCad 10.0.6 y ya estaba así en la BOM de S2; se conservó para no cambiar el formato.

---

## 11. ERC

- **Comando:** `kicad-cli sch erc --severity-all --format report --exit-code-violations -o S3_validation/ERC_report.rpt Sesion2_Izan/Sesion2_Izan.kicad_sch`, más la variante `--format json`.
- **Resultado:** **0 errores, 0 avisos**, código de salida 0, en las 6 hojas.
- **Comprobaciones ignoradas:** son las que el proyecto ya tenía ignoradas; no se cambiaron. "Global label only appears once", "Four connection points are joined together", "SPICE model issue" y "Assigned footprint doesn't match footprint filters".
  - La sección `erc` del `.kicad_pro` es **idéntica a la de main** (S2).
  - Esas 4 son también las que ignoran la mayoría de demos de KiCad 10; son los valores por defecto.
  - **Prueba con todo activado** (en una copia): un único aviso, `footprint_filter` en J101. Es la misma causa que en el DRC (§20): la huella Phoenix de S2 frente al filtro genérico del símbolo.
- **Revisión a mano:**
  - Referencias únicas.
  - Todos los símbolos con footprint, Manufacturer y MPN.
  - Conectividad comprobada por netlist: TP201 en VIN; C302, C303 y TP202 en 3V3; TP203 en GND.
- Se repitió el ERC al final (§24).

---

## 12. Sincronización esquema‑PCB

- No existe un "Update PCB from Schematic" en kicad-cli ni en la API Python de KiCad 10, y esta sesión no puede manejar la GUI. Por eso **se replicó el actualizador**:
  1. Netlist exportado por `kicad-cli sch export netlist`.
  2. Huellas cargadas de las librerías oficiales de KiCad 10, con su LIB_ID.
  3. Ruta jerárquica (KIID_PATH = tstamps de hoja + UUID del símbolo), sheetname, sheetfile y filtros copiados del netlist.
  4. Campos del símbolo copiados como campos ocultos en F.Fab (Manufacturer, MPN, Datasheet, Description).
  5. Se eliminó el campo de librería `KiLib_Generator`, que no existe en el símbolo.
  6. Red, función y tipo de pin en cada pad. Las 23 redes `unconnected-(…)` de los NC del MCU, igual que KiCad.
- **Validación:** `kicad-cli pcb drc --schematic-parity` → **0 problemas de paridad**. La paridad de KiCad 10 compara referencia, valor, footprint, nets por pad y también campos (`footprint_symbol_field_mismatch`).
- **Resultado:** 19 huellas, sin duplicados ni sobrantes. La ruta jerárquica correcta permite usar F8 en la GUI sin que KiCad reasocie ni borre huellas.

---

## 13. Stackup

| Capa | Tipo | Material | Espesor |
|---|---|---|---|
| F.SilkS / F.Paste | — | — | — |
| F.Mask | máscara | — | 0,01 mm |
| **F.Cu** | cobre | — | **0,035 mm (1 oz/ft²)** |
| dielectric 1 | **core** | **FR4** (εr 4,5; tan δ 0,02) | 1,51 mm |
| **B.Cu** | cobre | — | **0,035 mm (1 oz/ft²)** |
| B.Mask | máscara | — | 0,01 mm |
| B.Paste / B.SilkS | — | — | — |

- **2 capas de cobre**, espesor total **1,6 mm**, impedancia controlada desactivada.
- **Requisito docente:** 2 capas, FR4, 1 oz/ft² (diap. 12; ExplAIn 26:55).
- **Decisión de implementación, no exigida:** núcleo de 1,51 mm, total 1,6 mm, εr y tan δ por defecto de KiCad. El profesor mencionó el núcleo estándar 1,6 solo como teoría.
- **Cómo se hizo:** la API Python no expone el editor de stackup. El bloque se escribió con el formato de KiCad 10 (el mismo que traen sus demos de 2 capas). Después **pcbnew recargó y volvió a guardar** el fichero y se comprobó que el stackup se conserva y lo interpreta (`m_HasStackup = True`).

---

## 14. Reglas

| Regla | Valor | Fuente | Tipo |
|---|---|---|---|
| Clearance mínimo (Board Setup › Constraints) | **0,20 mm** | Diap. 21; ExplAIn 1:17:57 | REQUISITO DOCENTE |
| Ancho mínimo de pista (Constraints) | **0,25 mm** | Diap. 21; ExplAIn 1:17:57 | REQUISITO DOCENTE |
| Distancia mínima pista‑pista (regla `Track to track distance 0.25 mm` en `Sesion2_Izan.kicad_dru`: `A.Type == 'Track' && B.Type == 'Track'`) | **0,25 mm** | Diap. 21 ("Track Distance … 0,25 mm") | REQUISITO DOCENTE (su implementación es decisión mía) |
| Clearance de cada net class | 0,20 mm | Coherente con el mínimo | DECISIÓN DE INGENIERÍA |
| Separación del relleno de cobre | 0,30 mm | — | DECISIÓN DE INGENIERÍA (margen para soldar a mano) |
| Diámetro mínimo de vía 0,5; anillo 0,1; taladro 0,3; cobre‑agujero 0,25; agujero‑agujero 0,25; cobre‑borde 0,5; µvía 0,2/0,1; texto de serigrafía 0,8/0,08 | por defecto de KiCad 10 | Coinciden con la captura de la diap. 19 | Valores por defecto (no los fijó el profesor) |

- **Cómo se resuelve "clearance 0,2" frente a "distancia entre pistas 0,25".** El 0,20 es el mínimo general: pad‑pad, pad‑pista y cobre‑zona. El 0,25 es más estricto y solo se aplica entre pistas de redes distintas. Es la lectura literal del enunciado, que da dos valores distintos. Un mínimo general de 0,25 también lo cumpliría esta placa (el LQFP‑32 tiene 0,30 mm entre pads), pero no es lo que se pide.
- **Prueba de que la regla funciona.** En una copia se metieron pistas a 0,22 mm y a 0,26 mm. El DRC marcó la de 0,22 como *"regla 'Track to track distance 0.25 mm' margen 0,2500; real 0,2200"* y aceptó la de 0,26. Una pista de 0,22 de ancho también se marcó (mínimo 0,25).
- **Discrepancia documentada.** En la demo del DRC el profesor leyó "ancho mínimo 0,2" (1:14:22). Ese es el **valor por defecto de KiCad 10**, que también sale en la captura. Para la práctica mandan la tarea y la diapositiva 21, que dicen 0,25.
- **Medidas reales en la placa** (auditoría propia con pcbnew; la estadística de KiCad da también "margen mínimo de pista 0,275"):
  - pista‑pista mínima **0,300 mm** (regla 0,25);
  - pista‑vía mínima **0,275 mm**;
  - pista‑pad mínima **0,245 mm** (mínimo general 0,20);
  - ancho mínimo 0,25 mm.

---

## 15. Net Classes

| Clase | Nets | Ancho | Clearance | Vía (Ø/taladro) | Fuente / criterio |
|---|---|---|---|---|---|
| **GND** | `GND` | **1,30 mm** | 0,20 | 0,8/0,4 | Regla de la diap. 14 (W_GND > 2·W_POWER → 1,3 > 1,2). En la práctica GND va por planos (§19) |
| **POWER** | `/Alimentacion/VIN`, `/Microcontrolador/3V3` | **0,60 mm** | 0,20 | 0,8/0,4 | 2·W_POWER > 2·W_SIGNAL y lo dicho en clase (W_POWER > 2·W_SIGNAL → 0,6 > 0,5). Entra en pads LQFP de 0,5 dejando 0,25 al pad vecino |
| **SIGNAL** | `AIN1`, `AIN2`, `AIN3`, `AIN1_EXT`, `AIN2_EXT`, `AIN3_EXT`, `NRST`, `OUT1`, `SWCLK`, `SWDIO` (con prefijo `/Microcontrolador/`) | **0,25 mm** | 0,20 | 0,6/0,3 | El mínimo permitido |
| Default | 23 redes `unconnected-(U301-…)` de un solo pad (NC del MCU) | 0,25 | 0,20 | 0,6/0,3 | Sin pistas. Se alinea con el mínimo para que ninguna red quede por debajo de 0,25 |

- **Requisito docente:** existen las clases GND, POWER y SIGNAL ("con definir clase GND, power y signal es suficiente", 1:18:26), y W_GND > 2·W_POWER > 2·W_SIGNAL (diap. 14).
- **Lo que NO dijo el profesor:** no dio anchos numéricos por clase ni qué redes van en cada una. Los valores son **decisión de ingeniería** dentro de esa regla.
- **Formulaciones distintas de la regla.** La diapositiva dice "W_GND > 2·W_POWER > 2·W_SIGNAL". En clase se dijo "GND el doble de power, y power mayor que el doble de signal". 0,25 / 0,6 / 1,3 cumple la diapositiva, que tiene prioridad, y se acerca a lo dicho en clase (1,3 frente a "el doble" = 1,2).
- **Prioridades:** GND 0, POWER 1, SIGNAL 2.
- **Comprobación:** con pcbnew se verificó red a red que cada una resuelve a la clase prevista.
- **Excepción documentada:**
  - GND no se enruta (lo hacen los planos). Solo tiene enlaces cortos.
  - Donde la geometría lo permite usan 1,3 mm: GND del LDO → vía, C303 → vía, C301 → vía, C201 ↔ C202 → vía.
  - Hay 2 cuellos estrechos donde 1,3 mm es físicamente imposible (pads LQFP de 0,5 mm a paso 0,8):
    - C302 → VSS a **0,5 mm**;
    - VSS → vía a **0,4 mm**, para dejar 0,30 mm a la pista 3V3 del pin 4.
  - El puente C501 ↔ C601 y la bajada desde C601.2 a la vía van a **1,0 mm**: es lo máximo que cabe entre los pads de los filtros.
  - El ancho de una net class en KiCad es el valor por defecto al enrutar, no un mínimo comprobado por el DRC; el mínimo real es 0,25.

---

## 16. Edge.Cuts

- **Contorno:** rectángulo cerrado de una sola pieza en Edge.Cuts, línea de 0,05 mm, **39,00 × 26,70 mm** (1041,3 mm², según `kicad-cli pcb export stats`). Esquina superior izquierda en (100, 100) mm en coordenadas de KiCad.
- **Validación:** el contorno es un polígono cerrado y único, sin segmentos duplicados. Todas las courtyards quedan dentro y cobre‑borde ≥ 0,5. El DRC no da ningún aviso de borde.
- **Criterio de tamaño:** no hay medida obligatoria (ExplAIn §7: "no dicho"). Se compactó todo lo posible con estas condiciones:
  - Conectores en los bordes.
  - Courtyards sin solaparse.
  - Hueco para el ruteo sin vías.
  - Una franja inferior de ~1,1 mm para los nombres de pin de J301. Hice crecer la placa a propósito: es documentación (diap. 15).
- **Iteración:** 40×30 → 39×26,7 → 39×24,6 → 39×26,35 (se añadieron etiquetas y referencias) → **39×26,70** (revisión 2: la zona analógica baja 0,35 mm para que las referencias de los filtros quepan en horizontal). La guía del compañero proponía 45 × 35 como orientación.

---

## 17. Placement

Todo en la cara superior (diap. 10; "SMD por una sola cara").

- **Zona de potencia (arriba a la izquierda).** Flujo de izquierda a derecha:
  - **J101** en el borde izquierdo. La boca de cable mira al borde (comprobado en la vista lateral 3D).
  - Línea **VIN** recta: J101.1 → **C201** → pin 3 de **U201**. Es el orden "VCC → pad del condensador → pin".
  - **U201** girado con los pines hacia arriba y el tab hacia abajo, hacia el MCU.
  - **C202** en la columna entre J101 y U201, junto al tab.
  - Los condensadores de entrada y salida quedan a ≤ 2,3 mm del pin del regulador (C201 1,02 mm del pin 3; C202 2,21 mm del tab).
  - GND de C201 y C202 unidos con pista de 1,3 mm a una vía propia (13,75; 6,56), bajo el cuerpo de U201.
  - Polaridad de la borna marcada en serigrafía: `1:VIN 2:GND`.
- **Zona MCU (centro y derecha).**
  - **U301** en el centro, girado 0°: los pines 4 a 8 (alimentación, NRST, AIN1, AIN2) miran a la zona de potencia y analógica, y los pines 24/25 (SWD) miran a J302.
  - **C302** pegado a los pines 4 y 5: pad 3V3 a 1,60 mm de VDD y pad GND a 1,25 mm de VSS, con pista directa.
  - **C303** encima de C302, en el camino de 3V3 (3,04 mm de VDD).
  - **C301** a la izquierda del pin 6 (3,35 mm).
- **SWD:** **J302** vertical en el borde derecho, junto a la esquina SWD del MCU. Orden de pines compatible sin cruces (CLK por encima de DIO).
- **Zona analógica (abajo).**
  - **J301** horizontal en el borde inferior.
  - Fila de filtros con orden C401|R401 · R501|C501 · C601|R601.
  - Las R quedan hacia el conector. La C queda en el nodo hacia el ADC; en AIN2 la pista sale del propio pad de C501.
  - Distancia de cada C de filtro a su pin ADC: C601 2,10 mm (PA4), C501 3,43 mm (PA1), C401 9,44 mm (PA0). C401 queda lejos: es un compromiso documentado en §26.
  - El abanico AIN1/AIN2/AIN3/OUT1 respeta el orden de pines alrededor de la esquina del MCU, así que no hay cruces.
  - Separada de las líneas SWD, que van por el lado derecho.
- **Test points:** abajo a la izquierda, en zona libre (§9).
- **Iteraciones:** se revisaron solapes de courtyard con el DRC y renders 2D/3D en cada paso. Hubo 6 iteraciones de placement y después las revisiones 2, 3 y 4, tras cada ronda de revisión independiente. En la revisión 3 los test points bajaron 0,65 mm para separar la leyenda de J101. Resultado: 0 solapes de courtyard.

---

## 18. Routing

- **Capas.** Todo en **F.Cu** (70 segmentos, 169,2 mm), salvo el tramo largo de **NRST**, que va en **B.Cu** (2 segmentos, 11,1 mm). Total: **72 segmentos, 180,4 mm**. Es ruteo "manual": cada tramo está diseñado y documentado en `S3_validation/generator/layout.py`. **No se usó autorouter.**
- **Criterios aplicados:**
  - Pistas cortas.
  - Solo esquinas de 45°. La auditoría revisa todas las uniones, también las de 3 brazos y las T, y encuentra 0 ángulos agudos. Las 5 uniones de 90° están dentro de pads (R401.2, C501.1, C601.2, R601.2) o en el centro de una vía (20,75; 3,5).
  - En C303.1 se juntan 3 pistas de 3V3. La del LDO entra en horizontal para que no quede una muesca de 45° en el cobre (hallazgo de la ronda 2).
  - VIN y 3V3 a 0,6 mm.
  - Camino de 3V3: tab → C303 → C302 → VDD. Ramas a C202 → TP202 → J301.1 (por la izquierda) y a J302.1 (por encima del MCU).
  - Señales a 0,25 mm.
  - Analógicas cortas y lejos de SWD.
  - Ninguna pista de F.Cu va encima y en paralelo a la de B.Cu.
- **Vías: 6** (1 de señal + 5 de GND). Cada una tiene una razón:

| Vía | Red | Ø/taladro | Razón |
|---|---|---|---|
| (26,6; 13,3) bajo U301 | NRST | 0,6/0,3 | **Única vía de señal.** El pin 6 (NRST) está entre VDD/VSS (4–5) y las AIN (7–8, 11–12), en la esquina opuesta a SWD (24–25). Cualquier camino en F.Cu cruzaría la alimentación o el abanico analógico, con cualquier giro del MCU (análisis topológico). La pista en B.Cu termina directamente en el pad THT de J302.5, así que hace falta 1 vía y no 2 |
| (26,0; 11,9) bajo U301 | GND | 0,8/0,4 | VSS (pin 5) al plano B.Cu, justo bajo el MCU. Une también la isla de F.Cu bajo el chip. Está colocada para que todas las distancias pista‑vía sean ≥ 0,25 |
| (20,75; 3,5) | GND | 0,8/0,4 | GND del LDO (pin 1) y de C303 al plano. Diap. 11: "vías adyacentes" del desacoplo. Separada del marcador de pin 1 de U201 |
| (13,75; 6,56) bajo U201 | GND | 0,8/0,4 | **Añadida tras la revisión adversarial.** GND de C201 y C202 (entrada y salida del LDO) al plano. Acorta el retorno de ≈ 23 mm a ≈ 12 mm (hallazgo E1/L1, §22). Va bajo el cuerpo del SOT‑223 para no cortar su serigrafía |
| (16,0; 12,2) | GND | 0,8/0,4 | C301 y C401 quedan en una región de F.Cu cerrada por pistas de 3V3 y AIN1; sin la vía serían islas |
| (25,25; 21,85) | GND | 0,8/0,4 | C501 y C601, encerrados entre los nodos AIN y las pistas de la banda EXT. Se alimenta en vertical desde el pad C601.2 |

- **Lo que NO se enruta:** GND, salvo enlaces cortos a pads y vías (lo hacen los planos, ExplAIn 1:11:38). No hay pour de VCC: con 2 capas la prioridad es GND (1:06:45).

---

## 19. Plano GND

- **Zonas:** `GND_F` en F.Cu y `GND_B` en B.Cu. Ambas cubren toda la placa con el contorno de Edge.Cuts (el cobre se retira 0,5 mm del borde).
  - Separación 0,30 mm.
  - Espesor mínimo 0,25 mm.
  - **Alivios térmicos** en todos los pads: hueco 0,3 mm, radios de 0,4 mm.
  - Eliminación de islas activada.
- **Áreas rellenas:** F.Cu ≈ 605 mm², B.Cu ≈ 890 mm². Las cifras de cobre total de las estadísticas son 833/942 mm² (`S3_validation/board_stats.txt`).
- **B.Cu** es un plano casi continuo. Solo tiene el corte de la pista NRST (de debajo del MCU a J302.5). Ninguna señal de F.Cu cruza ese corte: AIN, SWD y OUT1 van por otras zonas.
- **Uniones entre planos:** los pads THT de GND (J101.2, TP203, J301.6, J302.3) y las 5 vías de GND.
- **F.Cu fragmentado.** Con el ruteo a una cara, el relleno de F.Cu queda partido en varias islas. Todas siguen conectadas a la red GND (por vías, pads THT o enlaces cortos): el DRC da 0 conexiones pendientes y 0 cobre aislado. La referencia continua de la placa es B.Cu.
- **Relleno final:** lo hizo **el propio kicad-cli** (`--refill-zones --save-board`). DRC posterior: 0 islas y 0 alivios insuficientes (`starved_thermal`).
- Al principio aparecieron 12 avisos de `isolated_copper`. La causa: mi script rellenaba antes de construir la conectividad. Se corrigió, y además el relleno definitivo es de KiCad.

---

## 20. DRC

- **Comando final, sobre el fichero del repo:** `kicad-cli pcb drc --refill-zones --schematic-parity --severity-all --exit-code-violations --format report|json -o S3_validation/DRC_report.* Sesion2_Izan/Sesion2_Izan.kicad_pcb`
  - Rellena las zonas en memoria antes de comprobar y no reescribe el fichero.
  - El relleno guardado en el fichero lo hizo el propio KiCad (`--refill-zones --save-board`) en la copia de trabajo, antes de copiarla al repo.
  - Se pasó también el DRC **sin** rellenar, sobre el fichero tal como está guardado. Mismo resultado.
- **Resultado:** **0 errores · 0 avisos · 0 conexiones pendientes · 0 problemas de paridad.** Código de salida 0. Sin exclusiones: ninguna regla se desactivó ni se excluyó.
- **Severidades.** Se compararon las severidades del `.kicad_pro` con las de un proyecto nuevo creado por KiCad 10: son **idénticas**.
  - KiCad ignora por defecto 5 comprobaciones: `footprint_filters_mismatch`, `footprint_type_mismatch`, `missing_courtyard`, `track_not_centered_on_via` y `tuning_profile_track_geometries`. Siguen así; no las cambié.
  - `drc_exclusions` está vacío.
  - Respecto a un proyecto nuevo, los ajustes de placa solo cambian en el clearance mínimo (0,2), el ancho mínimo (0,25) y los tamaños predefinidos de pista y vía.
- **Prueba con todo activado.** En una copia del proyecto se pusieron como error esas 5 comprobaciones. Resultado: 0 violaciones, 0 pendientes y **un solo aviso**, `footprint_filters_mismatch` en J101. La huella `TerminalBlock_Phoenix:…PT-1,5-2-5.0-H…` no encaja con el filtro genérico `Connector*:*_1x??_*` del símbolo. Es una elección de S2 que no cambié, sin efecto eléctrico, y el ERC del proyecto también la ignora por defecto.
- **Historial de iteraciones:**
  - Primera pasada de ruteo: 0 errores eléctricos, 47 avisos de serigrafía.
  - Tras corregir la serigrafía: 8 avisos, luego 3, luego 0.
  - Avisos `isolated_copper` resueltos (§19).
  - Revisión 2 (correcciones de la revisión adversarial): de nuevo 0 / 0 / 0.
  - Revisión 3 (correcciones de la ronda 2): un primer intento dio 2 avisos `silk_overlap`, porque la leyenda de J101 tocaba los anillos de TP201/TP203. Se bajaron los test points y quedó 0 / 0 / 0.
  - Revisión 4 (dos referencias movidas tras la ronda 3): 0 / 0 / 0.
- **El DRC no lo es todo.** Además del DRC hay una auditoría geométrica propia (`S3_validation/audit_geometry.txt`) que mide:
  - distancias mínimas pista‑pista, pista‑pad y pista‑vía;
  - ángulos en todas las uniones, también las de 3 brazos y las T;
  - anchos y clase de cada red;
  - serigrafía frente a aperturas de máscara, frente a otras leyendas y frente a la serigrafía de las huellas;
  - taladros de vía bajo serigrafía.

---

## 21. Paridad esquema‑PCB

- **Componentes:** 19 en el esquema y 19 huellas en el PCB, mismas referencias. Valores y footprints idénticos a la BOM.
- **Redes:** idénticas a las del netlist, pad a pad. La paridad de KiCad da 0. Los revisores independientes la recalcularon con un netlist exportado por ellos: los 73 nodos coinciden con la red de su pad.
- **Faltantes, sobrantes y duplicados:** ninguno.
- **Conexiones pendientes:** 0.

---

## 22. Revisión visual

Renders guardados en `S3_validation/renders/`.

- **top / bottom / 3D (`render_3d_*.jpg`):**
  - Todo dentro de la placa.
  - J101 con la boca hacia el borde izquierdo (vista lateral).
  - Conectores accesibles en los bordes.
  - Serigrafía legible.
  - Cara inferior sin componentes.
- **Capas 2D:** `layer_Fcu_silk.png`, `layer_Bcu.png`, `layer_fab_courtyard.png` y `layer_Fmask.png`.
- **Incidencias encontradas y corregidas durante el proceso:**
  - Solapes de courtyard en los primeros placements.
  - Esquinas de 90° en EXT1, EXT2, SWCLK y SWDIO, pasadas a chaflán de 45°: el profesor pidió "sin ángulos rectos".
  - Distancias al límite (0,250 y 0,200), ampliadas a 0,300 y 0,245.
  - Referencias de los filtros que no cabían; se bajó la zona analógica (0,55 mm y después otros 0,35 mm).
  - Etiquetas de J302 que pisaban pads del MCU; se pusieron en vertical.
  - Islas de cobre.

### Revisión adversarial independiente

El resultado detallado está en `S3_validation/review/ADVERSARIAL_REVIEW.md`.

- **Ronda 1 (sobre la revisión 1 del PCB).** Cuatro revisores independientes, cada uno con una lente: eléctrica/datasheets, cumplimiento de la práctica, calidad de layout y fabricación/documentación. Para cada revisor, un escéptico intentó refutar cada hallazgo contra los ficheros reales.
  - **Balance:** 54 hallazgos. Los escépticos confirmaron 38 (casi todos de gravedad menor o informativa) y refutaron 16.
  - **Errores eléctricos: ninguno.** Pinouts y polaridades confirmados. Paridad recalculada por el revisor: los 73 nodos del netlist están en la misma red en el PCB, y las 19 referencias tienen el mismo valor, footprint y ruta jerárquica.
  - **El único "bloqueante"** (F1/E9/i8) era que la placa revisada aún no estaba en el repositorio. Se resuelve con el commit de layout.
  - **Corregido en la revisión 2:**
    - Lazo de retorno GND del LDO largo (E1/L1): vía nueva junto a C201/C202. En la revisión 3 quedó en (13,75; 6,56).
    - Polaridad de J101 sin marcar (E3/M1/F4/L6): leyenda `1:VIN 2:GND`.
    - Puente GND C501‑C601 a 0,5 mm (L14): ahora a 1,0 mm.
    - Referencias de los filtros en vertical y ambiguas (F3/m1/m5/L12): ahora en horizontal y escalonadas.
    - Serigrafía junto a aperturas de máscara (m2): ninguna leyenda a < 0,15 mm.
    - Trazo de texto (m3): 0,15 mm en todo el texto.
    - `O1` poco claro (i2): ahora `OUT`.
    - Distancia pista‑vía 0,20 (i5/F10): ahora ≥ 0,25.
  - **Documentado, sin cambio:** C303 con retorno por el plano (E2/L2), C401 lejos de PA0 (L4), F.Cu fragmentado (F6/L3), C301 a 3,35 mm (F9/L7), OUT1 por la zona analógica (L8), térmica del LDO (L9), tamaño de placa (L5), cajetines vacíos (F13), peculiaridad de la BOM (m6), test points sin modelo 3D (m8). Todos aparecen en §26.
  - **Pendiente en la GUI:** teardrops (F2/m4/L13), §28.
  - **Refutados por los escépticos (16):** E4–E8, F5, F7, F8, F11, F12, F14, L10, L11, m7, i3, i4. Sin acción.
- **Ronda 2 (sobre la revisión 2).** Un verificador comprobó una a una las correcciones y un revisor nuevo, sin contexto previo, buscó regresiones; los dos con sus propias medidas, DRC y netlist.
  - Resultado: **las 6 correcciones verificadas.**
  - Encontraron 21 puntos, casi todos menores o informativos y la mayoría coincidentes entre los dos:
    - una muesca de 45° en el cobre 3V3 en C303.1, que mi auditoría no veía porque solo revisaba uniones de 2 pistas;
    - la ref de J101 dentro de su courtyard;
    - `OUT` y `GND` pegados;
    - `C303` en vertical;
    - vías que tocaban serigrafía;
    - un tramo VSS con 1,8° de inclinación.
  - **Revisión 3:** los corrige, y la auditoría revisa ahora todas las uniones.
  - Quedan aceptados y documentados: la leyenda de C302 en zona densa, la leyenda de J101 cruzando la pista VIN de TP201, el contorno de J301 sobre una vía, y leyendas sobre pistas tapadas por máscara.
- **Ronda 3 (sobre la revisión 3).** El mismo formato de dos agentes.
  - Resultado: **las 11 correcciones verificadas**, DRC 0 / 0 / 0, paridad recalculada con su propio netlist y ningún ángulo agudo.
  - Una cifra anunciada no era exacta: 0,212 mm, no 0,25, entre `C401` y `R401`.
  - Un punto menor por agente:
    - `C401` quedaba más cerca de TP202 que de su pieza;
    - el retorno de C201/C202 se alargó 0,55 mm al mover la vía del LDO. Se acepta: ≈ +5 % sobre ≈ 12 mm, despreciable, a cambio de no tener taladros bajo la serigrafía.
  - El resto, informativo y aceptado.
- **Revisión 4 (la commiteada).** Solo mueve dos referencias: `C401` bajo su pieza, en la posición que propuso y probó el revisor, y `C301` 0,1 mm más abajo.
  - El cobre, las huellas, las zonas y las reglas son idénticos a los de la revisión 3 (`compare_boards.py`).
  - DRC 0 / 0 / 0.
  - La auditoría no encuentra leyendas a < 0,15 mm de una apertura de máscara ni a < 0,2 mm de otra leyenda.
  - Por eso no hizo falta otra ronda de agentes.

---

## 23. Archivos modificados

Diff `main...sesion3-pcb`:

| Fichero | Cambio |
|---|---|
| `Sesion2_Izan/Alimentacion.kicad_sch` | TP201–TP203 y símbolo TestPoint |
| `Sesion2_Izan/Microcontrolador.kicad_sch` | C302, C303 (y C301 `100nF`, cambio heredado) |
| `Sesion2_Izan/FiltroRC.kicad_sch` | UUID de la hoja (cambio heredado del guardado de KiCad) |
| `Sesion2_Izan/Sesion2_Izan.kicad_pro` | Ajustes de BOM (heredado), designadores, reglas, net classes, tamaños predefinidos |
| `Sesion2_Izan/Sesion2_Izan.kicad_dru` | **Nuevo:** regla pista‑pista 0,25 mm |
| `Sesion2_Izan/Sesion2_Izan.kicad_pcb` | **PCB completo** (antes vacío) |
| `Sesion2_Izan/Sesion2_Izan_BOM.csv` | BOM actualizada |
| `S3_validation/` | **Nuevo:** `ERC_report.rpt/.json`, `DRC_report.rpt/.json`, `board_stats.txt`, `audit_geometry.txt`, `README.md`, `.gitignore` (solo `__pycache__`), `.gitattributes` (los `.sh` con LF, para que `regenerate.sh` funcione tras un checkout en Windows), `renders/` (3 vistas 3D + 4 vistas de capas), `generator/` (11 scripts) y `review/ADVERSARIAL_REVIEW.md` |
| `S3_AUTONOMOUS_REPORT.md` | **Nuevo:** este informe |

Sin ficheros temporales versionados: no hay `.lck`, `.kicad_prl`, `.history`, backups ni `__pycache__`. El `.kicad_prl` y la carpeta `.history` de Izan siguen en el disco, ignorados por git y sin tocar.

---

## 24. Git

**Commits** en `sesion3-pcb`, sobre `main` = `9509303` (baseline S2):

| # | Hash | Mensaje | Contenido |
|---|---|---|---|
| 1 | `e417981` | S3: carry over pending KiCad edits found uncommitted on main | Los 3 cambios de Izan que estaban sin commit en main (§2), sin modificar |
| 2 | `a17f5f1` | S3: add MCU decoupling and power test points | C302, C303, TP201–TP203, designadores, BOM y `S3_validation/ERC_report.*` |
| 3 | `68b1507` | S3: implement PCB layout and routing | `.kicad_pcb` completo; `.kicad_pro` con reglas, tamaños y net classes; `.kicad_dru` nuevo |
| 4 | `d7420ed` | S3: validate DRC and finalize PCB | `S3_validation/` completa (ERC/DRC regenerados al final) y este informe |
| 5 | (ver resumen final) | S3: record final git audit in report | Solo este apartado, con la salida de la auditoría final |

Un commit no puede llevar su propio hash, así que el del commit 5 está en el resumen final del chat y en `git log`.

**Push:** **BLOQUEADO.**
- Se intentó `git push -u origin sesion3-pcb` tras el commit de layout y de nuevo tras los de validación y auditoría.
- Respuesta: `remote: Permission to Public-University-of-Navarra/Sesion2_Izan.git denied to IzanVoltis.` → `403`.
- `origin/main` no se ha tocado; ningún push llegó al servidor.

**Copias de seguridad locales** (no publicadas): `stash@{0}` (`96d71b6…`) y la etiqueta `S2_FINAL_BASELINE` → `9509303`.

**Auditoría final.** Ejecutada después del commit 4 (`d7420ed`). El commit 5 solo añade este apartado.

`git status`:
```
On branch sesion3-pcb
nothing to commit, working tree clean
```

`git log --oneline --decorate -10`:
```
d7420ed (HEAD -> sesion3-pcb) S3: validate DRC and finalize PCB
68b1507 S3: implement PCB layout and routing
a17f5f1 S3: add MCU decoupling and power test points
e417981 S3: carry over pending KiCad edits found uncommitted on main
9509303 (tag: S2_FINAL_BASELINE, origin/microcontrolador, origin/main, origin/HEAD, microcontrolador, main) Complete microcontroller schematic and BOM
d26830f (origin/alimentacion, alimentacion) Complete power supply schematic
778da5e Create KiCad project hierarchy
1201375 Initial commit
```

`git diff main...HEAD --stat`: 36 ficheros, 10 047 inserciones y 13 borrados. Son exactamente los de §23: 5 ficheros del proyecto KiCad modificados, `Sesion2_Izan.kicad_dru` nuevo, la BOM, los 28 ficheros de `S3_validation/` y este informe.

| Comprobación | Resultado |
|---|---|
| Rama activa ≠ main | ✅ `sesion3-pcb` |
| main sigue en el baseline | ✅ `main` = `95093034…` |
| origin/main no modificado | ✅ `origin/main` = `95093034…`. `git ls-remote origin` da `refs/heads/main` = `95093034…` en el servidor |
| Rama S3 subida | ❌ **BLOQUEADO** (403). `git ls-remote` solo muestra `main`, `alimentacion` y `microcontrolador` |
| Temporales versionados | ✅ ninguno: ni `.lck`, ni `.kicad_prl`, ni `.history`, ni backups, ni `__pycache__`, ni `fp-info-cache` |
| Informe final | ✅ `S3_AUTONOMOUS_REPORT.md` en la raíz del repo |
| KiCad abre y valida los ficheros | ✅ sobre los ficheros versionados: ERC 0 errores / 0 avisos; DRC 0 / 0 / 0 con y sin relleno de zonas; `regenerate.sh` reconstruye la placa desde el esquema fuera del repo y sale `GEOMETRY IDENTICAL` |

---

## 25. Decisiones no impuestas por el profesor

1. Rama `sesion3-pcb`. El profesor no dio nombre.
2. Commit aparte (`e417981`) para los cambios del usuario que estaban sin commit.
3. MPN de C303: Samsung CL21B475KAFNNNE (X7R, mismo fabricante que el 100 nF).
4. Tres test points (VIN, 3V3, GND), Keystone 5000/5001/5003 THT con colores distintos. Su ubicación.
5. Interpretación de "Track Distance 0,25" como regla pista‑pista, manteniendo 0,20 como mínimo general.
6. Anchos 0,25 / 0,6 / 1,3, vías 0,6/0,3 y 0,8/0,4, prioridades de clase y patrones.
7. Mantener los valores por defecto de KiCad en el resto de restricciones.
8. Stackup: núcleo 1,51 mm, total 1,6 mm, εr/tan δ por defecto, máscara 0,01 mm.
9. Tamaño y forma de la placa: rectángulo de 39,00 × 26,70 mm sin redondear esquinas. Sin agujeros de montaje, porque no hay caja definida.
10. Todo el placement y el ruteo, giros incluidos. NRST en B.Cu.
11. Pours GND en ambas caras: separación 0,3, alivios 0,3/0,4, sin pour de VCC.
12. Serigrafía:
    - Texto de 0,8 mm con trazo de 0,15 mm.
    - Todas las referencias en horizontal; las de los filtros, escalonadas en dos filas. Solo los nombres de pin de J302 van en vertical, por falta de sitio.
    - Nombres de pin de J301 (`3V3 A1 A2 A3 OUT GND`) y de J302.
    - Polaridad de J101 (`1:VIN 2:GND`).
    - Texto de identificación ("DEE Sesion 3 · Izan · Rev A · 2026‑10 UPNA") y title block del PCB.
    - Criterios medidos: ninguna leyenda a < 0,15 mm de una apertura de máscara ni a < 0,2 mm de otra leyenda.
13. Hacer crecer la placa para poner los nombres de pin de J301 y separar las leyendas.
14. No hacer teardrops ni merge a main.
15. Aplicar las correcciones de las revisiones independientes (revisiones 2, 3 y 4), documentar el resto y decidir los compromisos en los que los revisores no coincidían (§22). Por ejemplo, la posición de la vía GND del LDO: separar la serigrafía o acortar el retorno.

---

## 26. Riesgos / deuda técnica

1. **Estabilidad del LD1117 con cerámicos a la salida.** El LD1117 es un diseño NPN antiguo que pide COUT ≥ 10 µF; según el foro de ST, también ESR ≥ 0,3 Ω. C202 (tántalo, ESR ≤ 1,8 Ω) lo cubre. Pero C303 (4,7 µF X7R, exigido por ST para el MCU) y C302 están en paralelo en la misma red 3V3 y bajan la ESR equivalente a alta frecuencia. Es la configuración habitual en muchas placas STM32 con reguladores x1117, pero **no está demostrado con datos del fabricante**.
   - Mitigación: medir con osciloscopio en TP202 en el prototipo.
   - Plan B: sustituir C303 por un 4,7 µF de tántalo o polímero, o poner 1 Ω en serie. Ninguna de las dos se hizo, porque contradice la recomendación "ceramic" de ST y no hay evidencia de problema.
2. **Corte del plano B.Cu por NRST** (11 mm bajo el MCU). Es una señal lenta y nadie cruza el corte, pero rompe la continuidad del plano bajo el chip.
3. **Térmica del LD1117.** No hay área de cobre 3V3 extra en el tab. P = (VIN − 3,3)·I. Con poca carga es despreciable, pero 3V3 sale por J301 y J302 hacia cargas desconocidas. VIN no está definido en el proyecto (rango del LD1117S33: 4,75–15 V). Con ≳50 mA y VIN alto, conviene reconsiderarlo.
4. **Cuellos de GND** de 0,5 mm (C302 → VSS) y 0,4 mm (VSS → vía), y tramos de 1,0 mm en C501/C601, por debajo del ancho de la clase GND (§15). Son justificados, pero un profesor estricto podría señalarlo.
5. **Teardrops sin hacer** (§28).
6. **Edición textual del esquema y generación del PCB por API.** Están validadas con kicad-cli (mismo parser y DRC que la GUI), pero **no se han abierto en la GUI** en esta sesión.
7. **OUT1** (salida digital) va por la zona analógica, a ~1,2 mm del filtro AIN3, porque comparte conector con las AIN (decisión de S2).
8. **Datasheets desde copias** (Rev 3 del DS12991 y Rev 19 del LD1117), porque st.com no respondía. Conviene contrastar con la última revisión.
9. **Serigrafía con compromisos de espacio:**
    - nombres de pin de J302 en vertical (el profesor prefiere el texto horizontal);
    - `C302` bajo C302, en zona densa: 0,31 mm de su pad, 0,21 mm de U301.6/7 y 0,25 mm de C301.1;
    - `1:VIN 2:GND` cruza la pista VIN de TP201;
    - el contorno de J301 pasa sobre el taladro de la vía (25,25; 21,85), y el fabricante recortará ahí la línea;
    - varias referencias van sobre pistas de señal tapadas por máscara.

    Todo es cosmético y el DRC no da avisos.
10. **C303 sin GND propio junto a VSS.** Su GND vuelve por la vía (20,75; 3,5) y el plano B.Cu: 5,72 mm de hueco de cobre a VSS. C302, que es el de alta frecuencia, sí está pegado a VDD/VSS. Para el condensador de reserva el impacto es pequeño.
11. **C401 a 9,4 mm de PA0.** El filtro AIN1 cumple su función (fc ≈ 1 kHz). Acercar C401 deja su pad GND en un canal cerrado y obliga a otra vía.
12. **Sin protección contra inversión de polaridad en J101.** Solo está la leyenda `1:VIN 2:GND`. Añadir un diodo o un MOSFET es un cambio de esquema que queda fuera de S3.
13. **F.Cu fragmentado** por el ruteo a una cara (§19). La referencia continua es B.Cu, cortado solo por NRST.
14. Los test points no tienen modelo 3D en la librería de KiCad 10, así que no aparecen en el render 3D. Los cajetines del esquema siguen vacíos desde S2.
15. **KiCad abierto con el proyecto anterior a S3.** En el equipo hay un `kicad.exe` abierto desde el 17/09, con `Sesion2_Izan.kicad_pro` en `open_projects`. No lo he cerrado: es la aplicación del usuario y podría tener trabajo sin guardar. Si se sigue usando esa ventana sin reabrir el proyecto, KiCad podría guardar encima los ajustes antiguos (sin reglas ni net classes de S3). Ver §27.2.

---

## 27. Qué debe comprobar Izan mañana

1. **Subir la rama.** Abrir el repo en GitHub Desktop con la cuenta de la UPNA y publicar `sesion3-pcb`, o `git push -u origin sesion3-pcb` con credenciales de esa cuenta. No hacer merge a main todavía.
2. **Antes de abrir nada, cerrar del todo el KiCad que sigue abierto** (proceso `kicad.exe` iniciado el 17/09). Según `%APPDATA%/kicad/10.0/kicad.json`, tiene `Sesion2_Izan.kicad_pro` como proyecto abierto desde antes de S3. Si se abre el PCB desde esa ventana, KiCad puede usar los ajustes antiguos del proyecto que tiene en memoria y, al guardar, sobrescribir las reglas y net classes del `.kicad_pro`. Después, abrir el proyecto de nuevo en **KiCad 10 GUI**. En el esquema: ver C302/C303 y TP201–TP203, guardar (KiCad puede reformatear algo) y pasar el ERC. Debe salir 0.
3. En el PCB: **Board Setup** → Physical Stackup (2 capas, FR4, 0,035), Constraints (0,2 / 0,25), Custom Rules (la regla 0,25) y Net Classes (GND/POWER/SIGNAL con sus patrones).
4. **F8 (Update PCB from Schematic)**: debe decir que no hay cambios. Si propone cambios, avisarme o anotarlo.
5. **B** (rellenar zonas) y **DRC** con "rellenar zonas" y "paridad": 0 errores, 0 sin conectar.
6. **Teardrops:** Edit › Edit Teardrops en pads y vías, luego B y DRC de nuevo, y commit si todo sigue limpio.
7. Ver en **3D (Alt+3)** la orientación de J101 y que nada se sale.
8. Repasar el razonamiento de la vía de NRST (§18) y el riesgo del LD1117 (§26.1), para poder defenderlos.
9. Confirmar con el profesor si quiere el merge a main para entregar. ExplAIn lo describe en el flujo, pero no lo exige.
10. Cuando ya no haga falta, borrar el stash de backup (`git stash drop stash@{0}`) y, si se quiere, la etiqueta local `S2_FINAL_BASELINE`.

---

## 28. Qué NO se pudo completar

- **Push de `sesion3-pcb` a origin: BLOQUEADO.** Error 403 con la cuenta `IzanVoltis`, la única configurada en Git Credential Manager y en `gh` en este equipo. La cuenta de la UPNA parece estar solo en GitHub Desktop. No modifiqué credenciales ni usé tokens ajenos.
- **Teardrops: REQUIERE REVISIÓN HUMANA (GUI).** Probé a activar los teardrops en pads y vías con la API y a rellenar zonas por API y por CLI. No se genera ninguna forma: KiCad 10 no tiene comando CLI ni API Python para "Edit Teardrops". No aparecen en la enumeración de la tarea (ExplAIn §12: exigencia dudosa), pero el profesor los mencionó como paso final.
- **Verificación en la GUI de KiCad: REQUIERE REVISIÓN HUMANA.** Esta sesión no puede manejar ventanas: el KiCad abierto en el equipo no se tocó (§26.15). Todo se validó con kicad-cli 10.0.6 y con la API Python de KiCad.
- No hay agujeros de montaje, porque no se definió caja. No es un requisito.
