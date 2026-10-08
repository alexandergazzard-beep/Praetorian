# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
import asyncio,json
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

async def main():
    async with streamable_http_client('http://127.0.0.1:8000/mcp') as (reader,writer):
      async with ClientSession(reader,writer) as session:
        await session.initialize()
        async def call(ts,name,args):
            result=await session.call_tool('call_tool',{'toolset_name':ts,'tool_name':name,'arguments':args})
            if result.is_error:raise RuntimeError(str(result.content))
            return json.loads(result.content[0].text)['returnValue']
        editor='EditorToolset.EditorAppToolset'
        if await call(editor,'IsPIERunning',{}):await call(editor,'StopPIE',{})
        bp={'refPath':'/Game/WreckagePrototype/Blueprints/BP_WreckagePlayer_Runtime.BP_WreckagePlayer_Runtime'}
        ts='editor_toolset.toolsets.blueprint.BlueprintTools'
        for name in ['DebugForward','DebugRight','DebugLook','DebugMoveTime','DebugCrouch','RequestInteract','RequestJump','RequestFire','RequestRestart','Health']:
            await call(ts,'set_variable_instance_editable',{'blueprint':bp,'variable_name':name,'instance_editable':True})
        await call(ts,'compile_blueprint',{'blueprint':bp,'warnings_as_errors':True})
        await call('editor_toolset.toolsets.asset.AssetTools','save_assets',{'asset_paths':[bp['refPath']]})
        print('Live test inputs made editable; Blueprint compiled and saved.')
asyncio.run(main())
