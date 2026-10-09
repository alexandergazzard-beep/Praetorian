# Medium, Large and D5 engine — 2026-10-08

User requested three 3D wreck models and corrected Very Large to **Large**, the upper-right specimen on the supplied size sheet. Current selection: Medium_WreckPanel, Large_WreckModule and Engine_MeshyNacelle. D090 supersedes D087. No new story facts or final appearance acceptance inferred.

All selected textured Meshy candidates succeeded and are preserved as original GLBs with separate base-color, normal, roughness and metallic maps. Prepared Blender scenes have packed textures, cleaned duplicate vertices, recalculated face normals, one UV layer, one material and centered bottom pivots. FBX exports are imported into isolated Unreal 5.8.3 packages; portable prepared GLB exports include textures and meter scale. Blender version verified 5.2.1 LTS. Physical sizes are provisional production choices.

| Selected model | Dimensions in meters | Unreal LOD triangles | Collision |
| --- | --- | --- | --- |
| Medium panel | 5.519 × 1.387 × 4.500 | 15,037 / 7,518 / 3,309 | One 16-vertex convex hull |
| Large wreck module | 12.000 × 9.706 × 6.885 | 14,501 / 7,250 / 3,190 | One 16-vertex convex hull |
| D5 engine nacelle | 12.000 × 5.444 × 5.603 | 12,952 / 6,476 / 2,850 | One 16-vertex convex hull |

Meshy's target counts are requests, not guaranteed final triangle counts. Conventional LOD thresholds 1 / .35 / .14; Nanite disabled. Unreal materials use 2K PBR maps, normal green-channel flip, linear roughness/metallic, and sRGB base color.

## Files and inspection

Under `assets/models/forest_wreck/<model>/`:

- `source/meshy_original.glb` and `source/meshy_original_textures/` preserve the generated source.
- `blender/meshy_source.blend` preserves the imported scene; `blender/prepared.blend` is the editable scaled/export source.
- `export/SM_<model>.fbx` is the Unreal mesh export; `export/SM_<model>.glb` is a portable textured export.

New Unreal folder: `/Game/LostVanguard/Environment/OpeningReview/Assets/WreckTrio`. Separate inspection map: `/Game/LostVanguard/Environment/OpeningReview/Maps/L_Wreck_Trio_Inspection`. No trio placements added to the original opening or existing forest review map. Imported exclusively through native editor APIs; no binary filesystem edits. Existing gameplay regression remains 19/19; this new isolated map requires only its relevant inspection/play-mode checks.

Evidence: `reports/wreck_trio_blender.json`, `wreck_trio_glb_exports.json`, `wreck_trio_unreal_import.json`, `wreck_trio_unreal_qa.json`. Front/back Blender images: `reports/<model>_blender_0.png` and `_1.png`. Unreal diagnostic captures: `reports/wreck_trio_unreal_0.png` through `_3.png`; improved lit view is `wreck_trio_unreal_final.png`. Saved-map reload and all three player-height collision traces passed. **4/4 focused PIE checks passed**: map runs and each selected mesh/collision profile is present in the actual play world. First smoke-test reader used incorrect BodyInstance property casing and failed; corrected to actual camelCase and reran successfully, with PIE stopped on both attempts. No player movement/physical input feel or opening-route integration claimed. Editor left on the trio inspection map, PIE stopped.

## Budget and superseded extra

Each paid task cost 15 credits: F01 tree plus engine, Medium, Very Large and corrected Large. **75 / 600 credits spent, 525 remaining; account balance 4,115; no pending jobs.** Very Large had already succeeded when user corrected selection; no cancellation or refund occurred. It is preserved at `assets/models/forest_wreck/VeryLarge_HullFace/source/meshy_original.glb` as an unused extra, with no Blender preparation or Unreal import. Two over-limit local connector requests were rejected before API submission and cost zero; corrected known jobs use the 15,000 target-face cap. Ledger: `reports/forest_wreck_spending.json`.

## Visual limits and next checkpoint

Front/back renders were inspected. The three silhouettes, gray/olive armor and pipe/frame motifs read in 3D. Large's unseen depth and opposite face are generated interpretations; fine edges, mechanical fixtures and plates show AI softness/distortion. Medium is largely armored on both sides. The engine has visible shallow cylindrical surfaces/open ends and does not reproduce a full engineered engine interior. Prepared meshes retain 239 / 217 / 146 nonmanifold edges respectively; watertightness and production topology acceptance are not claimed. Convex collision intentionally blocks visual gaps and engine openings; these are exterior props, not traversable interiors.

These are usable inspection candidates, not a finished environment pack or a proven 9/10 fidelity result. Performance, physical player feel, final lighting, repeated placements and full scene acceptance remain open. Next: review selected meshes, address high-value silhouette/shading issues, then integrate suitable pieces into the separate forest review and retest gameplay there. Preserve the full environment's tree/major-wreck sample gate before batch expansion.
