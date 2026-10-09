# Combined terrain, vegetation and movement

Updated 2026-10-08 (America/Los_Angeles).

## Result

The active main project remains `Unreal/LostVanguard 5.8/LostVanguard.uproject`. New review map: `/Game/LostVanguard/Environment/OrisonTerrain/Maps/L_Orison_Combined_Review`.

The combined map contains the existing 63 m Landscape and dirt/gravel/stone material, 36 rock/ledge placements, 44 earlier plant placements, and 12 new placements of F13/F14/F16 trees and F19/F21 bushes. Five new native FloraExpansion71 meshes have PBR textures, two-sided materials, and four decreasing engine LODs. Source GLB/FBX, four authored FBX LODs, and editable Blender scenes remain separate from the native packages. Engine LODs were generated with Unreal's reduction; they do not replace the authored FBX LOD sources. Tree canopies are collision-free; 16 invisible trunk blockers passed world traces. The earlier terrain proof and other environment maps remain available.

Accepted Reach-derived movement is saved through editor APIs in the mission player and the separate combined-terrain player: walk 562 cm/s, crouch 275, acceleration 3750, jump velocity 557.3, gravity scale 0.9478, air control 0.3. Mission mouse LookSensitivity remains 0.6. No fall damage; mission enemy damage, objectives and out-of-world protection retained. The gameplay builder reads the shared movement profile. The movement test map was rebuilt natively in main rather than copying Unreal binaries from Claude's worktree. Main helpers verify the main project's process and local marker on loopback 8000; Claude's original checkout/editor on 8001 remains untouched.

ExitGate height is now 450 cm in the playable, opening, and forest/wreck review maps, keeping its original bottom, footprint and LV_ExitGate tag so communications still removes it. This blocks the identified crouch-jump from the 150 cm comms panel (about 371 cm maximum reach). The level builder reproduces the height. Full boundary exploitation beyond this specific gate route is not claimed.

## Verification

- Main movement physics suite: 19/19 passed, including sampled speed, 167.2 cm jump apex, 1.20 s airtime, crouch, steps/slopes, air steering, 2–100 m drops, world protection, enemy damage and restart.
- Five new flora meshes: four decreasing native LODs each; import report `reports/combined_flora_import.json`.
- Combined map saved and reloaded; two new terrain Blueprints strictly compiled; all 16 trunk traces passed.
- Current opening mission route: 19/19 passed, no errors, including recovery, crouch, jump, combat/death/restart, clue/checkpoint retention, communications, objective-controlled gate removal, completion, and saved reload. The slow remote combat route uses temporary extra health; normal-health balance remains unverified.
- Combined terrain saved-reload play test: 3/3 passed (possession, walking and jumping/landing); live movement values match the accepted profile. Four mission runtime Blueprints compile with warnings as errors; saved Health 100, Step 0, LookSensitivity 0.6.
- Actual Unreal overview: `reports/combined_orison_overview.png`.

## Source control

Environment sources committed as `736e32d`. The integration commit also includes the previously untracked active Unreal project, earlier accumulated environment work, movement source, evidence and updated project records. Generated editor/cache folders, local marker and authentication values are excluded. Generated Android file-server token values were removed from publishable config, with exact local originals retained in ignored `tmp/local_config_backups`.

GitHub destination: `https://github.com/alexandergazzard-beep/Praetorian.git`, branch `main`. Approximately 8 GB of project files before Git/LFS compression. Automatic approval review rejected the initial asset upload because it requires explicit approval of this destination and payload. Upload remains pending user approval; no remote completion claim.

## Limits and recovery

These are playable review assets, not a finished first mission art pass. The combined terrain map has free movement rather than the mission objective sequence; opening mission gameplay remains in its existing maps with updated movement. Wind, instancing, foliage silhouette at every LOD, performance, gamepad, and packaged build remain unverified. Claude records that the user liked the movement after hands-on play; this integration adds automated checks, not a new human feel test.

The editor crashed once because generic asset duplication left an unsaved world alive during a map switch. Restarted main after saved plant/movement work; used the documented [LevelEditorSubsystem.new_level_from_template](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/LevelEditorSubsystem) map workflow successfully. No .uasset/.umap was edited or moved through filesystem operations. Original movement checkout is retained for comparison.
