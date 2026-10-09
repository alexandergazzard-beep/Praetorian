# Orison terrain proof — 2026-10-08

The user approved the proposed small hybrid terrain proof and increased the Meshy assignment spending ceiling by 300 credits, from 600 to 900. This is an isolated production/workflow test; its layout, sizes and candidate art are not accepted story facts or final mission art.

## Open and walk

In Unreal 5.8.3, open `/Game/LostVanguard/Environment/OrisonTerrain/Maps/L_OrisonTerrain_Review`. Press Play, click the viewport, use WASD and mouse, Space to jump, C to crouch; Escape ends Play. A separate player/game mode avoids the original mission's tutorial and enemy logic. The original maps and assets remain intact. Current editor left on this map with Play stopped.

## What was made

- One real native Landscape: 63 × 63 metres, 127 × 127 samples, two-by-two 63-quad components; low hills and a shallow winding central route. A locally authored little-endian R16 heightmap is preserved under `assets/models/orison_terrain/heightmaps`.
- Three independent source textures: Dirt, Gravel, Stone. `M_OrisonLandscape` blends them automatically with world-space coordinates, route/slope masks and broad colour variation. Mirrored addressing prevents hard tile boundaries but does not guarantee invisible repetition. Ground relief is a weak analytic shader normal, not a scanned PBR height/normal set. Dirt/Gravel/Stone override nodes exist, but Landscape layer-info/brush-painting setup has not been completed or tested. Sculpting uses normal Unreal Landscape tools.
- Three Meshy rocks R01/R02/R06 and stepped ledge T02. Four ledge placements plus 32 rock placements; ten existing trees and 34 existing understory plants reused separately. These are ordinary static-mesh actors in a small proof, not an optimized foliage/instance system. Understory is nonblocking. Production tree trunk-only collision has not been added in this test.
- Individual input PNGs, untouched downloaded textured GLBs/maps, packed Blender source and prepared scenes, portable textured GLB and FBX exports are under `assets/models/orison_terrain`. The pre-remesh high-resolution geometry was not downloaded. No external binary `.uasset`/`.umap` edits or filesystem moves were used.

## Reference consistency

The actual P5 planet alternatives, P1 forest valley, W1 waterfall sheet (accepted W01 top-left habitat), and opening forest-wreck reference were visually reviewed before R2/G2/T2 generation. Individual R01/R02/R06/T02 production inputs derive from those revised sheets; ground texture inputs use G2. Preserve pale weathered warm/cool gray geology, dark soil, muted growth and independent teal/violet flora. Alternative orbital geography remains unselected. Full exact image prompts are in `reports/orison_terrain_image_prompts.json`; prior reference provenance is in `ORISON_GEOLOGY_REFERENCE_REVISION.md`.

## Meshes and checks

| Candidate | UE triangles LOD0 / 1 / 2 / 3 | Actual convex hulls | Provisional longest horizontal size |
|---|---|---|---|
| R01 rounded boulder | 10,224 / 5,112 / 2,249 / 818 | 1 | 2 m |
| R02 fractured boulder | 14,353 / 7,176 / 3,158 / 1,148 | 2 | 2.5 m |
| R06 riverstone cluster | 14,326 / 7,163 / 3,151 / 1,146 | 2 | 3.5 m |
| T02 ledge | 36,450 / 18,224 / 8,018 / 2,916 | 4 | 9 m |

Four native LODs each, thresholds 1 / .4 / .18 / .06, auto-generated convex collision. Counts fit intended ranges. UVs/materials retained. Four actual Blender renders and Unreal preview inspected. Nonmanifold edges remain in generated surfaces (253 / 332 / 298 / 22 after basic cleanup); source quality is not certified watertight. Dedicated convex collision avoids relying on generated surface topology.

Nine editor collision traces passed: each model isolated away from Landscape, plus five route ground positions. Player/game-mode Blueprints strictly compiled; corrected game-mode default pawn compilation, saved and reopened map. Actual PIE then passed possession, walking about 13.15 metres across Landscape, and jumping about .85 metres before landing. Automation feeds movement into the character system and calls Jump; it does not prove physical keyboard/mouse/crouch feel. Evidence: `reports/orison_terrain_unreal_qa.json`, `orison_terrain_collision.json`, `orison_terrain_playtest.json`. Performance evidence is recorded separately in `orison_terrain_performance.json` with its local editor/short-sample limitations.

## Spending

Explicit Meshy7.1 Standard, Ultra4K geometry, 4K PBR, remeshing on, individual budgets10k/14k/14k/35k. Four successful jobs, actual35 each =140 for this batch, checked through successive account balance decreases3590→3555→3520→3485→3450. Pricing source: https://docs.meshy.ai/en/api/pricing (checked2026-10-08). Shared ledger now740/900 spent,160 remaining, zero pending jobs; account balance3450 at completion. Prior five flora expansion jobs account for600 spent before this batch. No credits were purchased and no paid retries were submitted.

## Limits and next use

This proves the combined Landscape + rock modules + separate vegetation approach. The 3D silhouettes/fractures are softer than their concept images, R01 is broader/flatter, and T02 loses fine terraces. Stone ground resembles aggregate, repetition remains visible, the horizon is an unfinished patch boundary, and the scene is sparse. Foliage wind/instancing, production lighting, robust painting layers, all-side climbing/walking collision and packaged-game performance still need work. Review the actual models and ground scale before expanding or integrating into the opening mission. No need to turn every reference image into a separate model.

Performance attempt:31 samples at uniform333.33ms (~3FPS) despite requesting MaxFPS60. Inconclusive for terrain cost; automation/editor rate limiting suspected, precise cause unverified. Previous MaxFPS0 restored. Foreground/packaged-game testing remains required.

Preview: `reports/orison_terrain_unreal_overview.png`.
