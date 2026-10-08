# Lost Vanguard — Level 01: Wreckage

Draft 1 — 2026-10-07. This is a story and level-design package, not an implemented or play-tested level. Established facts come from STORY_BIBLE.md; every new location, trigger, line, timing, and gameplay detail below is a proposal for review. Cinematics are planned only. Their production software is undecided and construction is deferred.

## Experience and scope

User-selected visual reference: [opening wreck in an alien forest](../assets/references/level_01/opening_wreck_alien_forest_reference.png). Approximate starting surroundings: a dark broken hull opening framing a burning wreck in lush alien vegetation, with a striking sky beyond. Use this as opening composition guidance; exact layout, celestial bodies, and character appearance are not selected by the image. Preserve the recovery sequence; exact placement of this view within it remains open.

Evan wakes inside his destroyed ship, checks that he can move, discovers the wreck is still being searched, and fights his way to a first clue and a route toward human contact. The player's immediate question is whether they can get out. The larger question becomes why the enemy is still searching this ship.

Target roughly 12–18 minutes on a first playthrough, to adjust after testing. One small connected wreck environment; one weapon; one enemy behavior; one evidence interaction; one exit. First-person perspective is a prototype proposal, not a newly accepted game-wide decision. Start with simple shapes and subtitles. Finished art, recorded voices, elaborate animation, and cinematic footage are later work.

## Continuity boundaries

- Evan survives the destruction and fall/crash, then wakes after days; no exact day count or altitude is fixed.
- Clank's recovery checks teach the player controls. Evan is already a trained soldier.
- The artifact was never aboard. Do not place it here as a collectible, prop, or reward.
- Clank retrieves new records. He cannot recall the attack's explanation from erased memories.
- The searchers speak an alien language; their physical design and precise allegiance are open. Use neutral placeholders until selected.
- The lost squad remains lost. The two other fleet Praetorians are separate characters; this level does not reveal a surviving squadmate.
- The level reveals a search for a specific artifact, not the complete relocation history, stabilization mechanism, or origin of the wider war.
- Officers' exact duties remain open. Any incoming transmission is labeled Human Signal until a speaker is chosen.

## Connected mission flow

| Beat | Player action and environment | Story result | Leads to |
| --- | --- | --- | --- |
| 1. Wake | Free Evan from wreckage; regain camera control | Alive, injured, incomplete information; Clank responds | Recovery check |
| 2. Recovery | Look toward a suit light; walk, crouch beneath a beam, cross a small break | Body and suit still function; no training-from-zero premise | Searchers heard nearby |
| 3. Hold | Observe searchers through a torn bulkhead; find a secured weapon locker | Wreck is occupied; enemy is looking for something | First fight |
| 4. Clear | Fight a small search party in a room with two cover routes | Evan's competence shown through player success | Enemy search terminal |
| 5. Read | Clank accesses a fresh search record while Evan secures the room | A specific artifact is the search target; record supplies no proof it was aboard | Restore communications |
| 6. Reach out | Activate a damaged communications panel and follow an external route | A weak human signal supplies a possible rally-point lead | Mission 02: Rally Point |

Proposed spatial chain: crushed compartment → broken passage → observation opening → search bay → communications alcove → exterior overlook. Surface wreckage on Orison is a convenient working staging choice, not accepted canon. If the wreck remains in another environment, adapt the exit and vista without changing the evidence sequence.

## Cinematic plan — no construction yet

Opening, approximately 15–25 seconds: black screen with faint suit alarms; Evan's vision returns beneath a metal panel; Clank's light catches the obstruction; Evan braces and shifts it. Give camera control back before the recovery checks. Do not show a flashback that resolves what Evan cannot remember. Debris removal can be a short animation or an interaction; implementation is undecided.

Mid-level: keep the searchers' arrival in gameplay. Audio and their movement beyond a torn wall direct the player's attention. Avoid taking control away just before the first fight.

Closing, approximately 6–10 seconds if desired: after activating communications, the player reaches a view of Orison's ancient structures beyond recent wreckage. A faint human transmission establishes the next direction. This can remain a playable vista instead of a cutscene. No officer, friendly ship placement, or rescue arrival is confirmed by the shot.

Later production choice: shots using game assets can be planned for Unreal; external generated footage can use the same scene intent. Camera plans remain optional until the approach is chosen. No generation, subscription, voice recording, or finished cinematic is authorized by this draft.

## Draft dialogue and triggers

All lines are proposals. Speaker labels are production metadata; they do not settle what either character remembers about names or history.

| ID | Trigger | Speaker | Draft line |
| --- | --- | --- | --- |
| L01_001 | Vision returns | Clank | Evan. Can you hear me? |
| L01_002 | Player frees debris | Evan | I hear you. |
| L01_003 | Recovery begins | Clank | Suit response is uneven. Follow the light. |
| L01_004 | Look check completes | Clank | Good. On your feet. |
| L01_005 | Walk check completes | Evan | The ship? |
| L01_006 | After question | Clank | I can't account for the attack. My records are damaged. |
| L01_007 | Low passage reached | Clank | Clearance ahead. Keep low. |
| L01_008 | Recovery route completes | Clank | Movement checks complete. |
| L01_009 | Searchers audible | Clank | Movement beyond that wall. |
| L01_010 | Evan observes searchers | Evan | Hold. |
| L01_011 | Weapon locker found | Clank | Manual release. Power is gone. |
| L01_012 | First fight completed | Evan | Clear. |
| L01_013 | Search terminal examined | Clank | Their search records. Give me a moment. |
| L01_014 | Record decoded | Clank | They're looking for an artifact. This ship is marked as a search site. |
| L01_015 | After decoded record | Evan | What artifact? |
| L01_016 | After question | Clank | The record doesn't identify it. |
| L01_017 | Communications restored | Human Signal | Any surviving units, respond. Rally-point transmission follows. |
| L01_018 | Evan replies | Evan | Receiving. Send location. |
| L01_019 | Next route supplied | Clank | Signal is weak. We have a direction. |
| L01_020 | Exit reached | Evan | Then we move. |

Search-party alien speech: temporary unintelligible sound or subtitles marked untranslated. Do not invent a language, confirmed translation ability, or enemy biography. The Clanker joke is reserved for a later suitable scene; it need not interrupt the opening.

Optional competence beat: an automatic door attempts to move, stalls, and Evan immediately uses the manual route. Let the action demonstrate his judgment; avoid adding a failure solely to make another character look foolish.

## Gameplay implementation requirements

Objectives advance from observed completion, not fixed timers. Recovery checks must tolerate players looking or moving before the prompt. Let experienced players finish quickly; offer an optional reminder if a player stalls. Opening cinematic should be skippable, with a safe playable state afterward.

Weapon pickup and first fight require clear feedback. Cover provides a direct route and a flank; enemies should not appear behind an unaware player during the tutorial. Death or reload resets the current encounter without replaying every opening line. Search-record access occurs after the room is safe, and the clue stays readable in an objective log.

Proposed checkpoints: after recovery, before combat, after reading evidence. Dialogue queues must prevent overlapping lines and repeats when a trigger is re-entered. Mission end requires the evidence interaction and communications step; simply reaching the exit should not skip the mystery clue.

## Build order and acceptance checks

1. Confirm wreck setting and create a small blockout with a navigable route. No final cinematic needed.
2. Add movement, debris interaction, objective tracking, and subtitle triggers.
3. Add one placeholder weapon and a small combat encounter.
4. Add evidence access, communications, and exit transition.
5. Test from a fresh start, death/reload, skipped intro, early movement, repeated interactions, and leaving/returning to triggers. Verify the artifact is absent and every reveal follows current canon.
6. Review pacing with the user, then choose cinematic tools and asset/voice production.

Implementation update, 2026-10-07: a saved editor prototype now implements this route using placeholders. See LEVEL_01_BUILD_REPORT.md for the actual assets, checks, and limitations. The narrative and visual proposals in this document remain proposals.

## Decisions needed before detailed implementation

Highest priority: surface wreck or other environment; plausible survival over the missing days; Clank's retained objective and how basic operation survived; search-party body type/allegiance.

Can wait: first human speaker, fleet arrival motive, officer hierarchy, specialist names, artifact mechanism/destination, exact elapsed days, final armor style, cinematic software and voice casting. Temporary design choices must stay labeled as proposals until accepted.
