# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
import asyncio,json
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
async def main():
 async with streamable_http_client('http://127.0.0.1:8000/mcp') as (r,w):
  async with ClientSession(r,w) as session:
   await session.initialize()
   async def call(ts,t,**kw):
    result=await session.call_tool('call_tool',{'toolset_name':'editor_toolset.toolsets.'+ts,'tool_name':t,'arguments':kw})
    if result.is_error: raise RuntimeError(str(result.content))
    return json.loads(result.content[0].text)['returnValue']
   for tag,cls in [('', '/Game/WreckagePrototype/Blueprints/BP_WreckagePlayer_Runtime.BP_WreckagePlayer_Runtime_C'),('LV_Searcher','/Script/Engine.Character')]:
    actors=await call('scene.SceneTools','find_actors',name='',tag=tag,collision_channels=[],actor_type={'refPath':cls})
    for a in actors:
     print(a, await call('actor.ActorTools','get_actor_transform',actor=a),flush=True)
     print(await call('object.ObjectTools','get_properties',instance=a,properties=['Health','CapsuleComponent','PrimaryActorTick']+(['AttackCooldown'] if tag else [])),flush=True)
     comp=await call('actor.ActorTools','get_root_component',actor=a)
     print(comp,await call('object.ObjectTools','get_properties',instance=comp,properties=['BodyInstance']),flush=True)
asyncio.run(main())
