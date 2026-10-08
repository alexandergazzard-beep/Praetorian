# From one prompt to a playable prototype

Created: 2026-10-07. Proposed workflow, not a promise of a finished game from one generation.

## Objective

Enable one user brief to start a multi-step AI production run: design a small experience, assemble assets, implement gameplay, inspect results, play-test, fix errors, package a build, and record the outcome. This refers to development assistance, not live model-driven NPC behavior in the released game.

## Required connections

| Capability | Connection | Evidence needed |
| --- | --- | --- |
| Design and continuity | Codex + project Markdown | Reads canon, goals, current status; writes mission brief without silently establishing new story facts |
| Code and files | Workspace editing, command runner, Python; C++ toolchain when needed | Can generate source, build/check it, read logs, repair failures |
| Unreal editor control | Epic Unreal 5.8 MCP and enabled toolsets | Discover tool schemas, inspect actors/assets, create/edit/save through supported editor operations |
| 3D generation/retrieval | Meshy official MCP/API or existing local exports | Authentication verified; retrieve/download assets; generation only with a defined credit budget |
| Asset preparation | Blender MCP + bpy scripts | Inspect/clean/scale/export, inspect output, preserve editable source |
| Rigging and motion | Meshy rig/animation API plus Unreal retargeting/animation tools | Skeleton compatible; actual movement verified in engine; generator output alone is insufficient |
| Voices, effects, music | ElevenLabs supported MCP tools/API or existing licensed audio | Account/tool access verified; files downloaded, imported, audible at correct moments |
| Cinematics | Unreal Sequencer editor tools/scripts | Camera, animation, dialogue timing work with in-game assets; Higgsfield deferred |
| Verification | Editor logs, compile checks, screenshots/renders, automation/play tests | AI observes the result rather than trusting tool success; builds launch outside editor |
| History | Git, Git LFS for large assets, asset manifest, work log | Changes recoverable; asset sources/settings tracked; next chat can resume |

Installed VS Code is useful as a human source editor, but adding another paid AI editor is not a prerequisite. Existing servers are optional workers/storage, not required editor bridges. Unreal's local MCP must not be exposed on those servers.

## What the agent does after the prompt

1. Read project goals, canon, and connection status.
2. Write a short mission brief, asset list, and concrete success checks.
3. Build a functional layout from simple shapes and existing template mechanics.
4. Reuse existing assets first; generate missing assets only within the authorized budget.
5. Prepare models in Blender and import using Unreal editor APIs.
6. Implement interactions, objectives, companion behavior, combat, interface, and audio.
7. Configure required animation states and test skeleton compatibility.
8. Observe the level, compile, run a play test, and fix issues.
9. Package a Windows build once gameplay works and required packaging tools are present.
10. Update STATUS, WORK_LOG, asset manifest, and verification evidence.

Unreal native MCP is experimental; inspect available tools before promising complete Blueprint graph authoring, animation setup, or packaging. Add a focused editor extension or C++ implementation only for demonstrated gaps. Python editor scripting does not replace runtime gameplay logic.

## Initial asset tracking

Track: asset ID, purpose, source/provider/task, prompt, creation date, license/account evidence, generation settings, Blender source, exported files, Unreal destination, and QA state. Do not record keys or tokens. Track expensive tasks and avoid repeated paid generation loops.

## Historical example starter prompt — superseded

The fortress example below is retained as history, not the current build target. Use LEVEL_01_BUILD_PROMPT.md for the current wreck opening and FIRST_LEVEL_BUILD_PLAN.md for staged scope. Cinematic construction is deferred.

Build a small single-player first-person Lost Vanguard prototype in this workspace. Read AGENTS.md and the project records first. Treat the following mission events as prototype proposals, not new story canon.

Create a five-minute abandoned-fortress segment: the player explores three rooms, their robot companion delivers one line, a switch restores power and opens a door, a small enemy encounter follows, and a terminal reveals the ship's loss. Use template gameplay, existing Meshy assets, and placeholder audio/art where needed. Do not start paid generations or buy services.

First create a mission brief and asset checklist. Build the functional layout, then replace placeholders. Use the connected Unreal and Blender tools; inspect available capabilities and report missing connections accurately. Verify movement, shooting, interaction, objective order, audio triggers, enemy behavior, and restart after death. Fix failures and package a Windows build if the required tools are available. Save editable sources and update project status, decisions, work log, and asset records. Do not mark the result complete without testing it.

## Current readiness

Project records and workspace coding are available. Blender was verified through a separate MCP client for read/edit/save/cleanup; a Codex restart may be needed for chat tool discovery. Unreal 5.8.3 is installed and the existing setup project previously passed temporary actor read/create/find/remove checks. Latest reconnect reached a loopback listener but toolset discovery did not complete; current editor responsiveness, map save/reload, and gameplay still require verification. Meshy and ElevenLabs subscriptions exist; bridge/API access unverified. Higgsfield spending and cinematic construction are deferred.

## Sources checked 2026-10-07

- [Epic Unreal MCP](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-mcp-in-unreal-editor?application_version=5.8)
- [Meshy AI tools including rigging/animation](https://docs.meshy.ai/en/api/ai)
- [Unreal auto retargeting](https://dev.epicgames.com/documentation/en-us/unreal-engine/auto-retargeting-in-unreal-engine)
- [ElevenLabs MCP](https://elevenlabs.io/mcp)
- [ElevenLabs sound effects](https://help.elevenlabs.io/hc/en-us/articles/25735182995985-What-is-Sound-Effects)
- [ElevenLabs music API](https://elevenlabs.io/docs/api-reference/music/compose/)
