# Claude task: first-mission gameplay and dialogue review

Copy the text below into Claude. If Claude cannot access this workspace, attach docs/HANDOFF.md and the documents named below. Include the source builders if you want source-level findings; without them, request a document review only.

---

We are building Lost Vanguard, an original military science-fiction game. I am working on environment assets with Codex. Your separate task is to review and improve the design of the existing first mission, so we have a concrete gameplay polish plan ready when the assets are integrated.

Read AGENTS.md, docs/PROJECT.md, docs/STATUS.md, docs/STORY_BIBLE.md, docs/TOOLCHAIN.md, the latest docs/WORK_LOG.md entries, relevant docs/DECISIONS.md entries, docs/LEVEL_01_WRECKAGE.md, docs/LEVEL_01_BUILD_REPORT.md, and docs/OPENING_VISUAL_BUILD_REPORT.md. Inspect relevant source builders if accessible. Reconcile older report limitations with the latest status and repairs.

The opening prototype already exists. I have personally completed the level, with some rough spots that I have not yet listed. Movement bindings and the obscured spawn view were repaired. Physical movement and my route completion are user-reported; the earlier automated route checks do not prove current control feel, normal-health balance, or performance.

Produce one proposed first-mission polish brief, saved as docs/CLAUDE_MISSION_REVIEW.md if you have workspace access, or returned as a document if you do not. Include:

1. A short review of recovery, movement tutorial, weapon acquisition, search-party encounter, clue, communications, and exit. Identify where objectives, route cues, pacing, or feedback may confuse a first-time player. Separate observed source/document findings from hypotheses needing a playthrough; do not invent experienced bugs.
2. The five highest-priority improvements. For each, give the evidence, player benefit, a small implementable change, and a clear completion check. Prefer polishing the existing loop over adding new systems or expanding the level.
3. A compact proposed Clank dialogue pass, organized by gameplay trigger. Keep lines short, useful, and consistent with damaged memories, restrained military tone, and dry humor. Label all new lines and staging as proposals; do not reveal facts Clank cannot know or settle open lore.
4. A 10–15 minute human playtest checklist covering physical controls, recovery, collision, route readability, normal-health combat, objective progression, death/restart, and completion. This is a checklist to run later, not evidence that testing happened.
5. Only the creative questions that actually block this polish pass, with optional proposed answers clearly labeled.

While Codex and I work on assets, read existing project files but write only your new review document. Do not edit shared status/log/story files, Unreal maps or Blueprints, Blender scenes, asset files, source builders, or configuration. Do not control the live editors. Do not generate paid content, install tools, or publish. Report inaccessible files and checks you could not perform. Explain recommendations in plain language for a beginner.

Finish with three small implementation tasks that Codex can take on after we review your brief.
