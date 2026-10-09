> Integration update (2026-10-08): movement source re-applied through editor APIs to the main project, environment assets retained, movement test map rebuilt natively. Main-copy movement helpers now target verified loopback port 8000; the original movement checkout remains untouched on 8001. Historical instructions below describe the pre-integration handoff. See COMBINED_ENVIRONMENT_REPORT.md for current state.

# Movement task: coordination and handoff notes

For the user, Codex, or a later Claude session merging `claude/movement-tuning`. Written 2026-10-08.
These notes deliberately do **not** edit the shared records (STATUS, WORK_LOG, DECISIONS) in either checkout. Ready-to-paste entries are in section 6. Full results are in `docs/CLAUDE_MOVEMENT_REPORT.md`.

**User feedback, 2026-10-08:** after hands-on play on `L_Movement_Test`, the user said the movement "feels amazing", accepting the Reach-derived feel. The mission-map playthrough and individual value tweaks were not reported. Update the proposed DECISIONS entry in section 6 from "accept or adjust after hands-on review" to "accepted by the user after hands-on play".

## 1. Checkout facts

- Starting commit: `642db8816b399cde19a73c6584f11dd90ba5a720` on `main`. Branch: `claude/movement-tuning` (local only; no commits, push or merge).
- Movement checkout: `C:\Users\alexa\Documents\AI STUFF\Project Big-movement` (Git worktree of `C:\Users\alexa\Documents\AI STUFF\Project Big`).
- Movement project: `...\Project Big-movement\Unreal\LostVanguard 5.8\LostVanguard.uproject`. Editor MCP is on `127.0.0.1:8001`; Codex stays on `8000`.
- Contents: `642db88` plus a **snapshot copy** of the untracked active 5.8 project and four working-copy scripts, taken at 2026-10-08 22:08 UTC. Every file is hashed in `reports/movement_baseline_manifest.json`.
- Main-checkout files this work depends on were unchanged at handoff (same hashes as the snapshot):

| File (original checkout) | SHA-256 at snapshot and at handoff |
| --- | --- |
| `Unreal/LostVanguard 5.8/Content/WreckagePrototype/Blueprints/BP_WreckagePlayer_Runtime.uasset` | `cf5b0c9b01dd000587c04434fecea5488585d2f3e57cef8650fc4dfd3bfd7f89` |
| `Unreal/LostVanguard 5.8/Content/WreckagePrototype/Maps/L_Wreckage_Opening.umap` | `591b275a2efcaa0c2db69b930a4c7d32921cb74867cc5d47ef34af666e9332a3` |
| `tools/build_wreckage_gameplay.py` | `71126e8d0f265d9024a38420450de3c89e9cbb0c3ff5f90eddefe187426989af` |
| `tools/test_wreckage.py` | `0d8cd4cb2968e9a29029a95eeabd2a5df81010c950b80f88c94fbfb541cfcbe7` |

Codex's work since the snapshot (`/Game/LostVanguard/Environment/SpaceImpact`, new tools, record updates) does not overlap these files.

## 2. Clean list of movement changes (the only files to merge)

Modified:
- `Unreal/LostVanguard 5.8/Content/WreckagePrototype/Blueprints/BP_WreckagePlayer_Runtime.uasset`, changed through editor APIs only. Final SHA-256 `78c35d9628b00a34efc63ad94bcc5bd613945b298ce2f990923576c4aac22cae`. Changes: CharacterMovement defaults (6 values); new float variable `LookSensitivity` (0.6, instance-editable); in the running tick chain, the yaw/pitch literals changed from 0.6/−0.6 to 1.0/−1.0, each multiplied by `LookSensitivity`.
- `tools/build_wreckage_gameplay.py`. Final SHA-256 `84d027ab…1062`. Diff against the snapshot version:

```diff
+import sys
+sys.path.insert(0,str(Path(__file__).parent))
+from movement_profiles import ACTIVE_PROFILE, LOOK_SENSITIVITY_DEFAULT, PROFILES
-'RequestFire':('bool',False),'RequestRestart':('bool',False)}
+'RequestFire':('bool',False),'RequestRestart':('bool',False),'LookSensitivity':('float',LOOK_SENSITIVITY_DEFAULT)}
-        if name.startswith('Debug') or name.startswith('Request') or name=='Health':
+        if name.startswith('Debug') or name.startswith('Request') or name in ('Health','LookSensitivity'):
-        (Pawn|Input|AddControllerYawInput :Val (+ (* dx 0.6) (* {g('DebugLook')} DeltaSeconds)))
-        (Pawn|Input|AddControllerPitchInput :Val (* dy -0.6))
+        (Pawn|Input|AddControllerYawInput :Val (+ (* dx {g('LookSensitivity')}) (* {g('DebugLook')} DeltaSeconds)))
+        (Pawn|Input|AddControllerPitchInput :Val (* dy (* {g('LookSensitivity')} -1.0)))
+    # Movement tuning lives in movement_profiles.py (...)
+    for name,value in PROFILES[ACTIVE_PROFILE].items():
+        BP.get_default_object(player).character_movement.set_editor_property(move_names[name],value)
```

New:
- `Unreal/LostVanguard 5.8/Content/MovementTest/Maps/L_Movement_Test.umap` (SHA-256 `e20bfec1…ce1f`). A separate test map built by `tools/build_movement_test_map.py` from the engine's Template_Default.
- `tools/movement_profiles.py` (profiles and derivation), `tools/movement_mcp.py` (guarded port-8001 client), `tools/apply_movement_tuning.py`, `tools/inspect_movement.py`, `tools/build_movement_test_map.py`, `tools/test_movement.py`, `tools/test_movement_route.py`, `tools/check_route_traversal.py`, `tools/verify_movement_build.py`.
- `docs/CLAUDE_MOVEMENT_REPORT.md`, `docs/CLAUDE_MOVEMENT_COORDINATION.md`.
- Evidence: `reports/movement_*.json`, `reports/movement_test_*.png`, `reports/movement_route_opening_wreckage_*.png`. The `reports/movement_schema_*.json` and `movement_mcp_toolsets.json` files are tool discovery dumps and optional.

**Do not merge from this checkout:** everything else under `Unreal/LostVanguard 5.8/`, and the overlaid `tools/build_wreckage_hud.py`, `tools/build_wreckage_opening.py` and `tools/test_wreckage.py`. Those are snapshot copies of the original checkout and show as untracked/modified here only for that reason.

Local only (ignored by Git, never merge): `Saved/Config/WindowsEditor/EditorPerProjectUserSettings.ini` (port 8001), `Saved/movement_checkout_marker.json`, `Saved/MovementBaseline/` (byte backup of the original Blueprint).

Not touched: environment assets, the shared mission maps (`L_Wreckage_Opening`, `L_Wreckage`, `L_Wreckage_Playable` were only loaded and played, never saved; confirmed not dirty), enemy Blueprint, HUD, GameMode, `Config/*.ini`, Codex's records.

## 3. Shared-file changes that need agreement (none applied)

1. **`tools/test_wreckage.py` step timing (needed once Reach movement is merged).** The route driver's timing assumes 450 cm/s. At 562 cm/s it can stop 249 cm from the comms panel, just outside the 240 cm range, and fail "Communications advances after clue". Proposed exact change, equivalent to the old behaviour at any speed (`WALK` = player MaxWalkSpeed, e.g. read from `movement_profiles.PROFILES[ACTIVE_PROFILE]`):
   - `speed=min(1.0,dist/500)` → `speed=min(1.0,dist/(WALK*500/450))`
   - `seconds=min(2.0,max(1.0,dist/450))` → `seconds=min(2.0,max(1.0,dist/WALK))`

   `tools/test_movement_route.py` applies exactly this at runtime and passes 19/19. Codex's `test_forest_wreck.py` imports `test_wreckage`, so it will need the same fix.
2. **`L_Wreckage_Opening` exit gate (shared map).** A running crouch-jump from the 150 cm CommsPanel lands on top of the 290 cm ExitGate (live result in `reports/movement_route_traversal.json`). Objectives stay logically gated. Suggested fix by the map owner: raise the gate to the wall height (360 cm) or add a blocking volume above it, then review blockers near the 150 cm props for possible wall-top climbs (calculated, not live-tested).
3. **Builder graph growth (pre-existing).** Each `build_wreckage_gameplay.py` run appends another tick chain (299 → 423 nodes). Worth a separate cleanup task; not caused by this work.
4. The base `BP_WreckagePlayer` (non-runtime) keeps its original movement values. Nothing at runtime uses it; leave it unless you want a historical match.

## 4. Suggested merge order

1. Let Codex finish and **commit its current scene work on `main` first**, including adding the active `Unreal/LostVanguard 5.8/` project to Git. Merging can't be clean while that project is untracked.
2. Do the hands-on checklist (report section 9) in the movement editor; accept or adjust the values.
3. In the movement checkout, commit **only the files in section 2** by listing them explicitly; never `git add .` there.
4. On `main`, check that the four hashes in section 1 still match. Then bring the movement commit across (for example `git cherry-pick`). The builder change merges as text. The player Blueprint is binary: Git will report a conflict because the branch adds a file that `main` already tracks. Resolve it by taking the movement version **only if** `main`'s copy still has hash `cf5b0c9b…`. If `main`'s Blueprint changed in the meantime, don't merge the binary; instead re-run `tools/apply_movement_tuning.py` against Codex's editor *after* changing its port guard, with agreement.
5. Apply the agreed shared changes from section 3 (test timing; exit gate) in `main`.
6. In the main editor, rerun the 19-check route test and `tools/test_movement.py` (after pointing the helper at that editor deliberately), then update records (section 6).
7. Clean up: close the movement editor; `git worktree remove "C:\Users\alexa\Documents\AI STUFF\Project Big-movement"`; delete the branch when no longer needed. These steps delete the movement checkout, so do them only after merging or deciding to discard.

## 5. Running the movement tools

From `C:\Users\alexa\Documents\AI STUFF\Project Big-movement`, with the movement editor open (each script aborts unless it is talking to this checkout's editor):

```bash
uv run tools/inspect_movement.py
```

```bash
uv run tools/apply_movement_tuning.py reach
```

```bash
uv run tools/test_movement.py reach
```

```bash
uv run tools/test_movement_route.py
```

To relaunch the movement editor if it is closed (keeps it on port 8001):

```bash
"C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor.exe" "C:/Users/alexa/Documents/AI STUFF/Project Big-movement/Unreal/LostVanguard 5.8/LostVanguard.uproject" "-ini:EditorPerProjectUserSettings:[/Script/ModelContextProtocolEngine.ModelContextProtocolSettings]:ServerPortNumber=8001"
```

## 6. Proposed shared-record entries (paste at merge time; not yet applied)

STATUS (new section):
> ## Player movement (Halo: Reach-referenced) — 2026-10-08
> User chose Halo: Reach as the movement priority. In a separate worktree (`claude/movement-tuning`, second editor on port 8001), BP_WreckagePlayer_Runtime was tuned to Reach-derived values scaled to Evan's 176 cm body: walk 562 cm/s, crouch 275, acceleration 3750, jump 557.3 with GravityScale 0.9478 (167 cm apex, 1.2 s airtime), AirControl 0.3. Mouse multiplier is now `LookSensitivity` (0.6). There is no fall damage (2–100 m landings tested); the out-of-world catch, enemy damage, death/restart and objectives are preserved. Movement suite 19/19 and mission route 19/19, including after an editor restart. Values are approximations from a 2011 community measurement; physical feel is unverified pending the user's hands-on check. Higher jump lets the player perch on the exit gate from the comms panel; a map fix is pending. Not yet merged. See CLAUDE_MOVEMENT_REPORT.md.

DECISIONS (next free number; D102 was the latest seen):
> - D10x (2026-10-08, gameplay): Movement prioritizes Halo: Reach over Halo 3 (user choice). Implementation uses body-relative values derived from labelled community measurements; no claim of exact Halo parity; no sprint/abilities added; no fall damage; out-of-world catch retained. Accept or adjust after hands-on review. Supersedes D094's open "primary reference" question only.

WORK_LOG:
> ## 2026-10-08 - Halo: Reach movement tuning (separate checkout)
> - Worktree `claude/movement-tuning` from 642db88 plus a hashed snapshot of the untracked active 5.8 project; second editor on loopback 8001 with port/marker identity guard. Codex editor untouched.
> - Researched available Halo references (no official values; 2011 Bungie.net fan measurements); user chose Reach. Applied six CharacterMovement values and a LookSensitivity variable through editor APIs; builder updated; rebuild verified headless on a scratch copy.
> - Tests: movement suite 19/19 (Reach and original), mission route 19/19 after a driver-timing scale, reload verification, no fall damage from 2–100 m, enemy damage/restart preserved. Found exit-gate perch via the comms panel (map fix pending) and pre-existing builder graph duplication.
> - Limits: no physical input or feel test; estimates for acceleration/air control; snapshot excludes later scene edits. Next: hands-on checklist, then merge per CLAUDE_MOVEMENT_COORDINATION.md.
