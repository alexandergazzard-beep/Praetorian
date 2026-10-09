"""Export portable textured flagship replacements from separate prepared sources."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/export_wreck_trio_glb.py').read_text()
for old,new in [('Medium_WreckPanel','Medium_Flagship71'),('Large_WreckModule','Large_Flagship71'),('Engine_MeshyNacelle','Engine_Flagship71'),('wreck_trio_glb_exports.json','wreck_flagship71_glb_exports.json')]:source=source.replace(old,new)
exec(compile(source,str(ROOT/'tools/export_wreck_trio_glb.py'),'exec'))
