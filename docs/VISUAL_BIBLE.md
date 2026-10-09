# Lost Vanguard visual bible — working draft

2026-10-07. Scope: human spacecraft and related hull debris. Forest and other factions remain open. This records current production choices, not a final ship specification.

## User-selected direction

- Human ship palette: gray armor with military olive-green markings as depicted in accepted concept A4. Exact material values remain open.
- Concept A is the preferred starting point, particularly its long, narrow silhouette.
- Ship weapons should read as compact, distinct turrets that can turn, following accepted concept A4. Concept artwork is the visual guide; final 3D articulation and exact specifications remain open.
- A4 is the accepted visual reference for the type of human ship that crashes in the opening; its construction should guide exterior hull debris.
- User withdraws the tentative central MAC-weapon idea; it is not a requirement. Specific weapon types and final ship specifications remain open.

## Reference state

A4 is accepted as the crashed ship type's visual reference, combining A's long narrow silhouette with olive-green markings and compact turrets. Earlier A/A2/A3/B images are preserved as exploration history; A2's brighter-blue palette is superseded. Interior architecture/materials remain open and need a separate reference before accepting interior debris designs.

- [A](../assets/concepts/human_ships/human_ship_a_angular_industrial_v1.png)
- [A2](../assets/concepts/human_ships/human_ship_a2_brighter_blue_v1.png)
- [B](../assets/concepts/human_ships/human_ship_b_modular_armored_v1.png)
- [A3](../assets/concepts/human_ships/human_ship_a3_military_green_turrets_v1.png)
- [A4](../assets/concepts/human_ships/human_ship_a4_compact_turrets_v1.png)
- [Full generation prompts and review notes](HUMAN_SHIP_VISUAL_EXPLORATION.md)

## Proposed asset rules — awaiting review

Current transport baseline: user prefers T1's original bulky detailed hull/cockpit and rejects T4's drift. Restore that body, then add wings with sufficient span. T2/T3/T4 geometry is superseded; their narrower hull should not guide later work. [T5](../assets/concepts/transports/transport_t5_original_hull_wings_v1.png) is the restored-body review candidate, not a final approved design. Preserve original panel depth and cockpit glazing when refining flight assemblies.

Latest transport refinement: user requests smaller, straighter wings than T3 and a second angle beside the top view. [T4](../assets/concepts/transports/transport_t4_compact_wings_two_views_v1.png) is the current two-view review candidate. Preserve compact wing direction in subsequent proposals; exact shape, span, view agreement and 3D geometry remain unapproved.

Current transport requirement: wings with integrated boosters replace the four separate-pod direction. [T3](../assets/concepts/transports/transport_t3_wings_integrated_engines_v1.png) is the new centered top-view review candidate. Exact wing silhouette/span, engine count and production geometry remain proposals. Earlier T1/T2 versions are historical explorations, not the current intended configuration.

Transport review: T1 is rejected for uneven boosters and other image problems. [T2](../assets/concepts/transports/transport_t2_centered_top_v1.png) is the requested centered top-down intact redraw, with paired pods; awaiting review. Develop broken transport parts only after resolving the intact design. Neither image is a validated blueprint or an accepted propulsion specification.

Shipboard transport: user establishes that the larger ship carries smaller human transports; their wreckage can provide another debris source. [T1](../assets/concepts/transports/transport_t1_shipboard_wreck_v1.png) proposes an original gray/olive utility transport with intact/wrecked/pod views. Specific silhouette, scale, capacity, propulsion and damage arrangement await review. See SHIPBOARD_TRANSPORT_VISUAL_EXPLORATION.md.

Latest bridge review: I4 is accepted as a general idea only; user identifies uneven layout and hologram orientation. Balanced layout/plan is deferred. [D1 debris sheet](../assets/concepts/debris/debris_d1_ship_starter_v1.png) uses A4/I1/I2 materials and construction as a new proposal for exterior panel, interior panel, electrical assembly and control-panel wreckage. See DEBRIS_VISUAL_EXPLORATION.md; no individual debris design accepted yet.

Bridge requirements: user requests seated crew stations, a captain/command area, monitors, forward glass windows and floating displays or a central hologram workspace. Any visible exterior must follow accepted A4. [I4](../assets/concepts/ship_interiors/ship_bridge_i4_crewed_windows_v1.png) is the new review candidate; exact room layout, window/hull geometry, crew appearances and display treatment remain unapproved. The earlier windowless I3 is suggested as a separate work area near a hangar, not the final bridge. Full prompts and limits: CREWED_BRIDGE_VISUAL_EXPLORATION.md.

Bridge panel exploration: [I2](../assets/concepts/ship_interiors/ship_bridge_i2_control_panels_v1.png) proposes freestanding and wall-mounted consoles plus a damaged faceplate. It follows accepted I1 gray/olive construction; console shapes, screen/button treatment, amber UI illumination and bridge arrangement await user review. See BRIDGE_CONTROL_PANEL_EXPLORATION.md for full prompt.

Accepted interior reference: [I1](../assets/concepts/ship_interiors/ship_interior_i1_panel_construction_v1.png). User approves its appearance and asks to save it. Use its removable gray/olive wall panels, dark ribs, cable routing and access boxes as the interior construction direction, distinct from exterior armor. See SHIP_INTERIOR_VISUAL_EXPLORATION.md for the full prompt and three proposed debris briefs; exact prop dimensions and production specifications remain open.

Use gray as the dominant painted armor color and muted military olive green as an identification accent, following the current reference. Prefer thick angular panels, practical seams and reinforcing ribs. Green is paint, not emissive illumination. Turrets should remain compact secondary forms with readable swivel mounts. Match the same neutral-light reference when reviewing generated assets; adjust shared material colors in Blender/Unreal after import. Debris should look like broken pieces of this construction, with localized damage rather than an unrelated material style. Exact material values, accent coverage, weathering, insignia and light colors remain open.

## Reusable prompt style paragraph — draft

Original human military spacecraft construction following Lost Vanguard's working visual direction: gray painted metal armor with muted military olive-green markings. Practical thick panels, believable reinforcing structure and a readable industrial silhouette. Green markings remain non-neon and non-glowing. Match the supplied reference colors and construction language; the individual asset brief specifies its shape and damage. For intact ships, compact weapon turrets read as separate articulated forms.

## Validation before expanding the set

Debris geometry requirement, 2026-10-07: user likes D4 very large engine designs but rejects enormous exposed-room wreckage. These assets keep outer armor attached, with scorch, deformation and localized shallow breaks showing electronics. Avoid rooms, doors, stacked interior decks, catwalks and unseen internal geometry. Use simple backing at breaks/exhausts; reserve geometric detail for visible silhouette and major structure, small wear/seams conveyed in materials. D5 is the revised review candidate. Exact mesh counts remain open; image appearance does not verify optimization. This supersedes prior exposed-deck production suggestions for these exterior wreckage assets, without changing separately accepted interior prop references.

Accepted transport reference, 2026-10-07: use ONLY the left/top image from transport_t9_matched_perspective_v1.png, continuing T8 top-view proportions. User rejects the right perspective because length and design do not agree. Do not use that perspective to infer transport geometry. A standalone generated presentation exists as transport_top_only_presentation_v1.png, but original left view remains authoritative where details differ. Scale, side profile, underside and exact production geometry remain open.

Compare shape language, gray/green balance, materials and detail density to the selected reference. Inspect actual scale, underside, topology and collision independently of concept art. Approve one imported hull panel before making a debris collection. No Meshy generation is submitted by this document.

## Orison nature — accepted 2026-10-08

Plant sheets F1 and F2 (F01-F12) are approved visual concepts. A1 animal selections are A02, A03 and A05. W1 first/top-left panel W01 is retained for a later mission area. References: assets/concepts/flora/orison_flora_f1_six_plants_v1.png; assets/concepts/flora/orison_flora_f2_six_plants_v1.png; assets/concepts/fauna/orison_fauna_a1_six_animals_v1.png; assets/concepts/environments/orison_waterfalls_w1_four_areas_v1.png. Catalogues and prompts: ORISON_FLORA_CONCEPTS.md and ORISON_NATURE_EXPLORATION.md.

Preserve selected silhouettes and plant palette during subsequent references. Naming, dimensions, biology, rigs and game-ready geometry remain open. Base rocks/soil are presentation dressing. Other animals/waterfalls are unselected explorations, not rejected. W01 is deferred to later mission planning; no current map change requested.

## Meridian forces — accepted direction, 2026-10-08

- Starting enemy types selected: scout drone, line robot and alien skirmisher. Specific silhouettes and robot palette remain open; ENEMY_ROSTER.md records proposed combat roles.
- Meridian enslaves members of its creator species and many other species as soldiers. Alien soldiers visibly wear collars and use issued weapons that make their captivity apparent. Exact collar/weapon forms and enforcement functions are undecided.
- Preserve distinct biological silhouettes across species. Shared collar and weapon fittings are a proposed way to link them visually to Meridian's machines, not an approved exact design.
- No enemy concept images or production models exist from this decision. Species anatomy, scale, equipment detail and animation requirements need later selection.

## Enemy visual direction — 2026-10-08

User rejects humanlike E1 robot and alien forms. Explore nonhumanoid machines and multiple distinct enslaved species with varied body plans and sizes; human height is not a constraint. Drone, line robot and alien skirmisher remain selected roles. E2's four species are visual proposals, not established species identities/anatomy or expanded mandatory combat roles. Collars and issued weapons remain accepted captivity cues. See ENEMY_CONCEPTS_E2.md.

## Current enemy direction E3 — 2026-10-08

User rejects all E2 concepts as too extreme and asks for aliens similar in appeal to Halo. Grounded, recognizable alien soldier silhouettes with distinct sizes are the current direction; bipedal forms are allowed, superseding D078's blanket nonhumanoid exploration preference. E1/E2 specific appearances remain rejected. E3 provides four review candidates, not accepted species canon. Collars/issued weapons and selected drone, line robot and skirmisher roles remain; robots need later redesign. See ENEMY_CONCEPTS_E3.md.

## Current enemy appearance direction E4 — 2026-10-08

User finds E3 faces unappealing compared with Halo's alien species. Prioritize creative distinctive faces: unusual eye/jaw structures, head silhouettes and optional masks/headgear. Roughly humanoid bodies are allowed. E4 supplies four portrait/body candidates; no particular face, mask, anatomy, name or equipment function accepted yet. Collars/issued weapons and selected enemy roles remain. E3 preserved as rejected exploration. See ENEMY_CONCEPTS_E4.md.

## Selected enemy designs and Veil-Eye revision — 2026-10-08

User likes E4 B Masked Infantry and C Veil-Eye with changes: replace C rear/top crest, reduce C to approximately 60% of B standing height, give C two eyes. Preserve B four-eyed masked design. Relative size supersedes earlier proposed meter heights; no absolute size selected. E7 proposes a compact ridged crown; exact new crown awaits review. Rendered common-floor lineup is nearer 65-66%, so enforce 60% in later model/blockout. Latest image: assets/concepts/enemies/meridian_e7_masked_infantry_veil_eye_v2.png; details/prompt in ENEMY_CONCEPTS_E7.md. Prior all-pending E4 states are superseded for B and conditional C selection. Species names, creator-species identity and equipment functions remain open.

## Veil-Eye green and feathers — 2026-10-08

User chooses green coloration and feathers for Veil-Eye. Supersedes previous purple skin and hard-ridged scalp proposal; retain two eyes, small adult proportions, mask/collar/issued equipment and 60%-of-Masked-Infantry height target. E8 green feathered crown is current review image; exact shade and plumage arrangement await review. Masked Infantry remains selected E4 B baseline. See ENEMY_CONCEPTS_E8.md and assets/concepts/enemies/meridian_e8_green_feathered_veil_eye_v1.png. Species names, biology and collar mechanisms remain open.

## Veil-Eye legs — 2026-10-08

User likes alien skirmisher-style legs and requests several digitigrade Veil-Eye lower-body options. Preserve current height, green feathered two-eye head and all appearance above waist; vary only below waist. Reference interpreted as E3 skirmisher legs, not its rejected full design. E9 options 1 Lean, 2 Raptor, 3 Power and 4 Armored await choice; no new anatomy or gear variation accepted by generation. Existing 60% relative height production target retained. See ENEMY_CONCEPTS_E9.md.

## Veil-Eye Raptor legs selected; arms/body exploration — 2026-10-08

User selects E9 option 2 Raptor legs and requests arm variants. Body/armor adjustments are authorized to make anatomy natural and cohesive, relaxing previous strict upper-body preservation for this exploration. Retain small stature/60% relative height target, green feathered two-eye identity and mask/captivity cues. E10 Talon, Feathered, Grip and Guard are proposals awaiting selection. E9 Raptor remains selected lower-body reference; E10 Grip thickened legs are unapproved variation. See ENEMY_CONCEPTS_E10.md.

## Raptor arms/legs selected and armed preview — 2026-10-08

User chooses raptor arms and legs for Veil-Eye and requests holding a weapon. Raptor arms interpreted as E10 option 2 Feathered; selected legs remain E9 option 2 Raptor. E11 combines those into a full-body two-handed rifle preview. Green feathers/two eyes/mask/collar/small stature retained; no absolute height or species identity selected. Exact consolidated plume/weapon details await review. See ENEMY_CONCEPTS_E11.md and assets/concepts/enemies/veil_eye_e11_raptor_armed_v1.png.

## Veil-Eye stance exploration — 2026-10-08

User requests a less humanlike stance; alien species need not all stand like humans. Explore forward-pitched raptor carriage, flexed digitigrade legs and extended alert neck while retaining selected anatomy/identity. E12 Stalk, Perch, Bound and Low Aim are unselected pose proposals, not accepted animations or abilities. Actual extended standing height unchanged; crouching changes head elevation. Extra generated back plumage remains unapproved. See ENEMY_CONCEPTS_E12.md.

## Veil-Eye E12 approved — 2026-10-08

User describes E12 stance sheet as cool/perfect. E12 is the accepted appearance/posture reference: green feathered two-eye masked/collared alien, raptor arms/legs, compact issued rifle and forward-pitched animal-like carriage. Pictured plumage/equipment approved as visual direction; exact anatomy/engineering unvalidated. Four shown stances are accepted visual references, but user did not pick one default stance or explicitly select proposed idle/combat mapping. Existing approx60% Masked Infantry extended-height target retained. Beam dressing is not established world content; no traversal abilities or animations implemented. Reference: assets/concepts/enemies/veil_eye_e12_four_raptor_stances_v1.png, ENEMY_CONCEPTS_E12.md. Earlier pending approval notes superseded by this acceptance.

## Enemy fleet ES2 - 2026-10-08
Current requirement: clearly alien futuristic spacecraft with plasma weapons and bottom-mounted beam. ES1 conventional treatment superseded. ES2 candidate: assets/concepts/enemy_ships/meridian_fleet_es2_alien_plasma_v1.png; curved iridescent armor, dark recessed structure, blue charged emitters and ventral warship beam. Palette/exact forms/roles await review. "Glass beam" interpreted as glassing beam, function unconfirmed. Full prompt and inspection: ENEMY_SHIPS_ES2.md.

## Alien troop carrier TC1 - 2026-10-08
Current carrier requirements supersede ES2 carrier: blue/dark gray, less futuristic, different shape, several angles. Candidate assets/concepts/enemy_ships/alien_troop_carrier_tc1_blue_gray_four_views_v1.png proposes enclosed wedge body and twin integrated aft housings with restrained cyan indicators. Four views are visual exploration, not exact blueprint. Exact shape/paneling await acceptance; full prompt/inspection ENEMY_TROOP_CARRIER_TC1.md. Other fleet work deferred.

## Alien troop carrier TC2 - 2026-10-08
TC1 rejected as wrong direction; seek more creative/alien silhouette inspired broadly by Covenant/Halo and Star Wars ship design. Retain blue/dark gray, less excessive futurism, multiple views. TC2 candidate assets/concepts/enemy_ships/alien_troop_carrier_tc2_arch_hull_four_views_v1.png: lower teardrop cabin under arched shoulders and swept outer drives. Exact design unapproved; full prompt/inspection ENEMY_TROOP_CARRIER_TC2.md. TC1 preserved as rejected history.

## Orison orbital appearance direction — 2026-10-08

User finds P4 too Earth-like and requests more creative planet appearance; planet may be lit with a space background. P5 explores teal/violet vegetation, pale geology and unusual continent/inland-sea/island-belt configurations. These are alternatives for one Orison, not additional planets. Exact geography/colors/atmosphere unapproved; dark-only presentation superseded. See ORISON_NATURE_EXPLORATION.md.

## Troop carrier TC3 - 2026-10-08
User rejects TC2. Current shape unselected; TC1/TC2 retained as rejected history. TC3 compares tall keel, broad low hull and twin blade hulls in blue/dark gray: assets/concepts/enemy_ships/alien_troop_carrier_tc3_three_silhouettes_v1.png. All options pending review. Three alternatives replace multi-view repetition temporarily; multi-view requirement resumes after a direction is selected. ENEMY_TROOP_CARRIER_TC3.md holds prompt/inspection.

## Carrier TC4 selected-B refinement - 2026-10-08
TC3 B central hull and lateral opening troop compartments selected; original nose/rear not accepted. Required alien energy boosters bottom/sides instead of rockets. TC4 front/rear proposal assets/concepts/enemy_ships/alien_troop_carrier_tc4_b_refinement_v1.png keeps blue/dark gray and broad bay canopies, adds cheek/chin nose, underside pads and luminous rear slots. Bulky pod housing remains; exact nose/propulsion/door closure pending. ENEMY_TROOP_CARRIER_TC4.md records prompt/limits.

## Carrier TC4 rear approved, view reconciliation pending - 2026-10-08
User describes rear view as really good; use rear hull/energy-booster treatment as selected reference. User flags mismatch with front and wants preferred front/rear combined into one craft. Current sheet is not consistent production blueprint. Preserve accepted rear and B troop-bay middle; reconcile front/side/underside geometry before modeling. Exact front elements remain open; do not promise generated model will resolve ambiguity automatically. D100.

## Human infantry visual direction - 2026-10-08
User requests ordinary soldiers visibly smaller than a Praetorian, wearing basic military science-fiction uniforms with Halo soldiers as a broad inspiration. Exact heights, proportions, palette, helmet, armor and equipment remain open. H1 is a review proposal; no franchise units or equipment become part of Lost Vanguard.

## Carrier TC5 reconciliation candidate - 2026-10-08
Single front three-quarter TC5 is pending review, not replacement of accepted TC4 rear. Shows existing nose/side bay with clearer aft mass/energy glimpse; intake-like forward recess remains, so exact front/rear geometry consistency unresolved. Reference and prompt: ENEMY_TROOP_CARRIER_TC5.md.

## Elite human infantry direction - 2026-10-08
User requests a soldier type somewhat stronger than regular marines with Halo ODST-like appeal, plus other soldier ideas. Exact name, armor, enhancement status and insertion method remain open. Conventional elite infantry between regular troops and Praetorians, H2 armor/loadouts, and specialist roster in HUMAN_SOLDIER_ROLES.md are proposals awaiting review, not established military organization or gameplay mechanics.

## Larger carrier FC1 exploration - 2026-10-08
New large carrier style requested after rejection of earlier big-ship appearance. FC1 straight top view is assistant interpretation of non-angled view, with provisional blue/dark gray continuity. assets/concepts/enemy_ships/alien_fleet_carrier_fc1_top_v1.png shows tapered bow, top-facing hangar-like wells and aft outriggers. Entire shape/class/hangar arrangement awaits acceptance; prior TC4 rear/B middle remain selected separately. ENEMY_FLEET_CARRIER_FC1.md holds prompt/inspection.

## Orison environment reference requirement - 2026-10-08
User explicitly requires reviewing existing planet appearance and relevant local habitat images before making rocks, soil, terrain and other environment asset references. Inspect images visually and supply them as generation references, not only a textual planet name/palette. Accepted opening forest and selected W01 guide local habitat; orbital P5 alternatives support broad appearance without choosing geography. Keep flora dressing separate in production. R1/G1/T1 superseded by current pending R2/G2/T2; see ORISON_GEOLOGY_REFERENCE_REVISION.md. This rule does not accept new generated designs as canon.
