# Lost Vanguard / Project Big

An original military science-fiction game and animation project developed with AI assistance throughout the production process.

Start with [Project goals](docs/PROJECT.md), [Current status](docs/STATUS.md), and [Story bible](docs/STORY_BIBLE.md).

- [AI tools and connection plan](docs/TOOLCHAIN.md)
- [Opening scene and tutorial outline](docs/OPENING_SEQUENCE.md)
- [One-prompt prototype workflow](docs/PROTOTYPE_WORKFLOW.md)
- [Additional tool recommendations](docs/TOOL_REVIEW.md)
- [Accepted decisions](docs/DECISIONS.md)
- [Work log](docs/WORK_LOG.md)
- [New-chat handoff](docs/HANDOFF.md)

Open new Codex chats against this same project folder so AGENTS.md can direct them to the current records. A chat outside this folder needs the handoff and relevant files supplied explicitly.

Current priority: refine the playable Wreckage opening and its forest/wreck composition, then review movement, combat, readability, and pacing before replacing temporary assets.

## Share the project

- [Project overview PDF](output/pdf/Lost_Vanguard_Project_Overview.pdf): premise, characters, reference art, actual prototype screenshot, and progress.
- [Story script PDF](output/pdf/Lost_Vanguard_Story_Script.pdf): first-mission dialogue and proposed opening campaign arc; contains spoilers.
- [Editable story script](docs/SHARE_SCRIPT.md)
- [First-level build report](docs/LEVEL_01_BUILD_REPORT.md)
- [Opening environment report](docs/OPENING_VISUAL_BUILD_REPORT.md)

Story proposals are labeled separately from accepted facts. Reference art shows the intended atmosphere; screenshots show the actual rough prototype.

## Open the Unreal prototype

Clone this repository with Git LFS installed, then run `git lfs pull`. Open `Unreal/LostVanguard/LostVanguard.uproject` using the recorded Unreal Engine 5.8.3 installation. The current startup map is `/Game/WreckagePrototype/Maps/L_Wreckage_Opening`. See the build reports for controls and verification limits. This is an editor prototype, not a packaged game.

Saved maps, Blueprints, materials, and other game assets are tracked with Git LFS. Unreal generates its cache, intermediate, and saved working folders locally. Credentials and local assistant settings are excluded.

[Git workflow and backup scope](docs/SOURCE_CONTROL.md)
