"""Create an image-led opening variant through native Unreal editor APIs.

The verified gameplay map and runtime Blueprints are preserved. Only the new
L_Wreckage_Opening map and OpeningVisuals materials are authored here.
"""
import json, math, random
from pathlib import Path
import unreal

ROOT='/Game/WreckagePrototype'
SOURCE=ROOT+'/Maps/L_Wreckage_Playable'
MAP=ROOT+'/Maps/L_Wreckage_Opening'
FOLDER='WreckagePrototype/OpeningVisuals'
report={'map':MAP,'preserved_map':SOURCE,'errors':[],'property_notes':[]}
levels=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
rng=random.Random(724)

def fields(obj,values):
    for name,value in values.items():
        try:obj.set_editor_property(name,value)
        except Exception as error:report['property_notes'].append(name+': '+str(error))

def mat(name,color,emissive=False,opacity=None):
    path=ROOT+'/OpeningVisuals/Materials/'+name
    asset=unreal.load_asset(path)
    if asset:return asset
    asset=unreal.AssetToolsHelpers.get_asset_tools().create_asset(name,ROOT+'/OpeningVisuals/Materials',unreal.Material,unreal.MaterialFactoryNew())
    c=unreal.MaterialEditingLibrary.create_material_expression(asset,unreal.MaterialExpressionConstant3Vector,-300,0)
    c.set_editor_property('constant',unreal.LinearColor(*color,1))
    unreal.MaterialEditingLibrary.connect_material_property(c,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR if emissive else unreal.MaterialProperty.MP_BASE_COLOR)
    rough=unreal.MaterialEditingLibrary.create_material_expression(asset,unreal.MaterialExpressionConstant,-300,150)
    rough.set_editor_property('r',.87)
    unreal.MaterialEditingLibrary.connect_material_property(rough,'',unreal.MaterialProperty.MP_ROUGHNESS)
    asset.set_editor_property('two_sided',True)
    if emissive:asset.set_editor_property('shading_model',unreal.MaterialShadingModel.MSM_UNLIT)
    if opacity is not None:
        asset.set_editor_property('blend_mode',unreal.BlendMode.BLEND_TRANSLUCENT)
        o=unreal.MaterialEditingLibrary.create_material_expression(asset,unreal.MaterialExpressionConstant,-300,300)
        o.set_editor_property('r',opacity)
        unreal.MaterialEditingLibrary.connect_material_property(o,'',unreal.MaterialProperty.MP_OPACITY)
    unreal.MaterialEditingLibrary.recompile_material(asset)
    assert unreal.EditorAssetLibrary.save_loaded_asset(asset)
    return asset

def shape(name,mesh,xyz,size,material,rot=(0,0,0),collision=False):
    a=actors.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(*xyz),unreal.Rotator(*rot))
    a.set_actor_label('OV_'+name);a.set_folder_path(FOLDER)
    c=a.static_mesh_component;c.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/'+mesh));c.set_material(0,material)
    c.set_collision_profile_name('BlockAll' if collision else 'NoCollision')
    c.set_editor_property('cast_shadow',not name.startswith(('Smoke','Sky','Fire')))
    if name.startswith('Smoke'):c.set_editor_property('bounds_scale',2.5)
    a.set_actor_scale3d(unreal.Vector(*(d/100 for d in size)))
    return a

def rising_smoke_material():
    path=ROOT+'/OpeningVisuals/Materials/M_RisingSmokeProxy_v3'
    found=unreal.load_asset(path)
    if found:return found
    asset=mat('M_RisingSmokeProxy_v3',(.04,.055,.065),False,.20)
    lib=unreal.MaterialEditingLibrary
    def node(cls,x,y,**props):
        n=lib.create_material_expression(asset,cls,x,y)
        for k,v in props.items():n.set_editor_property(k,v)
        return n
    def link(a,b,pin):assert lib.connect_material_expressions(a,'',b,pin)
    time=node(unreal.MaterialExpressionTime,-900,400)
    rate=node(unreal.MaterialExpressionMultiply,-700,400,const_b=.12);link(time,rate,'A')
    pos=node(unreal.MaterialExpressionObjectPositionWS,-1100,650)
    mask=node(unreal.MaterialExpressionComponentMask,-900,650,r=False,g=False,b=True,a=False);link(pos,mask,'')
    stagger=node(unreal.MaterialExpressionMultiply,-700,650,const_b=.002);link(mask,stagger,'A')
    total=node(unreal.MaterialExpressionAdd,-500,400);link(rate,total,'A');link(stagger,total,'B')
    phase=node(unreal.MaterialExpressionFrac,-350,400);link(total,phase,'')
    wind=node(unreal.MaterialExpressionConstant3Vector,-350,600,constant=unreal.LinearColor(90,30,250,1))
    offset=node(unreal.MaterialExpressionMultiply,-100,450);link(phase,offset,'A');link(wind,offset,'B')
    assert lib.connect_material_property(offset,'',unreal.MaterialProperty.MP_WORLD_POSITION_OFFSET)
    reverse=node(unreal.MaterialExpressionSubtract,-350,800,const_a=1.0);link(phase,reverse,'B')
    fade=node(unreal.MaterialExpressionMultiply,-100,800);link(phase,fade,'A');link(reverse,fade,'B')
    strength=node(unreal.MaterialExpressionMultiply,100,800,const_b=.8);link(fade,strength,'A')
    fresnel=node(unreal.MaterialExpressionFresnel,-300,1050)
    soft_edge=node(unreal.MaterialExpressionOneMinus,-100,1050);link(fresnel,soft_edge,'')
    density=node(unreal.MaterialExpressionMultiply,300,850);link(strength,density,'A');link(soft_edge,density,'B')
    assert lib.connect_material_property(density,'',unreal.MaterialProperty.MP_OPACITY)
    lib.recompile_material(asset);assert unreal.EditorAssetLibrary.save_loaded_asset(asset)
    return asset

def beam(name,p0,p1,width,material,collision=False):
    delta=unreal.Vector(*(b-a for a,b in zip(p0,p1)))
    length=math.sqrt(sum((b-a)**2 for a,b in zip(p0,p1)))
    a=shape(name,'Cube',tuple((a+b)/2 for a,b in zip(p0,p1)),(length,width,width),material,collision=collision)
    a.set_actor_rotation(unreal.MathLibrary.make_rot_from_x(delta),False)
    return a

def light(name,xyz,color,intensity,radius):
    a=actors.spawn_actor_from_class(unreal.PointLight,unreal.Vector(*xyz));a.set_actor_label('OV_'+name);a.set_folder_path(FOLDER)
    c=a.point_light_component
    assert unreal.ToolsetLibrary.set_object_properties(c,'{"Mobility":"Movable"}')
    c.set_light_color(unreal.LinearColor(*color,1));c.set_editor_property('intensity',intensity);c.set_editor_property('attenuation_radius',radius)
    return a

def tree(i,x,y,height):
    ground=-220
    lean=rng.uniform(-8,8)
    shape('TreeTrunk_'+str(i),'Cylinder',(x,y,ground+height*.36),(60,75,height*.74),bark,rot=(lean,rng.uniform(0,360),0),collision=True)
    for j,side in enumerate([-1,1]):
        beam('Branch_'+str(i)+'_'+str(j),(x,y,ground+height*.48),(x+100,y+side*height*.24,ground+height*.78),35,bark)
    for j,(dx,dy,h,w) in enumerate([(0,0,.88,.42),(60,-height*.19,.72,.35),(-80,height*.19,.77,.36)]):
        shape('Canopy_'+str(i)+'_'+str(j),'Sphere',(x+dx,y+dy,ground+height*h),(height*w,height*w*.95,height*.21),leaf if i%3 else teal,rot=(0,rng.uniform(0,360),rng.uniform(-12,12)))

try:
    if not unreal.EditorAssetLibrary.does_asset_exist(MAP):assert unreal.EditorAssetLibrary.duplicate_asset(SOURCE,MAP)
    assert levels.load_level(MAP)
    for a in actors.get_all_level_actors():
        if str(a.get_folder_path())==FOLDER:actors.destroy_actor(a)
    existing={a.get_actor_label():a for a in actors.get_all_level_actors()}
    dark=mat('M_HullShadow',(.012,.023,.029));metal=mat('M_BurnedHull',(.07,.10,.12));edge=mat('M_TornEdges',(.15,.20,.21))
    bark=mat('M_AlienBark',(.025,.065,.075));leaf=mat('M_BlueGreenCanopy',(.04,.25,.19));teal=mat('M_TealCanopy',(.035,.16,.26))
    soil=mat('M_CrashSoil',(.09,.12,.09));rock=mat('M_ForestRock',(.10,.15,.16));leaf_tip=mat('M_AlienLeafTips',(.10,.39,.30))
    flame=mat('M_LingeringFireDim', (.65,.075,.003),True);hot=mat('M_FuelGlowDim',(.9,.24,.008),True)
    smoke=rising_smoke_material();sky=mat('M_CoolSky',(.025,.065,.105),True)
    # Dark starting pocket; shorten roof so the breached forward section opens to sky.
    for label in ['Recovery_Floor','Recovery_Wall_-1','Recovery_Wall_1','Recovery_BackWall','Recovery_Ceiling']:
        existing[label].static_mesh_component.set_material(0,dark)
    roof=existing['Recovery_Ceiling'];roof.set_actor_location(unreal.Vector(-300,0,400),False,False);roof.set_actor_scale3d(unreal.Vector(4,8.5,.4))
    for side in [-1,1]:
        wall=existing['Recovery_Wall_'+str(side)];wall.set_actor_location(unreal.Vector(-200,side*425,180),False,False);wall.set_actor_scale3d(unreal.Vector(6,.5,3.6))
    # Keep collision bounds along the existing recovery route, but open the view.
    for side in [-1,1]:
        wall=existing['Passage_Wall_'+str(side)];wall.set_actor_location(unreal.Vector(800,side*205,35),False,False);wall.set_actor_scale3d(unreal.Vector(6,.5,.7))
        wall.static_mesh_component.set_material(0,metal)
        wall=existing['Landing_Wall_'+str(side)];wall.set_actor_location(unreal.Vector(1400,side*205,40),False,False);wall.set_actor_scale3d(unreal.Vector(4,.5,.8));wall.static_mesh_component.set_material(0,metal)
    for label in ['Passage_Floor','Landing_Floor']:
        existing[label].static_mesh_component.set_material(0,soil)
    existing['Crouch_Beam'].static_mesh_component.set_material(0,metal)
    existing['Surface_Prototype_Only'].static_mesh_component.set_material(0,soil)
    # Angular, torn hull rim. Centre corridor remains clear for the player capsule.
    for side in [-1,1]:
        beam('BreachRib_'+str(side),(90,side*390,15),(200,side*440,480),70,dark,True)
        beam('TornHeader_'+str(side),(200,side*440,480),(140,side*110,630),65,dark,True)
        shape('JaggedHull_'+str(side),'Cube',(160,side*420,350),(80,120,270),dark,rot=(side*12,side*19,side*14),collision=True)
        shape('RimLip_'+str(side),'Cube',(150,side*350,25),(200,130,30),metal,rot=(0,side*18,0),collision=True)
        for j in range(3):
            beam('ExposedRib_'+str(side)+'_'+str(j),(130+j*100,side*410,20),(170+j*100,side*410,375),15,edge)
    # Dangling cables stay beside the travel space rather than across it.
    for i in range(4):
        y=-350+i*30
        points=[(170,y,520),(180,y+10,370),(200,y+25,260),(215,y+15,150)]
        for j in range(3):beam('HangingCable_'+str(i)+'_'+str(j),points[j],points[j+1],5,bark)
    # Main wreck uses the existing combat bay as its accessible broken interior.
    # A roughly 27 m long, 15 m wide, 9 m tall section dominates the background.
    for side in [-1,1]:
        shape('MainHullFlank_'+str(side),'Cube',(2400,side*755,420),(1700,85,610),dark,rot=(side*8,0,side*9),collision=True)
        for j in range(3):
            shape('MainHullShard_'+str(side)+'_'+str(j),'Cube',(1850+j*550,side*815,480+j*20),(460,55,430),metal,rot=(side*(j*12-12),j*6,side*(j*7-6)))
        beam('MainKeel_'+str(side),(1580,side*700,160),(3310,side*850,640),90,edge,True)
        for j in range(5):
            shape('HullRib_'+str(side)+'_'+str(j),'Cube',(1770+j*290,side*785,450),(40,110,700),edge,rot=(side*8,0,side*9))
    for i,(x,y,z,sx,sy,roll) in enumerate([(1930,-190,720,740,1300,-9),(2550,220,805,710,1300,8),(3120,250,675,520,1100,18)]):
        shape('BrokenRoof_'+str(i),'Cube',(x,y,z),(sx,sy,60),metal,rot=(rng.uniform(-8,8),-7,roll),collision=True)
    shape('FracturedTailFin','Cube',(3180,540,820),(620,110,1150),metal,rot=(-21,-15,12),collision=True)
    shape('RearEngineMass','Cylinder',(3260,650,390),(470,470,600),metal,rot=(90,0,0),collision=True)
    shape('SplitForwardPlate','Cube',(1530,-520,230),(520,340,65),edge,rot=(-24,-16,21),collision=True)
    # Forest tiers: near framing, middle scale cues, then a distant tree line.
    tree_positions=[(650,-680,1000),(750,850,1150),(1150,-950,1250),(1250,1150,1400),(1750,-1300,1350),(1800,1500,1600),(2800,-1450,1550),(2900,1750,1700),(3700,-1800,1450),(3800,1950,1800)]
    for i in range(26):
        x=rng.uniform(800,5200);side=-1 if i%2 else 1;y=side*rng.uniform(1800,3400);tree_positions.append((x,y,rng.uniform(1150,1850)))
    for i,(x,y,h) in enumerate(tree_positions):tree(i,x,y,h)
    # Accessible route has fixed surfaces; decoration stays beyond its side rails.
    for i in range(26):
        x=rng.uniform(350,3650);y=(-1 if i%2 else 1)*rng.uniform(350,1300)
        if 1500<x<3300 and abs(y)<850:y=math.copysign(rng.uniform(950,1300),y)
        w=rng.uniform(120,280);h=rng.uniform(80,240)
        shape('Rock_'+str(i),'Sphere',(x,y,-190+h/2),(w,w*.7,h),rock,rot=(rng.uniform(-20,20),rng.uniform(0,360),rng.uniform(-25,25)),collision=True)
    for i in range(22):
        x=rng.uniform(100,1450);y=(-1 if i%2 else 1)*rng.uniform(310,1000)
        for j in range(5):
            angle=j*72+rng.uniform(-10,10)
            shape('AlienPlant_'+str(i)+'_'+str(j),'Cone',(x+math.cos(math.radians(angle))*45,y+math.sin(math.radians(angle))*45,10),(35,55,rng.uniform(130,220)),leaf_tip if j%2 else teal,rot=(35,angle,0))
    # Small hot pockets suggest trapped fuel/electrical fires persisting after days.
    pockets=[(1760,-590,420,110),(2130,-750,610,170),(2530,740,640,140),(2950,590,770,130)]
    for i,(x,y,z,h) in enumerate(pockets):
        for j in range(3):
            shape('Fire_'+str(i)+'_'+str(j),'Cone',(x+j*28,y+j*12,z+h*.3),(65,65,h*(1-j*.18)),flame,rot=(8,j*45,-12))
        shape('FireCore_'+str(i),'Sphere',(x,y,z),(90,70,35),hot)
        light('FireLight_'+str(i),(x-60,y,z+80),(1,.19,.025),18,900)
        for j in range(7):
            w=100+j*38
            shape('Smoke_'+str(i)+'_'+str(j),'Sphere',(x+40*j,y+18*j,z+160+j*145),(w,w*.85,230+j*20),smoke)
    # Broken metal beside the route and low cover around the visual crash site.
    for i in range(12):
        x=rng.uniform(500,1500);y=(-1 if i%2 else 1)*rng.uniform(320,650)
        shape('DebrisPlate_'+str(i),'Cube',(x,y,-80),(rng.uniform(80,200),rng.uniform(90,240),25),metal,rot=(rng.uniform(-25,25),rng.uniform(0,360),rng.uniform(-20,20)),collision=True)
    for i in range(5):beam('LooseCable_'+str(i),(500+i*80,-280,-80),(1100+i*65,-300,-70),5,bark)
    # Offset the large silhouette so Evan sees its side, not only an entrance
    # straight under a roof. The original bay remains accessible beside it.
    hero_names=('OV_MainHull','OV_MainKeel','OV_HullRib','OV_BrokenRoof','OV_FracturedTail','OV_RearEngine','OV_SplitForward','OV_Fire','OV_Smoke')
    angle=math.radians(80)
    for a in actors.get_all_level_actors():
        if a.get_actor_label().startswith(hero_names):
            p=a.get_actor_location();dx=p.x-2250;dy=p.y
            a.set_actor_location(unreal.Vector(3500+dx*math.cos(angle)-dy*math.sin(angle),300+dx*math.sin(angle)+dy*math.cos(angle),p.z+100),False,False)
            rot=a.get_actor_rotation();rot.yaw+=80;a.set_actor_rotation(rot,False)
    for i,(x,y) in enumerate([(3150,-1050),(3650,-1050),(3150,1050),(3650,1050)]):
        shape('CrashSupportMound_'+str(i),'Sphere',(x,y,20),(900,850,480),rock,collision=True)
    existing['RecoveryStart'].set_actor_rotation(unreal.Rotator(0,0,0),False)
    existing['RecoveryStart'].set_actor_location(unreal.Vector(-390,0,100),False,False)
    # Keep the recovery panel below the eye line and clear of the spawn capsule.
    # The original tall panel filled the entire fresh-start camera view.
    existing['DamagedPanel'].set_actor_location(unreal.Vector(-245,0,60),False,False)
    existing['DamagedPanel'].set_actor_scale3d(unreal.Vector(.9,1.8,.9))
    shape('SkyDome','Sphere',(2000,0,0),(140000,140000,140000),sky)
    # Keep illumination cool outside and much dimmer inside.
    for a in existing.values():
        if isinstance(a,unreal.PointLight):
            x=a.get_actor_location().x
            a.point_light_component.set_editor_property('intensity',.8 if x<400 else 8)
            a.point_light_component.set_light_color(unreal.LinearColor(.10,.28,.35,1))
        elif isinstance(a,unreal.DirectionalLight):
            a.light_component.set_editor_property('intensity',1.8)
            a.light_component.set_light_color(unreal.LinearColor(.48,.73,1,1))
            a.set_actor_rotation(unreal.Rotator(-28,-35,0),False)
        elif isinstance(a,unreal.SkyLight):
            a.light_component.set_editor_property('intensity',.5)
    light('BreachCoolBounce',(850,0,330),(.07,.28,.40),28,1600)
    fog=actors.spawn_actor_from_class(unreal.ExponentialHeightFog,unreal.Vector(2000,0,-180));fog.set_actor_label('OV_ForestHaze');fog.set_folder_path(FOLDER)
    fields(fog.component,{'fog_density':.009,'fog_height_falloff':.28,'start_distance':900,'fog_inscattering_luminance':unreal.LinearColor(.06,.13,.18,1)})
    pp=actors.spawn_actor_from_class(unreal.PostProcessVolume,unreal.Vector(0,0,0));pp.set_actor_label('OV_Exposure');pp.set_folder_path(FOLDER)
    pp.set_editor_property('unbound',True)
    settings=pp.get_editor_property('settings')
    fields(settings,{'override_auto_exposure_method':True,'auto_exposure_method':unreal.AutoExposureMethod.AEM_MANUAL,'override_auto_exposure_apply_physical_camera_exposure':True,'auto_exposure_apply_physical_camera_exposure':False,'override_auto_exposure_bias':True,'auto_exposure_bias':1.25,'override_vignette_intensity':True,'vignette_intensity':.22})
    pp.set_editor_property('settings',settings)
    # Hide editor-only icons/volume outlines in comparison captures; lighting,
    # post processing, and the PlayerStart's collision stay enabled.
    pp.brush_component.set_visibility(False)
    for a in actors.get_all_level_actors():
        for typ in [unreal.BillboardComponent,unreal.ArrowComponent]:
            for component in a.get_components_by_class(typ):component.set_visibility(False)
    for component in existing['RecoveryStart'].get_components_by_class(unreal.CapsuleComponent):component.set_visibility(False)
    # Save only this new map and its new visual materials. Runtime BPs untouched.
    assert levels.save_current_level()
    report['actor_count']=len(actors.get_all_level_actors())
    report['route_preserved']=['PlayerStart','Crouch_Beam','Break_SafetyFloor','WeaponLocker','Bay_Cover_A','Bay_Cover_B','SearchTerminal','CommsPanel','ExitGate']
    report['saved']=True
except Exception as error:
    report['errors'].append(str(error));raise
finally:
    Path(unreal.Paths.project_saved_dir(),'wreckage_opening_build.json').write_text(json.dumps(report,indent=2))
