# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
import asyncio,json
from pathlib import Path
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
async def main():
 async with streamable_http_client('http://127.0.0.1:8000/mcp') as (r,w):
  async with ClientSession(r,w) as session:
   await session.initialize()
   async def call(ts,t,**kw):
    result=await session.call_tool('call_tool',{'toolset_name':ts,'tool_name':t,'arguments':kw})
    if result.is_error:raise RuntimeError(str(result.content))
    return json.loads(result.content[0].text)['returnValue']
   editor='EditorToolset.EditorAppToolset';bp='editor_toolset.toolsets.blueprint.BlueprintTools'
   if await call(editor,'IsPIERunning'):await call(editor,'StopPIE')
   asset={'refPath':'/Game/WreckagePrototype/Blueprints/BP_WreckagePlayer_Runtime.BP_WreckagePlayer_Runtime'}
   graph=await call(bp,'get_graph',blueprint=asset,graph_name='EventGraph')
   result={}
   for query in ['GetCapsuleComponent','SetCollisionResponseToChannel','SetCollisionProfileName']:
    result[query]=await call(bp,'find_node_types',graph=graph,type_id_filter=query,context_pins=[])
   nodes=await call(bp,'find_nodes',graph=graph,title='BeginPlay',entry_points_only=True)
   result['begin']=await call(bp,'get_node_infos',nodes=nodes)
   Path('reports/wreckage_collision_nodes.json').write_text(json.dumps(result,indent=2));print('PROBED',flush=True)
   getnode=await call(bp,'create_node',graph=graph,type_id=result['GetCapsuleComponent'][0],pos={'x':-300,'y':-180})
   setnode=await call(bp,'create_node',graph=graph,type_id=result['SetCollisionResponseToChannel'][0],pos={'x':180,'y':-180})
   infos=await call(bp,'get_node_infos',nodes=[getnode,setnode])
   Path('reports/wreckage_collision_newnodes.json').write_text(json.dumps(infos,indent=2))
   def pin(info,direction,name):return next(p for p in info[direction+'_pins'] if p['name']==name)
   def pid(p):return p['pin_id']
   await call(bp,'set_pin_value',pin=pid(pin(infos[1],'input','Channel')),value='ECC_Visibility')
   await call(bp,'set_pin_value',pin=pid(pin(infos[1],'input','NewResponse')),value='ECR_Block')
   await call(bp,'connect_pins',output_pin=pid(infos[0]['output_pins'][0]),input_pin=pid(pin(infos[1],'input','self')))
   begin=pin(result['begin'][0],'output','then')
   old=begin['connected_pins'][0]
   await call(bp,'connect_pins',output_pin=pid(pin(infos[1],'output','then')),input_pin=old)
   await call(bp,'connect_pins',output_pin=pid(begin),input_pin=pid(pin(infos[1],'input','execute')))
   await call(bp,'compile_blueprint',blueprint=asset,warnings_as_errors=True)
   saved=await call('editor_toolset.toolsets.asset.AssetTools','save_assets',asset_paths=[asset['refPath']])
   print('SAVED',saved,flush=True)
asyncio.run(main())
