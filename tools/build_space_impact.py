"""Isolated cinematic impact scene; all asset writes stay in SpaceImpact."""
import unreal, math, random, json, shutil
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
D = '/Game/LostVanguard/Environment/SpaceImpact'
MAP = D + '/Maps/L_SpaceImpact_Cinematic'
T = unreal.AssetToolsHelpers.get_asset_tools()
L = unreal.MaterialEditingLibrary
E = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
S = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
random.seed(240)

def n(m, c):
    return L.create_material_expression(m, c)

def wire(a, out, b, pin):
    assert L.connect_material_expressions(a, out, b, pin), (b.get_class().get_name(), pin)

def prop(a, p, out=''):
    assert L.connect_material_property(a, out, p)

def c(m, v):
    a = n(m, unreal.MaterialExpressionConstant)
    a.set_editor_property('r', v)
    return a

def col(m, v):
    a = n(m, unreal.MaterialExpressionConstant3Vector)
    a.set_editor_property('constant', unreal.LinearColor(*v, 1))
    return a

def custom(m, code, inputs, kind=unreal.CustomMaterialOutputType.CMOT_FLOAT1):
    a = n(m, unreal.MaterialExpressionCustom)
    a.set_editor_property('code', code)
    a.set_editor_property('output_type', kind)
    pins=[]
    for k in inputs:
        pin=unreal.CustomInput();pin.set_editor_property('input_name',k);pins.append(pin)
    a.set_editor_property('inputs',pins)
    for k, (b, o) in inputs.items():
        wire(b, o, a, k)
    return a

def mat(name):
    a = unreal.load_asset(D + '/Materials/' + name) or T.create_asset(name, D + '/Materials', unreal.Material, unreal.MaterialFactoryNew())
    L.delete_all_material_expressions(a)
    return a

def save(a):
    L.recompile_material(a) if isinstance(a, unreal.Material) else None
    assert unreal.EditorAssetLibrary.save_loaded_asset(a)

def wp(m):
    return n(m, unreal.MaterialExpressionWorldPosition)

def texture(m, path, sampler=unreal.MaterialSamplerType.SAMPLERTYPE_COLOR):
    a = n(m, unreal.MaterialExpressionTextureSample)
    a.set_editor_property('texture', unreal.load_asset(path))
    assert a.texture, path
    a.set_editor_property('sampler_type', sampler)
    return a

def imptex(src, name):
    a = unreal.load_asset(D + '/Textures/' + name)
    if not a:
        t = unreal.AssetImportTask()
        t.set_editor_property('filename', str(src))
        t.set_editor_property('destination_path', D + '/Textures')
        t.set_editor_property('destination_name', name)
        t.set_editor_property('automated', True)
        t.set_editor_property('save', True)
        T.import_asset_tasks([t])
        a = unreal.load_asset(t.imported_object_paths[0])
    a.set_editor_property('max_texture_size', 2048)
    save(a)
    return a
texdir = ROOT / 'assets/models/space_impact/textures'
texdir.mkdir(parents=True, exist_ok=True)
for name, source in [('Fire', 'exec-885248aa-22fe-4adb-a51c-24797218d7ec.png'), ('Smoke', 'exec-ddc19788-cc74-4016-8ec8-d4ba50afb47d.png')]:
    dst = texdir / ('T_' + name + 'Atlas.png')
    shutil.copy2(Path('C:/Users/alexa/.codex/generated_images/01a11cb3-50f5-7131-8ed6-c789e60afb6b') / source, dst)
    imptex(dst, 'T_' + name + 'Atlas')
hero = mat('M_EntryScarredMetal')
base = '/Game/LostVanguard/Environment/OpeningReview/Assets/WreckFlagship71/Large_Flagship71/'
bc = texture(hero, base + 'T_Large_Flagship71_BaseColor')
rough = texture(hero, base + 'T_Large_Flagship71_Roughness', unreal.MaterialSamplerType.SAMPLERTYPE_MASKS)
norm = texture(hero, base + 'T_Large_Flagship71_Normal', unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL)
pos = wp(hero)
uv = n(hero, unreal.MaterialExpressionTextureCoordinate)
mask = custom(hero, 'float s=sin(P.x*.019+sin(P.z*.025))*sin(P.z*.023); return saturate((310-P.z)/240 + .15*s);', {'P': (pos, '')})
rgb = custom(hero, 'float scratches=pow(saturate(sin(U.x*2300+sin(U.y*65)*7)),35)*.14; float3 oxide=lerp(float3(.12,.07,.025),float3(.035,.038,.065),saturate(H*2)); return lerp(B*.72+scratches,oxide,H*.82);', {'B': (bc, 'RGB'), 'U': (uv, ''), 'H': (mask, '')}, unreal.CustomMaterialOutputType.CMOT_FLOAT3)
prop(rgb, unreal.MaterialProperty.MP_BASE_COLOR)
rg = custom(hero, 'float streak=pow(saturate(sin(U.x*1700+sin(U.y*34)*2)),22); return clamp(R*.55+.12+H*.32-streak*.12,.2,.88);', {'R': (rough, 'R'), 'U': (uv, ''), 'H': (mask, '')})
prop(rg, unreal.MaterialProperty.MP_ROUGHNESS)
met = custom(hero, 'return lerp(.82,.09,H);', {'H': (mask, '')})
prop(met, unreal.MaterialProperty.MP_METALLIC)
prop(norm, unreal.MaterialProperty.MP_NORMAL, 'RGB')
save(hero)
ground = mat('M_CharredDampSoil')
p = wp(ground)
soilsource=Path('C:/Users/alexa/.codex/generated_images/01a11cb3-50f5-7131-8ed6-c789e60afb6b/exec-83991b83-e6c7-4bc0-9b8d-bca7cdbbf8fe.png');shutil.copy2(soilsource,texdir/'T_ImpactSoil.png');imptex(texdir/'T_ImpactSoil.png','T_ImpactSoil')
soil=texture(ground,D+'/Textures/T_ImpactSoil');soiluv=custom(ground,'return P.xy/180;',{'P':(p,'')},unreal.CustomMaterialOutputType.CMOT_FLOAT2);wire(soiluv,'',soil,'UVs')
g = custom(ground, 'float burn=1-smoothstep(300,1100,length(P.xy-float2(0,180))); return B*lerp(.7,.18,burn);', {'P': (p, ''),'B':(soil,'RGB')}, unreal.CustomMaterialOutputType.CMOT_FLOAT3)
prop(g, unreal.MaterialProperty.MP_BASE_COLOR)
gr = custom(ground, 'return clamp(.58+B*.7,.55,.92);', {'B': (soil,'R')})
prop(gr, unreal.MaterialProperty.MP_ROUGHNESS)
gn=custom(ground,'return normalize(float3(ddx(B)*7,ddy(B)*7,1));',{'B':(soil,'R')},unreal.CustomMaterialOutputType.CMOT_FLOAT3);prop(gn,unreal.MaterialProperty.MP_NORMAL)
save(ground)
rock = mat('M_ImpactStone')
rp=wp(rock);rs=texture(rock,D+'/Textures/T_ImpactSoil');ru=custom(rock,'return (P.xy+P.z*.45)/110;',{'P':(rp,'')},unreal.CustomMaterialOutputType.CMOT_FLOAT2);wire(ru,'',rs,'UVs');rc=custom(rock,'return B*.32+float3(.05,.045,.036);',{'B':(rs,'RGB')},unreal.CustomMaterialOutputType.CMOT_FLOAT3);prop(rc,unreal.MaterialProperty.MP_BASE_COLOR)
prop(c(rock, 0.9), unreal.MaterialProperty.MP_ROUGHNESS)
rn=custom(rock,'return normalize(float3(ddx(B)*5,ddy(B)*5,1));',{'B':(rs,'R')},unreal.CustomMaterialOutputType.CMOT_FLOAT3);prop(rn,unreal.MaterialProperty.MP_NORMAL)
save(rock)
stones={}
for k in range(3):
 name='SM_ImpactStone_'+str(k);path=D+'/Assets/'+name;mesh=unreal.load_asset(path)
 if not mesh:
  opt=unreal.FbxImportUI();opt.set_editor_property('import_mesh',True);opt.set_editor_property('import_materials',False);opt.set_editor_property('import_textures',False);opt.static_mesh_import_data.set_editor_property('combine_meshes',True);opt.static_mesh_import_data.set_editor_property('auto_generate_collision',False)
  task=unreal.AssetImportTask();task.set_editor_property('filename',str(ROOT/'assets/models/space_impact/export'/(name+'.fbx')));task.set_editor_property('destination_path',D+'/Assets');task.set_editor_property('destination_name',name);task.set_editor_property('automated',True);task.set_editor_property('save',True);task.set_editor_property('options',opt);T.import_asset_tasks([task]);mesh=unreal.load_asset(task.get_editor_property('imported_object_paths')[0])
 stones[k]=mesh
timewind = {}
flora = '/Game/LostVanguard/Environment/OpeningReview/Assets/FloraFlagship71/'
for id in ['F01_Flagship71', 'F02_Flagship71', 'F08_Flagship71', 'F03_Flagship71', 'F05_Flagship71', 'F06_Flagship71', 'F10_Flagship71']:
    src = unreal.load_asset(flora + id + '/MI_' + id)
    assert src, id
    parent = unreal.load_asset(flora + 'M_FloraFlagship_PBR')
    wind = unreal.load_asset(D + '/Materials/M_WindPBR')
    if not wind:
        wind = unreal.EditorAssetLibrary.duplicate_asset(parent.get_path_name(), D + '/Materials/M_WindPBR')
        p = wp(wind)
        tm = n(wind, unreal.MaterialExpressionTime)
        obj = n(wind, unreal.MaterialExpressionObjectPositionWS)
        sway = custom(wind, 'float h=max(0,P.z-O.z+100); float a=saturate(h/650); float wave=sin(t*1.2+P.x*.002+P.y*.003)+.3*sin(t*2.7+P.y*.014); return float3(wave*9*a*a,sin(t*.9+P.x*.007)*5*a*a,0);', {'P': (p, ''), 'O': (obj, ''), 't': (tm, '')}, unreal.CustomMaterialOutputType.CMOT_FLOAT3)
        prop(sway, unreal.MaterialProperty.MP_WORLD_POSITION_OFFSET)
        save(wind)
    mi = unreal.load_asset(D + '/Materials/MI_Wind_' + id) or unreal.EditorAssetLibrary.duplicate_asset(src.get_path_name(), D + '/Materials/MI_Wind_' + id)
    L.set_material_instance_parent(mi, wind)
    save(mi)
    timewind[id] = mi
leaf = unreal.load_asset(D + '/Materials/M_WindLeaf') or unreal.EditorAssetLibrary.duplicate_asset(flora + 'M_F01_CurvedForkLeaf', D + '/Materials/M_WindLeaf')
if not L.get_material_property_input_node(leaf, unreal.MaterialProperty.MP_WORLD_POSITION_OFFSET):
    p = wp(leaf)
    tm = n(leaf, unreal.MaterialExpressionTime)
    w = custom(leaf, 'return float3(sin(t*1.6+P.x*.004+P.y*.007)*10,sin(t*2.4+P.y*.01)*5,sin(t*2.7+P.x*.017)*3);', {'P': (p, ''), 't': (tm, '')}, unreal.CustomMaterialOutputType.CMOT_FLOAT3)
    prop(w, unreal.MaterialProperty.MP_WORLD_POSITION_OFFSET)
save(leaf)
for kind in ['Fire', 'Smoke']:
    m = mat('M_' + kind)
    m.set_editor_property('blend_mode', unreal.BlendMode.BLEND_ADDITIVE if kind == 'Fire' else unreal.BlendMode.BLEND_TRANSLUCENT)
    m.set_editor_property('shading_model', unreal.MaterialShadingModel.MSM_UNLIT)
    m.set_editor_property('two_sided', True)
    L.set_material_usage(m, unreal.MaterialUsage.MATUSAGE_NIAGARA_SPRITES)
    u = n(m, unreal.MaterialExpressionTextureCoordinate)
    tm = n(m, unreal.MaterialExpressionTime)
    age = n(m, unreal.MaterialExpressionParticleRelativeTime)
    au = custom(m, 'float f=floor(frac(t*speed+age*.8)*16); return (clamp(U,.08,.92)+float2(fmod(f,4),floor(f/4)))/4;', {'U': (u, ''), 't': (tm, ''), 'age': (age, ''), 'speed': (c(m, 0.9 if kind == 'Fire' else 0.15), '')}, unreal.CustomMaterialOutputType.CMOT_FLOAT2)
    tx = texture(m, D + '/Textures/T_' + kind + 'Atlas')
    wire(au, '', tx, 'UVs')
    em = custom(m, 'return B*strength;', {'B': (tx, 'RGB'), 'strength': (c(m, 3.5 if kind == 'Fire' else 1.2), '')}, unreal.CustomMaterialOutputType.CMOT_FLOAT3)
    prop(em, unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    alpha = custom(m, 'float edge=smoothstep(0,.15,U.x)*(1-smoothstep(.85,1,U.x))*smoothstep(0,.08,U.y)*(1-smoothstep(.91,1,U.y)); return pow(A,1.5)*edge*sin(saturate(age)*3.14159)*strength;', {'A': (tx, 'A'), 'U': (u, ''), 'age': (age, ''), 'strength': (c(m, .7 if kind == 'Fire' else .8), '')})
    prop(alpha, unreal.MaterialProperty.MP_OPACITY)
    save(m)
spark = mat('M_Ember')
spark.set_editor_property('blend_mode', unreal.BlendMode.BLEND_ADDITIVE)
spark.set_editor_property('shading_model', unreal.MaterialShadingModel.MSM_UNLIT)
L.set_material_usage(spark, unreal.MaterialUsage.MATUSAGE_NIAGARA_SPRITES)
u = n(spark, unreal.MaterialExpressionTextureCoordinate)
a = n(spark, unreal.MaterialExpressionParticleRelativeTime)
prop(col(spark, (18, 2.4, 0.08)), unreal.MaterialProperty.MP_EMISSIVE_COLOR)
op = custom(spark, 'return pow(saturate(1-length((U-.5)*2)),2)*sin(age*3.14159);', {'U': (u, ''), 'age': (a, '')})
prop(op, unreal.MaterialProperty.MP_OPACITY)
save(spark)
coal = mat('M_GlowingCoals')
tm = n(coal, unreal.MaterialExpressionTime)
p = wp(coal)
ec = custom(coal, 'float f=.65+.2*sin(t*2.3+P.x*.16)+.15*sin(t*5.7+P.y*.13); return float3(5,.36,.008)*f;', {'t': (tm, ''), 'P': (p, '')}, unreal.CustomMaterialOutputType.CMOT_FLOAT3)
prop(ec, unreal.MaterialProperty.MP_EMISSIVE_COLOR)
prop(col(coal, (0.025, 0.006, 0.002)), unreal.MaterialProperty.MP_BASE_COLOR)
save(coal)
flick = mat('M_Firelight')
flick.set_editor_property('material_domain', unreal.MaterialDomain.MD_LIGHT_FUNCTION)
tm = n(flick, unreal.MaterialExpressionTime)
fc = custom(flick, 'return .82+.11*sin(t*11)+.07*sin(t*23.7);', {'t': (tm, '')})
prop(fc, unreal.MaterialProperty.MP_EMISSIVE_COLOR)
save(flick)
heat = mat('M_HeatHaze')
heat.set_editor_property('blend_mode', unreal.BlendMode.BLEND_TRANSLUCENT)
heat.set_editor_property('two_sided', True)
heat.set_editor_property('shading_model', unreal.MaterialShadingModel.MSM_UNLIT)
heat.set_editor_property('refraction_method',unreal.RefractionMode.RM_PIXEL_NORMAL_OFFSET)
u = n(heat, unreal.MaterialExpressionTextureCoordinate)
tm = n(heat, unreal.MaterialExpressionTime)
hn = custom(heat, 'return normalize(float3(sin(U.y*30-t*4)*.12,sin(U.x*27+U.y*13-t*3)*.12,1));', {'U': (u, ''), 't': (tm, '')}, unreal.CustomMaterialOutputType.CMOT_FLOAT3)
prop(hn, unreal.MaterialProperty.MP_NORMAL)
ho = custom(heat, 'return saturate(1-length((U-.5)*2))*.1;', {'U': (u, '')})
prop(ho, unreal.MaterialProperty.MP_OPACITY)
prop(c(heat, 1.025), unreal.MaterialProperty.MP_REFRACTION)
save(heat)
if unreal.EditorAssetLibrary.does_asset_exist(MAP):
    assert S.load_level(MAP)
else:
    assert S.new_level(MAP)
for a in E.get_all_level_actors():
    if a.get_actor_label().startswith('Impact_'):
        E.destroy_actor(a)

def spawn(cls, label, pos, rot=(0, 0, 0)):
    a = E.spawn_actor_from_class(cls, unreal.Vector(*pos), unreal.Rotator(pitch=rot[0],yaw=rot[1],roll=rot[2]))
    a.set_actor_label('Impact_' + label)
    a.set_folder_path('LostVanguard/SpaceImpact')
    return a

def put(mesh, label, pos, rot=(0, 0, 0), scale=(1, 1, 1), material=None, collision=False):
    a = spawn(unreal.StaticMeshActor, label, pos, rot)
    a.static_mesh_component.set_static_mesh(unreal.load_asset(mesh) if isinstance(mesh, str) else mesh)
    a.set_actor_scale3d(unreal.Vector(*scale))
    a.static_mesh_component.set_collision_profile_name('BlockAll' if collision else 'NoCollision')
    if material:
        a.static_mesh_component.set_material(0, material)
    return a

def h(x, y):
    x /= 100
    y /= 100
    return 100 * (-0.6 * math.exp(-((x / 17) ** 2 + (y / 22) ** 2)) + 0.2 * math.sin(x * 0.31) * math.cos(y * 0.24) + 0.12 * math.sin(x * 0.95 + y * 0.51) + max(0, (math.sqrt((x / 1.2) ** 2 + y * y) - 25) / 12) ** 2 * 1.7)
old = '/Game/LostVanguard/Environment/WreckShowcase/Assets/'
put(old + 'SM_ShowcaseTerrain', 'Terrain', (0, 0, 0), material=ground, collision=True)
put(base + 'SM_Large_Flagship71', 'EntryWreck', (0, 200, -90), (0, -12, 7), (1.15, 1.15, 1.15), hero, True)
for i in range(30):
    x = random.uniform(-2700, 3300)
    y = random.uniform(1400, 4300)
    id = ['F01_Flagship71', 'F02_Flagship71', 'F08_Flagship71'][i % 3]
    s = random.uniform(0.7, 1.25)
    a = put(flora + id + '/SM_' + id, 'Tree_' + str(i), (x, y, h(x, y) - 15), (0, random.uniform(0, 360), 0), (s, s, s), timewind[id])
    if id.startswith('F01'):
        a.static_mesh_component.set_material(1, leaf)
for i in range(95):
    x = random.uniform(-2600, 2700)
    y = random.uniform(-2200, 1800)
    if abs(x) < 800 and -550 < y < 900:
        continue
    id = ['F03_Flagship71', 'F05_Flagship71', 'F06_Flagship71', 'F10_Flagship71'][i % 4]
    s = random.uniform(0.55, 1.15)
    a = put(flora + id + '/SM_' + id, 'Understory_' + str(i), (x, y, h(x, y)), (0, random.uniform(0, 360), 0), (s, s, s), timewind[id])
    a.static_mesh_component.set_editor_property('ld_max_draw_distance', 7500)
for i in range(65):
    x = random.uniform(-2000, 2200)
    y = random.uniform(-1400, 1600)
    s = random.uniform(0.2, 0.85)
    put(stones[i%3], 'Stone_' + str(i), (x, y, h(x, y) - 12), (random.uniform(-25, 25), random.uniform(0, 360), 0), (s, s, s), rock)
for i in range(20):
    x = random.uniform(-1000, 1350)
    y = random.uniform(-700, 900)
    s = random.uniform(0.18, 0.6)
    put(old + 'SM_ShowcasePlate_' + str(i % 3), 'Armor_' + str(i), (x, y, h(x, y) + 5), (random.uniform(-18, 18), random.uniform(0, 360), 0), (s, s, s), hero)
sites = [(-450, -210, 15), (440, -110, 60), (720, 380, 35)]
system = unreal.load_asset(D + '/FX/NS_ImpactAtmosphere')
assert system
for i, (x, y, z) in enumerate(sites):
    a = spawn(unreal.NiagaraActor, 'Burn_' + str(i), (x, y, h(x, y) + z))
    a.get_component_by_class(unreal.NiagaraComponent).set_asset(system)
    light = spawn(unreal.PointLight, 'Firelight_' + str(i), (x, y - 30, 150))
    lc = light.light_component
    lc.set_editor_property('intensity', 600 if i == 0 else 450)
    lc.set_editor_property('attenuation_radius', 1000)
    lc.set_light_color(unreal.LinearColor(1, 0.22, 0.025, 1))
    lc.set_editor_property('source_radius', 75)
    lc.set_editor_property('light_function_material', flick)
    lc.set_editor_property('volumetric_scattering_intensity', 0.4)
    put('/Engine/BasicShapes/Plane', 'Heat_' + str(i), (x, y, 140), (90, 0, 0), (2.7, 3.2, 1), heat)
    for j in range(12):
        xx = x + random.uniform(-95, 95)
        yy = y + random.uniform(-70, 70)
        s = random.uniform(0.035, 0.1)
        put(old + 'SM_ShowcaseRock_' + str(j % 3), 'Coal_' + str(i) + '_' + str(j), (xx, yy, h(xx, yy) + 8), (0, random.uniform(0, 360), 0), (s, s, s * 0.5), coal)
spawn(unreal.SkyAtmosphere, 'Atmosphere', (0, 0, 0))
sun = spawn(unreal.DirectionalLight, 'DuskRim', (0, 0, 2000), (-12, -130, 0))
lc = sun.light_component
lc.set_editor_property('intensity', 3)
lc.set_light_color(unreal.LinearColor(0.46, 0.62, 1, 1))
lc.set_editor_property('atmosphere_sun_light', True)
lc.set_editor_property('light_source_angle', 2)
sky = spawn(unreal.SkyLight, 'Sky', (0, 0, 1500))
sky.light_component.set_editor_property('real_time_capture', True)
sky.light_component.set_editor_property('intensity', 1)
key = spawn(unreal.RectLight, 'MetalSoftbox', (-1000, -1500, 1050), (-22, 55, 0))
lc = key.light_component
lc.set_editor_property('intensity', 18000)
lc.set_editor_property('attenuation_radius', 4500)
lc.set_editor_property('source_width', 1100)
lc.set_editor_property('source_height', 750)
lc.set_light_color(unreal.LinearColor(0.6, 0.73, 1, 1))
fog = spawn(unreal.ExponentialHeightFog, 'Mist', (0, 0, -80))
fc = fog.get_component_by_class(unreal.ExponentialHeightFogComponent)
fc.set_editor_property('fog_density', 0.013)
fc.set_editor_property('fog_height_falloff', 0.3)
fc.set_editor_property('enable_volumetric_fog', True)
fc.set_editor_property('fog_inscattering_luminance', unreal.LinearColor(0.07, 0.11, 0.17, 1))
fc.set_editor_property('start_distance', 600)
post = spawn(unreal.PostProcessVolume, 'Grade', (0, 0, 0))
post.set_editor_property('unbound', True)
ps = post.get_editor_property('settings')
for name, val in {'override_auto_exposure_method': True, 'auto_exposure_method': unreal.AutoExposureMethod.AEM_MANUAL, 'override_auto_exposure_apply_physical_camera_exposure': True, 'auto_exposure_apply_physical_camera_exposure': False, 'override_auto_exposure_bias': True, 'auto_exposure_bias': -1.8, 'override_bloom_intensity': True, 'bloom_intensity': 0.25, 'override_vignette_intensity': True, 'vignette_intensity': 0.2, 'override_motion_blur_amount': True, 'motion_blur_amount': 0.15}.items():
    ps.set_editor_property(name, val)
post.set_editor_property('settings', ps)
post.brush_component.set_visibility(False)
camera = spawn(unreal.CineCameraActor, 'CinematicCamera', (-950, -1450, 310), (-1, 60, 0))
cc = camera.get_cine_camera_component()
cc.set_editor_property('current_focal_length', 30)
camera.set_editor_property('auto_activate_for_player', unreal.AutoReceiveInput.PLAYER0)
ws = unreal.EditorLevelLibrary.get_editor_world().get_world_settings()
ws.set_editor_property('default_game_mode', unreal.GameModeBase.static_class())
spawn(unreal.PlayerStart, 'Start', (-1450, -2250, 120), (0, 58, 0))
for a in E.get_all_level_actors():
    for b in a.get_components_by_class(unreal.BillboardComponent):
        b.set_visibility(False)
assert S.save_current_level()
(ROOT / 'reports/space_impact_build.json').write_text(json.dumps({'map': MAP, 'actor_count': len(E.get_all_level_actors()), 'hero': base + 'SM_Large_Flagship71', 'new_paid_generations': 0, 'preserved_existing_maps': True, 'effects_system': system.get_path_name(), 'camera_cm': [-1450, -2250, 330], 'verification': 'pending Niagara configuration, live visual inspection and PIE'}, indent=2))
print('SPACE_IMPACT_BUILD_COMPLETE', flush=True)
