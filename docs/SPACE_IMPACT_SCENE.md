# Cinematic space impact scene

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
