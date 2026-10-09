# First debris pair — 2026-10-08

The user authorized a couple of Meshy 3D assets, cleanup, Unreal placement and quality iteration. Generated M17 supply trunk from D9 and S04 grille from D6, each using a new isolated ChatGPT single-prop reference. These particular finished meshes still await user visual approval.

## Completed production

| Asset | Longest dimension | Triangles near / middle / far | Materials | Collision |
| --- | --- | --- | --- | --- |
| M17 supply trunk | 1.8m | 4,224 / 2,111 / 1,056 | 1 | One convex hull, no simulation |
| S04 vent grille | 0.75m | 1,302 / 650 / 326 | 1 | None, decorative |

Meshy used meshy-t2 Smart Topology with PBR textures, requested 4,500/1,200 triangles, generated actual counts above. Two successful tasks consumed 15 credits each: **30 total; balance verified 4,220 -> 4,190**. No purchase, recharge, animation, rigging or extra 3D generation.

Original GLBs and downloaded PNG maps remain untouched in each assets/models/debris/{asset}/source folder. Separate Blender 5.2.1 source and game-ready scenes are in blender/; meter-scale FBX game exports are in export/. Duplicate vertices and degenerates were cleaned; UVs retained. Each has one UV set/material and centered bottom pivot. Models represent closed props; no modeled ship rooms or interiors.

Unreal 5.8.3 meshes and four-map PBR materials are under /Game/LostVanguard/Art/Debris/FirstPair. A shared master M_Debris_PBR_Final feeds two material instances; roughness is clamped to at least 0.6 to avoid overly glossy damaged paint. Base color uses sRGB; scalar maps use linear data; normal uses normal compression/green inversion from the GLB convention. Crate textures are capped at 2K, grille at 1K with streaming retained. Shader compilation passed after correcting Clamp's input name to None. Conventional LODs are used; these small meshes do not need Nanite.

Both are saved beside the early recovery path in /Game/WreckagePrototype/Maps/L_Wreckage_Opening: crate (350,250,0cm), grille (100,290,9cm), grille laid down with 90-degree roll. The center route and PlayerStart are unchanged. Separate neutral-lit inspection map: /Game/LostVanguard/Art/Review/L_Debris_FirstPair_Review.

## Verification and limitations

Saved reports: debris_pair_meshy_tasks.json, debris_pair_blender.json, debris_pair_unreal_import.json and debris_pair_unreal_qa.json under reports/. Actual Unreal captures: debris_pair_in_level.png and debris_pair_studio.png. Early untextured mesh thumbnail captures are geometry diagnostics, not the final material appearance.

Live queries confirm bounds, three LODs, material assignment and placed actors. **The final gameplay rerun passed all 19 checks with no errors**, including recovery, movement/crouch/jump, combat damage and kills, death/restart, record retention, communications and gated mission completion. Report: opening_playtest.json. Initial attempts exposed a false PIE-warmup error and expected death occurring during the test's turning loop; the helper verifies actual PIE state and explicitly handles death during that expected-death test. No gameplay Blueprint changes were needed.

No packaged build or repeat-instance frame-time benchmark yet. Triangle counts alone do not establish FPS. Human keyboard/mouse feel and close-up review remain necessary. AI-generated edges/handles retain some soft, uneven geometry; these are background/mid-distance debris candidates rather than finished close-up hero props. A solid 9/10 overall quality rating is not yet substantiated.

## Integration findings

The actual running editor uses **Unreal/LostVanguard 5.8/LostVanguard.uproject**. Older records and initial import referred to Unreal/LostVanguard/LostVanguard.uproject. Both initial new debris assets also exist in that older project; the verified live import and placement are in the active 5.8 copy. No existing assets were removed or binary-edited. New project selection must verify the active editor path; never print its full process command line because launch arguments can include temporary authentication data.

Commandlets cannot access the live StaticMeshEditorSubsystem, so LOD/collision preparation ran through native live MCP instead. Live native AssetTools initially could not save the master absent from its cached registry; duplicating it through the editor API as M_Debris_PBR_Final registered it, and explicit save calls passed. Do not rerun background authoring scripts against already loaded assets while the editor has unsaved changes.

Next: user visual review; sharpen major damaged edges/handles if these will be used close to the player, and profile repeated instances on a chosen target machine before bulk generation.
