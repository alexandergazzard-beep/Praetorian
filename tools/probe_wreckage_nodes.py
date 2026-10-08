import json
from pathlib import Path
import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as BP

bp=unreal.load_asset('/Game/WreckagePrototype/Blueprints/BP_WreckagePlayer')
graph=BP.get_graph(bp,'EventGraph')
filters=['GetInputMouseDelta','IsInputKeyDown','WasInputKeyJustPressed','AddMovementInput','AddControllerYawInput','AddControllerPitchInput','GetActorForwardVector','GetActorRightVector','GetActorLocation','Crouch','Jump','PrintString','LineTraceByChannel','BreakHitResult','ApplyDamage','GetAllActorsWithTag','SetActorLocation','SetHiddenInGame','GetControlRotation','GetForwardVector','GetCameraLocation','GetCameraRotation','SpawnActorfromClass','Array|Add','Array|RemoveIndex','Array|Get','Array|Length','GetSafeNormal','GetDistanceTo','SetActorRotation','FindLookatRotation','ReceiveTick','ReceiveAnyDamage','IsCrouched','GetPlayerCharacter','GetPlayerController','VectorLength','GetComponentsByClass','SetVisibility','DrawText']
result={}
for f in filters:
    for n in BP.find_node_types(graph,f,[]):
        try:
            info=BP.get_node_type_pins(graph,n)
            result[n]={'in':[{ 'name':p.name,'type':p.type_id,'value':p.value} for p in info.input_pins], 'out':[{ 'name':p.name,'type':p.type_id} for p in info.output_pins]}
        except Exception as error:
            result[n]={'error':str(error)}
Path(unreal.Paths.project_saved_dir(),'wreckage_node_pins.json').write_text(json.dumps(result,indent=2))
