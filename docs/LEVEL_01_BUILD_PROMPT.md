# Copyable build prompt — Lost Vanguard Level 01

Use the text below in a new local chat attached to Project Big. This file is a task brief, not evidence that tools are connected or a level exists.

---

Start building the first playable Lost Vanguard level in this local workspace:
C:/Users/alexa/Documents/AI STUFF/Project Big

Read AGENTS.md and its required project records, then docs/LEVEL_01_WRECKAGE.md and docs/FIRST_LEVEL_BUILD_PLAN.md. Use the existing Unreal project at Unreal/LostVanguard/LostVanguard.uproject. Preserve existing work. Check the latest files rather than relying on another chat's memory.

The goal is a small, playable first-person Wreckage prototype using simple shapes, placeholder characters, and subtitles. Build the actual level through supported Unreal editor APIs and runtime gameplay tools, then inspect and play-test it. A plan or editor script alone is not completion. Finished character models, a complete planet, and cinematic construction can wait.

Inspect the user-supplied visual reference at assets/references/level_01/opening_wreck_alien_forest_reference.png and its README. The user wants approximately this starting environment: a dark torn hull opening looking toward a burning wreck in an alien forest. Use its composition for the blockout and later visual review; do not treat every pictured detail as canon or as a required finished asset. Character armor is not depicted. Keep the established recovery sequence and delay of days consistent.

First verify current editor access with a real scene query. Prior temporary actor edits succeeded, but the most recent discovery request stalled; do not assume the current connection works. Inspect available tools and use their actual schemas. Resolve routine local connection issues within authorized scope. Keep bridges on loopback. If editor access remains unavailable, preserve useful source work and report precisely what could not be built or tested; do not claim success from configuration or an open port.

Connection setup is already documented in docs/TOOLCHAIN.md and docs/STATUS.md. Unreal Engine 5.8.3 is installed at C:/Program Files/Epic Games/UE_5.8. Open the existing LostVanguard.uproject and keep its editor running. The project has Unreal MCP, All Toolsets, Python editor scripting, and editor scripting utilities enabled, with automatic server startup configured. The registered local Unreal MCP endpoint is http://127.0.0.1:8000/mcp. Use the available unreal connection's discovery tools to inspect the actual toolsets, then query the scene. If tools are not exposed in the chat, the existing tools/unreal_mcp.py protocol client is a fallback; inspect its usage and the prior reports/unreal_mcp_verification.json before using it. Avoid rerunning a verification mode that overwrites historical evidence. A listening endpoint alone is insufficient: the editor must answer actual requests. Record the current result and report any unresolved startup dialog or unresponsive request rather than making unsupported changes. Do not create another project or install a replacement bridge merely because this connection needs troubleshooting.

Build in checkpoints:
1. Create a dedicated prototype map with a compartment, damaged passage, combat bay, evidence station, communications alcove, and exit. Use a small surface-wreck staging on Orison as a temporary prototype choice, clearly labeled as a proposal rather than new canon. Simple terrain and distant ruin shapes are enough; no entire landscape required.
2. Establish responsive movement, camera, collision, and interactions. The recovery tutorial checks look, walk, crouch, and crossing a small break. Evan already knows how to fight; the tutorial represents recovery. Use Unreal's built-in physics, fixed structural collision, and only limited moving debris. Tune for playability; no custom physics engine or whole-ship destruction simulation.
3. Add one placeholder weapon and a small search-party encounter with readable cover and a flank. Enemy appearance and exact allegiance remain undecided; placeholders do not select them.
4. Add objective progression, Clank subtitle triggers, new search-record access, communications, and an exit leading toward the proposed Rally Point mission. Use the draft lines as editable placeholders. Keep the human radio speaker unidentified until an officer role is selected.
5. Add checkpoints/restart behavior, inspect the saved map, compile relevant gameplay assets, and play-test. Fix demonstrated problems before reporting completion. Defer packaged builds until this editor prototype works.

Keep story facts consistent: Evan is a Praetorian leader; Clank is his small robotic companion. Meridian destroyed the ship mistakenly believing the stabilization artifact was aboard. It was never aboard. No replacement artifact cargo or surviving member of the lost squad should be invented. Clank has damaged personal memories; he discovers fresh system records rather than remembering the attack. This level reveals only that a specific artifact is being sought. Relocation history, the AI's full motive, and the wider war explanation belong later. Evan wakes after days, not an exact week. Officer duties, survival mechanism, and final designs remain open. Record temporary implementation assumptions without turning them into accepted story decisions.

Use reusable existing/template assets where suitable. Do not purchase services, start paid generations, build finished cinematics, or introduce extra integrations without a demonstrated need. Keep editable sources; do not directly edit or move .uasset/.umap binaries through filesystem operations. Do not spawn subagents. Proceed with routine reversible implementation choices without stopping for repeated confirmations.

Verify at least: complete route from a fresh start; walk/crouch traversal; interactions; objective order; first combat; death/restart; evidence remains available; subtitles do not overlap or replay on repeated triggers; exit cannot bypass the clue; saved-map reload. Report any check not actually run.

Write docs/LEVEL_01_BUILD_REPORT.md with what exists, map/assets changed, temporary design assumptions, controls, how to launch it, completed and failed checks, remaining blockers, screenshots/evidence references when available, and the next concrete iteration. Update STATUS and append WORK_LOG. Record new user-accepted decisions only if there are any. Keep the report concise enough for the planning chat to review.

Finish with a plain-language result and a link to that build report. I will return to the planning chat to review the actual result and prepare the next change request.
