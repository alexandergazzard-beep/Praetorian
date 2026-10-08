# Level 01 — Wreckage build report

2026-10-07. Engine: Unreal 5.8.3. Existing project: `Unreal/LostVanguard/LostVanguard.uproject`.

## What exists

An actual saved editor prototype, using native runtime Blueprints and simple shapes. Python is used to author assets; gameplay does not require Python or an AI service. No packaged build has been produced.

- Playable map: `/Game/WreckagePrototype/Maps/L_Wreckage_Playable`.
- Preserved initial blockout: `/Game/WreckagePrototype/Maps/L_Wreckage`.
- Runtime assets under `/Game/WreckagePrototype/Blueprints/`: `BP_WreckagePlayer_Runtime`, `BP_SearcherPlaceholder_Runtime`, `BP_WreckageGameMode_Runtime`, and `BP_WreckageHUD`.
- Six connected areas: recovery compartment, low passage and break, combat bay, search-record station, communications alcove, exit. Fixed structural collision, two cover blocks, a flank divider, simple exterior ground and distant ruin shapes.
- First-person camera, walk/crouch/jump, debris interaction, weapon pickup, camera-trace firing, two stationary damaging searchers, death/restart, recovery and evidence checkpoints.
- Ordered objectives, one subtitle at a time with queued cues and seen flags, persistent readable search record with Tab, communications interaction, gated mission completion.

## Launch and controls

Open the existing project. In the Content Browser, open `Content/WreckagePrototype/Maps/L_Wreckage_Playable`, then press Play and click the game view. Escape stops Play; Shift+F1 releases the mouse.

| Control | Action |
| --- | --- |
| WASD / mouse | Move / look |
| Hold C / Space | Crouch / jump |
| E | Shift debris, collect weapon, access record, restore communications, finish at exit |
| Left mouse | Fire after pickup |
| R | Restart at current checkpoint |
| Hold Tab | Read the acquired record |

Follow the objective at the top of the screen. The cyan stations are the record and communications panels. The red cylinders are searcher placeholders. The red exit gate opens after communications. Completion displays the proposed next mission; it does not load an unbuilt Mission 02.

## Verification

Fresh native editor queries succeeded through the existing loopback MCP bridge. Saved graphs compile with warnings treated as errors. The map and its connected GameMode/player/HUD assets were inspected in the editor and in Play-In-Editor. Current detailed observations: `reports/wreckage_playtest.json`.

The route test uses editable debug input properties that feed the real Character movement/controller, interaction, and weapon functions. It does not set objective steps or teleport through the route. Normal 100-health death/restart is tested separately. The subsequent slow remote route uses extra test health without changing saved defaults; normal-health encounter balance and physical mouse/keyboard feel require a human pass.

All 19 recorded checks passed: fresh start, debris/look/walk/crouch/break traversal, weapon pickup, normal-health death, encounter restart, no opening-cue replay, real weapon hits defeating both searchers, ordered evidence access, repeat-interaction cue protection, evidence persistence after restart, locked exit, communications, mission completion, and saved-map reload. All four connected runtime Blueprints also passed a final strict compile/save inspection. Saved player defaults remain Health 100, Step/Checkpoint 0, debug movement off, and weapon/evidence/communications false. See `reports/wreckage_saved_inspection.json`.

## Problems found and fixed

- Recovery dialog prevented editor responsiveness; the user resolved it and left one editor open.
- Native tool decorators could log authoring exceptions without failing scripts. Authoring now raises exceptions and uses strict compilation; unchanged graphs are not accepted as evidence.
- Local function/variable nodes required supported native graph editor callbacks rather than assumed discovery names.
- The background editor runs slowly, so short automated movement pulses undershot the jump and simple waypoint inputs oscillated. Tests now use observed positions and reduced input near targets.
- Literal newline escapes appeared in the HUD. Saved string pins now contain actual line breaks.
- Static lights showed Preview shadows. Prototype lights are now movable.
- Character capsule defaults ignored enemy visibility traces. Saved BeginPlay now explicitly blocks that channel; actual incoming damage and death were subsequently observed.

## Temporary choices and limits

Surface-wreck staging on Orison, geometry, lighting, dialogue wording, gun shape, stationary red sentries, and ruin silhouettes are prototype proposals. They do not establish final setting details, enemy bodies/allegiance, officer duties, survival mechanism, or character appearance.

Clank accesses fresh search records and states his memories are damaged. The record reveals only an artifact search, not the full motive, relocation history, or war explanation. No artifact is placed aboard or collected. The signal remains Human Signal. No survivor of the lost squad is introduced. No exact week is stated.

Clank currently has subtitles rather than a visible robot or recorded voice. Debris disappears on interaction rather than simulating a full collapse. Enemies are simple stationary sentries rather than navigation/combat AI. Lighting and exterior art remain rough. No cinematic, paid generation, purchase, external publication, new bridge, or subagent was used.

The existing MCP client emits a session-termination HTTP 202 warning even after successful operations. This chat requires hidden external helper processes to access the live editor; direct tool exposure remains unavailable. Historical verification files are preserved.

## Evidence and editable sources

Screenshots: `reports/wreckage_recovery_play.png`, `reports/wreckage_combat_play.png`, `reports/wreckage_death_play.png`, `reports/wreckage_evidence_play.png`, and `reports/wreckage_complete_play.png`. These capture the actual editor/game view, including HUD. The completion screenshot predates a cosmetic Unicode-escape correction in the saved label; see reports/wreckage_end_label_fix.json for the strictly compiled and saved repair.

Authoring sources: `tools/build_wreckage.py`, `tools/build_wreckage_gameplay.py`, `tools/build_wreckage_hud.py`, `tools/finalize_wreckage_map.py`. Verification: `tools/test_wreckage.py`. Live fixes: `tools/fix_wreckage_display.py`, `tools/fix_wreckage_collision.py`. Native authoring summaries are in `Unreal/LostVanguard/Saved/wreckage_*build.json` and `wreckage_final_map.json`.

Assets were authored and saved using Unreal editor APIs. No `.uasset` or `.umap` binary was directly edited or moved through filesystem operations. Keep the running editor and offline authoring processes from editing the same asset simultaneously; these sources are reviewable build records, not a one-click safe rebuild workflow.

## Next concrete iteration

Subsequent image-led iteration: `/Game/WreckagePrototype/Maps/L_Wreckage_Opening` preserves this map's gameplay and adds the reference-led environment. See [OPENING_VISUAL_BUILD_REPORT.md](OPENING_VISUAL_BUILD_REPORT.md) for the latest screenshots and verification. This original report remains the baseline gameplay record.

Play the saved map by hand to tune mouse sensitivity, incoming damage, cover effectiveness, interaction readability, and subtitle pacing. Then add a readable health label/hit feedback, improve the two sentries and cover encounter, and replace only the opening compartment with a small wreck/forest asset kit guided by the supplied reference. Keep final visual and story selections with the user.
