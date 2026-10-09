import unreal,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];items=[]
cls=unreal.load_class(None,'/Script/NiagaraEditor.NiagaraEmitterEditorData')
for obj in unreal.ObjectIterator(cls):
 p=obj.get_path_name()
 if 'NS_ImpactFireVolume' in p:
  items.append(p);obj.set_editor_property('bShowSummaryView',False)
(R/'reports/volume_editor_objects.json').write_text(json.dumps(items,indent=2));print('VOLUME_STACK_EXPOSED',items,flush=True)
