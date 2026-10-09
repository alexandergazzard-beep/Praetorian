# Orison new flora production - 2026-10-08

Five models generated, prepared and visually reviewed. User requests a bunch of new 3D models using best Meshy model and good visual quality. Five choices fit remaining175 credits: F13 broad canopy, F14 spire, F16 cascading tree, F19 cupped-leaf bush, F21 fan-leaf bush. Selection is assistant production judgment within authorized request, not botanical canon or approval of all F13-F22.

## Generation

Explicit meshy-7.1 Standard, Ultra geometry4k, PBR textures4k, image enhancement false, triangular remesh targets60k/45k/60k/16k/14k. Both GLB/FBX requested; high-detail pre-remesh preservation requested. Isolated references remove label, soil and neighboring plants. F13 outermost leaves have tight margins. Isolation is production interpretation rather than exact guaranteed reconstruction.

Official [generation options](https://docs.meshy.ai/en/api/image-to-3d) and [pricing](https://docs.meshy.ai/en/api/pricing) checked2026-10-08: latest equals7.1; textured2K/4K30 plus Ultra5 =35 each. Five jobs measured35 each by immediate before/after account balance,3765 to3590. Assignment600/600, zero remaining. No paid retries or increased cap.

Authoritative tasks/spend: reports/forest_wreck_spending.json. Individual requests reports/F13_expansion71_request.json etc.; specs reports/flora_expansion71_specs.json. Existing approved flora, sources and gameplay maps preserved.

## Reference preparation prompts

Built-in imagegen used, referencing assets/concepts/flora/orison_flora_f3_large_trees_v1.png for trees, orison_flora_f4_bushes_v1.png for bushes. Final references assets/models/forest_wreck/references/F13_isolated_v1.png etc.

- F13: Isolate ONLY F13, TOP LEFT broad canopy tree; preserve thick branching trunk, broad irregular dense layered teal canopy, violet backs, bark and root flare. Remove all other plants, labels, soil and shadow. Plain light gray studio background, entire tree with margin, large readable leaves, branching gaps, realistic neutral lighting. No redesign/text/base disk.
- F14: Isolate ONLY F14, TOP RIGHT tall stepped spire tree; preserve twisting fluted trunk, ascending tiers, tall narrow crown, broad forked teal/violet leaves and lime growth. Remove other trees/labels/ground. Light gray background, full roots/leaves with10% margin. Thick woody structure and gaps, preserve silhouette, no disk.
- F16: Isolate ONLY F16, BOTTOM RIGHT cascading tree; preserve muscular bent trunk/branches, dense draping leaf clusters, teal/violet/lime, no hair vines. Remove neighbors/text/soil/shadow; light gray background, full crown/root flare with10% margin, no redesign/disk.
- F19: Isolate ONLY F19, TOP RIGHT rounded cupped bush; preserve woody stems and dense thick scooped teal leaves with divided tips/violet backs/lime growth. Remove neighbors/text/soil/shadows. Light gray, full bush/base with margins, plausible leaf thickness/gaps, no flowers/disk/redesign.
- F21: Isolate ONLY F21, BOTTOM MIDDLE fan bush; preserve knotted low branches and layered upright thick deeply lobed teal fans/violet backs/lime growth, asymmetric open silhouette. Remove neighbors/text/soil/shadow; gray studio background, neutral light, full plant/margins, no disk/redesign.

## Prepared models and verification

All five tasks SUCCEEDED, downloaded original textured GLB/PBR and untextured high-detail pre-remesh source. Balance3590; assignment600/600, no pending jobs. Blender5.2.1 LTS version rechecked. Packed editable meshy_source.blend preserves import; prepared.blend has duplicate/degenerate cleanup, smooth normals, gentle smoothing (.12 x2), UVs and centered-bottom provisional meter scale. Individual front/back renders inspected. GLB exports verify one mesh, three embedded images and triangles within preferred ranges; color/normal4096 square, roughness/metallic2048 square. Raw sources2.43-7.99million triangles are archived separately, not game exports.

| Plant | Four actual LOD triangle counts | Approx height |
| --- | --- | --- |
| F13 broad canopy | 47969 / 26138 / 14193 / 3771 | 14m |
| F14 spire | 41594 / 20483 / 14124 / 4060 | 16m |
| F16 cascading | 55302 / 30333 / 23344 / 6961 | 12m |
| F19 cupped bush | 15948 / 7908 / 6257 / 4467 | 1.6m |
| F21 fan bush | 14150 / 6786 / 3307 / 2002 | 2m |

Each assets/models/forest_wreck/F##_Expansion71 folder contains source, blender and export folders: base FBX/portable textured GLB and four separate FBX LOD files. FBX materials need accompanying source textures during engine import. LOD reduction first hit a floor on nonmanifold foliage; corrected with increasing distance-based vertex welding plus collapse, retaining UV loops. Distant silhouettes/texture seams still require engine distance testing before game acceptance.

Actual [1920x1080 Cycles48 model overview](../reports/flora_expansion71_overview.png), all five labeled/fully visible, normalized display sizes rather than common world scale. Editable presentation assets/models/forest_wreck/Flora_Expansion71_Presentation.blend. This is a render of real prepared meshes, not image-generated concept art.

Limits: leaf edges are angular in places, some small canopy leaves merge or crumple, back geometry is inferred, reduced foliage not identical to isolated references. F13 canopy is less continuous than concept. All retain generated foliage; no bare-tree repair or paid retries. Open/nonmanifold boundaries694-11311 per base mesh remain; not watertight engineered geometry. No Unreal changes, wind, collision, instancing, play tests or FPS validation in this batch. User visual acceptance pending. Next: review actual candidates, then authorized placement/import and representative distance/performance tuning.

Evidence: flora_expansion71_blender.json, _glb_exports.json, _file_verification.json, _lods.json and front/back PNGs in reports. Blender harmless restricted thumbnail/add-on-log warnings occurred; owned model files/export/render completion verified independently. Initial Blender LOD assertion returned exit0; corrected runner uses --python-exit-code1 and checks actual reports/files.

Twenty exported FBX LODs were actually reimported, all five base counts matched, each had UVs and four decreasing nonzero levels. FBX importer removed a small number of invalid reduced triangles; authoritative counts in flora_expansion71_lods.json use reimport results, pre-export counts retained. See flora_expansion71_fbx_roundtrip.json.

Concurrent-work ledger clarification:600/600 and balance3590 above are snapshots at this five-plant batch completion, not latest account totals. Final shared-ledger read found a separately recorded terrain approval raising cap to900, four other terrain jobs costing140 pending, total740/900,160 remaining, balance3450. This chat's five flora jobs are all complete and cost175; it submitted no terrain jobs and did not increase the cap. Preserve other work's ledger entries.
