import unreal,json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
assets=unreal.EditorAssetLibrary.list_assets('/NiagaraFluids',recursive=True)
(r/'reports/volume_plugin_inventory.json').write_text(json.dumps(assets,indent=2))
print('VOLUME_PLUGIN_ASSETS',len(assets),flush=True)
