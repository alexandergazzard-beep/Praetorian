# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
"""Verify saved runtime defaults and compile connected assets through the editor."""
import asyncio,json
from pathlib import Path
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
async def main():
 async with streamable_http_client('http://127.0.0.1:8000/mcp') as (r,w):
  async with ClientSession(r,w) as session:
   await session.initialize()
   async def call(ts,tool,**args):
    result=await session.call_tool('call_tool',{'toolset_name':ts,'tool_name':tool,'arguments':args})
    if result.is_error:raise RuntimeError(str(result.content))
    return json.loads(result.content[0].text)['returnValue']
   editor='EditorToolset.EditorAppToolset';bp='editor_toolset.toolsets.blueprint.BlueprintTools'
   assert not await call(editor,'IsPIERunning'),'Finish the play test before saved inspection'
   result={'compiled':[]}
   assets=[]
   for name in ['BP_WreckagePlayer_Runtime','BP_SearcherPlaceholder_Runtime','BP_WreckageGameMode_Runtime','BP_WreckageHUD']:
    asset={'refPath':'/Game/WreckagePrototype/Blueprints/'+name+'.'+name};assets.append(asset['refPath'])
    await call(bp,'compile_blueprint',blueprint=asset,warnings_as_errors=True)
    result['compiled'].append(name)
    if name=='BP_WreckagePlayer_Runtime':
     result['saved_player_defaults']=json.loads(await call('editor_toolset.toolsets.object.ObjectTools','get_properties',instance=asset,properties=['Health','Step','Checkpoint','DebugForward','DebugRight','DebugLook','DebugCrouch','HasWeapon','EvidenceRead','CommsRestored']))
     assert result['saved_player_defaults']['Health']==100
     assert result['saved_player_defaults']['Step']==0
   result['saved']=await call('editor_toolset.toolsets.asset.AssetTools','save_assets',asset_paths=assets)
   result['level']=await call('editor_toolset.toolsets.scene.SceneTools','get_current_level')
   result['actors']=await call('editor_toolset.toolsets.scene.SceneTools','find_actors',name='',tag='',collision_channels=[])
   Path('reports/wreckage_saved_inspection.json').write_text(json.dumps(result,indent=2));print('SAVED_ASSETS_VERIFIED',flush=True)
asyncio.run(main())
