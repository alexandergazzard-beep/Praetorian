"""Author editable runtime Blueprints for the Wreckage blockout."""
import json
import textwrap
from pathlib import Path
import unreal
import toolset_registry
from editor_toolset.toolsets.blueprint import BlueprintTools as BP, ContainerType
from editor_toolset.toolsets import blueprint_dsl

# Native tool decorators log some Python exceptions instead of raising by default.
# Authoring must fail visibly rather than reporting an unchanged graph as compiled.
exception_context=toolset_registry.tool_raising_exceptions()
exception_context.__enter__()

ROOT='/Game/WreckagePrototype/Blueprints/'
SAVED=Path(unreal.Paths.project_saved_dir())
player=unreal.load_asset(ROOT+'BP_WreckagePlayer_Runtime') or unreal.EditorAssetLibrary.duplicate_asset(ROOT+'BP_WreckagePlayer',ROOT+'BP_WreckagePlayer_Runtime')
enemy=unreal.load_asset(ROOT+'BP_SearcherPlaceholder_Runtime') or unreal.EditorAssetLibrary.duplicate_asset(ROOT+'BP_SearcherPlaceholder',ROOT+'BP_SearcherPlaceholder_Runtime')
report={'compiled':[],'errors':[]}
function_bodies={}

def var(bp,name,typ,default=None,array=False):
    if name not in BP.list_variables(bp):
        BP.add_variable(bp,name,typ,container_type=ContainerType.ARRAY if array else None)
    if default is not None:
        BP.compile_blueprint(bp)
        BP.get_default_object(bp).set_editor_property(name,default)

def g(name): return '(Variables|Default|Get'+name+')'
def s(name,value): return '(Variables|Default|Set'+name+' '+str(value)+')'
def q(text): return '"'+text.replace('\\','\\\\').replace('"','\\"')+'"'
def v(x,y,z): return f'(Math|Vector|MakeVector :X {float(x)} :Y {float(y)} :Z {float(z)})'

def write(bp,graphname,code):
    graph=BP.get_graph(bp,graphname) if graphname=='EventGraph' else BP.add_function_graph(bp,graphname)
    def create_node(gph,typ,pos):
        editor=unreal.BlueprintGraphEditor.get_graph_editor(gph)
        if typ.startswith('Variables|Default|Get'):
            node=editor.add_get_member_variable_node(typ.split('|')[-1][3:])
        elif typ.startswith('Variables|Default|Set'):
            node=editor.add_set_member_variable_node(typ.split('|')[-1][3:])
        elif typ.startswith('LV|'):
            node=editor.add_call_function_node(typ.split('|')[-1])
        elif typ in ['AddEvent|EventAnyDamage','AddEvent|EventTick','AddEvent|EventBeginPlay']:
            event={'AddEvent|EventAnyDamage':'ReceiveAnyDamage','AddEvent|EventTick':'ReceiveTick','AddEvent|EventBeginPlay':'ReceiveBeginPlay'}[typ]
            node=BP.add_event(bp,event,pos)
        else:
            node=BP.create_node(gph,typ,pos)
        assert node,typ
        node.set_node_pos(pos)
        return node
    blueprint_dsl.Transpiler(graph,create_node,BP.connect_pins,BP._get_node_info,BP.set_pin_value,lambda gph:BP.find_nodes(gph),delete_node_fn=BP.delete_node,find_node_types_fn=lambda f:BP.find_node_types(graph,f)).transpile(code)
    BP.compile_blueprint(bp,True)
    if graphname!='EventGraph':
        function_bodies[graphname]=code.split('()',1)[1].strip()[:-1]

def function_call(bp,graph,fn,**pins):
    # Use the supported native graph editor for local calls omitted by discovery.
    return '(LV|'+fn+')'

def queue(text): return f'(Utilities|Array|Add :TargetArray {g("SubtitleQueue")} :NewItem {q(textwrap.fill(text,82))})'

try:
    defaults={'Step':('int',0),'Checkpoint':('int',0),'Health':('float',100.0),'Dead':('bool',False),'HasWeapon':('bool',False),'EvidenceRead':('bool',False),'CommsRestored':('bool',False),'Objective':('string','E: shift the wreckage'),'Subtitle':('string',''),'SubtitleTime':('float',0.0),'LookTotal':('float',0.0),'ShotCooldown':('float',0.0),
              'DebugForward':('float',0.0),'DebugRight':('float',0.0),'DebugLook':('float',0.0),'DebugMoveTime':('float',0.0),'DebugCrouch':('bool',False),'RequestInteract':('bool',False),'RequestJump':('bool',False),'RequestFire':('bool',False),'RequestRestart':('bool',False)}
    for name,(typ,default) in defaults.items():var(player,name,typ,default)
    for name in defaults:
        if name.startswith('Debug') or name.startswith('Request') or name=='Health':
            BP.set_variable_instance_editable(player,name,True)
    var(player,'SubtitleQueue','string',array=True)
    for i in range(11):var(player,'Cue'+str(i),'bool',False)
    for name in ['RefreshObjective','Advance','SpawnSearchers','Interact','Fire','Restart','RecoveryChecks']:
        BP.add_function_graph(player,name)
    BP.compile_blueprint(player)
    unreal.EditorAssetLibrary.save_loaded_asset(player)
    unreal.EditorAssetLibrary.save_loaded_asset(enemy)
    # Functions use the same paths for normal controls and editor-driven tests.
    steps=[('E: shift the wreckage','Clank: Evan. Can you hear me?'),('Look around to check suit response','Clank: Suit response is uneven. Follow the light.'),('WASD: walk to the damaged passage','Clank: Good. On your feet.'),('Hold C: pass under the low beam','Clank: I cannot account for the attack. My records are damaged. Clearance ahead. Keep low.'),('Space: cross the small break','Clank: Check your footing.'),('E near the locker: take the weapon','Clank: Movement checks complete. Movement beyond that wall. Manual release; power is gone.'),('Left mouse: clear the two searchers. Use cover or the flank.','Clank: Searchers ahead. Their speech is untranslated.'),('E near the cyan search terminal: access the record','Evan: Clear.'),('E near the communications panel: restore the signal','Clank: Fresh search records. They are looking for an artifact. This ship is marked as a search site. The record does not identify it.'),('Follow the route to the exit; E to continue','Human Signal: Any surviving units, respond. Rally-point transmission follows. Clank: Signal is weak. We have a direction.'),('WRECKAGE COMPLETE — proposed next mission: Rally Point','Evan: Then we move.')]
    cases=[]
    for i,(objective,line) in enumerate(steps):
        cases.append(f'(:{i} {s("Objective",q(textwrap.fill(objective,78)))} (if (not {g("Cue"+str(i))}) {queue(line)} {s("Cue"+str(i),"true")}))')
    write(player,'RefreshObjective','(fn RefreshObjective () (switch int '+g('Step')+' '+' '.join(cases)+'))')
    graph=BP.get_graph(player,'EventGraph')
    call=lambda fn,**kw:function_call(player,graph,fn,**kw)
    refresh=call('RefreshObjective')
    write(player,'Advance','(fn Advance () '+s('Step','(+ '+g('Step')+' 1)')+' '+refresh+')')
    graph=BP.get_graph(player,'EventGraph'); call=lambda fn,**kw:function_call(player,graph,fn,**kw)
    advance=call('Advance')
    # Clank is a suit companion in this prototype; no final robot model selected.
    write(player,'SpawnSearchers',f'''(fn SpawnSearchers ()
      (bind old (Actor|GetAllActorswithTag :Tag "LV_Searcher"))
      (for a old (Actor|DestroyActor :self a))
      (Game|SpawnActorfromClass :Class "{ROOT}BP_SearcherPlaceholder_Runtime.BP_SearcherPlaceholder_Runtime_C" :SpawnTransform (Math|Transform|MakeTransform :Location {v(2480,-480,100)}) :CollisionHandlingOverride "AlwaysSpawn")
      (Game|SpawnActorfromClass :Class "{ROOT}BP_SearcherPlaceholder_Runtime.BP_SearcherPlaceholder_Runtime_C" :SpawnTransform (Math|Transform|MakeTransform :Location {v(2780,150,100)}) :CollisionHandlingOverride "AlwaysSpawn"))''')
    graph=BP.get_graph(player,'EventGraph'); call=lambda fn,**kw:function_call(player,graph,fn,**kw)
    spawn=call('SpawnSearchers')
    interact=f'''(fn Interact ()
      (bind loc (Transformation|GetActorLocation))
      (switch int {g('Step')}
        (:0 (bind panels (Actor|GetAllActorswithTag :Tag "LV_Debris")) (for a panels (Actor|DestroyActor :self a)) {advance})
        (:5 (if (< (Math|Vector|VectorLength (- loc {v(1530,-130,100)})) 240.0)
              {s('HasWeapon','true')} (Development|SetHiddeninGame :self (Variables|Components|GetPlaceholderWeapon) :NewHidden false) {advance}))
        (:7 (if (< (Math|Vector|VectorLength (- loc {v(2920,420,100)})) 240.0)
              {s('EvidenceRead','true')} {s('Checkpoint','8')} {advance}))
        (:8 (if (< (Math|Vector|VectorLength (- loc {v(3710,-240,100)})) 240.0)
              {s('CommsRestored','true')} (bind gates (Actor|GetAllActorswithTag :Tag "LV_ExitGate")) (for a gates (Actor|DestroyActor :self a)) {advance}))
        (:9 (if (and (and {g('EvidenceRead')} {g('CommsRestored')}) (> (.x loc) 4100.0)) {advance}))))'''
    # Component variable category is discovered from the graph rather than assumed.
    component_nodes=['Actor|GetComponentsByClass']
    gun_show='(bind meshes (Actor|GetComponentsByClass :ComponentClass "/Script/Engine.StaticMeshComponent")) (for mesh meshes (bind scene (Utilities|Casting|CastToSceneComponent :Object mesh) (:then (Development|SetHiddeninGame :self scene :NewHidden false)) (:CastFailed)))'
    interact=interact.replace('(Development|SetHiddeninGame :self (Variables|Components|GetPlaceholderWeapon) :NewHidden false)',gun_show)
    interact=interact.replace('(:5','(:1) (:2) (:3) (:4) (:5').replace('(:7','(:6) (:7')
    write(player,'Interact',interact)
    # Fire a collision trace from the actual first-person camera; cover blocks damage.
    hit_names=['block','overlap','time','distance','location','impact','normal','impactnormal','physmat','hitactor','hitcomp','bone','bone2','item','element','face','trace_start','trace_end']
    fire=f'''(fn Fire () (if (and {g('HasWeapon')} (<= {g('ShotCooldown')} 0.0))
      {s('ShotCooldown','0.22')}
      (bind cam (Game|GetPlayerCameraManager :PlayerIndex 0))
      (bind start (Camera|GetCameraLocation :self cam))
      (bind rot (Camera|GetCameraRotation :self cam))
      (bind (hit success) (Collision|LineTraceByChannel :Start start :End (+ start (* (Math|Vector|GetForwardVector :InRot rot) 5000.0)) :TraceChannel "TraceTypeQuery1" :DrawDebugType "ForDuration" :DrawTime 0.12 :bIgnoreSelf true))
      (if success (bind ({' '.join(hit_names)}) (Collision|BreakHitResult :Hit hit))
        (Game|Damage|ApplyDamage :DamagedActor hitactor :BaseDamage 34.0 :DamageCauser self))))'''
    write(player,'Fire',fire)
    # Restart preserves clues and seen subtitle flags; combat respawns only before evidence checkpoint.
    restart=f'''(fn Restart ()
      {s('Health','100.0')} {s('Dead','false')} {s('Step',g('Checkpoint'))}
      {s('Subtitle','""')} {s('SubtitleTime','0.0')} (Utilities|Array|Clear :TargetArray {g('SubtitleQueue')})
      (if (>= {g('Checkpoint')} 8)
        (Transformation|SetActorLocation :NewLocation {v(3110,0,100)} :bTeleport true)
        (else (if (>= {g('Checkpoint')} 5)
          (Transformation|SetActorLocation :NewLocation {v(1400,0,100)} :bTeleport true)
          {s('HasWeapon','false')} {gun_show.replace('NewHidden false','NewHidden true')} {spawn}
          (else {s('Step','1')} (Transformation|SetActorLocation :NewLocation {v(-150,0,100)} :bTeleport true)))))
      {refresh})'''
    write(player,'Restart',restart)
    write(player,'RecoveryChecks',f'''(fn RecoveryChecks ()
      (bind loc (Transformation|GetActorLocation))
      (if (< (.z loc) -350.0) {s('Health','0.0')} {s('Dead','true')} {s('Objective',q('You fell. Press R to restart.'))})
      (switch int {g('Step')}
        (:0)
        (:1 (if (> {g('LookTotal')} 8.0) {advance}))
        (:2 (if (> (.x loc) 350.0) {advance}))
        (:3 (if (and (> (.x loc) 940.0) (Variables|Character|GetIsCrouched)) {advance}))
        (:4 (if (> (.x loc) 1250.0) {s('Checkpoint','5')} {advance}))
        (:5)
        (:6 (bind remaining (Actor|GetAllActorswithTag :Tag "LV_Searcher")) (if (== (Utilities|Array|Length remaining) 0) {advance}))))''')
    graph=BP.get_graph(player,'EventGraph'); call=lambda fn,**kw:function_call(player,graph,fn,**kw)
    # Key structures use native import-text syntax, avoiding changes to global input configuration.
    down=lambda key: f'(Game|Player|IsInputKeyDown :self pc :Key "(KeyName={key})")'
    pressed=lambda key: f'(Game|Player|WasInputKeyJustPressed :self pc :Key "(KeyName={key})")'
    tick=f'''(event EventBeginPlay
      (Collision|SetCollisionResponsetoChannel :self (Variables|Character|GetCapsuleComponent) :Channel "ECC_Visibility" :NewResponse "ECR_Block")
      {spawn} {refresh})
    (event EventAnyDamage (Damage DamageType InstigatedBy DamageCauser)
      (if (not {g('Dead')}) {s('Health','(- '+g('Health')+' Damage)')}
        (if (<= {g('Health')} 0.0) {s('Dead','true')} {s('Objective',q('You died. Press R to restart at the checkpoint.'))})))
    (event EventTick (DeltaSeconds)
      (bind pc (Game|GetPlayerController :PlayerIndex 0))
      {s('DebugMoveTime','(- '+g('DebugMoveTime')+' DeltaSeconds)')}
      (if (<= {g('DebugMoveTime')} 0.0) {s('DebugForward','0.0')} {s('DebugRight','0.0')} {s('DebugLook','0.0')})
      (if (or {pressed('R')} {g('RequestRestart')}) {s('RequestRestart','false')} {call('Restart')})
      (if (not {g('Dead')})
        (bind (dx dy) (Game|Player|GetInputMouseDelta :self pc))
        (Pawn|Input|AddControllerYawInput :Val (+ (* dx 0.6) (* {g('DebugLook')} DeltaSeconds)))
        (Pawn|Input|AddControllerPitchInput :Val (* dy -0.6))
        {s('LookTotal','(+ '+g('LookTotal')+' (+ (* dx dx) (* '+g('DebugLook')+' DeltaSeconds)))')}
        (Pawn|Input|AddMovementInput :WorldDirection (Transformation|GetActorForwardVector) :ScaleValue (+ {g('DebugForward')} (- (select {down('W')} 1.0 0.0) (select {down('S')} 1.0 0.0))))
        (Pawn|Input|AddMovementInput :WorldDirection (Transformation|GetActorRightVector) :ScaleValue (+ {g('DebugRight')} (- (select {down('D')} 1.0 0.0) (select {down('A')} 1.0 0.0))))
        (if (or {down('C')} {g('DebugCrouch')}) (Character|Crouch) (else (Character|UnCrouch)))
        (if (or {pressed('SpaceBar')} {g('RequestJump')}) {s('RequestJump','false')} (Character|Jump))
        (if (or {pressed('E')} {g('RequestInteract')}) {s('RequestInteract','false')} {call('Interact')})
        {s('ShotCooldown','(- '+g('ShotCooldown')+' DeltaSeconds)')}
        (if (or {down('LeftMouseButton')} {g('RequestFire')}) {call('Fire')} {s('RequestFire','false')})
        {call('RecoveryChecks')})
      {s('SubtitleTime','(- '+g('SubtitleTime')+' DeltaSeconds)')}
      (if (<= {g('SubtitleTime')} 0.0)
        {s('Subtitle','""')}
        (if (> (Utilities|Array|Length {g('SubtitleQueue')}) 0)
          {s('Subtitle','(Utilities|Array|Get(acopy) :Array '+g('SubtitleQueue')+' :"Dimension 1" 0)')}
          (Utilities|Array|RemoveIndex :TargetArray {g('SubtitleQueue')} :IndexToRemove 0) {s('SubtitleTime','6.0')}))
      )'''
    tick=tick.replace('(:1 (if (> '+g('LookTotal'),'(:0) (:1 (if (> '+g('LookTotal')).replace('(:6 (bind remaining','(:5) (:6 (bind remaining')
    write(player,'EventGraph',tick)
    for name,(typ,value) in defaults.items():BP.get_default_object(player).set_editor_property(name,value)
    for name,typ,value in [('Health','float',100.0),('AttackCooldown','float',1.0)]:var(enemy,name,typ,value)
    egraph=BP.get_graph(enemy,'EventGraph')
    # Readable stationary sentries; genuine traces block attacks behind structural cover.
    ecode=f'''(event EventAnyDamage (Damage DamageType InstigatedBy DamageCauser)
      {s('Health','(- '+g('Health')+' Damage)')} (if (<= {g('Health')} 0.0) (Actor|DestroyActor)))
    (event EventTick (DeltaSeconds)
      {s('AttackCooldown','(- '+g('AttackCooldown')+' DeltaSeconds)')}
      (bind target (Game|GetPlayerCharacter :PlayerIndex 0))
      (bind loc (Transformation|GetActorLocation :self target))
      (if (and (and (> (.x loc) 1650.0) (< (.x loc) 3200.0)) (<= {g('AttackCooldown')} 0.0))
        {s('AttackCooldown','1.2')}
        (bind origin (Transformation|GetActorLocation))
        (bind (hit success) (Collision|LineTraceByChannel :Start (+ origin {v(0,0,35)}) :End (+ loc {v(0,0,20)}) :bIgnoreSelf true :DrawDebugType "ForDuration" :DrawTime 0.15))
        (if success (bind ({' '.join(hit_names)}) (Collision|BreakHitResult :Hit hit))
          (if (== hitactor target) (Game|Damage|ApplyDamage :DamagedActor target :BaseDamage 12.0 :DamageCauser self)))))'''
    write(enemy,'EventGraph',ecode)
    for bp in [player,enemy]:
        BP.compile_blueprint(bp,True)
        assert unreal.EditorAssetLibrary.save_loaded_asset(bp)
        report['compiled'].append(bp.get_path_name())
except Exception as error:
    report['errors'].append(str(error)); raise
finally:
    (SAVED/'wreckage_gameplay_build.json').write_text(json.dumps(report,indent=2))
