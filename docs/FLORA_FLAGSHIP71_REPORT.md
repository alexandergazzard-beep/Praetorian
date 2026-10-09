# Flagship reference vegetation recreation — 2026-10-08

User requests trees and other reference plants recreated with the new Meshy model. This batch follows the existing seven-plant opening selection, not every specimen on both sheets. Old models and gameplay/review maps preserved. New dimensions remain provisional production choices, not lore.

## Generation and spending

Explicit meshy-7.1 Standard, geometry_resolution 4k, textured/PBR, 4k base color/normal and actual 2k metallic/roughness, triangle remesh targets 28k/22k/18k/8k/6k/4k/3k, image_enhancement false. Raw untextured pre-remesh sources preserved separately from gameplay exports. Current official [Image-to-3D options](https://docs.meshy.ai/en/api/image-to-3d) and [pricing](https://docs.meshy.ai/en/api/pricing) checked. Seven succeeded jobs charged 35 each: **245 this batch, 425/600 assignment spent, 175 remaining, zero pending jobs**. Account balance 3765. No paid retries.

F01 uses the previous isolated reference. Six other plants were isolated from approved F1/F2 sheets with built-in imagegen, visually inspected and saved under assets/models/forest_wreck/references. Exact prompts and source/output paths: reports/flora_flagship71_reference_prompts.json. Isolation removes rocks/soil/companion vegetation and is a production interpretation, not a redesign accepted as canon.

## Prepared assets

| Asset | Preferred LOD0 range | Actual four LOD triangle counts | Height (meters) |
| --- | --- | --- | --- |
| Layered canopy tree (repaired foliage) | 24000–32000 | 25,907 / 12,954 / 5,699 / 2,073 | 9.0 |
| Split-trunk tree | 18000–26000 | 22,847 / 11,424 / 5,026 / 1,828 | 5.5 |
| Leaning fan tree | 14000–22000 | 16,443 / 8,220 / 3,617 / 1,316 | 4.5 |
| Spreading shrub | 6000–10000 | 7,501 / 3,751 / 1,649 / 601 | 2.0 |
| Arched fern | 4000–8000 | 5,249 / 2,625 / 1,153 / 420 | 1.2 |
| Blade clump | 3000–6000 | 4,138 / 2,069 / 910 / 332 | 1.0 |
| Ground cover | 2000–4500 | 2,076 / 1,038 / 456 / 167 | 0.45 |

Each assets/models/forest_wreck/<ID>/ contains source/meshy_original.glb and original PNG PBR maps; source/meshy_pre_remeshed.glb is untextured raw geometry; blender/meshy_source.blend preserves packed import; blender/prepared.blend contains centered-bottom meter-scaled prepared mesh; export/SM_<ID>.fbx and .glb are separate portable exports. All seven GLBs verify one mesh, embedded PBR images, actual counts within preferred ranges and actual PNG dimensions. Raw sources span 0.95–8.04M triangles and are excluded from gameplay; larger files need Git LFS before any requested push. No commit/push performed.

## Canopy repair and visual limits

F01 flagship remesh returned only 11,507 triangles and almost no canopy despite the leafy reference. File range verification rejected that result; no charge was repeated. Preserved generated source and raw high-resolution geometry, retained new generated trunk, authored 600 curved forked leaves at 60 actual upper-branch anchors. Repaired F01: 25,907 triangles and two material slots. Leaf texture is existing project T_Leaf_BaseColor with violet reverse in Blender/Unreal; wood retains new Meshy PBR. This is a hybrid repair, not an untouched successful Meshy canopy reconstruction. Sources show the failure in F01_Flagship71_blender_0/1.png; final repaired presentation is flora_flagship71_overview.png. Canopy density and branch silhouette still fall short of the reference.

Other six retain generated geometry, with small duplicate/degenerate cleanup, recalculated normals, UVs and packed textures. Broad leaves have teal/violet distinction but some edges, particularly ground cover, remain angular or merged after reduction. Nonmanifold/open leaf boundaries remain; watertightness, engineering topology and final visual acceptance are not claimed. No wind, instancing, foliage-system placement, packaged build or frame-time benchmark. Provisional size and trunk collider fit need representative gameplay review.

The 1920×1080 overview is an actual Blender Cycles32 render of the prepared meshes with normalized display sizes, not relative gameplay scale or a generated illustration. Editable presentation: assets/models/forest_wreck/Flora_Flagship71_Presentation.blend. First bright inspection renders washed out color; overview exposure and label material corrected without repainting textures. Portable GLB retains textured two-sided F01 leaves but its format uses the front texture on both sides; the custom violet-back shader is present in Blender/Unreal.

## Unreal verification

Active Unreal/LostVanguard 5.8/LostVanguard.uproject, Unreal5.8.3, imported with supported native editor APIs. New folder /Game/LostVanguard/Environment/OpeningReview/Assets/FloraFlagship71; separate map /Game/LostVanguard/Environment/OpeningReview/Maps/L_Flora_Flagship71_Inspection. Generated materials two-sided, base color sRGB, normal green flipped, roughness/metallic linear. Four conventional LODs at thresholds1/.4/.18/.07; Nanite disabled. Mesh collision disabled for all foliage; three isolated hidden cube blockers cover tree trunks.

Saved map reload and all three trunk-hit/canopy-clear traces plus all four understory-clear traces passed. **11/11 focused actual PIE checks passed**, including startup, each plant mesh/nonblocking foliage and the three blocking trunk proxies. Editor left on the new inspection map, PIE stopped; authoritative result in reports/flora_flagship71_unreal_qa.json. Original opening/forest review/rejected showcase/prior inspections preserved; no automatic gameplay replacement. FPS and full environment quality gate remain unverified.

Evidence: flora_flagship71_blender.json, _glb_exports.json, _file_verification.json, _unreal_import.json, _unreal_qa.json and actual _unreal_0/1/2/3/final.png captures in reports. Next: user judges these candidates, then address foliage outline/canopy fidelity, wind/instancing and representative scene/performance checks.
