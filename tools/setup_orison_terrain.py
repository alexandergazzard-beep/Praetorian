"""Native editor terrain review setup. Own new packages only."""
import unreal,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[1];D='/Game/LostVanguard/Environment/OrisonTerrain'
MAP=D+'/Maps/L_OrisonTerrain_Review';T=unreal.AssetToolsHelpers.get_asset_tools();L=unreal.MaterialEditingLibrary
E=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);S=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
assert 'LostVanguard 5.8' in unreal.Paths.get_project_file_path()
if not unreal.EditorAssetLibrary.does_asset_exist(MAP):
 assert S.save_current_level();assert S.new_level(MAP)
else:
 assert unreal.EditorLevelLibrary.get_editor_world().get_path_name().split('.')[0]==MAP
def imp(src,name):
 existing=unreal.load_asset(D+'/Textures/'+name)
 if existing:return existing
 task=unreal.AssetImportTask();task.filename=str(src);task.destination_path=D+'/Textures';task.destination_name=name;task.automated=True;task.save=True
 T.import_asset_tasks([task]);assert task.imported_object_paths
 a=unreal.load_asset(task.imported_object_paths[0]);a.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_DEFAULT)
 a.set_editor_property('mip_gen_settings',unreal.TextureMipGenSettings.TMGS_FROM_TEXTURE_GROUP)
 a.set_editor_property('lod_group',unreal.TextureGroup.TEXTUREGROUP_WORLD);a.set_editor_property('max_texture_size',2048)
 a.set_editor_property('address_x',unreal.TextureAddress.TA_MIRROR);a.set_editor_property('address_y',unreal.TextureAddress.TA_MIRROR)
 unreal.EditorAssetLibrary.save_loaded_asset(a);return a
textures={k:imp(R/'assets/models/orison_terrain/textures'/(k+'_BaseColor.png'),'T_'+k+'_BaseColor') for k in ['Dirt','Gravel','Stone']}
def node(m,cls):return L.create_material_expression(m,cls)
def wire(a,o,b,p):assert L.connect_material_expressions(a,o,b,p)
def prop(a,p,o=''):assert L.connect_material_property(a,o,p)
def const(m,v):
 a=node(m,unreal.MaterialExpressionConstant);a.set_editor_property('r',v);return a
def custom(m,code,inputs,kind=unreal.CustomMaterialOutputType.CMOT_FLOAT1):
 a=node(m,unreal.MaterialExpressionCustom);a.set_editor_property('code',code);a.set_editor_property('output_type',kind)
 pins=[]
 for k in inputs:
  p=unreal.CustomInput();p.set_editor_property('input_name',k);pins.append(p)
 a.set_editor_property('inputs',pins)
 for k,(v,o) in inputs.items():wire(v,o,a,k)
 return a
m=unreal.load_asset(D+'/Materials/M_OrisonLandscape') or T.create_asset('M_OrisonLandscape',D+'/Materials',unreal.Material,unreal.MaterialFactoryNew());assert m
L.delete_all_material_expressions(m)
m.set_editor_property('tangent_space_normal',False)
p=node(m,unreal.MaterialExpressionWorldPosition);normal=node(m,unreal.MaterialExpressionVertexNormalWS)
uv=custom(m,'return P.xy/280.0;',{'P':(p,'')},unreal.CustomMaterialOutputType.CMOT_FLOAT2)
samples={}
for k,tex in textures.items():
 s=node(m,unreal.MaterialExpressionTextureSample);s.set_editor_property('texture',tex);s.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_COLOR);wire(uv,'',s,'UVs');samples[k]=s
gravel=custom(m,'float center=170*sin(P.y*.0009); float trail=1-smoothstep(95,280,abs(P.x-center)); float n=.5+.5*sin(P.x*.0023+sin(P.y*.0021)*2); return saturate(trail*.75+n*.18);',{'P':(p,'')})
stone=custom(m,'float n=.5+.5*sin(P.x*.0016+sin(P.y*.002)*2); float side=smoothstep(750,1850,abs(P.x)); return saturate(side*.72+n*.14+(1-N.z)*2);',{'P':(p,''),'N':(normal,'')})
mix=node(m,unreal.MaterialExpressionLinearInterpolate)
wire(samples['Dirt'],'RGB',mix,'A');wire(samples['Gravel'],'RGB',mix,'B');wire(gravel,'',mix,'Alpha')
mix2=node(m,unreal.MaterialExpressionLinearInterpolate)
wire(mix,'',mix2,'A');wire(samples['Stone'],'RGB',mix2,'B');wire(stone,'',mix2,'Alpha')
last=mix2
# Artist overrides can be painted after creating corresponding layer infos.
for name in ['Dirt','Gravel','Stone']:
 w=node(m,unreal.MaterialExpressionLandscapeLayerWeight);w.set_editor_property('parameter_name',name);w.set_editor_property('preview_weight',0)
 wire(last,'',w,'Base');wire(samples[name],'RGB',w,'Layer');last=w
rgb=custom(m,'float macro=.86+.14*sin(P.x*.00053)*sin(P.y*.00071);return B*macro;',{'P':(p,''),'B':(last,'')},unreal.CustomMaterialOutputType.CMOT_FLOAT3)
prop(rgb,unreal.MaterialProperty.MP_BASE_COLOR)
prop(const(m,.87),unreal.MaterialProperty.MP_ROUGHNESS);prop(const(m,0),unreal.MaterialProperty.MP_METALLIC);prop(const(m,.2),unreal.MaterialProperty.MP_SPECULAR)
detail=custom(m,'float2 q=P.xy*.07;float dx=.045*cos(q.x)*sin(q.y)+.02*cos(q.x*1.7+q.y*1.3);float dy=.045*sin(q.x)*cos(q.y)+.015*cos(q.x*1.7+q.y*1.3);return normalize(N+float3(-dx,-dy,0));',{'P':(p,''),'N':(normal,'')},unreal.CustomMaterialOutputType.CMOT_FLOAT3)
prop(detail,unreal.MaterialProperty.MP_NORMAL)
L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m)
def spawn(cls,label,loc,rot=(0,0,0)):
 a=E.spawn_actor_from_class(cls,unreal.Vector(*loc),unreal.Rotator(*rot));a.set_actor_label(label);return a
sun=spawn(unreal.DirectionalLight,'Terrain_Sun',(0,0,2000),(-38,-30,0));sun.light_component.set_mobility(unreal.ComponentMobility.MOVABLE);sun.light_component.set_editor_property('intensity',3.0)
sky=spawn(unreal.SkyLight,'Terrain_Sky',(0,0,1500));sky.light_component.set_mobility(unreal.ComponentMobility.MOVABLE);sky.light_component.set_editor_property('source_type',unreal.SkyLightSourceType.SLS_SPECIFIED_CUBEMAP)
cube=unreal.load_asset('/Engine/EngineResources/DefaultTextureCube');sky.light_component.set_editor_property('cubemap',cube);sky.light_component.set_editor_property('intensity',.7)
spawn(unreal.SkyAtmosphere,'Terrain_Atmosphere',(0,0,0))
fog=spawn(unreal.ExponentialHeightFog,'Terrain_Haze',(0,0,-200));fog.component.set_editor_property('fog_density',.004)
pp=spawn(unreal.PostProcessVolume,'Terrain_Exposure',(0,0,0));pp.set_editor_property('unbound',True);settings=pp.get_editor_property('settings')
settings.set_editor_property('override_auto_exposure_method',True);settings.set_editor_property('auto_exposure_method',unreal.AutoExposureMethod.AEM_MANUAL)
settings.set_editor_property('override_auto_exposure_bias',True);settings.set_editor_property('auto_exposure_bias',.0)
settings.set_editor_property('override_auto_exposure_apply_physical_camera_exposure',True);settings.set_editor_property('auto_exposure_apply_physical_camera_exposure',False)
pp.set_editor_property('settings',settings)
assert S.save_current_level()
(R/'reports/orison_terrain_setup.json').write_text(json.dumps(dict(map=MAP,material=m.get_path_name(),textures={k:v.get_path_name() for k,v in textures.items()},landscape_pending=True),indent=2))
print('ORISON_TERRAIN_SETUP_SAVED')
