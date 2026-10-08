"""Create a clear prototype HUD using supported native Blueprint graph APIs."""
import json
from pathlib import Path
import unreal
import toolset_registry
from editor_toolset.toolsets.blueprint import BlueprintTools as BP
from editor_toolset.toolsets import blueprint_dsl
ctx=toolset_registry.tool_raising_exceptions();ctx.__enter__()
ROOT='/Game/WreckagePrototype/Blueprints/'
player=unreal.load_asset(ROOT+'BP_WreckagePlayer_Runtime')
hud=unreal.load_asset(ROOT+'BP_WreckageHUD') or BP.create(ROOT,'BP_WreckageHUD',unreal.HUD.static_class())
graph=BP.get_graph(hud,'EventGraph')
def create(g,typ,pos):
    editor=unreal.BlueprintGraphEditor.get_graph_editor(g)
    if typ=='AddEvent|DrawHUD':node=BP.add_event(hud,'ReceiveDrawHUD',pos)
    elif typ=='LVPlayer|Cast':
        node=BP.create_node(g,'Utilities|Casting|CastToCharacter',pos)
        BP.retarget_node_class(node,unreal.Character.static_class(),player.generated_class())
    elif typ.startswith('LVPlayer|Get'):
        node=editor.add_get_member_variable_node(typ.split('|')[-1][3:],player.generated_class().get_path_name())
    elif typ=='LVNative|HealthText':node=editor.add_call_function_node('/Script/Engine.KismetStringLibrary:Conv_DoubleToString')
    else:node=BP.create_node(g,typ,pos)
    assert node,typ
    node.set_node_pos(pos);return node

code='''(event DrawHUD (SizeX SizeY)
  (bind pawn (Game|GetPlayerCharacter :PlayerIndex 0))
  (bind p (LVPlayer|Cast :Object pawn)
    (:then
      (HUD|DrawRect :RectColor "(R=0.015,G=0.025,B=0.035,A=0.85)" :ScreenX 16.0 :ScreenY 16.0 :ScreenW (- SizeX 32.0) :ScreenH 122.0)
      (HUD|DrawText :Text "LOST VANGUARD / WRECKAGE — PROTOTYPE" :TextColor "(R=0.2,G=0.8,B=1,A=1)" :ScreenX 30.0 :ScreenY 24.0 :Scale 1.25)
      (HUD|DrawText :Text (LVPlayer|GetObjective :self p) :TextColor "(R=1,G=0.85,B=0.45,A=1)" :ScreenX 30.0 :ScreenY 52.0 :Scale 1.3)
      (HUD|DrawText :Text "WASD move | Mouse look | C crouch | Space jump | E interact | LMB fire | R restart | Tab record" :TextColor "(R=0.75,G=0.8,B=0.85,A=1)" :ScreenX 30.0 :ScreenY 91.0 :Scale 1.0)
      (HUD|DrawText :Text (LVNative|HealthText :InDouble (LVPlayer|GetHealth :self p)) :TextColor "(R=1,G=0.4,B=0.3,A=1)" :ScreenX 30.0 :ScreenY 112.0 :Scale 1.0)
      (HUD|DrawText :Text "+" :TextColor "(R=0.6,G=1,B=1,A=1)" :ScreenX (- (/ SizeX 2) 4) :ScreenY (- (/ SizeY 2) 8) :Scale 1.3)
      (bind subtitle (LVPlayer|GetSubtitle :self p))
      (HUD|DrawRect :RectColor "(R=0.015,G=0.025,B=0.035,A=0.9)" :ScreenX 16.0 :ScreenY (- SizeY 106.0) :ScreenW (- SizeX 32.0) :ScreenH 90.0)
      (HUD|DrawText :Text subtitle :TextColor "(R=0.85,G=0.95,B=1,A=1)" :ScreenX 30.0 :ScreenY (- SizeY 94.0) :Scale 1.15)
      (bind pc (Game|GetPlayerController :PlayerIndex 0))
      (if (and (LVPlayer|GetEvidenceRead :self p) (Game|Player|IsInputKeyDown :self pc :Key "(KeyName=Tab)"))
        (HUD|DrawRect :RectColor "(R=0.01,G=0.04,B=0.05,A=0.95)" :ScreenX 30.0 :ScreenY 165.0 :ScreenW (- SizeX 60.0) :ScreenH 125.0)
        (HUD|DrawText :Text "SEARCH RECORD — fresh system access\\nA specific artifact is being sought.\\nThis ship is marked as a search site.\\nThe record does not identify it or prove it was aboard." :TextColor "(R=0.6,G=1,B=1,A=1)" :ScreenX 46.0 :ScreenY 178.0 :Scale 1.2)))
    (:CastFailed)))'''
code=code.replace('\\n','\n')
blueprint_dsl.Transpiler(graph,create,BP.connect_pins,BP._get_node_info,BP.set_pin_value,lambda g:BP.find_nodes(g),delete_node_fn=BP.delete_node,find_node_types_fn=lambda f:BP.find_node_types(graph,f)).transpile(code)
BP.compile_blueprint(hud,True)
assert unreal.EditorAssetLibrary.save_loaded_asset(hud)
Path(unreal.Paths.project_saved_dir(),'wreckage_hud_build.json').write_text(json.dumps({'hud':hud.get_path_name(),'compiled':True},indent=2))
