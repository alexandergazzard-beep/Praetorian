"""Finalize focused project records only after successful file verification."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
roundtrip=json.loads((ROOT/'reports/flora_expansion71_fbx_roundtrip.json').read_text())
assert len(roundtrip)==20 and all(x['roundtrip'] for x in roundtrip)
lods=json.loads((ROOT/'reports/flora_expansion71_lods.json').read_text())
report=ROOT/'docs/FLORA_EXPANSION71_REPORT.md';text=report.read_text(encoding='utf-8')
for asset,record in lods.items():
 key=asset[:3];counts=' / '.join(str(n) for n in record['triangles'])
 text=re.sub(r'(^\| '+key+r' [^|]+\| )[^|]+( \|)',lambda m:m[1]+counts+m[2],text,flags=re.M)
text+='\nTwenty exported FBX LODs were actually reimported, all five base counts matched, each had UVs and four decreasing nonzero levels. FBX importer removed a small number of invalid reduced triangles; authoritative counts in flora_expansion71_lods.json use reimport results, pre-export counts retained. See flora_expansion71_fbx_roundtrip.json.\n'
report.write_text(text,encoding='utf-8')
status=ROOT/'docs/STATUS.md';raw=status.read_bytes()
head=b'## Additional Orison trees and bushes - 2026-10-08'
start=raw.index(head);end=raw.find(b'\n## ',start+len(head));assert end>start
note='''## New Orison flora models - 2026-10-08

Five new plants F13/F14/F16 trees and F19/F21 bushes generated using Meshy7.1 Standard Ultra4K geometry/PBR, cleaned in Blender5.2.1, packed editable sources plus portable textured GLB/base FBX and four FBX LODs each. Actual LOD0 counts47969/41594/55302/15948/14150 fit ranges. Five GLBs/textures verified; twenty FBX LODs actually reimported with UVs/decreasing counts. Actual front/back and1920x1080 overview renders inspected. Generated/raw sources preserved; no Unreal changes or performance/wind/distance testing. Some angular/merged leaves and inferred backs remain; visual acceptance pending. Batch175; assignment600/600 spent, zero pending, balance3590. See FLORA_EXPANSION71_REPORT.md and reports/flora_expansion71_overview.png. Next: user reviews actual models before placement/import.
'''
raw=raw[:start]+note.encode()+raw[end:]
marker=b'## Orison flora expansion production - 2026-10-08 (in progress)'
if marker in raw:
 start=raw.index(marker);end=raw.find(b'\n## ',start+len(marker))
 raw=raw[:start]+(raw[end:] if end>=0 else b'')
status.write_bytes(raw)
with (ROOT/'docs/WORK_LOG.md').open('a',encoding='utf-8') as f:
 f.write('''\n\n## 2026-10-08 - New flagship flora batch completed
- Five paid tasks succeeded/downloaded; no retries, balance3590, assignment600/600, zero pending. Sources include original GLB/PBR and untextured2.43-7.99M-triangle raw geometry.
- Prepared packed Blender sources and centered-bottom provisional scale; duplicate/degenerate cleanup, smooth normals and gentle smoothing. Actual front/back renders inspected; all retain generated foliage.
- Portable textured GLB/base FBX, four separate FBX LODs per model, editable real-model presentation and Cycles48 overview saved. LOD0 counts47969/41594/55302/15948/14150 pass budgets; texture dimensions verified.
- Initial collapse-only LODs hit nonmanifold floor. Added distance-based welding, triangulation/cleanup and actual twenty-file FBX reimport verification; importer strips some reduced invalid triangles, recorded actual counts and pre-export differences. All base counts match, UVs present, distance counts decrease. Blender Python errors now use nonzero exit code in checks.
- Angular/merged small leaves, imperfect canopy fidelity/inferred backs and open geometry remain; no production-quality guarantee. No Unreal edits, engine distance/wind/instancing/FPS tests or canon changes. Full report FLORA_EXPANSION71_REPORT.md; STATUS current. Next: user judges actual models, then requested engine placement/tuning.
''')
print('FLORA_EXPANSION_RECORDS_COMPLETE',len(roundtrip),flush=True)
