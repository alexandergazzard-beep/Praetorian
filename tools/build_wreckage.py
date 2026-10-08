"""Create Wreckage prototype assets through Unreal editor APIs.

Run with UnrealEditor-Cmd -run=pythonscript -script=<this file>.
Only /Game/WreckagePrototype assets belong to this builder. Runtime is Blueprint.
"""
import json
from pathlib import Path
import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as BP
from editor_toolset.toolsets.actor import ActorTools

ROOT = '/Game/WreckagePrototype'
MAP = ROOT + '/Maps/L_Wreckage'
SAVED = Path(unreal.Paths.project_saved_dir())
SOURCE = Path(__file__).parent
report = {'map': MAP, 'checks': [], 'errors': []}

def blueprint(name, parent):
    path = ROOT + '/Blueprints/' + name
    existing = unreal.load_asset(path)
    return existing or BP.create(ROOT + '/Blueprints', name, parent.static_class())

def component(bp, typ, name):
    # Existing authored component templates are returned on subsequent iterations.
    sds = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    for handle in sds.k2_gather_subobject_data_for_blueprint(bp):
        data = unreal.SubobjectDataBlueprintFunctionLibrary.get_data(handle)
        obj = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(data)
        if str(unreal.SubobjectDataBlueprintFunctionLibrary.get_variable_name(data)) == name:
            return obj
    return ActorTools.add_component(bp, typ.static_class(), name)

def material(name, rgb):
    path = ROOT + '/Materials/' + name
    mat = unreal.load_asset(path)
    if mat:
        return mat
    mat = unreal.AssetToolsHelpers.get_asset_tools().create_asset(name, ROOT+'/Materials', unreal.Material, unreal.MaterialFactoryNew())
    color = unreal.MaterialEditingLibrary.create_material_expression(mat, unreal.MaterialExpressionConstant3Vector, -300, 0)
    color.set_editor_property('constant', unreal.LinearColor(*rgb, 1))
    unreal.MaterialEditingLibrary.connect_material_property(color, '', unreal.MaterialProperty.MP_BASE_COLOR)
    unreal.MaterialEditingLibrary.recompile_material(mat)
    unreal.EditorAssetLibrary.save_loaded_asset(mat)
    return mat

def box(name, xyz, size, mat):
    actor = actors.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(*xyz))
    actor.set_actor_label(name)
    actor.set_folder_path('WreckagePrototype/Blockout')
    mesh = actor.static_mesh_component
    mesh.set_static_mesh(cube)
    mesh.set_material(0, mat)
    mesh.set_collision_profile_name('BlockAll')
    actor.set_actor_scale3d(unreal.Vector(*(d/100 for d in size)))
    return actor

def setup():
    global actors, cube
    actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    levels = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    if unreal.EditorAssetLibrary.does_asset_exist(MAP):
        assert levels.load_level(MAP)
        # Rebuild only actors tagged by this source, leaving manually placed work.
        for actor in actors.get_all_level_actors():
            if str(actor.get_folder_path()).startswith('WreckagePrototype/'):
                actors.destroy_actor(actor)
    else:
        assert levels.new_level(MAP)
    cube = unreal.load_asset('/Engine/BasicShapes/Cube')
    metal = material('M_WreckMetal', (.14,.2,.24))
    floor = material('M_Floor', (.22,.29,.31))
    cover = material('M_Cover', (.36,.27,.16))
    clue = material('M_Evidence', (.02,.65,.8))
    danger = material('M_Searcher', (.8,.12,.06))
    ground = material('M_OrisonGround', (.12,.16,.12))
    # Metres-scale compartment, low passage, bay, alcove, and overlook.
    for name, x, length, width in [('Recovery',0,1000,800),('Passage',800,600,360),('Landing',1400,400,360),('Bay',2350,1500,1400),('Comms',3550,900,800),('Exit',4250,500,600)]:
        box(name+'_Floor',(x,0,-25),(length,width,50),floor)
        for side in [-1,1]:
            box(name+'_Wall_'+str(side),(x,side*(width/2+25),180),(length,50,360),metal)
    box('Break_SafetyFloor',(1150,0,-200),(220,360,40),floor)
    box('Crouch_Beam',(850,0,180),(180,360,110),metal)
    box('Recovery_BackWall',(-525,0,180),(50,850,360),metal)
    box('Recovery_Ceiling',(0,0,380),(1000,850,40),metal)
    box('DamagedPanel',(-280,0,135),(90,180,120),cover)
    box('WeaponLocker',(1530,-130,75),(110,90,150),cover)
    box('Bay_Cover_A',(2050,170,65),(220,180,130),cover)
    box('Bay_Cover_B',(2460,-170,65),(220,180,130),cover)
    box('Bay_FlankDivider',(2340,380,120),(600,70,240),metal)
    box('SearchTerminal',(2920,420,75),(120,90,150),clue)
    box('CommsPanel',(3710,-240,75),(120,90,150),clue)
    box('ExitGate',(4040,0,145),(45,610,290),danger)
    box('Surface_Prototype_Only',(2500,0,-280),(18000,18000,100),ground)
    for i, (x,y,h) in enumerate([(5000,2500,1300),(6000,-2000,1000),(7600,500,1900)]):
        box('Proposed_DistantRuin_'+str(i),(x,y,h/2-220),(220,320,h),metal)
    for typ, name, pos in [(unreal.DirectionalLight,'Sun',(1000,0,2000)),(unreal.SkyLight,'Ambient',(2000,0,1000)),(unreal.PlayerStart,'RecoveryStart',(-350,0,100))]:
        a=actors.spawn_actor_from_class(typ,unreal.Vector(*pos))
        a.set_actor_label(name); a.set_folder_path('WreckagePrototype/Setup')
        if typ == unreal.DirectionalLight:
            a.set_actor_rotation(unreal.Rotator(-40,-25,0),False)
            a.light_component.set_editor_property('intensity', 3.0)
        if typ == unreal.SkyLight:
            a.light_component.set_editor_property('intensity', 1.5)
    for x in [0,800,2000,2800,3550]:
        a=actors.spawn_actor_from_class(unreal.PointLight,unreal.Vector(x,0,270))
        a.set_folder_path('WreckagePrototype/Setup')
        a.point_light_component.set_editor_property('intensity',2000)
        a.point_light_component.set_editor_property('attenuation_radius',1400)
    player=blueprint('BP_WreckagePlayer',unreal.Character)
    camera=component(player,unreal.CameraComponent,'FirstPersonCamera')
    camera.set_editor_property('relative_location',unreal.Vector(0,0,64))
    camera.set_editor_property('use_pawn_control_rotation',True)
    gun=component(player,unreal.StaticMeshComponent,'PlaceholderWeapon')
    gun.set_static_mesh(cube)
    gun.set_editor_property('relative_location',unreal.Vector(48,18,45))
    gun.set_editor_property('relative_scale3d',unreal.Vector(.65,.12,.12))
    gun.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
    gun.set_editor_property('hidden_in_game',True)
    cdo=BP.get_default_object(player)
    cdo.set_editor_property('use_controller_rotation_yaw',True)
    move=cdo.character_movement
    move.set_editor_property('max_walk_speed',450)
    move.set_editor_property('max_walk_speed_crouched',220)
    move.set_editor_property('jump_z_velocity',450)
    move.set_editor_property('gravity_scale',1.2)
    move.set_editor_property('crouched_half_height',44)
    nav=move.get_editor_property('nav_agent_props'); nav.set_editor_property('can_crouch',True)
    move.set_editor_property('nav_agent_props',nav)
    enemy=blueprint('BP_SearcherPlaceholder',unreal.Character)
    body=component(enemy,unreal.StaticMeshComponent,'PlaceholderBody')
    body.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Cylinder'))
    body.set_material(0,danger)
    body.set_editor_property('relative_location',unreal.Vector(0,0,-5))
    body.set_editor_property('relative_scale3d',unreal.Vector(.55,.55,1.6))
    body.set_collision_profile_name('BlockAll')
    ecdo=BP.get_default_object(enemy)
    ecdo.set_editor_property('tags',[unreal.Name('LV_Searcher')])
    ecdo.character_movement.set_editor_property('max_walk_speed',140)
    mode=blueprint('BP_WreckageGameMode',unreal.GameModeBase)
    BP.compile_blueprint(player); BP.compile_blueprint(enemy); BP.compile_blueprint(mode)
    BP.get_default_object(mode).set_editor_property('default_pawn_class',player.generated_class())
    world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    world.get_world_settings().set_editor_property('default_game_mode',mode.generated_class())
    # Probe runtime graph nodes using the actual installed editor definitions.
    graph=BP.get_graph(player,'EventGraph')
    filters=['GetPlayerController','GetInputMouseDelta','IsInputKeyDown','WasInputKeyJustPressed','AddMovementInput','AddController','GetActorForwardVector','GetActorRightVector','GetActorLocation','Crouch','Jump','PrintString','GetWorldDeltaSeconds','GetGameTime','LineTraceByChannel','BreakHitResult','ApplyDamage','GetAllActorsWithTag','DestroyActor','SetActorLocation','SetHiddenInGame','SetTimer','GetControlRotation','GetForwardVector','GetPlayerCameraManager','GetCameraLocation','GetCameraRotation','SpawnActorfromClass','Array|','GetVelocity','ReceiveTick','ReceiveAnyDamage']
    node_report={}
    for f in filters:
        node_report[f]=list(BP.find_node_types(graph,f,[]))
    (SAVED/'wreckage_node_types.json').write_text(json.dumps(node_report,indent=2))
    for bp in [player,enemy,mode]:
        unreal.EditorAssetLibrary.save_loaded_asset(bp)
    assert levels.save_current_level()
    report['checks'].append('Saved blockout and initial Character/GameMode assets via editor APIs')
    report['actor_count']=len(actors.get_all_level_actors())

try:
    setup()
except Exception as error:
    report['errors'].append(str(error))
    raise
finally:
    (SAVED/'wreckage_build.json').write_text(json.dumps(report,indent=2))
