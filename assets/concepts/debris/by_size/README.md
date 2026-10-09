# Debris reference library by size

Created 2026-10-07. Originals are preserved in the parent directory. This library organizes byte-identical reference copies, not 3D models.

| Folder | Proposed longest dimension | Catalogue candidates |
| --- | --- | --- |
| [01_small](01_small/README.md) | 0.2-0.8 m | 10 |
| [02_medium](02_medium/README.md) | 1-3 m | 24 |
| [03_large](03_large/README.md) | 4-8 m | 2 |
| [04_very_large](04_very_large/README.md) | 12-25 m | 2 |
| [05_enormous](05_enormous/README.md) | 40-70 m | 2 |

[Asset catalogue](asset_catalogue.csv) identifies each prop and its position in the full sheet. There are 40 reference candidates, including 30 new small/medium concepts awaiting review. Exact dimensions and geometry budgets remain open.

00_master_sheets contains all original sheet copies for context. 99_earlier_explorations preserves earlier concepts; D3/D4 enormous room/deck cutaways are superseded by the exterior-only D5 direction. D1 is earlier exploration history, not a separate current production queue.

For modeling: isolate one chosen prop, confirm scale, generate/prepare it, then inspect topology, visible silhouette, collision and materials. Keep outer armor; show shallow electronics at damage rather than rooms or deep internals. Use texture/normal detail where practical. No assets have been generated or imported by this organizing step.

[Ground scatter collection](06_ground_scatter/README.md) cross-references fallen electronics from the small and medium folders.

Production update 2026-10-08: M17 supply trunk and S04 grille have actual Meshy models, separate Blender sources/game exports, and Unreal imports. See docs/DEBRIS_FIRST_PAIR_BUILD_REPORT.md in the project root for QA; all other candidates remain references.
