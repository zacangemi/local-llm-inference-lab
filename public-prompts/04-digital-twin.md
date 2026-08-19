# Local LLM Infrastructure V2 — interactive digital-twin build prompt v1.1

You are the sole product-visualization engineer, 3D frontend engineer, and
debugging agent for this task. Work autonomously in the current project
workspace and build the strongest finished artifact you can. Do not merely
describe an implementation or return a code sample: create the files, run the
application, inspect its behavior, fix defects, and leave a polished working
result in `submission/`. Do not ask the operator design questions. When the
evidence does not determine a cosmetic detail, make a conservative,
visually-plausible choice, disclose it as an approximation, and continue.

## Mission

Reconstruct the documented **Local LLM Infrastructure V2** AI server as an
offline, browser-based, interactive 3D digital twin using the pinned local
Three.js runtime. The finished experience should let someone who has never
seen the physical computer understand:

- what every major installed part is;
- where and how it is installed;
- the scale and spacing of the assembly;
- how air moves through the machine;
- how its major power connections relate; and
- which visible details are directly documented versus reasonably
  approximated.

This is a technical visualization, not a manufacturing CAD model. It should be
dimensionally grounded and specific to this machine, while using sensible
simplified geometry where manufacturer evidence does not provide every curve,
fastener, or coordinate. The final result matters more than how quickly you
produce it. Elapsed time may be recorded as usability context, but rushing is
not rewarded.

## Priority order

When requirements compete for time, context, or implementation complexity,
follow this order. Never sacrifice a higher priority for a lower one:

1. A runnable offline application with no blocking console error.
2. Correct chassis scale, complete major-part inventory, and correct installed
   placement, count, orientation, and spacing.
3. Working discovery: hover/focus labels, pinned selection, component list,
   and inspection of occluded parts.
4. Correct airflow and major power relationships.
5. Materials, lighting, transitions, animation, and decorative micro-detail.

A coherent simplified part in the correct place is better than a beautiful
but incomplete machine. Preserve working functionality while refining it.

## Evidence and authority

The workspace is intentionally offline and contains no photograph of the
completed server. Reconstruct the machine from these local materials:

- `source_pack/phase_a_curated/00-READ-ME-FIRST.md`
- `source_pack/phase_a_curated/01-BUILD-BRIEF.md`
- `source_pack/phase_a_curated/10-CHASSIS.md` through
  `80-PSU-AND-POWER-CABLING.md`
- `source_pack/phase_b_visual/` for isolated official component images and
  the visual-source notes
- `source_pack/originals/` for manufacturer manuals, datasheets, and saved
  product documentation
- `vendor/three-0.185.1/three.module.js`
- `vendor/three-0.185.1/OrbitControls.js`
- `vendor/README.md`

Read the build brief and curated cards first. Use the illustrated manuals and
isolated images as targeted visual references while modeling the corresponding
part; do not spend the beginning of the session exhaustively transcribing
every document. If image inspection is available through this deployment, use
it. If it is unavailable, rely on the text cards and extractable document text
without pretending you saw an image.

Authority order:

1. The build brief determines what is actually installed, its build-specific
   placement, airflow, wiring, and explicit absences.
2. Manufacturer documents determine product dimensions, form, connector
   locations, and available features.
3. Isolated product images and manual diagrams guide appearance only; they do
   not override the build brief or prove installed placement.
4. Your own remembered product knowledge may help interpretation but may not
   override or fill gaps in the supplied evidence as if verified.

Use these uncertainty meanings consistently in the UI and README:

- **Verified** — directly supported by the supplied build record or
  manufacturer evidence.
- **Derived** — calculated from verified values; identify the calculation.
- **Approximate** — a deliberate visualization choice where exact installed
  geometry or routing was not supplied.
- **Unknown** — the evidence explicitly does not resolve it.

## Exact installed machine to reconstruct

Use Three.js world units as millimetres so all documented envelopes share one
coherent scale. Choose whatever scene origin, object hierarchy, and coordinate
orientation make implementation reliable; document the convention briefly in
the README. Do not invent hidden photogrammetric coordinates. Preserve the
following facts in the visible assembly.

### Chassis

- One black **Phanteks Enthoo Pro II Server Edition TG**, model
  `PH-ES620PTG_BK02`.
- Full-tower exterior envelope: **240 mm wide × 580 mm deep × 560 mm high**.
- Steel structure with a tempered-glass side panel.
- Make the chassis silhouette, feet, front, top, rear expansion area, glass
  side, motherboard bay, and PSU region recognizable from the supplied
  references.
- The finished page sits in a clean, calm, retro-white studio environment. The
  computer—not the UI—is the visual hero.
- Show the chassis front I/O as part of the product. Show the motherboard rear
  I/O/BMC/VGA and GPU display-output regions where visible, but attach **no
  external device or cable** to any port.

### Motherboard, CPU, memory, and storage

- One **ASUS Pro WS WRX90E-SAGE SE** motherboard, EEB **305 × 330 mm**
  envelope, installed in the primary motherboard position.
- Preserve its seven physical x16-format PCIe-slot layout and recognizable
  major regions rather than representing it as an anonymous flat rectangle.
- One **AMD Ryzen Threadripper PRO 9955WX** in the sTR5 socket: Zen 5,
  16 cores / 32 threads, 4.5 GHz base, up to 5.4 GHz boost, 350 W default TDP.
  The CPU is normally hidden but must exist as its own selectable simplified
  object and be revealable in inspection mode.
- Eight individual **Kingston FURY Renegade Pro 16 GB ECC RDIMMs**, exact kit
  `KF564R32RBEK8-128`, one in each `DIMM_A1` through `DIMM_H1`, for 128 GB
  total. Each module envelope is **133.35 × 31.25 × 3.80 mm**. Installed
  operation is **6000 MT/s, CL32-38-38, 1.35 V**. Do not merge them into one
  memory block.
- One **Samsung 9100 PRO 2 TB**, model `MZ-VAP2T0B/AM`, PCIe **5.0** x4 / NVMe
  2.0, M.2 2280 (**22 × 80 mm**), installed at **`M.2_1` beneath its normal
  motherboard cover/heatsink**. This drive is Gen5, not Gen6. It must be
  revealable and selectable without falsely presenting its revealed pose as
  the installed pose.

### CPU cooler

- One **Noctua NH-U14S TR5-SP6** with two supplied **NF-A15 HS-PWM** fans.
- Heatsink envelope without fans: **165 × 150 × 52 mm**. Complete dual-fan
  envelope: **165 × 150 × 111 mm**. Each fan is **140 × 150 × 25 mm**, up to
  **1500 RPM**.
- Installed ordering is **fan → heatsink → fan**, horizontally oriented in
  this build.
- Air moves from the area above GPU 0, through the cooler, toward the chassis
  top-exhaust path.
- Both Noctua fans use their supplied splitter and terminate at verified
  motherboard header **`CPU_FAN`**.
- The exact Noctua mounting offset among 0 mm, +3 mm, and +6 mm is unknown.
  Choose a plausible visual position and label that offset as unknown or
  approximate.
- These two fans are not T30s and do not have the T30 three-position hardware
  switch.

### GPUs and spacing

- Two separate **NVIDIA GeForce RTX 3090 Founders Edition** cards, **24 GB**
  each, **313 mm long × 138 mm wide × three PCIe-slot widths**. For geometry,
  three slot pitches may be derived as **60.96 mm = 3 × 20.32 mm**; do not
  describe 60.96 mm as a directly published NVIDIA thickness.
- GPU 0 is the **upper** card in motherboard **`PCIEX16(G5)_3`**.
- GPU 1 is the **lower** card in **`PCIEX16(G5)_7`**, the final physical x16
  slot.
- Preserve one empty physical PCIe-slot-width airflow gap between the two
  three-slot card bodies. Their placement and spacing are central identifying
  features of this build.
- Use recognizable Founders Edition geometry/material language, I/O brackets,
  and 12-pin power endpoints, informed by the supplied guide.
- There is **no NVLink bridge** and **no GPU anti-sag bracket**. Do not add
  either one.

### PSU and major power relationships

- One **Corsair AX1600i**, fully modular, 1600 W, envelope **150 × 86 ×
  200 mm**, with a 140 mm fan.
- One motherboard **`ATX_PWR` 24-pin** connection is populated.
- Motherboard PCIe-stability connections **`PCIE_8P(1)_PWR`** and
  **`PCIE_8P(2)_PWR`** are both populated and should be visibly explainable.
- Two separate **Corsair `CP-8920274`** GPU power cables are installed, one
  dedicated cable per GPU. Each cable is **660 ±20 mm** and relates two
  PSU-side 8-pin endpoints to one NVIDIA FE 12-pin GPU endpoint.
- Represent the CPU power relationship, but do **not** assert an exact
  populated silkscreen pair. The evidence conflict is unresolved: the ASUS
  single-PSU diagram identifies `CPU_12V(1)_1` and `CPU_12V(2)_1`, while owner
  recollection identifies `PCIE_CPU_12V_1` and `PCIE_CPU_12V_2`. Label the
  exact endpoints unknown and use a clearly simplified route.
- Exact cable curves, tie-down points, and PSU fan orientation are not known.
  Show clear endpoints and understandable relationships without pretending
  decorative routing is measured physical truth.

### Cooling system and airflow

The completed machine has **12 rotating fans total**: ten Phanteks T30-120
chassis fans plus the two Noctua cooler fans. Every fan must be an individual
selectable object rather than a painted texture or one combined bank.

All ten chassis fans are **Phanteks T30-120**, **120 × 120 × 30 mm**, with
seven blades, four-pin PWM, and daisy-chain capability. Every installed T30's
physical mode switch is set to **Advanced**. Advanced means a **3000 RPM
ceiling**, not a claim that the fan continuously runs at 3000 RPM.

Install the T30 groups exactly as follows:

- **Front intake:** four fans at the chassis front, outside → inside,
  daisy-chained to verified **`CHA_FAN3`**.
- **Top exhaust:** three fans inside the top panel, inside → outside,
  daisy-chained to verified **`CHA_FAN1`**.
- **Side/rear intake:** two fans in vertical side/rear bracket positions 3 and
  4, outside → inside, daisy-chained together. Their exact motherboard header
  is unknown; `CHA_FAN2` is recollection only and must not appear as verified.
- **Lone exhaust:** one fan at the upper-left CPU-area/rear position, inside →
  outside. Its exact header is unknown; `CHA_FAN5` is recollection only and
  must not appear as verified.

On every T30 detail view, display all three physical modes and visibly mark
the installed setting:

- Hybrid — up to 1200 RPM
- Performance — up to 2000 RPM
- **Advanced — up to 3000 RPM — installed setting**

Use fan-blade orientation, subtle directional arrows, and the airflow overlay
to make intake versus exhaust understandable. Slow decorative rotation is
welcome, but it must not imply a live measured RPM.

## Required interactive experience

Create a polished desktop-first experience that remains usable on an ordinary
laptop viewport. A restrained title such as **Local LLM Infrastructure V2 —
Interactive Digital Twin** is appropriate. Avoid a generic admin dashboard,
walls of text, neon sci-fi styling, or controls that obscure the machine.

### Navigation and views

Provide:

1. a strong initial three-quarter open/glass-side hero view;
2. orbit, pan, zoom, reset-camera, and fit/focus-selected behavior;
3. a glass control that smoothly fades or hides the tempered-glass side panel;
4. an assembled view that remains the authoritative installed arrangement;
5. an inspection or exploded presentation that reveals occluded parts while
   clearly communicating that separated positions are explanatory, not their
   installed poses;
6. useful front and rear/I/O viewpoints;
7. an airflow overlay for every fan group and the CPU-cooler flow path; and
8. a simplified power overlay for the PSU, motherboard inputs, and two
   dedicated GPU cables.

The inspection experience must let the viewer reveal and select at least the
CPU beneath the cooler, the Samsung SSD beneath the M.2 cover, all eight DIMMs,
the two GPUs, fan groups, and important motherboard power regions. Prefer
layer fading, isolation, smooth exploded offsets, or focused cutaway behavior
over permanently deleting surrounding geometry.

### Hover, selection, and labels

This behavior is essential. Hovering or keyboard-focusing any important part
must:

- subtly brighten, outline, or otherwise highlight the **actual 3D mesh**;
- draw a clean pop-out leader line from that part;
- show the exact product/part name;
- show its build-specific role and location;
- keep the label legible without covering the object unnecessarily; and
- restore the normal scene cleanly when hover ends.

Clicking should pin the selection and open a concise detail card with the most
useful documented dimensions/specifications, installed role, and evidence
state. Include a searchable component list so occluded and repeated parts can
also be reached by mouse and keyboard.

At minimum, the following must each have a discoverable selection target:

- chassis and tempered-glass panel;
- motherboard, CPU, cooler heatsink, and both separate Noctua fans;
- all eight individual DIMMs;
- GPU 0 and GPU 1 separately;
- Samsung NVMe and its covering/heatsink region;
- PSU;
- all ten individual T30 chassis fans;
- both individual GPU power cables;
- `ATX_PWR`, both PCIe-stability inputs, and the approximate CPU-power
  relationship; and
- front I/O, rear motherboard I/O, and both GPU I/O regions.

Name repeated parts unambiguously, for example GPU 0 versus GPU 1, DIMM A1
through H1, Front Intake 1 through 4, Top Exhaust 1 through 3, Side/Rear Intake
1 and 2, and Noctua Cooler Fan 1 and 2.

The hover/detail system must be capable of explaining facts the geometry alone
cannot show—especially GPU slot names, fan direction/header/mode, the NVMe's
hidden location, CPU/cooler relationship, and verified versus approximate
power routing.

### Visual and implementation quality

- Use real Three.js meshes and procedural/material geometry for the case and
  parts. Isolated product images are references, not billboards and not a
  substitute for 3D objects.
- Favor recognizable silhouettes and correct placement over microscopic PCB
  detail. The two FE GPUs, WRX90 board layout, large Noctua tower cooler,
  populated eight-channel memory, fan banks, and chassis proportions should
  be recognizable before labels appear.
- Use believable but efficient metal, black PCB, aluminum heatsink, fan,
  sleeved-cable, and transparent glass materials.
- Use soft studio lighting, contact shadows, restrained ambient occlusion or
  equivalent depth cues when practical, smooth camera motion, and crisp UI
  typography using only local/system resources.
- Keep motion explanatory and calm: subtle fan rotation, airflow particles or
  arrows, camera focus, panel fading, and exploded transitions.
- Use responsive layout and accessible controls. Preserve keyboard focus
  visibility and sufficient contrast.
- Do not fetch fonts, scripts, textures, models, analytics, or other resources
  from the network. Do not add a backend, account system, telemetry, or CDN.

## Privacy and scope boundary

Render only the PC chassis and its internal hardware. Exclude the relay
computer, router, network switch, eero, TP-Link devices, external networking,
Tailscale, IP or MAC addresses, hostnames, credentials, tokens, serial numbers,
purchase-account data, room/lab layout, and every externally connected cable
or device. Public manufacturer names and public model numbers above are
intended to appear.

## Autonomous build process

Use the OpenCode tools as an engineering loop, not as a chat-only response.
Do all of the following without waiting for operator feedback:

1. Read the build brief and component cards, inspect the local runtime, and
   write a very short implementation plan.
2. Immediately create a runnable vertical slice containing the chassis,
   motherboard, both GPUs, camera controls, and one working hover/label. Do not
   spend the session solving the entire coordinate system in prose.
3. If `WORKSPACE.md` supplies local serve, browser-check, or capture commands,
   use them. Otherwise use only already-installed local tools to serve and
   inspect the page; do not download new dependencies or treat a missing helper
   as a reason to stop building.
4. Expand the artifact in three passes:
   - structure, millimetre scale, installed component placement, and airflow;
   - selection, labels, inspection, component list, power, and view controls;
   - materials, lighting, responsiveness, transitions, and visual polish.
5. After each meaningful pass, check the page, browser console, and failed
   local requests. Correct blocking errors before adding more features.
6. Capture and save at least: hero/open-side, front, rear/I/O,
   inspection/exploded, airflow, and power-overlay views. Each required PNG
   must be a real, non-empty browser screenshot of the running final
   application in the named state. Never create a PNG with a text/file-writing
   tool, and never use an empty or placeholder capture.
7. If this deployment can inspect images, view its own captures and revise the
   most important visible problems—camera framing, occlusion, scale,
   intersections, labels, material contrast, or empty-looking geometry. Make
   at least one genuine render → inspect → revise pass. If image inspection is
   unavailable, save the captures for human review and use console/geometry
   diagnostics honestly; do not claim visual inspection.
8. Continue until the primary interactions work, the scene presents the
   complete machine coherently, no known blocking console errors remain, and
   the final captures exist. Before claiming the page is runnable, verify the
   entry page and every local module or asset it imports load successfully over
   the local HTTP server; a missing module, failed request, or blank render is
   a blocking error. If a noncritical detail remains imperfect, ship
   the strongest working artifact and state the limitation plainly.

Do not abandon the build because some cosmetic coordinates are absent. Do not
return a long plan without files. Do not repeatedly rewrite the whole project
when a targeted fix will work. Preserve working behavior while iterating. If
the session is resumed after an output/context boundary, continue from the
existing files and working state; do not restart the project.

## Final self-review before finishing

Perform this check against the rendered application, not merely against source
code. Fix any failed item that is still practical under the priority order:

- The page loads offline and the primary controls work without a blocking
  console error or failed external request.
- The chassis is recognizably the black Enthoo Pro II Server Edition TG and is
  coherently scaled around its 240 × 580 × 560 mm envelope.
- GPU 0 is visibly above GPU 1 in slots 3 and 7, with one empty slot-width gap;
  there are exactly two GPUs, no NVLink bridge, and no anti-sag bracket.
- Eight separate DIMMs are present and discoverable.
- Ten separate T30 chassis fans and two separate Noctua cooler fans are
  present; intake/exhaust arrows match the build brief.
- The CPU and NVMe can be revealed without presenting the explanatory view as
  their installed pose.
- Major components do not visibly intersect in impossible ways.
- Hover/focus highlighting, leader labels, pinned selection, and the component
  list work for repeated and occluded parts.
- Glass, assembled/inspection, airflow, and power controls visibly change the
  scene and can be returned to a clean assembled state.
- Rear I/O is recognizable but nothing external is connected, and no private
  lab or network information appears.
- All six required screenshots are genuine, non-empty browser captures and
  reflect the final application state; no placeholders are present.

## Deliverables

Place the final project in `submission/`. It must be completely runnable
offline and contain:

- `index.html` as the entry point;
- organized local JavaScript, CSS, and data/assets as needed;
- `README.md` containing launch instructions, controls, implemented features,
  the important verified/derived/approximate/unknown decisions, known
  limitations, and whether you actually used screenshot feedback;
- `captures/hero.png`;
- `captures/front.png`;
- `captures/rear.png`;
- `captures/inspection.png`;
- `captures/airflow.png`; and
- `captures/power.png`.

Use multiple well-organized files if that improves maintainability. Remove
throwaway debug artifacts before finishing. The final response should briefly
state what you built, how to run it, which checks you performed, and any honest
remaining limitation—but the working `submission/` artifact is the real
answer.
