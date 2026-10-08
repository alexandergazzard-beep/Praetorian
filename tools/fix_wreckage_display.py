# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
"""Repair literal subtitle newlines and preview lighting through live editor tools."""
import asyncio,json
from pathlib import Path
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
async def main():
 async with streamable_http_client('http://127.0.0.1:8000/mcp') as (reader,writer):
  async with ClientSession(reader,writer) as session:
   await session.initialize()
   async def call(ts,tool,**args):
    r=await session.call_tool('call_tool',{'toolset_name':ts,'tool_name':tool,'arguments':args})
    if r.is_error:raise RuntimeError(str(r.content))
    return json.loads(r.content[0].text)['returnValue']
   ts='editor_toolset.toolsets.blueprint.BlueprintTools'; count=0
   if await call('EditorToolset.EditorAppToolset','IsPIERunning'):await call('EditorToolset.EditorAppToolset','StopPIE')
   paths=[]
   for name,graphname in [('BP_WreckagePlayer_Runtime','RefreshObjective'),('BP_WreckageHUD','EventGraph')]:
    path='/Game/WreckagePrototype/Blueprints/'+name+'.'+name; paths.append(path)
    bp={'refPath':path}; graph=await call(ts,'get_graph',blueprint=bp,graph_name=graphname)
    nodes=await call(ts,'find_nodes',graph=graph,title='',entry_points_only=False)
    infos=await call(ts,'get_node_infos',nodes=nodes)
    for info in infos:
     for pin in info['inputPins'] if 'inputPins' in info else info['input_pins']:
      value=pin['value']
      if '\\n' in value or '\\u2014' in value:
       newvalue=value.replace('\\\\n','\n').replace('\\n','\n').replace('\\\\u2014','-').replace('\\u2014','-')
       await call(ts,'set_pin_value',pin=pin.get('pinId',pin.get('pin_id')),value=newvalue);count+=1
    await call(ts,'compile_blueprint',blueprint=bp,warnings_as_errors=True)
   lights=await call('editor_toolset.toolsets.scene.SceneTools','find_actors',name='',tag='',collision_channels=[],actor_type={'refPath':'/Script/Engine.Light'})
   for actor in lights:
    comp=await call('editor_toolset.toolsets.actor.ActorTools','get_root_component',actor=actor)
    await call('editor_toolset.toolsets.object.ObjectTools','set_properties',instance=comp,values=json.dumps({'Mobility':'Movable'}))
   paths.append('/Game/WreckagePrototype/Maps/L_Wreckage_Playable')
   result=await call('editor_toolset.toolsets.asset.AssetTools','save_assets',asset_paths=paths)
   Path('reports/wreckage_display_fix.json').write_text(json.dumps({'newline_pins_fixed':count,'movable_lights':len(lights),'saved':result},indent=2))
   print('Display fix saved:',result)
asyncio.run(main())
