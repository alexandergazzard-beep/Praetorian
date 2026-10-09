"""Import replacements in new native Unreal packages/map, preserving old comparisons."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/import_wreck_trio.py').read_text()
for old,new in [('Medium_WreckPanel','Medium_Flagship71'),('Large_WreckModule','Large_Flagship71'),('Engine_MeshyNacelle','Engine_Flagship71'),('Assets/WreckTrio','Assets/WreckFlagship71'),('L_Wreck_Trio_Inspection','L_Wreck_Flagship71_Inspection'),('wreck_trio_unreal_import.json','wreck_flagship71_unreal_import.json'),('max_texture_size\',2048','max_texture_size\',4096')]:source=source.replace(old,new)
exec(compile(source,str(ROOT/'tools/import_wreck_trio.py'),'exec'))
