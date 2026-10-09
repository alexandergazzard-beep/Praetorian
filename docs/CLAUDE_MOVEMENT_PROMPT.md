# Claude task: Halo-referenced movement

Work on Lost Vanguard's player movement and jumping. My target is as close as possible to Halo 3 or Halo: Reach, explicitly with NO FALL DAMAGE. Ask which game to prioritize before locking final tuning.

Read AGENTS.md and the current project records first. Locate the active project from STATUS. Preserve recovery, combat, mission objectives and restart. Inspect the actual player implementation before changing it.

Tune walking speed, acceleration, stopping, gravity, jump height, time to apex, airtime, horizontal air control, crouching, slopes, steps and landing response. Keep mouse sensitivity adjustable. Verify reference behavior using reliable sources or clearly labeled measurements; do not invent exact Halo values or add sprint/abilities without agreement.

Disable fall damage, including high drops, while preserving enemy damage, death/restart and protection from leaving the playable world. Loose-prop physics and whole-wreck destruction are separate tasks.

Coordinate a live Unreal editing window with my Codex asset work before making changes. Use supported editor APIs, retain original settings, make a reversible tuning pass, compile/save, and update relevant source builders so rebuilding retains changes. Do not edit Unreal binaries through filesystem operations or touch environment assets.

Test actual controls, jump height/airtime, landings from several heights with unchanged health, enemy damage, collision and the mission route. Confirm saved/reloaded settings. Distinguish actual checks from unavailable tests and my subjective feel assessment. If editor access is unavailable, return a concrete proposal instead of claiming implementation.

Write docs/CLAUDE_MOVEMENT_REPORT.md with original/new settings, evidence, limitations and a hands-on comparison checklist. During concurrent asset work, leave shared records for a coordinated follow-up. Do not claim an exact Halo match from parameter values alone.
