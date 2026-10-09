# Asset optimization rules — working proposal

2026-10-08. User asks for practical rules for high visual quality and optimized game assets. Current project uses Unreal 5.8.3 and AI-assisted debris production. These are recommendations and starting budgets, not accepted hardware/performance specifications or measured results. Existing accepted exterior-only wreckage requirement remains in force.

## 1. Set a measurable target before mass production

Recommend beginning with a 60 FPS target at 1080p on a specified minimum PC, with adjustable quality settings. 60 FPS permits approximately 16.7ms per frame. CPU and GPU work overlap; diagnose their timings rather than adding them together. User's RTX 3080 Ti is a development machine, not an established minimum requirement. Minimum hardware, resolution and final FPS target remain open.

Test a representative packaged/development build at fixed settings and camera route, including a busy scene with repeated debris, trees, lighting and gameplay. Record frame times and texture memory, including spikes, not just average FPS. Compare before/after importing a new asset set. Profile the bottleneck rather than assuming triangles are the problem.

## 2. Spend geometry on shapes players see

Preserve silhouette, important bevels, thick armor edges, major damage and gameplay openings. Use base-color, roughness and normal-map detail for fine circuitry, scratches, small bolts and soot where silhouette/parallax do not require geometry. Normal maps do not replace actual silhouette or openings.

Exterior debris keeps most armor attached. Shallow local breaches end in a simple backing with only visible electronics. No modeled hidden rooms, decks or furniture. Inspect underside/back when an asset can be flipped or seen from another direction; don't remove surfaces the player can actually see. Simplify tiny shards and hair-thin wiring; use a few readable cable strands. Use consistent normals without accidentally faceting every triangle. UV/normal seams can split imported vertices, so verify Unreal's actual mesh statistics.

## 3. Starter conventional-mesh budgets

Budget final triangulated game meshes, not Blender polygon/quad counts. These ranges are assistant-proposed triage targets, not engine limits, Nanite limits or guaranteed performance. Screen size, visual importance and repetitions override physical size.

| Asset use | Starting triangles per unique mesh | Starting texture size |
| --- | --- | --- |
| Small repeated scatter | 300-1,500 | 512-1,024 |
| Medium prop | 1,500-6,000 | 1,024-2,048 |
| Large visible prop | 5,000-20,000 | 1,024-2,048 plus shared materials |
| Very large/enormous wreck | Budget individual visible structural pieces; select Nanite or conventional LODs after testing | Shared tiled/trim textures plus limited unique damage maps |

Do not force a hero prop to lose its silhouette for a numeric limit. A plain plate may need far fewer triangles; many close-up instances may justify a tighter budget. Reused texture atlases and trim sheets can change the per-asset texture recommendation. Avoid defaulting to unique 4K/8K maps for every scrap. Maintain comparable texture detail per visible meter; avoid stretching a single small texture across enormous hulls.

## 4. Keep materials and textures economical

Aim for one material slot on simple debris; use two when visibly justified. Material instances share a parent shader and help consistency, but do not automatically merge draw calls. Favor opaque materials for armor, unpowered monitors and scorch. Use translucent glass only when players benefit from seeing through it. Avoid expensive multi-layer shaders on every small object. Compress textures appropriately, enable mipmaps/streaming and inspect memory in a representative level. Doubling both image dimensions quadruples pixel count; actual GPU memory depends on format/mips/compression.

## 5. Reuse and reduce work with distance

Use instanced meshes for repeated compatible static debris rather than thousands of unique actors, textures and materials. Build variety from a limited mesh set, rotation, reasonable scale variation and material variation. Use appropriate distance culling for tiny scatter without obvious pop-in; keep navigational landmarks visible. Conventional meshes need useful LODs; eligible Nanite content provides automatic geometric detail management but still needs profiling. Watch dense thin disconnected fragments, cable nests and closely stacked layers: they can produce expensive overdraw and poor simplification.

Do not combine an entire level into one mesh. Large wrecks can use a modest set of coherent shell sections and reusable engine modules, while avoiding hundreds of separate tiny actors. Decide grouping by visibility, reuse, streaming and gameplay, not simply smallest possible object size.

## 6. Collision, physics and gameplay

Tiny decorative wires/scraps often need no blocking collision. Use simple primitive/convex collision for interactable props; build a simplified shell collision for big obstacles. Use complex collision only when required and tested, not automatically on dense generated meshes. Walkable terrain-like wreckage may need more accurate collision while still omitting fine visual damage from it. Only debris with a gameplay purpose simulates physics; allow bodies to sleep and limit active simulations. Static debris does not need per-frame script updates.

## 7. Lighting/shadows are a scene budget

Use lighting and strong composition to establish quality before adding microscopic mesh detail. Limit overlapping shadow-casting movable lights, unnecessary long-range shadows and expensive material displacement. Evaluate whether small distant debris needs dynamic shadows. Virtual Shadow Maps depend on cache reuse; moving objects/lights and animated/deformed shadow casters can increase work. Lumen, foliage, particles and transparency also require scene-level testing. Nanite does not eliminate those costs or collision/physics cost.

## 8. AI asset acceptance checklist

1. Generate one chosen isolated prop at a time, with scale and visible-shell requirements.
2. Keep original source/high-detail output separate from cleaned game export.
3. Inspect connected pieces, hidden/duplicate surfaces, tiny fragments, normals, UVs and actual triangulated counts. Retopologize/remesh where needed; do not merely decimate until damage looks melted.
4. Bake useful high-detail appearance onto the cleaned mesh where appropriate; check lighting and silhouette at real player distance.
5. Reduce material slots and texture sizes; assign simple collision and an appropriate LOD/Nanite choice.
6. Verify import, real scale, grounded pivot/orientation and material appearance in Unreal. Test player movement and physical interactions when relevant.
7. Test many repeated instances in a representative dense scene and record frame-time/memory changes before expanding the library.

No 3D asset, triangle count or performance claim has yet been verified through this guidance task.

## Official sources checked 2026-10-08

- [Epic: performance profiling](https://dev.epicgames.com/documentation/en-us/unreal-engine/introduction-to-performance-profiling-and-configuration-in-unreal-engine)
- [Epic: working with Nanite content](https://dev.epicgames.com/documentation/en-us/unreal-engine/working-with-naniteenabled-content)
- [Epic: instanced static meshes](https://dev.epicgames.com/documentation/en-us/unreal-engine/instanced-static-mesh-component-in-unreal-engine)
- [Epic: simple versus complex collision](https://dev.epicgames.com/documentation/en-us/unreal-engine/simple-versus-complex-collision-in-unreal-engine)
- [Epic: Virtual Shadow Maps](https://dev.epicgames.com/documentation/en-us/unreal-engine/virtual-shadow-maps-in-unreal-engine)
- [Epic: artist performance guidance, legacy general principles](https://dev.epicgames.com/documentation/en-us/unreal-engine/performance-guidelines-for-artists-and-designers?application_version=4.27)

The numeric triangle/texture ranges and proposed 60 FPS/1080p target above are project starting recommendations, not values mandated by these sources.
