# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
"""Repair only the literal Unicode escape in the completion label."""
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
    return json.loads(result.content[0].text).get('returnValue')
   assert not await call('EditorToolset.EditorAppToolset','IsPIERunning')
   ts='editor_toolset.toolsets.blueprint.BlueprintTools'
   bp={'refPath':'/Game/WreckagePrototype/Blueprints/BP_WreckagePlayer_Runtime.BP_WreckagePlayer_Runtime'}
   graph=await call(ts,'get_graph',blueprint=bp,graph_name='RefreshObjective')
   nodes=await call(ts,'find_nodes',graph=graph,title='',entry_points_only=False)
   infos=await call(ts,'get_node_infos',nodes=nodes);fixed=[]
   for node in infos:
    for pin in node['input_pins']:
     value=pin['value']
     if '\\u2014' in value:
      clean=value.replace('\\\\u2014','-').replace('\\u2014','-')
      await call(ts,'set_pin_value',pin=pin['pin_id'],value=clean);fixed.append(clean)
   await call(ts,'compile_blueprint',blueprint=bp,warnings_as_errors=True)
   saved=await call('editor_toolset.toolsets.asset.AssetTools','save_assets',asset_paths=[bp['refPath']])
   Path('reports/wreckage_end_label_fix.json').write_text(json.dumps({'fixed':fixed,'saved':saved},indent=2));print('LABEL_SAVED',saved,flush=True)
asyncio.run(main())
