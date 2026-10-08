# First-level production plan

2026-10-07 — proposed workflow. The user wants to start the first level and plan physics and eventual world/character assets. Finished visual design and cinematic construction are deferred. No final art direction or cinematic software has been selected.

## First milestone

Build a small playable version of Wreckage with simple shapes: wake, move through the damaged passage, fight a search party, read the search record, and reach the exit. A blockout is a rough level made of basic shapes that tests space and gameplay before finished art. The narrative draft is in LEVEL_01_WRECKAGE.md.

Success means a fresh play session can complete the route with understandable objectives, working collision, and the intended first clue. A map that only looks like a wreck is not yet a playable mission. Implementation update, 2026-10-07: the saved Wreckage prototype has passed its recorded route checks; see LEVEL_01_BUILD_REPORT.md for results and test limitations. This plan remains the staged production guide.

## Physics approach

Use Unreal's built-in Chaos physics rather than developing a separate physics engine. Tune how the game feels: movement speed, acceleration, jump height, landing, weapon impacts, and object weight. These values are undecided until a playable test gives us evidence.

Keep floors, cover, structural beams, and the wreck's main shell fixed with simple collision. The ship is already destroyed when play begins; depicting its aftermath does not require simulating the whole ship breaking apart. Let only a few small props move. Debris removal can initially use a controlled interaction/animation so it cannot accidentally trap the player. Add selective breakable panels later if they improve an encounter.

Do not simulate every fragment or turn critical walkways into unstable physics objects. Check that movement and collisions work at different frame rates and that loading a checkpoint restores the correct debris and objective states. No custom physics code, destruction setup, or performance claim is verified yet.

References: [Epic physics documentation](https://dev.epicgames.com/documentation/unreal-engine/physics-in-unreal-engine?lang=en-US), [Epic destruction overview](https://dev.epicgames.com/documentation/unreal-engine/destruction-overview?lang=en-US).

## Work in stages

| Stage | Concrete output | Completion evidence |
| --- | --- | --- |
| 1. Route and scale | One compartment, passage, combat bay, evidence station, and exit made of simple shapes | Player fits through route; cover and sightlines work |
| 2. Player feel | Movement, camera, interactions, a placeholder weapon | Controls are responsive; no recurring collision snags |
| 3. Mission loop | Recovery objectives, one enemy type, evidence, subtitles, transition | Complete mission from a fresh start and after death/reload |
| 4. Visual direction | Compare a few concepts for wreck architecture, Orison ruins, Evan, Clank, and searchers | User approves shapes/material language before asset production |
| 5. Small finished section | Replace one tested room and its immediate props | Scale, collision, lighting, readability, and performance checked in play |
| 6. Expansion | Extend the approved modular kit through the rest of the level | Consistent visual language without redesigning every room |
| 7. Presentation | Voices, effects, animation, optional cinematics | Chosen tools tested; scene transitions and skipping work |

Stages are a recommendation, not a schedule or completion claim. Avoid building the entire planet or complete fleet before the opening can be played.

## Initial asset budget by purpose

Reusable wreck kit: floor, wall, ceiling, door frame, bent beam, broken hull panel, debris cluster, and cables. Make intact and damaged variants only where the route needs them. An exterior ship silhouette can be separate from the rooms the player enters; a complete functional ship interior is unnecessary for this first slice.

Gameplay essentials: one placeholder player/suit setup, Clank marker/model, one searcher body, one weapon, one terminal, and one communications panel. Use placeholders before deciding anatomy, armor, detailed animation, or final weapon design.

Orison identity: one ancient structure silhouette, one material palette, and one distant landmark. Their shapes are unselected. Present alternatives for user review later; do not silently establish extinct-civilization culture through a generated design.

Asset workflow: concept approval → reuse or authorized generation → Blender inspection/cleanup → export → Unreal import → collision/material/animation checks → play test. Preserve Blender sources separately from exports. Existing Meshy assets may be assessed for suitability before spending credits on new ones. No paid generation is part of this plan.

## Immediate prerequisites and limitations

Before building, resolve the wreck environment or explicitly choose a temporary prototype staging. Verify the live editor bridge can make, save, reload, and inspect a dedicated level. Prior toolchain verification covered temporary actor edits only. The latest editor launch opened a local listener, but a fresh toolset-discovery request did not complete and was cancelled; current end-to-end responsiveness still needs checking.

No cinematic has been built, no level assets were modified during this planning pass, and no game play test has run. Next implementation milestone is a saved, walkable blockout; combat and objectives follow after that is verified.
