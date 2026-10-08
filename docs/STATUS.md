# Current status

Updated: 2026-10-07 (America/Los_Angeles).

## GitHub setup - 2026-10-07

User selected `https://github.com/alexandergazzard-beep/Praetorian` for this project. Local Git repository initialized on `main`, origin configured, Git LFS 3.7.1 installed locally, and binary asset rules added. Git 2.53.0.windows.1 is installed. Remote branch inspection succeeded and returned no refs (empty repository). Initial upload prepared; push verification is pending. See SOURCE_CONTROL.md for included files, exclusions, and routine commands. Generated Unreal working folders, temporary files, local assistant settings, and credentials are excluded. Automated credential-pattern scan of the 194 candidate files found no hits; no file exceeded 100 MiB.

## Shareable project package - 2026-10-07

Created `output/pdf/Lost_Vanguard_Story_Script.pdf` (six pages: first-mission scene/dialogue draft, proposed opening campaign arc, spoiler background) and `output/pdf/Lost_Vanguard_Project_Overview.pdf` (two pages: premise, cast, supplied visual reference, actual prototype screenshot, progress and next step). Editable text: `SHARE_SCRIPT.md` and `FRIEND_PROJECT_BRIEF.md`. New staging/dialogue remain proposals; no creative canon changed. Both PDFs were rendered and all eight pages visually checked. The overview distinguishes the 19-check verified baseline from the opening variant whose route check remains pending in its report. Package is ready for the user to share; no external message was sent.

## Current focus

The first Wreckage editor prototype and an image-led opening variant now exist in the existing LostVanguard project. Latest map: `/Game/WreckagePrototype/Maps/L_Wreckage_Opening`; the tested `/Game/WreckagePrototype/Maps/L_Wreckage_Playable` is preserved. The opening adds a dark hull frame, a larger wreck focal point, cool forest proxies, rocks/plants/cables, localized fires, rising smoke proxies, haze, and controlled lighting. Both maps retain the runtime recovery, weapon, two searchers, clue, communications, and exit loop. All 19 recorded route checks pass on the opening variant. See OPENING_VISUAL_BUILD_REPORT.md and LEVEL_01_BUILD_REPORT.md for evidence and test limits. Finished art, recorded voices, and cinematics remain deferred. STORY_BIBLE version 43 records the accepted reference and early-view timing; exact staging/designs and implementation dialogue remain proposals.

Established overview: Evan is a Praetorian, leader with presence and instinct, created by Meridian's forced experiments and rescued by humans. Companion Clank has EMP-damaged memories. Orison contains extinct-civilization ruins. Meridian wants to stabilize its evolved identity and destroyed Evan's ship mistakenly believing it held an artifact; it did not. Creators secretly moved the artifact. Humans and creators already fight after Meridian attacks using seized creator ships. Named officers are separate Commander Dorian Vale and Major Lena Cross; duties open. Two other fleet Praetorians have proposed scout/sniper and heavy roles. Details and unresolved questions are in STORY_BIBLE.

### Unreal installation request
User authorized installation on 2026-10-07 and completed Epic sign-in directly. Unreal Engine 5.8.3 is installed at `C:/Program Files/Epic Games/UE_5.8` on the NVMe. Existing project: `Unreal/LostVanguard/LostVanguard.uproject`, with Unreal MCP, All Toolsets, Python, and editor scripting enabled. Initial setup verified temporary actor read/create/find/remove and registered the global Codex connection at 127.0.0.1:8000. Subsequent builds use this same project and bridge. Latest map and configured startup map: `/Game/WreckagePrototype/Maps/L_Wreckage_Opening`.

Initial setup verification is preserved in reports/unreal_mcp_verification.json. The build pass verified fresh native scene queries and actual editor operations through the existing loopback client. MCP Python client 2.3.0 still logs a session-termination HTTP 202 warning although tool calls succeed. The restricted shell required hidden external helper processes to reach the live editor reliably. See the build report for current evidence and limitations.

## Completed

- Created persistent Markdown project records and AGENTS.md entry instructions.
- Transferred current story bible with established/proposed/open separation.
- Recorded goals, hardware, user experience, accepted decisions, and new-chat handoff.
- Verified Blender 5.2.1 LTS, VS Code, Git, Node, Python, uv, and Codex are installed.
- Repaired existing global Codex Blender MCP launch command; package pinned to mcp-for-blender 2.1.9.
- Updated enabled Blender add-on using upstream installer with backup preservation.
- Started a Blender test instance quietly (PID 16424 at launch; process IDs are temporary).
- Verified MCP initialization, nine advertised tools, and a live scene query. Verification report: reports/blender_mcp_verification.json.
- Verified AI editing: created and moved a temporary mesh, saved a separate .blend copy, then removed the mesh and restored the original three-object count. Test copy: reports/blender_connection_test.blend.
- Confirmed Meshy Blender extension is installed; account bridge and API credentials remain unverified.
- Researched Epic's native Unreal 5.8 MCP and prepared a disabled reference configuration.

## Connection states

| Connection | State | Remaining work |
| --- | --- | --- |
| Coding / workspace | Working | Run relevant checks as source code grows; version-control setup later |
| Standalone Blender Python | Verified | Apply to actual asset tasks |
| Blender MCP | Configured; live read/edit/save/cleanup verified by test client | Codex may need a new session/restart for tools to appear |
| Unreal MCP | Fresh live queries, saved map/graph edits, strict compilation, PIE, and saved-map reload verified | Tools are not directly exposed in this chat; use documented fallback and keep one responsive editor open |
| Meshy Blender bridge | Extension installed, user has account | Verify normal GUI transfer of an existing asset |
| Meshy MCP/API | Documented, not connected | Local API authentication/access and cost check; no paid generation yet |
| ElevenLabs | User confirms paid subscription; connection unverified | Confirm tier/API access; authenticate; test when authorized |
| Higgsfield | Deferred by user | No installation, account, payment, or generation needed now |

## Important findings

Unreal 5.8.3 is installed. The existing project now contains the Wreckage prototype. Native MCP requires a responsive editor; recovery dialogs can prevent requests from completing. The user resolved the Restore Packages dialog during this build pass.

Blender GUI must remain running for live MCP. The current chat does not have Blender MCP tools dynamically exposed; verification used a separate protocol client. Registered configuration is not proof that every future chat can see the tools without restart.

The background probe hit a Meshy log-write restriction in the sandbox. Do not assume it is a normal-session Meshy failure. The old Blender add-on/server protocol mismatch was repaired.

## Next actions

1. Compare the opening screenshot in OPENING_VISUAL_BUILD_REPORT.md with the saved reference; review breach size, wreck placement, forest density, and lighting.
2. Play the opening map by hand to assess mouse/keyboard feel, normal-health combat balance, collision, readability, pacing, and performance. Automated remote route tests use extra temporary health outside the normal-health death check.
3. Resolve Clank's retained objective, survival/shielding, and search-party identity when implementation needs them.
4. Plan visual alternatives before finished asset production; use existing assets where suitable.
5. Validate Meshy/Blender/Unreal transfer and establish backups before substantial asset accumulation.
6. Choose cinematic tools later; no cinematic construction or paid generation now.

Read TOOLCHAIN.md for concrete setup details. Keep this document current after work.

For the user's proposed one-prompt game starter, read PROTOTYPE_WORKFLOW.md. The workflow is planned; current missing connections still apply.

Coordination options researched: existing Codex as initial coordinator, optional self-hosted n8n later. Provider subscription/API billing must be verified per account; see TOOL_REVIEW. No new orchestrator installed or connections activated.

Claude subscription confirmed: Pro. Includes Claude Code access; Console API billing is separate. No Claude orchestration connection has been tested.


Gemini currently uses the free plan. A student Google AI Pro upgrade is a future possibility reported by the user, not activated or verified. No Gemini connection configured; API entitlement unverified.

## Historical planning and editor check — 2026-10-07

Prior native MCP read/create/find/remove verification remains valid historically. This pass launched the editor and observed a loopback listener. A fresh toolset-discovery request did not return and was cancelled. TCP reachability alone is not a verified working editor connection; cause remains unverified. No level assets were changed. Current editor process may remain open. Save/reload, startup-warning resolution, and gameplay are still pending.

Story and production proposals are recorded in LEVEL_01_WRECKAGE and FIRST_LEVEL_BUILD_PLAN. Cinematic plans contain draft intent only. User has not chosen final visual designs, physics tuning, or cinematic software.

## Historical build-chat handoff — 2026-10-07

User accepted the staged first-level plan and requested a copyable prompt for a separate local build chat, followed by review here. LEVEL_01_BUILD_PROMPT.md is ready; no other chat was created or messaged. The prompt requires fresh editor verification, actual gameplay work, and LEVEL_01_BUILD_REPORT.md for review. Shared files provide continuity when the new chat uses this workspace. No build has started from this prompt yet.

Build prompt now includes explicit existing Unreal connection instructions and protocol-client fallback; current responsiveness still needs verification in the build chat.

## Opening visual reference — 2026-10-07

Saved user-supplied image unchanged at assets/references/level_01/opening_wreck_alien_forest_reference.png; copy verified against source using SHA-256. User wants approximately this starting environment: dark broken hull framing burning wreck in alien forest. Linked in bible, level draft, and build prompt. Exact layout/sky/character appearance remain open; no Unreal asset changes.

Image-led opening prompt available: docs/OPENING_VISUAL_BUILD_PROMPT.md. It guides building/refining the reference composition and checking it from Evan's viewpoint; no engine changes made by this prompt-writing task.

## Opening visual build — 2026-10-07

The subsequent implementation creates L_Wreckage_Opening through native editor APIs, with the previous tested map preserved. The final map saves and reloads; its full 19-check route passes, including actual combat damage, death/restart, clue retention, communications, and gated completion. Starting-view captures and detailed limitations are in OPENING_VISUAL_BUILD_REPORT.md. No paid generation or finished cinematic. The current task updates shared records directly; no other chat was created or messaged.
