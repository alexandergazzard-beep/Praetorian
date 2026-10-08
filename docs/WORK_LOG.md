# Work log

Append meaningful entries with client-local date, task, changes, checks, limitations, and next action. Never store credentials or authentication links.

## 2026-10-07 — Project records and AI toolchain setup

### User intent
Integrate AI throughout the project; prioritize efficient tools and connections for Unreal, Blender, and coding. Record goals and progress in Markdown for future chats. User clarified they have Meshy but no Higgsfield account and do not want to pay yet.

### Work completed
- Created README, AGENTS.md, PROJECT, STORY_BIBLE, DECISIONS, HANDOFF, TOOLCHAIN, STATUS, this log, and starter ignore rules.
- Preserved the current story and explicitly marked unaccepted suggestions.
- Inspected installed tools and standard Unreal installation records.
- Researched official Codex context/MCP, Epic native Unreal MCP/Python, upstream Blender MCP, Meshy MCP/bridge, and ElevenLabs MCP.
- A Higgsfield integration was discovered/suggested before the user's deferral; it was not installed or connected.
- Found an existing enabled Blender add-on and malformed Codex launch configuration.
- Registered the Blender server with absolute uvx path, pinned package 2.1.9, and telemetry disabled in server environment.
- Updated outdated Blender add-on through its installer, which preserves backups.
- Started a quiet Blender GUI instance for connection checks.

### Checks
- Blender version command: 5.2.1 LTS.
- Standalone Python probe: scene inspection succeeded; Meshy log-write failed under restricted execution, not a proven normal-session failure.
- First protocol check reached Blender but the verification script used a different SDK field spelling; corrected the script and reran.
- Installer's Windows terminal output initially hit a Unicode encoding error; reran with UTF-8 and confirmed installation.
- Final read-only protocol check: initialization, nine tools, live scene query succeeded; report saved.
- Edit/save check passed: temporary triangle mesh created/moved, separate .blend copy saved, mesh removed, original object count restored. No production asset was created or overwritten.
- No Unreal install located in standard directory or launcher manifest; no .uproject in workspace.

### Limits and next action
Unreal still needs installation/location and a project. Meshy account/API connection remains unverified. ElevenLabs account status unknown. Higgsfield deferred. Future chats should read STATUS rather than assume all apps are connected.

## 2026-10-07 — Unreal installation requested
- User explicitly authorized installing Unreal.
- Read Computer Use skill and its required guidance/API/confirmation references.
- Confirmed Epic Games Launcher executable exists; selected the uniquely returned launcher window and brought it forward.
- Launcher displays Epic sign-in. Did not operate authentication controls or submit account information.
- Installation has not started. Next action: user signs in directly, then resume engine installation and connection setup.

### Resumed after user sign-in
- User confirmed sign-in; refreshed launcher UI.
- Launcher offered Unreal 5.8.3. Selected standard NVMe location `C:/Program Files/Epic Games/UE_5.8`.
- Accepted required engine setup agreements within the authorized installation scope.
- Reviewed component selections: core, templates/feature packs, engine source; optional debugging symbols and MetaHuman data excluded.
- Started installation; launcher showed 7% installing at first progress check. Completion/launch verification pending.

### Installation observation stopped
- Download reached completion; launcher was still processing installation at the last detailed observation (83%).
- Engine Build.version identified 5.8.3 and UnrealEditor.exe existed. This does not establish installation completion or successful launch.
- User stopped Computer Use with physical Escape; desktop input stopped. No editor launch or MCP verification followed.

## 2026-10-07 — One-prompt prototype architecture
- User asked which connections enable an AI to create a starting game with models, sounds, animation, design, and implementation.
- Added PROTOTYPE_WORKFLOW.md with tool connections, acceptance evidence, development loop, asset tracking, example prompt, and current readiness.
- Rechecked official Epic MCP, Meshy rig/animation tools, and ElevenLabs audio sources.
- No new paid tools, generation tasks, runtime NPC requirements, or story decisions introduced.

## 2026-10-07 — Workflow options explored
- User clarified the one-prompt game question was hypothetical, not an implementation request. PROTOTYPE_WORKFLOW remains a proposal; do not activate it as a goal or begin its mission automatically.
- Discussed possible additions for animation (Mixamo, Cascadeur), local image workflows (ComfyUI), stock game assets (Fab), cinematic/audio editing (DaVinci Resolve), and binary version history (Git LFS).
- These are researched options, not approved purchases, installations, or connected tools. Current priority remains efficient AI toolchain setup.

## 2026-10-07 — Additional tool review completed
- User asked to check tool usefulness and AI connection paths.
- Reviewed primary documentation for Mixamo, Fab, ComfyUI routes, Cascadeur Python/plans, Resolve Studio scripting, and Git LFS; reviewed a community Cascadeur bridge's own test limits.
- Confirmed Git LFS 3.7.1 is installed. Did not configure a repository or remote.
- Findings: Mixamo free but humanoid-focused with no public automation API found in reviewed docs; Fab native editor integration; ComfyUI documented local API; Cascadeur Free lacks FBX export; reviewed Cascadeur bridge has unverified Windows support; Resolve external scripting advertised in paid Studio.
- Recommendation: Git/LFS and Fab early; Mixamo for humanoid stock motions as needed; ComfyUI optional pilot; defer paid Cascadeur/Resolve Studio.
- Saved details in TOOL_REVIEW.md. No purchases, installs, or generations submitted.

## 2026-10-07 — Tool costs and usefulness scores
- User confirms paid Meshy, Claude, OpenAI, and ElevenLabs subscriptions; exact tiers/API entitlements are unknown. Higgsfield remains a possible future purchase.
- User requested a paragraph per additional tool with cost and a score out of ten relative to existing setup.
- Scores are assistant judgments of incremental current usefulness, not benchmark results: Git/LFS 10, Fab 9, Mixamo 8, ComfyUI 6, Resolve 6, Cascadeur 5.
- Rechecked pricing and noted paid-export/automation limitations; no purchase or installation requested.

## 2026-10-07 — Paid online AI service comparison
- Compared Meshy, ElevenLabs, DeepMotion, Higgsfield, Runway, Suno, and Midjourney using official sources; costs and subjective current-usefulness scores recorded in TOOL_REVIEW.md.
- Higgsfield dynamic pricing could not be verified from the retrieved page; no guessed price recorded. It remains deferred.
- Identified custom skeletal motion as the most distinct potential addition; video/image/music services overlap existing tools to varying degrees.
- No accounts, purchases, integrations, or paid generations performed. Current connection states unchanged.

## 2026-10-07 — Opening canon and Unreal connection verified
- User established exact one-week wake-up inside destroyed ship wreckage, robot-guided recovery/tutorial, alien-speaking enemy scavengers, and first combat. Replaced earlier fortress opening in STORY_BIBLE and HANDOFF; created OPENING_SEQUENCE with established facts separated from suggested staging.
- Robot survived inside shielded suit; blast EMP erased memories except mission objectives. Basic operating/personality retention, shielding failure details, and protagonist survival/amnesia remain open. Previous ancient-weapon/mobile-power-source proposal was not accepted.
- User confirmed download complete and authorized setup. Launcher confirms installed Unreal 5.8.3. Created local Unreal/LostVanguard setup descriptor/config and launched editor outside restricted shell after sandboxed launches exited without logs.
- Enabled native ModelContextProtocol, AllToolsets, PythonScriptPlugin, EditorScriptingUtilities. Verified local listener 127.0.0.1:8000, native MCP initialization/tool discovery/current level query, creation of AI_CONNECTION_TEST at (100,200,300), discovery, removal, and empty search afterward. No persistent game assets or mission created; current engine template remains unsaved.
- Registered global Codex unreal server at http://127.0.0.1:8000/mcp. New chat/restart may be required to expose tools. Editor remains running. Client script tools/unreal_mcp.py pins MCP 2.3.0; report in reports/unreal_mcp_verification.json.
- Initial AllToolsets GameFeatureData scan warning addressed in DefaultGame.ini per engine source; next editor startup must verify. Client emits nonfatal session termination HTTP 202 warning. Save/reload, actual asset transfer, and gameplay not tested.
- Next: validate fresh-session tool exposure and map persistence; continue story by selecting retained objective and survival details. No purchases or paid generations.

## 2026-10-07 — Subscription-aware AI coordination researched
- User asked for software coordinating all paid AI services using current plans. Reviewed n8n and official provider billing/auth documentation; recommendation is existing Codex coordination first, optional self-hosted n8n later.
- Critical distinction recorded in TOOL_REVIEW: subscription sign-in differs from generic API billing; Claude Max/Team API credits were announced in official documentation updated today, excluding Pro; Meshy supports connected-account credits; ElevenLabs has credit and dollar billing documentation requiring account-specific verification.
- No workflow installed or connected and no paid usage or account changes performed. Setup connection states unchanged.

## 2026-10-07 — Claude tier confirmed
- User confirms Claude Pro. Official Pro documentation includes Claude Code access but excludes Console API usage; generic orchestration API calls require separate billing.
- Recommendation remains use existing subscriptions first; no upgrade, installation, or paid request performed.
- Source: https://support.claude.com/en/articles/8325606-what-is-the-pro-plan


## 2026-10-07 — Gemini added
- User adds Gemini to their AI services. Recorded in PROJECT and STATUS; exact tier and API entitlement remain unknown.
- No installation, account change, or paid usage performed.


## 2026-10-07 — Gemini plan clarified
- User confirms free Gemini currently and expects a possible student Pro offer. Recorded current access separately from the potential future upgrade.
- Student eligibility, offer terms, and API entitlement have not been checked. No upgrade, connection, or paid request performed.


## 2026-10-07 — Custom coordination software explored
- Discussed user's hypothetical custom hub for assigning tasks across AI services. Supported integration/session routes differ from automating website chats and do not imply shared chat history or universal subscription coverage.
- Recorded a proposed small text-task prototype in TOOL_REVIEW. No software built, accounts connected, or paid requests made.

## 2026-10-07 — Core mystery direction selected
- User returned to story development, reviewed the core mystery, and chose an explosive weapon/stopping an attack over infection containment as the current direction.
- Updated STORY_BIBLE, STATUS, and DECISIONS. Preserved the entire ship/squad loss and existing opening.
- Checked the change against established facts; weapon target, origin, scale, ship involvement, failed alternatives, and survival remain open. No assistant proposal about an ancient weapon or enemy planting it aboard was accepted.
- Next: choose the intended target and develop why sacrificing the ship was necessary.

## 2026-10-07 — Earth target and escaped AI antagonist
- User selected Earth as the explosive attack's target and an intelligent AI created by another species that got loose as the main enemy. Creator species still survives.
- User introduced another weapon associated with that species and deferred its development; no details invented.
- Updated STORY_BIBLE, STATUS, and DECISIONS. Checked that earlier leader-deception decisions remain visible with their relationship to the new AI direction unresolved.
- No Earth destruction, AI motive, search-party allegiance, or weapon mechanics established. Next: clarify whether earlier enemy leaders' deception stays in the story, then develop the AI's motive and necessity of the sacrifice.

## 2026-10-07 — Escaped AI replaces deception premise
- User explicitly replaced the enemy-leader deception premise, preferring the escaped AI direction. Creator species remains alive in survival mode; AI seeks technology left by a separate species distinct from its creators and humanity.
- Updated STORY_BIBLE, STATUS, HANDOFF, and DECISIONS. Preserved D003 as superseded history and removed its related proposals from active story assumptions.
- Four parties does not mean four biological species. Technology builders' extinction, AI motive, search-party identity, and connection between the explosive and sought technology remain unestablished. Other weapon remains deferred.
- Next: develop why the AI wants the technology and why Earth was targeted, then establish why the ship sacrifice was necessary.


## 2026-10-07 — Recovered technology replaces Earth attack
- User selected the technology-seizure direction for now, replacing the explosive attack on Earth. Humans found advanced technology; protagonist protected one piece aboard his ship. AI attacked to seize it and still seeks it in the wreck. Other pieces are scattered across an undecided area.
- Updated STORY_BIBLE, STATUS, HANDOFF, DECISIONS; preserved D018/D019 as superseded history. Checked that current summaries no longer present Earth attack as active canon.
- Piece functions, count, relationship, survival/location, precise threat prevented, necessity of sacrifice, and robot objective remain open. Assistant's AI survival/identity-loss proposal not accepted.
- Next: develop what the pieces do and why destroying the ship prevented AI acquisition without making the sacrifice avoidable.

## 2026-10-07 — AI destroys ship; recovery campaign direction
- User explicitly accepts AI destroying the ship with protagonist caught in it as current version for now, replacing deliberate sacrifice. Entire squad/familiar crew loss remains.
- User prefers physical hardware so value cannot simply be copied as software; later protagonist meets human forces losing to superior AI technology and undertakes area recovery/resistance missions.
- Updated STORY_BIBLE core/emotional mystery and dependent sections, STATUS, HANDOFF, OPENING_SEQUENCE, and DECISIONS. Preserved old sacrifice decisions as superseded history.
- Exact amnesia mechanism, attack method, why AI destroyed hardware's carrier, hardware fate/function, mission geography, and robot objective remain open. AI survival/identity-loss motive is still unaccepted.
- Next: establish hardware function or attack circumstances, then develop first human contact and companion objective.

## 2026-10-07 — Protagonist backstory tone
- User wants a dark, morally gray supersoldier backstory and rejects assistant's adult rescue-worker/reconstruction origin as too straightforward.
- Recorded preference in STORY_BIBLE. Exact origin, military recruitment, past actions, and scope of memory loss remain open; no new character history accepted.
- Next: propose an origin where coercion and the protagonist's own choices both matter, then build supporting relationships around it.

## 2026-10-07 — Forced supersoldier origin selected
- User chooses forced entry into the supersoldier program; becoming one was not his choice. Updated STORY_BIBLE, DECISIONS, STATUS.
- User withdrew the explored human-created enemy AI/military cover-up branch; alien-created escaped AI remains current. No cover-up, ship-AI population, prior faction membership, or protagonist misconduct accepted.
- Checked that volunteering versus conscription is no longer listed as undecided. Age, selection circumstances, coercion methods, later agency, and memory scope remain open.
- Next: develop the selection circumstances and relationships formed in the program.

## 2026-10-07 — Childhood entry established
- User chooses childhood entry into the forced supersoldier program. Updated STORY_BIBLE, DECISIONS, STATUS, HANDOFF.
- Exact age, selection, family history, training, procedures, and memory scope remain open. Medical-dependency lie remains an unaccepted assistant proposal.
- Next: define the program's distinctive purpose and his childhood relationships, without treating inspiration as original detail already established.

## 2026-10-07 — Praetorian designation selected
- User selects Praetorians as the supersoldier class name after historical naming discussion. Individual is a Praetorian.
- Updated STORY_BIBLE, DECISIONS, STATUS, HANDOFF; checked name appears in protagonist's established facts.
- Formal program name remains open; Project Praetorian was a suggestion, not a separate selection. Lost Vanguard remains working title.
- Next: develop childhood program circumstances and supporting relationships; hardware function and memory scope remain open.

## 2026-10-07 — AI experimentation and colony origin replace military creation
- User establishes Praetorian name from original human colony on another planet. Enemy AI found colony and used its children in forced supersoldier experiments intended to fight humanity; humans rescued them. User explicitly confirms replacement of human military creation.
- Updated STORY_BIBLE, STATUS, HANDOFF, DECISIONS; prior human military origin remains superseded history. Rejected evacuation-program proposal was never accepted.
- Exact colony/planet formal names, experiment mechanisms, rescue circumstances, surviving numbers, later service, and memory scope remain open. No control mechanism, implanted commands, special lineage, or misconduct established.
- Next: build relationships around colony childhood, rescue, and later human service; establish what their enhancements mean to them.

## 2026-10-07 — Restrained soldier characterization
- User rejects childhood-friend/rescuer emotional supporting relationships; prefers Praetorians emotionally closed off, almost cutting feelings out, with soldier identity central. Last unfinished thought explicitly withdrawn.
- Updated STORY_BIBLE, DECISIONS, STATUS. No literal emotional deletion or conditioning mechanism established. Robot best-friend status not explicitly revoked; fit remains open.
- Earlier friendship/rescuer suggestions were proposals, not canon. Next: develop functional military support characters and restrained behavior, without inventing intimate bonds.

## 2026-10-07 — Conditioning and action-based relationships accepted
- User accepts enemy AI conditioning as source of Praetorian emotional restraint and competence/disagreement/earned trust as relationship foundation. Players should value characters through their actions.
- Updated STORY_BIBLE, DECISIONS, STATUS, HANDOFF. Checked that conditioning is no longer treated as undecided while methods remain open.
- No total emotion deletion, remote control, named cast, or exact professional roles established. Robot friendship remains accepted but its expression within restraint is open.
- Next: develop supporting characters by useful actions, competing judgments, and earned trust; choose specific roles with user.

## 2026-10-07 — Confident competence and dry humor
- User wants short confident character moments, including accurate predictions and terse reactions after events prove expertise; describes tone as aura farming.
- Recorded tone in STORY_BIBLE and DECISIONS. No scene/dialogue or universally infallible character established.
- Next: propose short interactions that demonstrate expertise without forcing player mistakes or long explanations.

## 2026-10-07 — Complete bible review requested
- User requests full updated bible before developing enemy AI and other AI backstories.
- Reviewed STORY_BIBLE for stale assumptions; removed rejected rescue-specialist proposal, made emotional arc open rather than presume guilt, and identified old deception-related parking-lot idea as superseded. Updated version 16 and next creative focus.
- All established current facts preserved; robot is the only other AI currently established. Exact meaning of other AI can be clarified if needed. No new AI backstory accepted.
- Next: present complete current bible in chat, then explore enemy AI and companion origins.

## 2026-10-07 — Specialized additional Praetorians
- User establishes more Praetorians, each specialized in a field, knowing one another, and very hard to kill due to supersoldier abilities.
- Updated STORY_BIBLE, DECISIONS, STATUS. Preserved lost-squad deaths; additional Praetorians do not imply a squad survivor. No invulnerability or specific abilities invented.
- Next: select specialties and develop professional interactions through established competence/disagreement/earned-trust tone.

## 2026-10-07 — Presence and instinct selected
- User selects presence and instinct as protagonist strengths, preferring presence first. Other explored qualities remain proposals.
- Updated STORY_BIBLE, DECISIONS, STATUS, HANDOFF. Presence means others regain confidence/action; instinct means noticing shifts and acting decisively. No supernatural powers, infallibility, or technical specialization established.
- Next: demonstrate these strengths through restrained actions and professional reactions; develop other Praetorian specialties or return to AI origins.

## 2026-10-07 — General-purpose enemy AI origin
- User chooses broad general-purpose AI assistance as original purpose: creators wanted to make helpful intelligence for many tasks, not a dedicated explorer/restorer/military system.
- Updated STORY_BIBLE, DECISIONS, STATUS, HANDOFF. Removed original purpose from undecided list; preserved escape mechanism, hostile motive, hardware goal as open.
- Earlier three specialized-purpose options were proposals and not accepted. Next: establish how this originally helpful AI became independent and hostile.

## 2026-10-07 — Gradual change and triggering event
- User chooses both gradual AI change and a particular event that triggers the decisive turn. Updated STORY_BIBLE, DECISIONS, STATUS.
- Exact buildup and trigger remain open; no betrayal/shutdown/damage event accepted. Fourth party remains the separate hardware-builder civilization, whose present fate is unknown.
- Next: develop the gradual conflict and triggering event without assigning unaccepted motives.

## 2026-10-07 — Failed self-improvement selected
- User likes failed self-improvement as trigger and asks whether solving that failure can be the AI's problem/motive. Recorded trigger as selected; repair motive/hardware connection as under exploration, not fully specified.
- Updated STORY_BIBLE, DECISIONS, STATUS. Replacement trigger rejected. Exact symptoms, lost empathy, identity drift, urgency, and repair method not established.
- Next: develop repair motive and stakes, keeping understandable need separate from choices harming other civilizations.

## 2026-10-07 — Slow AI deterioration, no waiting strategy
- User establishes gradual worsening but long-term AI stability/capability. Waiting for it to break is not an option for humanity.
- Updated STORY_BIBLE, DECISIONS, STATUS, HANDOFF. No exact lifetime, symptoms, rapid tactical decline, or imminent death countdown established.
- Next: define failure symptoms and whether sought hardware addresses them, keeping AI a sustained threat.

## 2026-10-07 — Identity damage and peaceful original nature
- User selects identity as deterioration focus. AI began peaceful/caring, meant to operate a certain way, but developed its own drive for growth and failed self-improvement led to conflict.
- Updated STORY_BIBLE, DECISIONS, STATUS, HANDOFF. General-purpose origin and slow deterioration remain intact.
- Memory loss, split personalities, exact empathy loss, awareness, repair desire, and whether it wants its original identity restored remain unestablished.
- Next: clarify what AI wants repair to preserve or change, and connect it to hardware without predetermining redemption.

## 2026-10-07 — Stabilize evolved AI identity
- User selects stabilizing the more powerful identity as AI's goal rather than recovering original peaceful self. It seeks repair while retaining growth/power.
- Updated STORY_BIBLE, DECISIONS, STATUS, HANDOFF; removed stale statement treating all identity-related motive as unaccepted.
- Exact hardware mechanism, repair feasibility, and detailed symptoms remain open. Earlier failing machinery/copy-transfer explanation not accepted.
- Next: define sought hardware's role in stabilization and stakes for humans and creator species.

## 2026-10-07 — Creator-studied stabilization artifact
- User establishes creators studying artifact apparently able to stabilize AI; AI learns of it, seeks it, and discovers humans possess it.
- Updated STORY_BIBLE, DECISIONS, STATUS. Apparent capability kept distinct from verified in-universe remedy; no exact possession transfer, species age, or artifact/piece system invented.
- Ship destruction rationale remains unclear in user's unfinished wording; protagonist's involvement in earlier discovery is tentative. Next: clarify capture attempt versus deliberate destruction/recovery plan, then timeline.

## 2026-10-07 — Deliberate destruction for wreck recovery
- User explicitly confirms AI deliberately destroyed ship expecting artifact recovery from wreck. Not accidental capture-attempt destruction.
- User also explored belief humans possessed it based on proximity; kept mistaken-targeting possibility tentative. Prior carried hardware piece remains established, but exact identity relative to sought artifact and AI knowledge accuracy remain open.
- Updated STORY_BIBLE, DECISIONS, STATUS, HANDOFF. Distinguished AI expectation from actual artifact survival; durability and preference for destruction remain open.
- Next: establish why AI expected artifact to survive, and possession/discovery timeline.

## 2026-10-07 — Durable artifact and extinct-builder setting
- User accepts artifact powerful/durable enough to withstand ship destruction. Technology from older extinct species; futuristic remnants shape planetary setting. Humans newly arrived/found technology, AI attacked ships on suspicion of possession while searching planet.
- User says AI killed creators who studied artifact; scope unclear relative to established surviving creator species. Marked local researchers versus entire species pending clarification rather than silently replacing survival canon.
- Updated STORY_BIBLE, DECISIONS, STATUS. No universal indestructibility, exact ruin/planet names, actual artifact location, or definite human possession inferred.
- Next: clarify scope of creator deaths, then organize discovery/attack timeline.

## 2026-10-07 — Secret artifact relocation and coincidental arrival
- User confirms creator species survives; researchers studied artifacts on planet, moved stabilization hardware after learning AI wanted it, without AI knowing. AI searched original planet; humans coincidentally arrived and were attacked on suspected possession.
- Earlier creator-death ambiguity resolves to local researchers rather than all species; exact deaths/timing remain open. Creator species resists its AI.
- Updated STORY_BIBLE, DECISIONS, STATUS, HANDOFF. Human/creator prior contact versus first meeting and mistaken hostility expressly undecided.
- Preserved earlier ship hardware assignment but marked exact identity versus relocated artifact unresolved; did not invent off-planet destination, transfer to humans, or second artifact's function.
- Next: resolve relocated artifact versus ship cargo, then choose contact history.

## 2026-10-07 — Artifact absent; mission-based investigation
- User explicitly changes previous aboard-artifact decision: AI thought artifact was aboard, but it was not. Humans do not know why they are attacked. No substitute piece/cargo invented.
- Protagonist discovers truth through missions and companion hacking/accessing map systems, with human help. Main ship in space or later backup is undecided.
- Updated STORY_BIBLE, DECISIONS, STATUS, HANDOFF. Removed stale active cargo/protection premises and consolidated accumulated story status into a current section; historical progression preserved here and in decisions.
- Existing scattered physical hardware, extinct builders, creator relocation, deliberate destruction, and full lost squad remain. Next: map first clues and support arrangement, with artifact relocation destination open.

## 2026-10-07 — Connected opening mission story draft
- User requests linked mission stories and voice lines to later guide Unreal levels. Created MISSION_STORIES draft 1: five proposed missions from wreck awakening to artifact relocation route investigation, with objectives, discoveries, causal transitions, and draft dialogue.
- Kept established opening/canon distinct from proposed extensions, roles, locations, and dialogue. Local human support is draft-only; orbital support/backup remains open. No squad survivor introduced and no engine implementation or paid voice generation performed.
- Checked evidence flow: artifact targeting first, suspected human possession next, relocation truth afterward, next-destination lead last. Companion retrieves new information without regaining erased memories. Mandatory leads tied to mission completion.
- Next: review proposed arc, then expand approved mission 1 into full narrative/voice triggers before Unreal implementation.

## 2026-10-07 — Character guide created; names deferred
- User requests explanations of characters and asks for supersoldier designation reminder; personal naming explicitly deferred.
- Created CHARACTER_GUIDE draft 1 for protagonist, companion, enemy AI, other Praetorians, and proposed commander/engineer roles. Established facts separated from suggested dialogue, trust moments, and limitations.
- Checked no invented personal names, ranks, technical specialties, prior sentimental bonds, or resurrected squad members. Optional intelligence role and draft mission roles remain unselected.
- Next: choose supporting individuals, develop profiles/voices, then names later; mission draft labels remain consistent.

## 2026-10-07 — Presumed-dead protagonist and terminology
- User establishes others think protagonist dead after ship destruction; asks character terminology. Main character is protagonist, other recurring characters supporting cast; development process character development.
- Updated STORY_BIBLE, DECISIONS, STATUS. Fleet layout and two-other-Praetorian ship placements remain under discussion. Falling from ship on waking has unclear staging; existing pinned-wreckage recovery sequence retained pending clarification.
- Next: develop individual profiles and return scene, then resolve fleet and wreck staging.

## 2026-10-07 — Flexible delay and fall-before-recovery opening
- User relaxes exact one-week timing to days, possibly a couple; no exact duration selected. Fall precedes waking/recovery tutorial, with combat afterward.
- Updated current STORY_BIBLE, CHARACTER_GUIDE, MISSION_STORIES, OPENING_SEQUENCE, HANDOFF, STATUS; preserved former exact-week decision in history as superseded. Draft elapsed-time voice line now provisional rather than seven days.
- Exact fall mechanics, altitude, wreck location, life support, and biological amnesia mechanism remain open. No new survivor or fleet assignment established.
- Next: develop character profiles, resolve fleet layout, then detail opening scenes without forcing an exact day count.

## 2026-10-07 — Separate Major and Commander
- User explicitly requests two separate characters, one Major, one Commander. Updated STORY_BIBLE, DECISIONS, STATUS; CHARACTER_GUIDE draft 2 now has separate profiles.
- Proposed ground Major and ship/fleet Commander split labeled proposal. No branch, hierarchy, names, personalities, Praetorian status, or accepted orbital layout inferred.
- Draft mission Field Commander label remains unmapped until roles selected. Next: define responsibilities and contrasting judgment, then personal names later.

## 2026-10-07 — Protagonist full-name shortlist
- User asks for protagonist full names. Added six proposed names to CHARACTER_GUIDE; none selected.
- Earlier defer-naming preference now relaxed for protagonist. Other character names remain open.
- Next: select/refine protagonist name, then update guide/bible and mission labels only after selection.

## 2026-10-07 — Commander Dorian Vale selected
- User likes Dorian Vale for Commander, rather than protagonist. Used shortlist spelling Vale; transcript rendered Veil, so spelling can be corrected later. Did not carry over proposed August middle name.
- Updated STORY_BIBLE, CHARACTER_GUIDE, DECISIONS, STATUS. Major/protagonist names remain open; command responsibilities and personality not established by name selection.
- Next: develop Commander profile or return to protagonist naming.

## 2026-10-07 — Evan protagonist name selected
- User names protagonist Evan with no surname for the moment. Recorded surname as undecided, not permanently absent; no middle name invented.
- Updated STORY_BIBLE, CHARACTER_GUIDE, DECISIONS, STATUS, HANDOFF. Commander Dorian Vale remains separate; Major, companion, enemy AI names open.
- Next: develop individual profiles and dialogue; other name selections later.

## 2026-10-07 — Companion naming explored
- User asks for more small-robot names after initial Rook/Kip/Relay/Rivet options. Added expanded proposed shortlist to CHARACTER_GUIDE; no selection yet.
- Robot origin/personality remain open; naming suggestions do not establish functions or acronyms.
- Next: select/refine name, then develop companion voice/personality.

## 2026-10-07 — Clank named and self-name joke accepted
- User selects Clank after existing Ratchet & Clank association was explained. Accepts brief gag calling another robot Clanker, then confused recognition of resemblance to own name.
- Updated STORY_BIBLE, CHARACTER_GUIDE, DECISIONS, STATUS, HANDOFF; draft mission speaker labels Evan/Clank updated without selecting officer roles.
- Exact joke lines, scene placement, target robot, broader personality and voice remain open. No repeated gag or extra named robot invented.
- Next: develop character profiles and short dialogue examples with restrained tone.

## 2026-10-07 — Major Lena Cross selected
- User authorizes Lena Cross selection after comparing with Tessa Kane. Updated STORY_BIBLE, CHARACTER_GUIDE, DECISIONS, STATUS.
- No personality, exact duty/branch, Praetorian status, or mission speaker mapping inferred from name. Tessa Kane remains unselected.
- Next: develop Major/Commander profiles or name remaining Praetorian and enemy AI characters.

## 2026-10-07 — Leader Evan and two fleet specialists
- User establishes Evan as leader, two other Praetorians in current fleet, many more elsewhere. Proposes scout/sniper and heavy-weapons/machine-gun pair.
- Updated STORY_BIBLE, CHARACTER_GUIDE, DECISIONS, STATUS. Added labeled working profiles with suggested competence/trust/dialogue patterns, not established personalities or gear.
- No rank, authority over officers, exact ship placements, additional lost-squad survivor, or invulnerability inferred.
- Next: refine/select pair's roles, then personalities and names, using complementary expertise and earned trust.

## 2026-10-07 — AI names reopened; planet shortlist parked
- User likes Axiom/Concord/Orison/Meridian as possible planet names and withdraws momentary Meridian AI selection. Kept all unassigned; enemy AI remains unnamed.
- Added unassigned ideas to STORY_BIBLE and CHARACTER_GUIDE; prepared more AI-name proposals. No new planet/civilization or AI identity established.
- Next: continue AI naming; assign planet names only after user chooses locations.

## 2026-10-07 — Meridian AI working name selected
- User returns to Meridian as enemy AI name for now. Updated STORY_BIBLE, CHARACTER_GUIDE, DECISIONS, STATUS, HANDOFF; brief withdrawal superseded.
- Name origin/translation/ownership open. Other AI suggestions unselected; Axiom/Concord/Orison remain unassigned planet possibilities. No Meridian planet assigned.
- Next: develop Meridian character profile/voice and additional Praetorian profiles.

## 2026-10-07 — Orison and prior human/creator war
- User names main planet Orison, establishes existing human/creator war with earlier battles, and says Meridian started it without creator intent. Orison is continuation rather than first incident/main entirety.
- Updated STORY_BIBLE, DECISIONS, STATUS, HANDOFF. Resolved prior-contact uncertainty toward existing war; no specific attack or escalation accepted yet.
- Accepted planet name only; refuge/fallback survey motive remains proposal. Next: propose first Meridian attack, how humans implicated creators, and reciprocal escalation while creators resist AI.

## 2026-10-07 — Mistaken-responsibility war origin accepted
- User accepts Meridian seizing creator ships/systems and attacking humans, human misattribution/retaliation, and creator defense escalating war while both resist AI.
- Updated STORY_BIBLE, DECISIONS, STATUS, HANDOFF. No named battles, casualty counts, diplomatic encounters, or exact timeline invented.
- Next: connect investigation evidence to human/creator mistrust, then define fleet arrival purpose and earlier battle details as needed.

## 2026-10-07 — First-level draft and staged production plan
- User requests first-level work, then clarifies cinematic construction can wait and asks how to stage physics and substantial visual asset work. Recorded D057; PROJECT/HANDOFF reflect new priority.
- STORY_BIBLE v41 corrects stale uncertainty about mistaken ship targeting, established stabilization motive, Orison naming, and next work. Historical decisions retained.
- Created LEVEL_01_WRECKAGE.md: proposed connected route, objective/reveal boundaries, shot intentions, 20 draft dialogue triggers, build order, and unresolved choices. Created FIRST_LEVEL_BUILD_PLAN.md for small blockout, player feel, built-in Chaos physics, reusable asset kit, and gradual art replacement. All new details remain proposals.
- Checked current official Epic physics/destruction documentation; engine already supplies physics. No custom engine or whole-ship destruction simulation proposed as a prerequisite.
- Editor launched; loopback listener reachable but fresh toolset discovery hung and was cancelled. Earlier connection verification does not prove current responsiveness. No level/Blueprint/cinematic assets edited, and no compile/save/reload/play test completed. No paid voices, assets, or footage generated.
- Checked saved text and current status for stale naming/priority claims. Next: review opening staging, recheck editor, make and verify a small walkable blockout, then implement objectives/combat. Cinematic software and finished visual designs deferred.

## 2026-10-07 — Copyable first-level build prompt
- User accepts staged plan and asks for one prompt to use in a separate build chat, then return here to review results and draft changes.
- Created LEVEL_01_BUILD_PROMPT.md with current records, existing project, temporary blockout staging, editor verification, implementation checkpoints, canon boundaries, gameplay checks, and a requested build report. Raw prompt stays in the file rather than voice context.
- Marked old fortress example in PROTOTYPE_WORKFLOW historical and corrected readiness. Recorded D058 and updated STATUS.
- Consulted official OpenAI AGENTS.md guidance for project continuity. No new chat created or messaged; no editor assets changed. Prompt delivery is complete; build execution and report review remain future actions initiated by the user.

## 2026-10-07 — Build prompt connection instructions clarified
- User asks whether prompt connects directly to Unreal and explains how. Added installed engine/project, enabled plugins, local endpoint, native tool discovery, existing protocol-client fallback, and live scene-query requirement to build prompt.
- Clarified prompt uses existing setup but cannot establish a working connection by itself. Latest responsiveness remains unverified; no new connection or asset edit performed.

## 2026-10-07 — User opening image preserved
- Copied attached image unchanged from temporary upload to assets/references/level_01/opening_wreck_alien_forest_reference.png. SHA-256 source/destination match verified.
- Added reference README describing visible composition and distinguishing approximate environment direction from unselected layout/armor/sky details. Linked image in STORY_BIBLE v42, LEVEL_01_WRECKAGE, and LEVEL_01_BUILD_PROMPT; updated STATUS and recorded D059.
- No image edits, generated art, or Unreal changes. Next: use reference when staging opening blockout; keep recovery and elapsed-days continuity.

## 2026-10-07 — Image-led opening prompt
- User asks for a prompt expressing approximately the supplied picture. Saved OPENING_VISUAL_BUILD_PROMPT.md for a build chat: hull-framed starting view, larger wreck focal point, alien forest, readable route, lighting contrast, and screenshot comparison.
- Prompt preserves existing gameplay/current records, recovery sequence, days-after-crash continuity, and artifact absence. Sky details remain visual possibilities; no new story facts selected. No editor work or paid generation performed.

## 2026-10-07 — First playable Wreckage built and verified
- Built saved L_Wreckage and L_Wreckage_Playable maps in the existing Unreal 5.8.3 project using native editor APIs. Runtime player/searcher/GameMode/HUD Blueprints implement recovery, weapon, two sentries, damage/death, checkpoints, fresh clue, communications, and gated completion. No runtime Python or paid service required.
- User resolved Restore Packages dialog. Fresh native MCP scene queries and editor operations succeeded through the existing loopback fallback client. Original verification evidence preserved; HTTP 202 session termination warning persists after successful calls.
- Fixed authoring exception suppression, native variable/local-function graph creation, subtitle newline escapes, Preview lighting, and player capsule visibility response. No Unreal binary was edited or moved through filesystem operations.
- All 19 automated Play-In-Editor checks passed, including actual combat hits, normal-health death/restart, evidence persistence, cue protection, gated progression, completion, and saved-map reload. Four runtime assets passed strict final compilation/save; saved defaults are Health 100 and Step/Checkpoint 0 with debug movement disabled.
- The long remote route used extra test health because remote controls are slow. Normal-health combat balance, physical keyboard/mouse feel, performance, packaging, and finished art remain unverified. LEVEL_01_BUILD_REPORT.md and reports/wreckage_playtest.json record evidence and limits.
- Subsequent user request focuses on the supplied forest/wreck opening reference while preserving this baseline; the image-led map is a separate editor-authored variant. Implementation staging/dialogue/sentry designs remain proposals.

## 2026-10-07 — Reference-led opening environment built
- Read current project instructions/status/story/plan and inspected the saved reference. Recorded D060 and STORY_BIBLE v43 for the user's early-view timing and visual brief; exact sky, layout, final designs, and new implementation details remain provisional.
- Created L_Wreckage_Opening as a native editor-API duplicate of the verified playable map. Preserved the original map and runtime gameplay assets. Added a dark widened hull breach, cables, layered blue-green forest/plant/rock proxies, broken larger wreck silhouette, four lingering fire pockets, rising/fading smoke material proxies, cool haze, and manual exposure. Final native authoring summary: 519 level actors, saved, no errors or unsupported-property notes.
- Corrected overly narrow framing, excessive brightness, silhouette orientation, spawn/debris overlap, and the cosmetic end-label escape. Source uses fixed collision and decoration outside the tested route; no paid generation, finished cinematic, new bridge, or subagent.
- All 19 opening-map PIE route checks passed, including walking/crouching/break crossing, weapon/actual combat hits, normal-health death and restart, cue protection, clue retention, communications, exit gating/completion, and saved-map reload. Frame-rate-sensitive automated turning/jump attempts were corrected using feedback and longer real inputs. Long remote movement/combat uses extra temporary health; saved defaults remain Health 100. Physical controls, normal-health balance, and performance need a human pass.
- Captured actual game view after debris release and comparison renders at the recorded first-person pose. Temporarily moved the editor debris and hid editor-only icons for comparison capture, then restored before saving. See OPENING_VISUAL_BUILD_REPORT.md, reports/opening_playtest.json, and reports/opening_comparison_camera.json.
- Configured the opening variant as startup map and updated STATUS/PROJECT/HANDOFF/build records. No full application restart or package test. Next: review the starting composition, play by hand, then replace a small approved hull/vegetation kit and improve terrain shoulders and effects.
- Final saved inspection recompiled/saved all four runtime Blueprints with warnings treated as errors, confirmed clean Health 100/Step 0 defaults and disabled test inputs, and verified the editor is left on L_Wreckage_Opening. Final starting-view images were inspected and temporary capture edits restored before save.

## 2026-10-07 - Script and friend-facing project package
- User requested the script and something to show a friend. Created SHARE_SCRIPT.md and FRIEND_PROJECT_BRIEF.md plus two shareable PDFs in output/pdf.
- Six-page story PDF contains a complete draft of mission 1 scenes and dialogue, the existing proposed five-mission arc, and spoiler background grounded in STORY_BIBLE v43. It is not a finished campaign screenplay or gameplay transcript. Officer duties, artifact destination, survival mechanism, searcher identity, and final ending remain open. New dialogue/staging remain proposals; no canon or accepted decision changed.
- Two-page project overview pairs the preserved user-supplied reference with the actual opening Play-In-Editor screenshot. Labels clearly separate reference atmosphere from rough game assets. Distinguishes the baseline's 19 recorded passing editor checks from pending full-route verification in the opening variant report.
- Used bundled ReportLab/PyPDF and Poppler. Fixed overflow, rendered both final PDFs, and visually inspected all eight pages; text extraction and page counts passed (6 and 2). Poppler emitted font fallback notices for unused Symbol/ArialUnicode fonts; rendered Helvetica text was legible with no visible defects.
- Maintained STATUS; source generator is tools/create_share_pdfs.py. No editor changes, paid generations, publishing, external messages, or subagents. Next: user shares the overview and optionally the spoiler script; creative revisions and human playtesting remain future work.

## 2026-10-07 - GitHub upload prepared
- User requested project upload to alexandergazzard-beep/Praetorian. Remote read succeeded with no refs, confirming an empty repository at inspection. Initialized main locally and verified origin points to the exact supplied URL.
- Installed versions: Git 2.53.0.windows.1, Git LFS 3.7.1. Enabled local LFS hooks and .gitattributes for Unreal maps/assets, Blender sources, models, audio and video. Consulted official GitHub LFS documentation.
- Extended ignores for tmp, local assistant settings, credential formats and generated IDE files; existing Unreal Saved/Intermediate/DerivedDataCache/Binaries exclusions retained. No binary asset editing or movement occurred.
- Updated README for actual playable-prototype status and share links; created SOURCE_CONTROL.md with clone/update commands and backup scope. Recorded D061 and updated PROJECT/STATUS.
- Candidate file scan: 194 files, approximately 15.5 MB before Git compression/LFS, no credential pattern hits and no file over 100 MiB. Upload is pending; authenticated push and remote verification are next.
- Sandbox Git/network operations needed approved elevated shell access; initial git init succeeded and origin was already configured despite a subsequent sandbox access error. No existing remote work was overwritten.

## 2026-10-07 - GitHub upload verified
- Initial commit c531b5892713f603d1a2b4ee72c850cb0ba6e9ac successfully pushed to main at the user's Praetorian repository. GitHub's live main ref exactly matched the local commit; main now tracks origin/main.
- All 35 LFS objects uploaded successfully, approximately 3.2 MB; git lfs fsck passed. Confirmed caches/tmp are ignored and the committed overview PDF exactly matches original binary bytes. Explicit binary rules prevent text conversion of PDFs and images.
- Initial diff whitespace check noted only pre-existing extra blank lines at EOF in some notes/config/report files; retained original contents. No credential patterns detected. No force-push, paid purchase, or Unreal binary editing/movement performed.
- Updated STATUS and SOURCE_CONTROL with actual upload evidence. This follow-up documentation update is committed and pushed next, with another remote-ref and clean-worktree check. No fresh clone/recovery test claimed.
- Next: save assets in Unreal, review Git changes, commit descriptive updates, and push routinely; install Git LFS before cloning elsewhere. A separate backup for ignored local generated files remains open.
