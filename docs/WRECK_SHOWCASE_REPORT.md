# Large wreck visual test — 2026-10-08

User requested a cool scene with textured Large ship pieces to test what AI can produce. Built an editable 3D crash-site presentation using two placements of the selected Large module, the D5 engine, Medium armor, M17 supply trunk for familiar scale, alien trees, rough ground, stones and armor fragments. Cool forest lighting, warm fault lights and haze provide depth. Lighting/dressing are presentation choices, not established story facts or user acceptance of final appearance.

**Subsequent user review: result rejected as not what they wanted.** Assistant identified warped/soft wreck geometry, weak material/color separation, paper-like foliage and muted lighting/fog as contributing weaknesses. User directs flagship Meshy regeneration instead of Smart Topology (D092). Preserve this scene as historical evidence, not an accepted visual target or successful quality gate.

## Results and files

- Clean real 3D render: `reports/wreck_showcase_beauty.png`, 1920×1080, Cycles 64 samples with denoising. Blender 5.2.1 LTS; observed background run approximately 2 minutes 29 seconds, not a real-time performance measurement.
- Editable Blender scene: `assets/models/wreck_showcase/blender/LargeWreck_Showcase.blend`. All loaded material image dependencies packed; source reopened and checked via `reports/wreck_showcase_blender_verification.json`.
- Editable dressing source: `assets/models/wreck_showcase/blender/ShowcaseDressing.blend`, with separate FBX exports for 30,752-triangle terrain, three 80-triangle rock shapes and three 12-triangle broken armor plates. Ground and rock surfaces are procedural materials; wreck/wood/foliage use existing textured materials. Blender scene also contains sparse short grass geometry.
- Isolated Unreal map: `/Game/LostVanguard/Environment/WreckShowcase/Maps/L_LargeWreck_Showcase`. New assets/materials live under `/Game/LostVanguard/Environment/WreckShowcase`. 154 showcase actors. Original meshes/materials reused without modifying them; no Very Large extra used.
- Actual Unreal captures: `reports/wreck_showcase_0.png`, `_1.png`, `_2.png`. These are real editor viewport views and can retain editor grid/icons. Blender beauty is separately labelled and must not be represented as an Unreal screenshot. The two authored presentations differ in renderer, lighting, transforms and minor dressing.

Unreal's saved-map reload, player-start ground collision trace (430.53cm) and actual PIE startup with the hero wreck present passed. Editor left on this scene at the main camera, PIE stopped. No player navigation/encounter/mission regression claimed for this isolated visual test. Existing opening/review gameplay checks remain preserved separately.

## Iteration and compatibility

First Unreal material connection needed the installed Noise node's `World Position` pin, rather than the property name `Position`. The installed fog component uses `enable_volumetric_fog`. Resolved through actual material pin enumeration and installed 5.8 headers; final commandlet completed with zero errors/warnings. Checked Epic's current [Exponential Height Fog documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/exponential-height-fog-in-unreal-engine) and [Volumetric Fog documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/volumetric-fog-in-unreal-engine) for scene fog/light controls.

First captured composition was obstructed by a foreground tree and lighting washed out the textures. Preserved first-pass images, moved twelve obstructing trees into the background, reduced key/rim/fault lighting, adjusted exposure and recaptured. Final images were visually inspected. Blender scene independently renders the actual textured meshes with procedural ground bump and atmospheric volume; no generated flat illustration or image retouching used.

## Scope, cost and limits

No new Meshy generation, upload or paid operation. Assignment spend remains 75/600, 525 remaining. No credentials or new service required. Original opening, forest review and trio inspection maps preserved; native editor APIs authored all Unreal assets/maps, with no binary filesystem edits.

This fulfills the requested visual demonstration. It is not the finished forest/wreck environment pack. Generated wreck edge softness, inferred unseen geometry, paper-like foliage, simple rock topology, collision around openings, repeated-asset appearance, performance and physical player feel remain production concerns. No FPS, 9/10 quality or full gameplay readiness claim. Next: user judges the style/result; refine the representative assets and carry suitable scene techniques into the separate gameplay review before its next route regression.
