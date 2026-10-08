# AI production toolchain

Researched 2026-10-07. Recommendations are project-specific, not a claim that any product is universally best. Connection states live in STATUS.md.

## Recommended starting stack

| Work | Tool | AI connection | Why use it here |
| --- | --- | --- | --- |
| Planning, story, code, coordination | Codex with workspace Markdown | Workspace files, shell, MCP | Already available; one assistant can maintain context and implement work |
| Source editing | Existing VS Code | Codex can edit the same workspace; IDE extension optional | No additional paid coding subscription needed initially |
| Live Unreal editing | Unreal Engine 5.8 native Unreal MCP | Local HTTP endpoint from editor | Epic-provided option to try first |
| Repeated Unreal asset tasks | Python Editor Script Plugin / Editor Scripting Utilities | AI-written source scripts executed by editor | Repeatable imports, inspections, naming, scene setup |
| Gameplay | Blueprints and C++ as needed | AI authors source and supported editor operations; compile/play-test | Python editor automation is not packaged gameplay logic |
| Blender | Blender 5.2.1 LTS plus MCP for Blender | Local add-on socket plus stdio MCP server | Scene inspection/editing, materials, scripted cleanup and export |
| Initial 3D assets | Existing Meshy account | Blender bridge now; official Meshy MCP/API if authenticated later | Reuse user's experience and assets |
| Voice production | ElevenLabs, when account access confirmed | Official creative MCP or API | Planned character dialogue pipeline |
| Cinematics | Unreal Sequencer; Higgsfield deferred | Game assets in engine; generated video later | User has no Higgsfield account and does not want to pay yet |
| History/backups | Git, later Git LFS and backup destination | AI records text/source changes and asset provenance | Reversible work and recoverable project state |

## Blender setup and verification

Installed Blender: `C:/Program Files/Blender Foundation/Blender 5.2/blender.exe`, version 5.2.1 LTS.

An existing Codex server used `cmd` with a bare `blender-mcp` argument. Replaced with the actual uvx executable and pinned package `mcp-for-blender==2.1.9`. Minimal setup:

```toml
[mcp_servers.blender]
command = 'C:\Users\alexa\AppData\Local\Programs\Python\Python312\Scripts\uvx.exe'
args = ["--from", "mcp-for-blender==2.1.9", "mcp-for-blender"]
env = { DISABLE_TELEMETRY = "true" }
```

Registered via Codex CLI in the user's existing global MCP configuration. Existing Blender add-on found enabled. Its protocol was older than the server; the package installer updated it and preserves a backup. See STATUS for final verification.

The add-on needs a GUI Blender process; background Blender is appropriate for standalone scripts but cannot service this add-on's live command loop. Only use one agent connection at a time for a given scene. A separate protocol client can verify it before tools load into a new Codex session.

`tools/blender_probe.py` checks standalone script execution and writes `reports/blender_probe.json`. `tools/verify_blender_mcp.py` performs MCP initialization, tool discovery, and a live scene query. By default it does not modify scene content. With `--write-test` it creates/moves a temporary mesh, saves a separate scene copy in reports, and removes the mesh to restore the object count. Both modes passed on 2026-10-07.

Source: [MCP for Blender upstream setup](https://github.com/ahujasid/mcp-for-blender). This is a third-party integration, not a Blender Foundation product.

## Unreal connection procedure

Historical initial search found no engine; this was superseded by the verified Unreal 5.8.3 installation and local project documented below.

For Unreal 5.8:
1. Install/open the engine and create a small First Person project. Record its actual location/version.
2. Enable **Unreal MCP** and **All Toolsets** in Edit > Plugins; restart. Enable Python Editor Script Plugin / Editor Scripting Utilities when needed for scripts.
3. In Editor Preferences > General > Model Context Protocol, enable Auto Start Server, or run `ModelContextProtocol.StartServer` in the editor console.
4. Confirm the Output Log reports the endpoint, normally `http://127.0.0.1:8000/mcp`.
5. Run `ModelContextProtocol.GenerateClientConfig Codex` from the project, or register the confirmed local URL through Codex's MCP settings. Preserve existing configurations.
6. Start/reconnect the agent after the editor. Discover available toolsets; first inspect selection/actors, then test one reversible scene change, save and verify.

Epic labels this experimental; capabilities must be checked, not assumed. It needs toolsets enabled in addition to the MCP plugin. Calls must be sequential. Keep the endpoint local: it has no authentication and is not designed for remote exposure. Do not expose it on the servers.

If a required Blueprint/animation operation is missing, extend an editor toolset or evaluate an additional integration in a test project. Do not install multiple overlapping bridges before a demonstrated need.

Paid alternative to evaluate later: Aura, formerly associated with Flopperam. Its product claims require an actual task trial and current compatibility/pricing check before purchase. Older chongdashu/unreal-mcp describes itself as experimental; it is not our default when Epic's native bridge is available.

Sources: [Epic Unreal MCP](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-mcp-in-unreal-editor?application_version=5.8), [Epic Python scripting](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python), [Aura](https://www.tryaura.dev/), [experimental community Unreal MCP](https://github.com/chongdashu/unreal-mcp).

## Meshy: current access and next connection

User confirms they have Meshy. A Meshy extension exists in Blender's installed extensions. Existence does not prove account authentication, bridge operation, or API access.

Two different connections:
- Meshy's Blender plugin transfers assets between the web workspace and Blender.
- Meshy's official MCP exposes generation/task/download tools to an AI coding client and requires MESHY_API_KEY.

Do not ask for a key pasted into chat. Set it locally through a suitable secret/environment mechanism. Before enabling generation, confirm API access and credit costs for this account; owning a web subscription is not proof that API generation is included. Start with account/task inspection and an existing asset transfer, without creating a paid task.

An initial restricted-environment Blender probe failed to write the Meshy extension's log. This was a permissions limitation during that probe, not proof the extension is broken in normal Blender. Verify the normal session before changing it.

Sources: [Meshy official AI integration](https://docs.meshy.ai/en/api/ai), [Meshy MCP setup](https://www.meshy.ai/mcp), [Meshy integrations](https://www.meshy.ai/integrations).

## Voices and cinematics

ElevenLabs is desired, but account/API connection is not confirmed. Its official MCP includes creative capabilities; verify the actual available speech tool and authentication before use. No voice generation was submitted.

Higgsfield is deferred by the user's explicit instruction: no account yet and no payment now. An integration was discovered and suggested before this clarification, but nothing was installed or connected. Do not repeat that suggestion or treat it as a blocker.

Source: [ElevenLabs creative/agents MCP](https://elevenlabs.io/mcp).

## Repeatable production loop

Brief -> story/design reference -> generate or reuse asset -> inspect in Blender -> clean up/scale/export -> import into Unreal -> implement gameplay -> inspect/play-test -> record outcome.

Each asset should eventually track its name/ID, brief, prompt, source service/task, date, license/access evidence, generation settings, Blender source, export, Unreal destination, and QA result. Initial checks: correct scale, readable silhouette, triangle count, texture/material count, collision, and character skeleton/animation compatibility. A face-count limit alone is not a performance guarantee.

## New-chat continuity

### Wreckage build verification — 2026-10-07

The existing Unreal 5.8.3 project now has actual saved prototype assets. Fresh MCP scene queries, Blueprint edits/strict compilation, map saving, and Play-In-Editor are exercised through the existing client. See LEVEL_01_BUILD_REPORT.md and reports/wreckage_playtest.json for results and limits. The user resolved a Restore Packages dialog; keep one responsive editor open. Sequential hidden external client helpers were needed because this restricted shell could not reliably access the live bridge. The loopback endpoint and historical verification evidence were preserved.

Authoring uses native editor Python and BlueprintGraphEditor APIs. Runtime gameplay is Blueprint. Engine-bundled Python is 3.11.8; the external MCP client uses Python 3.12 and mcp 2.3.0. A C++ compiler/Windows SDK was not available; no C++ compilation or packaged build is claimed. Native tool wrappers can suppress Python exceptions into logs, so authoring enables exception propagation and treats Blueprint warnings as errors. The client's HTTP 202 termination warning persists after successful calls.

AGENTS.md instructs project chats to load goals/status/story/toolchain and log meaningful work. It is not a transcript archive or universal memory. New chats must use this project folder. For outside chats, provide HANDOFF plus current status/relevant files.

Sources: [official AGENTS.md behavior](https://developers.openai.com/codex/guides/agents-md), [official Codex MCP configuration](https://developers.openai.com/codex/mcp).

## Verified Unreal connection update — 2026-10-07

Installed Unreal 5.8.3; local setup project: Unreal/LostVanguard/LostVanguard.uproject. Enabled native ModelContextProtocol (friendly name Unreal MCP), AllToolsets, PythonScriptPlugin, EditorScriptingUtilities. DefaultEditorPerProjectUserSettings enables automatic server startup and tool discovery. HTTP server explicitly binds to 127.0.0.1 in DefaultEngine.ini.

Global Codex unreal MCP registered at http://127.0.0.1:8000/mcp. The editor must remain running; a new Codex chat/restart may be required for tool exposure. Protocol client verified initialization, three discovery/meta-tools, live scene query, temporary actor creation/find/removal and empty search afterward. This does not verify all discoverable toolsets or gameplay.

Client: tools/unreal_mcp.py, MCP Python SDK 2.3.0 pinned in script metadata. Run with uv; calls must remain sequential. Report: reports/unreal_mcp_verification.json. Current chat uses this separate client because native Unreal tools were not dynamically loaded here.

Initial AllToolsets startup warning required a GameFeatureData asset-manager scan rule. Added to DefaultGame.ini per installed GameFeaturesEditor source; validate next editor startup. SDK emits a session termination HTTP 202 warning despite successful requests. Save/reload, asset imports, packaged builds, and gameplay remain untested.
