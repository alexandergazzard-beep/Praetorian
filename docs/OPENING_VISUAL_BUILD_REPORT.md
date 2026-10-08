# Wreckage opening — visual blockout report

2026-10-07. Existing LostVanguard project, Unreal 5.8.3. Main reference: `assets/references/level_01/opening_wreck_alien_forest_reference.png`.

## Saved result

New opening variant: `/Game/WreckagePrototype/Maps/L_Wreckage_Opening`. The tested `/Game/WreckagePrototype/Maps/L_Wreckage_Playable` is preserved for comparison. Both use the same runtime player, enemy, GameMode, and HUD Blueprints. No new gameplay system replaces the working recovery sequence.

The opening uses a dark starting compartment, a wider angular hull breach, torn ribs and hanging cables, a cool forest with three depth layers, rocks and alien plant proxies, and a larger sideways wreck silhouette beyond the route. Broken panels and roof sections, a damaged fin, and an engine mass establish the focal ship section. Four small orange fire pockets suggest lingering trapped fuel, with translucent smoke proxies that rise, drift, fade, and repeat through a native material animation.

The route still includes debris release, look/walk checks, the crouch beam, the small break, weapon pickup, the existing two-searcher encounter, the fresh record, communications, and gated completion. The view appears immediately after freeing the debris and remains visible during the first movement checks. The spawn was moved back about 40 cm to avoid overlap with the debris; the route and checkpoints retain their existing positions.

Lighting uses a dark interior, cool outdoor fill, localized warm firelight, distance haze, and fixed exposure. The sky is a plain cool placeholder; no sky-body identities or final dramatic sky are selected. Editor-only icons and volume outlines are hidden for comparison captures without disabling lighting, post processing, or collision.

## How to view and play

Open `Unreal/LostVanguard/LostVanguard.uproject`. In the Content Browser, open `Content/WreckagePrototype/Maps/L_Wreckage_Opening`, press Play, and click the view. Press E to free the debris and reveal the vista. WASD moves, mouse looks, C crouches, Space jumps, E interacts, left mouse fires after pickup, R restarts, and Tab displays the acquired record. Escape stops Play.

## Checks and evidence

Fresh live editor queries verified access before environment work. All four existing runtime assets passed strict compilation/save inspection before work and were rechecked after the final captures. Clean saved defaults remain Health 100, Step/Checkpoint 0, no debug movement, and no acquired weapon/evidence/communications: `reports/wreckage_saved_inspection.json`. The new map was authored and saved through native Unreal editor APIs. The final build summary reports no errors or unsupported-property notes: `Unreal/LostVanguard/Saved/wreckage_opening_build.json`.

All 19 recorded route checks passed on the final opening map: fresh 100-health start, debris/look/walk/crouch/break traversal, weapon pickup, normal-health death and checkpoint restart, cue protection, both searchers defeated through real weapon traces, ordered clue access, repeat interaction, clue persistence after restart, the blocked early exit, communications, completion, and saved-map reload. Evidence: `reports/opening_playtest.json`; final stdout ends `ALL_CHECKS_PASSED`.

Test inputs feed actual character movement and gameplay functions. Normal-health death is tested separately; slow remote movement/combat uses extra temporary health, restored to 100 before the death check and by checkpoint restart. Saved player health remains 100. Physical keyboard/mouse feel, normal-health combat balance, and performance still need a human pass. The opening map is configured as the editor/game startup map; the existing editor is left on it. A full application restart and packaged build were not tested.

Comparison captures:

- `reports/opening_starting_view_play.png`: actual Play-In-Editor view from Evan's position after freeing the debris, with HUD and editor window visible.
- `reports/opening_starting_view.png`: editor viewport render at the recorded first-person camera pose, with debris temporarily moved away for the already-freed view and then restored before saving. Camera metadata: `reports/opening_comparison_camera.json`.
- `reports/opening_starting_view_smoke_later.png`: same editor camera at a later time for inspecting the smoke animation.

The final comparison camera is at (-390, 0, 154.15) cm, facing along the route with a 90-degree field of view. This matches the observed prototype player's eye pose after debris release. Both captures were visually inspected; the gameplay screenshot includes the actual HUD, while the comparison render removes the HUD and editor icons. The smoke and vegetation remain visibly simple proxies.

Early screenshots exposed a narrow portal, excessive fire brightness, and poor wreck framing. The portal was widened, the silhouette moved to a side view farther along the route, and manual exposure introduced. The spawn overlap was corrected. Early automated turning/jump checks also failed with varying editor frame rates; the harness now uses observed headings/positions, a longer forward jump input, and an optional real jump to recover footing if it lands in the break. These failed attempts are not counted as gameplay passes. The final test crosses the break and completes the mission without setting objective steps or teleporting along the route.

## What remains rough

This is a composition and movement blockout. Trees use trunk/canopy shapes, plants use cones, and smoke uses fading mesh proxies rather than a finished particle effect. The ship needs a coherent damaged hull kit, texture variation, scorched surfaces, more natural ground transitions, and richer vegetation. The original combat room and UI remain visibly utilitarian. Performance has not been profiled; foliage should be consolidated into instances before expansion. No packaged build or finished cinematic is claimed.

Surface staging, exact hull architecture, vegetation, sky, and fire placement are provisional interpretations of the accepted reference. The artifact is absent. Clank still reads fresh records rather than remembering the attack. No exact elapsed day count, enemy allegiance, officer duties, or new survivor is established. No paid generation, purchase, external publishing, new bridge, or subagent was used.

## Editable sources and next step

Environment source: `tools/build_wreckage_opening.py`. Live preview/camera capture: `tools/preview_wreckage_opening.py`. Route checks: `tools/test_wreckage.py` with the opening map argument. These use native editor APIs; Unreal binary assets were not directly edited or moved through filesystem operations.

Next: compare the saved starting view with the reference and play the route by hand. Approve the breach size, wreck placement, forest density, and light level before replacing a small set of hull and foliage proxies with reusable assets. Then improve terrain shoulders, cover readability, smoke/fire effects, and subtitle pacing.

The existing local connection follows [Epic's Unreal 5.8 MCP documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-mcp-in-unreal-editor?application_version=5.8). Actual installed editor APIs and schemas were inspected; compatibility is supported by successful native edits and play tests, rather than configuration alone.
