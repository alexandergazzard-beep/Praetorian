# Flagship wreck replacements — 2026-10-08

User explicitly requests Meshy's flagship rather than Smart Topology, with controlled optimization. Current selected Medium, Large and D5 engine were recreated using `meshy-7.1`, `model_type: standard`, `geometry_resolution: 4k`, `should_remesh: true`, triangle topology, target counts 30,000/65,000/45,000, PBR and 4K textures. `image_enhancement: false` preserves the deliberate isolated source appearance. No adaptive decimation_mode, which would override target counts. Source images are the same isolated references; no paid reference-image generation or new design/canon.

Official [Image-to-3D settings](https://docs.meshy.ai/en/api/image-to-3d) identify latest as Meshy 7.1 and describe Standard/remesh controls. [API pricing](https://docs.meshy.ai/en/api/pricing) checked 2026-10-08: 30 credits for textured flagship 4K plus 5-credit Ultra geometry surcharge, **35 per model / 105 batch**. Actual immediate account differences match. Assignment **180/600 spent, 420 remaining**, account 4,010; all three succeeded, no pending jobs. Ledger preserves all prior jobs, unused Very Large charge and zero-charge local failures. Never resubmit unknown task outcomes.

## Optimized outputs

| Model | Preferred LOD0 range | Actual Unreal LOD triangles | Provisional dimensions, meters |
| --- | --- | --- | --- |
| Medium_Flagship71 | 25,000–35,000 | 29,950 / 14,975 / 6,588 / 2,393 | 6.472 × 1.513 × 4.500 |
| Large_Flagship71 | 55,000–75,000 | 66,252 / 33,126 / 14,576 / 5,301 | 12.000 × 5.913 × 5.670 |
| Engine_Flagship71 | 35,000–55,000 | 44,866 / 22,432 / 9,871 / 3,587 | 12.000 × 4.366 × 5.064 |

Conventional LOD thresholds 1/.4/.18/.07; Nanite disabled; one 16-vertex convex hull per prop. Triangle targets are approximate, actual counts checked. These budgets are production choices, not FPS guarantees. Collision treats pieces as solid exterior obstacles; visual openings are not traversable.

Under `assets/models/forest_wreck/<model>/`: source/meshy_original.glb is the generated textured remesh; source/meshy_original_textures contains actual 4096×4096 base color/normal and 2048×2048 metallic/roughness. source/meshy_pre_remeshed.glb preserves high-detail **untextured** geometry: 4,290,194 / 6,325,202 / 5,095,510 triangles, approximately 103/152/122 MB. These source files do not go into gameplay. They exceed 100 MB in places and would require the project's Git LFS workflow before any requested push; no commit/push performed.

Blender/source scenes preserve imported geometry; blender/prepared.blend has packed textures, duplicate/degenerate cleanup, recalculated normals, one UV layer, one material, centered bottom pivot and provisional meter scale. Export/SM_<model>.fbx supports Unreal import; export/SM_<model>.glb is portable, with one mesh and three embedded PBR images verified. Old Smart Topology directories, sources, exports and maps untouched.

New native Unreal folder: `/Game/LostVanguard/Environment/OpeningReview/Assets/WreckFlagship71`. Neutral inspection map: `/Game/LostVanguard/Environment/OpeningReview/Maps/L_Wreck_Flagship71_Inspection`. Original gameplay, forest review, prior trio inspection and rejected showcase preserved; no automatic scene replacement or full gameplay integration in this batch. Materials use 4K maximum texture size, sRGB base color, flipped normal green and linear roughness/metallic. All Unreal writes via supported editor APIs.

Evidence: reports/wreck_flagship71_blender.json, wreck_flagship71_glb_exports.json, wreck_flagship71_file_verification.json, wreck_flagship71_unreal_import.json and wreck_flagship71_unreal_qa.json. Blender front/back renders are reports/<model>_blender_0.png and _1.png; Large_Flagship71_close.png provides a closer neutral view. Saved map reload and all three player-height traces pass; all four focused actual PIE checks passed (startup and each mesh/collision presence), recorded in the QA report. Editor left on this inspection map with PIE stopped.

## Visual judgment and limits

Compared neutral front/back renders to preserved older outputs. Large's overall horizontal construction is closer to its selected reference, with shallower inferred depth and more distinct frame/panel edges. Medium piping and armor boundaries and engine plate seams read more clearly. Gray/olive coloring remains deliberately muted; the flagship switch alone is not a finished art pass or guarantee of sharp engineering detail. Back/side geometry is still inferred and some thin edges/mechanical features remain softened.

Prepared meshes retain 1,099 / 3,886 / 2,396 nonmanifold edges respectively, so watertightness and production topology acceptance are not claimed. Budgeted counts/LODs do not prove performance. F01 tree, paper-like foliage and scene composition/lighting require separate work; no tree or unused Very Large regeneration charged in this batch. Full environment gate remains open. Next: user judges these clearer neutral candidates before further shape/material polishing or scene replacement.
