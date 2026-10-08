# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
import asyncio,json,sys
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
async def main():
 async with streamable_http_client('http://127.0.0.1:8000/mcp') as (reader,writer):
  async with ClientSession(reader,writer) as session:
   await session.initialize()
   async def call(ts,name,args):
    r=await session.call_tool('call_tool',{'toolset_name':ts,'tool_name':name,'arguments':args})
    if r.is_error:raise RuntimeError(str(r.content))
    return json.loads(r.content[0].text)['returnValue']
   p=(await call('editor_toolset.toolsets.scene.SceneTools','find_actors',{'name':'','tag':'','collision_channels':[],'actor_type':{'refPath':'/Game/WreckagePrototype/Blueprints/BP_WreckagePlayer_Runtime.BP_WreckagePlayer_Runtime_C'}}))[0]
   props=json.loads(sys.argv[1]); wait=float(sys.argv[2]) if len(sys.argv)>2 else 1
   await call('editor_toolset.toolsets.object.ObjectTools','set_properties',{'instance':p,'values':json.dumps(props)})
   for i in range(4):
    await asyncio.sleep(wait/4)
    state=await call('editor_toolset.toolsets.object.ObjectTools','get_properties',{'instance':p,'properties':['Step','Health','bPressedJump','JumpCurrentCount','DebugMoveTime','bIsCrouched','CharacterMovement']})
    transform=await call('editor_toolset.toolsets.actor.ActorTools','get_actor_transform',{'actor':p})
    print(json.dumps({'state':json.loads(state),'transform':transform}),flush=True)
asyncio.run(main())
