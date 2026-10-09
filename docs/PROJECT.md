# Project goals

Updated: 2026-10-07 (America/Los_Angeles).

## Vision

Create an original game with the military science-fiction scale and mystery that the user enjoys in Halo, while developing distinct characters, designs, factions, and lore. Also create animations and mission cinematics. Working title: Lost Vanguard.

## User experience

The user is new to game development. Their existing experience is a Roblox RTS project and many Meshy-generated assets kept below approximately 10,000 faces. Provide practical explanations and achievable milestones without limiting the long-term creative vision.

## Current priority

Refine the first level's opening around the supplied dark-hull/forest/wreck reference while preserving its working gameplay. Review route, player feel, physics, and small asset needs before making the full world or finished characters. Cinematic construction is deferred; software is undecided. Maintain durable Markdown records so future project chats understand goals, decisions, story, setup, and progress.

## Goals and completion evidence

| Goal | Completion evidence | State |
| --- | --- | --- |
| Persistent project context | AGENTS.md and maintained project/story/status/log files | Created; ongoing maintenance |
| AI-assisted coding | Agent can edit project source and run relevant checks | Workspace editing works |
| AI-assisted Blender | Inspect scene, perform a reversible edit, save, and verify | Verified through MCP test client; new Codex session may be needed |
| AI-assisted Unreal | Connect to live editor, inspect a level, make a reversible edit, and verify | Fresh live queries and actual saved map/Blueprint edits verified; see build report |
| Repeatable asset workflow | One Meshy asset passes Blender cleanup and Unreal import checks | Planned |
| Voices and cinematics | One scripted exchange and short scene imported into a test mission | Planned |
| First playable mission | Small wreck opening with recovery, companion lines, combat, and a search clue | Saved editor prototype exists; verification and limits in LEVEL_01_BUILD_REPORT.md |

## Production preferences

- Unreal Engine 5.8.3 is installed and a local setup project has launched; verification details are in STATUS.
- Blender for asset preparation and scenes.
- Meshy for initial 3D assets; user has existing experience and assets.
- ElevenLabs for character voices.
- Higgsfield for generated cinematic footage between missions and at selected objectives.
- Consider Unreal Sequencer for cinematics that use the game's own assets.
- AI should help plan, generate, implement, inspect, and iterate. The user retains creative decisions.
- No subscription budget or purchase authorization has been established.
- User confirms existing Meshy and ElevenLabs subscriptions. User has no Higgsfield account and explicitly defers paying for it; keep Higgsfield optional.
- Latest clarification: user pays for Meshy, Claude Pro, OpenAI, and ElevenLabs. Other plan tiers and account-specific API access/billing remain unverified. Higgsfield is a possible later purchase.

## Hardware verified in prior session

PC: Ryzen 7 5800X (8 cores / 16 threads), RTX 3080 Ti, 32 GB RAM. Samsung 980 PRO 2 TB NVMe with about 600 GB free at inspection. Additional HDDs approximately 4 TB and 1 TB. Keep active development on NVMe; capacity readings are snapshots.

socialpost: Linux, i7-8086K, approximately 64 GB RAM, RTX 3060 12 GB; large storage volumes available. Candidate backup/processing machine.

alexserver: Linux, Core Ultra 7 265K, approximately 64 GB RAM, Intel integrated graphics; system volume had about 53 GB available. Candidate automation/services machine.

Server access details remain in the user's separate SSH configuration. Do not copy credentials into this repository. Servers do not automatically accelerate the local Unreal editor.

## Open production decisions

Paid-tool budget, final asset style, cinematic production software, and whether the game ever needs model-driven NPC dialogue during play. User selected the Praetorian GitHub repository for project version control on 2026-10-07; upload verification is recorded in STATUS. A separate backup for local generated files remains open. Engine and local setup project are recorded in STATUS.


## Additional AI service — 2026-10-07
- User currently uses free Gemini. They expect a possible Google AI Pro upgrade through a student offer; upgrade and eligibility are not verified. API access and billing remain unconfirmed.



## Player movement target - 2026-10-08
User wants Halo 3 or Halo Reach movement/jumping feel, explicitly no fall damage. Primary reference and numerical tuning remain open; hands-on comparison required.
