# Meshy connection

Prepared 2026-10-07 at user's request. User reports 5,000 monthly credits; exact tier and usable API balance remain unverified.

## State

Official @meshy-ai/meshy-mcp-server 0.6.0 installed in ignored tmp/meshy-connector with npm 11.9.0, Node 24.14.0. Package requires Node >=18. Installation skipped package lifecycle scripts. Global Codex server `meshy` registered through Codex CLI; existing blender/unreal entries preserved. Authenticated initialization, discovery of 24 tools, and a read-only balance call succeeded on 2026-10-07: **4,229 available API credits**. Evidence: reports/meshy_mcp_verification.json. This does not establish the funding source or auto-recharge settings. No generation submitted; download/Blender/Unreal asset workflow remains unverified.

## User setup

1. Open Meshy's Developer Platform API Keys page in your browser; sign in yourself if needed.
2. Create a project-specific API key. A monthly limit of 200 credits is an optional small initial allowance, covering the proposed three-prop trial with room for some extra processing; this limit has not been set.
3. Paste the key into the local **Connect Meshy to Lost Vanguard** masked window and choose **Save key**. Do not paste the key into chat or project files.
4. Tell the assistant the key is saved. Run the read-only verification before submitting generation. Codex may need a new chat/restart to expose a newly registered server.

The local entry window was launched during setup. To reopen it, run tools/set_meshy_key.ps1 with Windows PowerShell. The helper stores a Windows-user-encrypted credential outside this repository, under LocalAppData/LostVanguard/Meshy. tools/start_meshy_mcp.ps1 decrypts it for the connector process; the global config and project source contain no key.

## Checks

- Both PowerShell helpers parse without syntax errors; Python verification source compiles.
- Environment presence checks found no Meshy API key in process, user or machine variables at setup. No values were printed.
- tools/verify_meshy_mcp.py initializes the official stdio server, discovers tools and calls only meshy_check_balance. It suppresses raw server error output, records a sanitized failure if needed, and never generates or purchases.
- Authenticated initialization and balance passed. Model download, Blender transfer and Unreal import remain pending. No generation submitted.
- Save retry: explicitly load and qualify Windows encryption commands before the Forms callback. The launcher uses the equivalent Windows DPAPI API directly because module import from the Python child process produced duplicate type-data errors. The verification helper uses the pinned MCP 2.3.0 snake-case result fields.

## Reinstallation

2026-10-08 actual 3D verification: two explicitly authorized Smart Topology image-to-3D jobs succeeded, downloaded GLB/PBR maps, and passed Blender-to-Unreal integration. M17 task 01a11a81-d75d-7713-a07e-c3ee4ff0dd5a and S04 task 01a11a83-5a57-7471-a6ee-a502fdf8f28c consumed 15 credits each. Read-only balance after completion: 4,190. No new purchase. See DEBRIS_FIRST_PAIR_BUILD_REPORT.md; historical pending statements below no longer describe the current pair.

Generation verification, 2026-10-07: explicit user authorization covered one Nano Banana Pro text-to-image transport trial. Task succeeded and native image download saved T6 locally. Credits changed from 4,229 to 4,220. Report: reports/meshy_transport_t6_trial.json. The helper tools/meshy_transport_trial.py persists the submission before polling and resumes the same task on subsequent runs; it does not automatically submit another generation. Initial waiting status call failed locally; a read-only status check recovered the completed task without another paid call. 3D generation, Blender transfer and Unreal import remain pending.

The connector package lives in an ignored setup folder and is not backed up by Git. From the project root, reinstall with:

```powershell
npm.cmd install --prefix tmp/meshy-connector --ignore-scripts --no-audit --no-fund --save-exact @meshy-ai/meshy-mcp-server@0.6.0
```

Windows DPAPI storage is tied to this Windows user; recreate a connection securely on another machine. Never commit encrypted or plaintext credentials.

Sources: [Meshy official connector](https://docs.meshy.ai/en/api/ai), [Meshy account/API access](https://docs.meshy.ai/en/api/developer-platform), [Meshy API pricing](https://docs.meshy.ai/en/api/pricing), [official Codex MCP configuration](https://developers.openai.com/codex/mcp).
