from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];perf=json.loads((R/'reports/space_impact_v2_performance.json').read_text())
perf.update(editor_pie_resolution_override_disabled=True,dynamic_resolution_disabled=True,background_throttle_disabled_before_capture=True,quality_scope='1526x862 full-resolution editor viewport; not native 1080p packaged-game guarantee')
(R/'reports/space_impact_v2_performance.json').write_text(json.dumps(perf,indent=2))
doc='''# Cinematic space impact scene

Updated 2026-10-08. The user rejected the first presentation: flat fire, pixelated/shimmering ground and poor lighting. Earlier compile/FPS checks did not establish acceptable visual quality. This revision is a review candidate, not accepted or certified production art.

Open `/Game/LostVanguard/Environment/SpaceImpact/Maps/L_SpaceImpact_Cinematic` and press Play. The cinematic camera activates automatically. No gameplay or story changes, no paid generation; assignment spend remains 425/600.

## Corrections

The owned soil texture had TC_EditorIcon compression and TMGS_NoMipmaps. It now uses world-texture compression and generated mipmaps. Soil/stone materials no longer derive normals from screen-space derivatives, which made shading depend on the camera. Unstable heat-refraction cards are hidden; heat distortion remains unfinished.

Fire and smoke now use three bounded, continuously simulated Niagara Fluids 3D gas volumes. NiagaraFluids is enabled in the project; mesh distance-field generation is enabled for its collision dependency. NS_ImpactFireVolume copies Epic's Grid3D_Gas_Fire template into owned assets. Maximum-axis resolutions are 112/80/80, with 240 x 240 x 450 cm bounds per site. Invisible source particles are limited to 20,000/s per site, below the template's 50,000/s; their debug sprite renderer is disabled. Temperature, smoke density and owned MI_ImpactFireVolume tune appearance. NS_ImpactEmbers retains only the old sparks emitter. Original atlas systems/materials are preserved but their fire/smoke emitters are no longer used by burn actors.

Lights are Movable rather than relying on baked lighting, removing the unbuilt Preview shadow markings. The broad key is dimmer, dusk fill/fog adds forest depth, and local flickering firelights have reduced intensity/range. Owned vegetation parents use nonmetallic, rough shading while retaining wind and source color textures.

## Verification and remaining limits

Actual PIE captures: reports/space_impact_v2_cinematic.png and space_impact_v2_alternate.png. Six orbit views and an 18-second continuous runtime camera sweep were recorded and inspected. The ground looks more stable in these tested views and the fire retains depth across the arc. This is limited visual inspection, not artifact-free certification at every distance or on every GPU.

Both Niagara systems compile without errors. The fluid template retains one unused collision ParticleReader warning and module-version information. A live volume-material update caused an Unreal render-thread access violation; the saved scene recovered, and subsequent fresh-launch/play/camera tests completed without another crash. This history remains recorded; short tests do not certify engine-wide stability.

The clean native CSV sample averaged 102.07 FPS: frame mean 9.80 ms, p95 12.61 ms, GPU mean 7.90 ms over 2,334 frames on Ryzen 7 5800X/RTX 3080 Ti. The 1526 x 862 viewport used screen percentage 100 with the editor PIE override and dynamic resolution disabled. Background throttling was disabled before capture and restored afterward, along with the editor override and automatic screen percentage. This is not a native 1920 x 1080 packaged-game guarantee. The 1920 x 1080 images are separate HighResShot captures. Earlier automatic-resolution captures are historical, not the final benchmark.

AI wreck edges remain soft, terrain is a basic presentation mesh/material, rocks need stronger surface detail and some vegetation is angular. Fire shape, framing and environmental art still require user judgment. Technical corrections do not establish the user's desired cinematic quality. Heat distortion is currently disabled, not completed.

Authoring: tools/repair_impact_surfaces.py, install_impact_volume.py, refine_fire_volume_material.py, refine_impact_lighting.py and finalize_impact_repair.py. Native Niagara edits are captured in reports/space_impact_v2_qa.json. Verification: verify_impact_v2.py, orbit_impact_runtime.py and benchmark_impact_v2.py. Historical build/atlas scripts restore rejected settings; do not rerun them as a polish step. Blender source scenes and exported meshes remain distinct. No binary asset edits or filesystem moves were used.
'''
(R/'docs/SPACE_IMPACT_SCENE.md').write_text(doc,encoding='utf-8')
status=R/'docs/STATUS.md';raw=status.read_bytes();heading=b'## Cinematic space impact scene - 2026-10-08';start=raw.index(heading);end=raw.find(b'\n## ',start+len(heading));end=len(raw) if end<0 else end
section='''## Cinematic space impact scene - 2026-10-08

**User rejected the first result**: 2D fire, pixelated/shimmering ground and poor lighting. Original compile/FPS checks did not demonstrate acceptable art. Revised isolated SpaceImpact map is saved for review, not visually accepted.

Corrected soil TC_EditorIcon/NoMipmaps import to world compression/generated mipmaps; removed camera-dependent derivative normals from soil/stone shaders and hid unstable heat cards. Replaced fire/smoke cards with three bounded Niagara Fluids GPU volumes (112/80/80 maximum-axis grids), retained separate sparks, disabled source debug sprites and reduced source rate from 50k to 20k/s per site. Enabled the installed plugin and required mesh distance fields. Made scene lights Movable, removed Preview shadow artifacts, rebalanced dusk/key/firelight and applied rough/nonmetallic vegetation shading. Shared source assets/gameplay maps preserved.

Both effects systems compile without errors; fluid template retains one collision-reader warning. An Unreal render-thread crash occurred during a live material update; saved recovery and later fresh play/camera tests completed without another crash. Six views plus an 18-second continuous camera sweep inspected: ground looks more stable and flames retain depth in tested views. Clean full-resolution 1526x862 PIE timing: 102.07 FPS average / 9.80 ms frame / p95 12.61 ms / 7.90 ms GPU, 2,334 frames on 5800X/3080 Ti. Editor resolution override and dynamic resolution disabled for test; override/automatic screen percentage/background throttle restored. Not native 1080p or packaged/hardware-wide certification.

Actual revised images: reports/space_impact_v2_cinematic.png and space_impact_v2_alternate.png; V2 QA/performance/motion evidence and SPACE_IMPACT_SCENE.md. Terrain surface/rock detail, AI mesh edges and overall art remain unfinished; heat distortion is disabled. No new Meshy spend (425/600). Next: review revised live scene before claiming visual acceptance or expanding production.
'''
status.write_bytes(raw[:start]+section.encode('utf-8')+raw[end:])
log='''
## 2026-10-08 - Rejected impact presentation: rendering repair
- User rates fire/ground/lighting roughly 3/10 and identifies flat fire and moving-ground artifacts. Acknowledged overstated quality; previous compile/FPS evidence did not establish cinematic art acceptance.
- Found owned ground imported as TC_EditorIcon/NoMipmaps; switched to world compression/generated mipmaps, removed screen-derived normals from soil/stone and hid unstable heat-refraction cards. Existing textures/source meshes preserved.
- Enabled installed NiagaraFluids and mesh distance fields; built owned 3D gas fire/smoke volumes, independent ember system, disabled source debug sprites, bounded 112/80/80 grids and reduced source rate to 20k/s. Old atlas assets preserved. Native stack APIs required switching the grid emitter out of summary view; protected editor-data setter attempt failed and changed nothing. Both systems compile without errors; unused collision ParticleReader warning remains.
- Converted lights to Movable to remove Preview shadows and support real-time lighting; broadened/dimmed key, adjusted dusk/fog/firelight, made owned flora shading rough/nonmetallic. A live volume material update caused an engine render-thread access violation. Saved scene recovered; subsequent fresh-launch PIE and moving-camera runs passed without another crash. No broader stability claim.
- Inspected actual 1920x1080 Unreal captures from two angles and six moving-camera views. Continuous 18-second/24-degree runtime sweep recorded. Ground looks more stable across tested views and fire has volume; terrain/rock/AI structural detail and overall art remain limited. Heat distortion disabled and unfinished.
- Discovered editor PIE screen-percentage override, then took a clean sample with override/dynamic resolution disabled, 100 percent screen percentage and background throttle off before capture. 2,334 frames: 102.07 FPS, mean 9.80 ms / p95 12.61 ms, GPU 7.90 ms at 1526x862 on 5800X/3080 Ti. Restored editor override/automatic screen percentage/background throttle, stopped PIE. Earlier incorrect/automatic captures excluded from final timing. Actual V2 images/QA/native CSV/performance reports saved. No paid jobs or gameplay/lore changes, spend425/600.
- Next: user reviews corrected live candidate; no claim of finished art or renewed visual acceptance. Further surface detail, impact-site dressing, heat distortion and art direction remain.
'''
with (R/'docs/WORK_LOG.md').open('ab') as f:f.write(log.encode('utf-8'))
print('IMPACT_REPAIR_RECORDS_UPDATED')
