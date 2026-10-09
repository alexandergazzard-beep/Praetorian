"""Prepare flagship replacements with the proven source-preserving Blender workflow."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/prepare_wreck_trio.py').read_text()
for old,new in [('Medium_WreckPanel','Medium_Flagship71'),('Large_WreckModule','Large_Flagship71'),('Engine_MeshyNacelle','Engine_Flagship71'),('wreck_trio_blender.json','wreck_flagship71_blender.json')]:source=source.replace(old,new)
exec(compile(source,str(ROOT/'tools/prepare_wreck_trio.py'),'exec'))
