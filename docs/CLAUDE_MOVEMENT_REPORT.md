> Integration update (2026-10-08): the accepted profile and sensitivity are now saved in the main project; all 19 movement checks passed there. This report records Claude's original worktree results. See COMBINED_ENVIRONMENT_REPORT.md for integration, environment and gate changes.

# Claude movement report: Halo: Reach-referenced tuning

Date: 2026-10-08 (America/Los_Angeles). Author: Claude (Claude Code), working in a separate movement checkout.
Status: **implemented, saved, tested in the movement editor; not merged, not committed.** Awaiting your hands-on review.

## 1. What changed, in plain language

- Evan now runs faster (450 → 562 cm/s), jumps much higher and floatier (feet clear 86 cm → 167 cm; 0.79 s → 1.2 s in the air), and can steer strongly in mid-air.
- These values were derived from a Halo: Reach fan measurement, scaled to Evan's body size. They are an approximation, **not** an exact Halo match.
- There is still **no fall damage**: landings from 2 m up to 100 m leave health at 100.
- Mouse look sensitivity is now a named setting (`LookSensitivity`, default 0.6 = exactly the old feel) instead of a hidden number.
- Enemy damage, death, R-restart, checkpoints, objectives and the "fell out of the world" safety catch all still work.
- One level issue: the higher jump lets you climb the 150 cm comms panel and hop onto the 290 cm exit gate. Mission completion is still blocked until the comms objective is done, but the gate no longer *physically* stops you. Fixing it is a shared-map change. See section 7.

You chose **Halo: Reach** as the priority when asked (2026-10-08). A Halo 3 variant is documented but not applied.

## 2. Separate checkout and editor

| Item | Value |
| --- | --- |
| Starting commit | `642db8816b399cde19a73c6584f11dd90ba5a720` (main, "Record verified GitHub project upload") |
| Branch | `claude/movement-tuning` (Git worktree; not pushed) |
| Movement checkout | `C:\Users\alexa\Documents\AI STUFF\Project Big-movement` |
| Movement project | `C:\Users\alexa\Documents\AI STUFF\Project Big-movement\Unreal\LostVanguard 5.8\LostVanguard.uproject` |
| Engine | Unreal Engine 5.8.3 (`C:\Program Files\Epic Games\UE_5.8`) |
| Movement editor | Second UnrealEditor process; MCP on `127.0.0.1:8001` (loopback only) |
| Codex editor | Untouched; still on `127.0.0.1:8000` with the original checkout |

**Does this checkout include the current scene work? Yes, as a snapshot.** The active Unreal project (`Unreal/LostVanguard 5.8/`) has never been committed, so the last commit alone contains only the older `Unreal/LostVanguard/` copy. After creating the worktree, I copied the active project's `.uproject`, `Config/` and `Content/`, and the four working-copy gameplay scripts (`build_wreckage_gameplay.py`, `build_wreckage_hud.py`, `build_wreckage_opening.py`, `test_wreckage.py`) into it at **2026-10-08 22:08 UTC**. I hashed every file before and after (173 files, none changed during the copy); see `reports/movement_baseline_manifest.json`. I did not copy generated folders (`Saved`, `Intermediate`, `DerivedDataCache`). Codex scene edits made after that time are not in this checkout.

Git LFS: the existing `.gitattributes`/LFS configuration is unchanged. `git lfs fsck` passed in the worktree, and the committed `.uasset` files there are real binaries, not pointer files.

Targeting safety: every editor script uses `tools/movement_mcp.py`. That helper refuses port 8000 and checks two things before any call:
1. The process listening on 8001 was launched with this checkout's `.uproject`.
2. The editor can read a private random token from this checkout's `Saved/` folder.

Both checks passed at the start of every session, including after two editor restarts. The port override lives only in ignored local files (`Saved/Config/WindowsEditor/EditorPerProjectUserSettings.ini`) plus the launch command line. The shared `Config/` files are unchanged.

The original checkout was only read. It still has no movement changes. Its copies of the four files this work touches or depends on (player Blueprint, opening map, gameplay builder, route test) still match the snapshot hashes exactly.

## 3. Reference data and how values were derived

No official Halo 3 or Halo: Reach movement numbers are publicly documented in a source I could verify. These are the best available sources, all community-made:

| Source | What it gives | Reliability |
| --- | --- | --- |
| Bungie.net forum post by "mdenni", 2011-10-08 ([link](https://www.bungie.net/en/Forums/Post/3291870)) | Reach default: run 6.82 m/s; jump apex (foot-to-head-top) 1.95 Spartan heights; 1.2 s airtime. Halo 3: 7.69 m/s; 2.45 heights; 1.4 s | Hand measurement on Forge grids and the Spartan model. Airtime is timed to about 0.1 s. One label in the post is inconsistent (H3 MLG speed) |
| Halo editing-kit player metrics ([Halo CE page](https://nikon.bungie.org/misc/hek_tutorial/references/general/halo_player_stats.html), [Halo 2 page](https://www.h2maps.net/editingkit/player%20statistics%20and%20metrics.html)) | Player about 7 ft (213 cm); 45° maximum slope; step height about 17% of body height | Older games; used only for scale and as context |
| Bungie.net thread ([link](https://www.bungie.net/en/Forums/Post/3526423)) | Unverified claim of 2.20 (Reach) vs 2.25 (H3) speed values | Not used |

Derivation (all in `tools/movement_profiles.py`, computed in code so it can be checked):
- Scaling: everything is relative to body height. Evan's capsule is 176 cm; a Spartan is taken as 213.4 cm.
- Run speed = 6.82 m/s × 176/213.4 = **562 cm/s**.
- Jump clearance = (1.95 − 1) × 176 = **167 cm**. Airtime **1.2 s**.
- A symmetric arc then gives gravity = 8 × 167 / 1.2² = 929 cm/s² (**GravityScale 0.9478**) and **JumpZVelocity 557.3 cm/s**.
- **Estimates with no Halo data behind them** (for you to judge by feel): acceleration 3750 cm/s² (about 0.15 s to full speed), AirControl 0.3, and crouch speed 275 cm/s (the original crouch:run ratio kept).

Uncertainty is large. A ±0.05 s airtime error changes gravity by about ±8%, and the Spartan-height assumption shifts run speed by ±5–7%. Matching these numbers does **not** prove the game feels like Reach; only hands-on play can judge that.

## 4. Original and new settings (BP_WreckagePlayer_Runtime)

| Setting | Original | New (Reach-derived) | Basis |
| --- | --- | --- | --- |
| MaxWalkSpeed | 450 | **562** | Measurement, scaled |
| MaxWalkSpeedCrouched | 220 | **275** | Original ratio kept |
| MaxAcceleration | 2048 | **3750** | Estimate |
| JumpZVelocity | 450 | **557.3** | Measurement, derived |
| GravityScale | 1.2 | **0.9478** | Measurement, derived |
| AirControl | 0.05 | **0.3** | Estimate |
| LookSensitivity (new variable) | 0.6 (was hard-coded) | 0.6 | Same feel; now adjustable |
| BrakingDecelerationWalking / GroundFriction / BrakingFrictionFactor | 2048 / 8 / 2 | unchanged | Already stops in about 0.1 s |
| BrakingDecelerationFalling / FallingLateralFriction | 0 / 0 | unchanged | Momentum kept in the air, like Halo |
| MaxStepHeight | 45 | unchanged | A Halo-relative 30 cm could snag on existing route props |
| WalkableFloorAngle | 44.77° | unchanged | Already about the Halo EK 45° |
| CrouchedHalfHeight / capsule 88×34 | 44 / 88×34 | unchanged | Needed by the 125 cm crouch beam |
| JumpMaxHoldTime / JumpMaxCount | 0 / 1 | unchanged | Fixed-height single jump; no new abilities |

No sprint, double jump or other abilities were added.

Mouse look graph change: the two hard-coded multipliers (`0.6` yaw, `−0.6` pitch) became `1.0 × LookSensitivity` and `−1.0 × LookSensitivity`. This was done only in the tick chain that actually runs (see limitation 6). To change sensitivity: open `BP_WreckagePlayer_Runtime` → Class Defaults → `Look Sensitivity`.

## 5. Fall damage and world protection

Inspection showed the player never had landing-based fall damage. The only fall-related rule is the out-of-world catch (`RecoveryChecks`: below z = −350 → "You fell. Press R to restart."). That rule is protection from leaving the playable world, so it was **kept**. In the mission map the lowest legitimate floor is the pit safety floor at −180 (the outside ground is −230), so normal drops never trigger it. The world KillZ is the engine default (−1,048,575). Tests confirm landings from 2, 5, 10, 20, 40 and 100 m, plus walking off a 10 m platform, all leave health at 100. Enemy damage (12 per hit) still kills and restart restores 100.

## 6. Evidence

All tests ran in the movement editor on PIE with real character physics. They drive the Blueprint's existing test inputs (`DebugForward/Right/Crouch`, `RequestJump/Restart`), which call the same `AddMovementInput`, `Jump` and `Crouch` nodes as the keyboard. Timing uses game time (the Blueprint's own `DebugMoveTime` countdown), with samples about 26–46 ms apart.

| Check | Result | Evidence |
| --- | --- | --- |
| Movement suite, Reach profile, test map (19 checks) | **19/19** (also 19/19 after each of two editor restarts) | `reports/movement_tests_reach.json`, `movement_test_reach.png` |
| Same suite, original profile (before/after baseline) | **19/19** | `reports/movement_tests_original.json` |
| Mission route on the snapshot of `L_Wreckage_Opening` (recovery, crouch, break jump, weapon, combat death/restart, clue, comms, gated exit, reload) | **19/19** before and after the final reload | `reports/movement_route_playtest.json`, `movement_route_*.png` |
| Saved settings after full editor restart | Values match; Blueprint loads clean and stays unmodified through both suites | `reports/movement_inspection_final_reload.json` |
| Builder rebuild (updated builder run headless on a scratch copy of the pre-tuning content) | Reproduces all six values and `LookSensitivity`; running look code uses it; compiles with warnings as errors | `reports/movement_builder_rebuild_check.json` |
| Restore path (`apply_movement_tuning.py original`, then `reach`) | Both read back exactly and saved | `reports/movement_apply_*.json` |
| Climbing reach in the mission map plus a live gate attempt | See section 7 | `reports/movement_route_traversal.json` |

Measured on the test map (`/Game/MovementTest/Maps/L_Movement_Test`):

| Measurement | Original | Reach-derived |
| --- | --- | --- |
| Top run speed | 450 cm/s | 562 cm/s |
| Time to 90% speed | 0.21 s | 0.15 s |
| Stop after release | 0.08 s / 5 cm | 0.09 s / 10 cm |
| Jump apex (predicted) | 86.0 cm (86.1) | 167.2 cm (167.2) |
| Airtime (predicted) | 0.79 s (0.77) | 1.20 s (1.20) |
| Running jump distance, holding forward | 369 cm | 697 cm |
| Running jump, pull back in air | 330 cm forward | lands 85 cm *behind* takeoff |
| Running jump, strafe only | 33 cm sideways | 472 cm sideways |
| Crouch speed | 220 cm/s | 275 cm/s |
| Highest ledge reached: standing / crouch-jump | under 120 / 150 cm | 180 / 220 cm |
| Steps climbed (20/35/44/46/55 cm) | yes/yes/yes/no/no | same |
| Slopes walkable (30/40/44/46/50°) | yes/yes/yes/no/no | same |
| Health after 2 m to 100 m landings | 100 | 100 |
| Out-of-world catch + restart | works | works |

Note on ledges: the capsule's rounded bottom lets the player catch a ledge about 10 cm above the feet's peak height. Crouching mid-air lifts the feet a further 44 cm (Halo-style crouch-jumping).

## 7. Level interactions found (need a coordinated map change)

The mission map was built around the old 86 cm jump. With Reach movement:
- **Newly climbable:** WeaponLocker, SearchTerminal and CommsPanel (150 cm), Bay covers (130 cm, previously crouch-jump only), and the OV_TreeTrunk_0 dressing (about 170–206 cm).
- **Exit gate:** in a live attempt, a running crouch-jump from the top of the comms panel landed the player **on top of the 290 cm ExitGate**, from where they can drop into the exit area. Completion is still impossible without the comms step (the Blueprint checks `Step`, `EvidenceRead` and `CommsRestored`), and the route test's "Exit cannot bypass clue/communications" check passes. Physically, though, the gate can now be bypassed.
- **Wall tops (360 cm):** from a 150 cm prop, the crouch-jump reach is about 371 cm. That *might* allow reaching a wall top when the prop is within about a metre of a wall. This is a calculation only, not live-tested. Note that the opening variant had already lowered the passage and landing walls to 70–80 cm, which the original jump could clear.

Recommended (not done here, because the map is shared): raise ExitGate to wall height or add an invisible blocking volume above it, and review blockers near 150 cm props. No jump or crouch-jump reaches 290 cm from the floor (measured).

## 8. Limitations and unavailable tests

1. No physical keyboard or mouse was used; feel is unverified. Use the checklist below.
2. Halo values are approximations from one fan measurement. Acceleration, air control and crouch speed are estimates.
3. Mouse sensitivity was checked by graph inspection, compile and runtime value only; real mouse movement could not be injected.
4. Route tests ran on the 22:08 UTC snapshot of the opening map; Codex's later scene edits are not included.
5. The shared route test's step timing assumes 450 cm/s. At 562 cm/s its driver once stopped 249 cm from the comms panel (the range is 240) — a test artifact, not a gameplay fault. `tools/test_movement_route.py` runs the unchanged shared test with those two timing constants scaled to the profile speed; a permanent fix is proposed in the coordination notes.
6. Pre-existing issue: each run of `build_wreckage_gameplay.py` appends a new tick graph and leaves the old one unconnected (299 → 423 nodes in the rebuild check). Harmless at runtime, but it bloats the Blueprint. Cleanup is out of scope.
7. A background Unreal editor throttles itself to about 3 FPS. Tests switch this off for the movement editor process only (not saved to config) and switch it back afterwards.
8. The editor's `read_graph_dsl` tool marks Blueprints as modified even though it only reads them. `tools/inspect_movement.py` now uses it only with `--dsl`.
9. No packaged build, gamepad, frame-rate benchmark or multiplayer test.

## 9. Hands-on comparison checklist

Use the movement editor (window title shows `LostVanguard`; path under `Project Big-movement`).
1. Open `/Game/MovementTest/Maps/L_Movement_Test`, press Play. Run, stop and strafe on the open floor. Is the run speed Reach-like? Does stopping feel crisp?
2. Jump in place several times. Does the ~1.2 s hang time feel like Reach, or too floaty?
3. Run and jump, then steer in the air (pull back; strafe). Is mid-air steering too strong (AirControl 0.3) or too weak?
4. Ledge row (far left lanes): standing jump should reach 180 cm but not 200; crouch-jump (press C after takeoff) should reach 220 but not 250.
5. Walk off the 10 m platform and jump from high places. Health must stay 100.
6. Run under the 125 cm crouch bar with and without C.
7. Change `Look Sensitivity` in the Blueprint's Class Defaults (for example 0.4 and 0.9), compile, play, and compare mouse feel.
8. Open `/Game/WreckagePrototype/Maps/L_Wreckage_Opening` and play the whole mission. Check the break jump, combat, cover use, and whether climbing the panels or the exit gate feels acceptable.
9. If you have Halo: Reach (MCC) available, alternate short sessions and note "faster/slower, higher/lower, floatier/heavier, more/less air steering".
10. Tell me what to adjust. Each value is one line in `tools/movement_profiles.py`, and `apply_movement_tuning.py` re-applies it.

## 10. Restoration

- Back to the original movement while keeping the sensitivity setting: with the movement editor open, run `uv run tools/apply_movement_tuning.py original` from the movement checkout (this saves only the player Blueprint). For future rebuilds, set `ACTIVE_PROFILE = 'original'` in `tools/movement_profiles.py`.
- Exact original Blueprint file: a byte copy is kept at `Unreal/LostVanguard 5.8/Saved/MovementBaseline/BP_WreckagePlayer_Runtime.uasset` (SHA-256 `cf5b0c9b…7f89`, the same as the original checkout). Restore it only with the movement editor closed, like a version-control revert.
- Discard everything: nothing in the original checkout depends on this work. Close the movement editor, then remove the worktree and branch when you're sure. These steps delete work, so they're listed in the coordination notes rather than run.

## Sources

- [Bungie.net — classic Halo movement speed, jump height, gravity, and shield recharge (2011)](https://www.bungie.net/en/Forums/Post/3291870)
- [Bungie.net — Why does Halo: Reach's movement speed feel so much slower…](https://www.bungie.net/en/Forums/Post/3526423)
- [Halo player statistics (HEK reference, bungie.org)](https://nikon.bungie.org/misc/hek_tutorial/references/general/halo_player_stats.html)
- [Halo 2 Editing Kit tutorial — player statistics and metrics](https://www.h2maps.net/editingkit/player%20statistics%20and%20metrics.html)
- [Halopedia — MLG playlist settings](https://www.halopedia.org/MLG_(playlist))
- [Game Developer — Analyzing core character movement in 3D](https://www.gamedeveloper.com/design/analyzing-core-character-movement-in-3d) (qualitative only)
