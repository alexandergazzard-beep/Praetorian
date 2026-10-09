import unreal,json,sys
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as BP
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from movement_profiles import PROFILES,ACTIVE_PROFILE
report={'blueprints':[]}
for name in ['BP_WreckagePlayer_Runtime','BP_WreckageGameMode_Runtime','BP_WreckageHUD','BP_SearcherPlaceholder_Runtime']:
 path='/Game/WreckagePrototype/Blueprints/'+name
 bp=unreal.load_asset(path)
 assert bp,path
 BP.compile_blueprint(bp,True);assert unreal.EditorAssetLibrary.save_loaded_asset(bp)
 report['blueprints'].append({'path':path,'strict_compile':True})
bp=unreal.load_asset('/Game/WreckagePrototype/Blueprints/BP_WreckagePlayer_Runtime');cdo=BP.get_default_object(bp)
report['defaults']={'Health':cdo.get_editor_property('Health'),'Step':cdo.get_editor_property('Step'),'LookSensitivity':cdo.get_editor_property('LookSensitivity')}
assert report['defaults']=={'Health':100,'Step':0,'LookSensitivity':.6}
report['profile']=PROFILES[ACTIVE_PROFILE]
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
(R/'reports/combined_blueprint_verification.json').write_text(json.dumps(report,indent=2))
print('COMBINED_BLUEPRINTS_VERIFIED')
