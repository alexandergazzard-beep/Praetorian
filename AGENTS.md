# Lost Vanguard: instructions for project assistants

This workspace is the shared project record. Read these files before substantive work:
1. `docs/PROJECT.md` for the user's goals, experience, and scope.
2. `docs/STATUS.md` for verified progress, connection states, and next actions.
3. `docs/STORY_BIBLE.md` for established story facts versus proposals.
4. `docs/TOOLCHAIN.md` when working on software, integrations, or production.
5. The latest entry in `docs/WORK_LOG.md` and relevant entries in `docs/DECISIONS.md`.

The user is a beginner building an original military science-fiction game and animations. They want AI involved throughout production and currently prioritize efficient tools and connections over building the first mission. Explain work in plain language and help them learn through concrete results.

Maintain continuity: update STATUS after meaningful work; append dated entries to WORK_LOG with changes, checks, limitations, and next steps. Record accepted durable decisions in DECISIONS. Update STORY_BIBLE when the user establishes or changes story facts. Never turn assistant suggestions into established facts without user acceptance. Preserve superseded decisions in the log rather than treating them as current.

Do authorized reversible work autonomously. Do not claim a tool is connected from configuration alone: distinguish researched, configured, reachable, and verified end-to-end. Check current official documentation for software compatibility. Document actual installed versions and test results.

Use editor APIs for Unreal assets; do not edit .uasset/.umap binary files or move them through filesystem operations. Use source scripts, supported editor tools, Blueprints, and C++ where appropriate. Validate editor changes by inspection, compilation, and a relevant play test. Keep Blender source scenes and exported game assets distinct.

Preserve existing work and configurations. Do not store passwords, API keys, tokens, private keys, or authentication links in project records. Keep local editor bridges on loopback. Purchases, paid generations, and external publishing require a concrete user instruction or existing authorization. Development assistance is the current AI goal; AI-driven NPC dialogue at runtime is not yet a requirement.

Do not spawn subagents unless the user explicitly requests delegation. Keep notes focused and current rather than duplicating full chat transcripts. For chats outside this workspace, provide docs/HANDOFF.md as a portable introduction; do not promise automatic memory outside this project.
