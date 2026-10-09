# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
import asyncio,json
from pathlib import Path
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
R=Path(__file__).resolve().parents[1];UI='SlateInspectorToolset.SlateInspectorToolset';ED='EditorToolset.EditorAppToolset';OB='editor_toolset.toolsets.object.ObjectTools'
async def main():
 async with streamable_http_client('http://127.0.0.1:8000/mcp') as (r,w):
  async with ClientSession(r,w) as s:
   await s.initialize()
   async def c(ts,n,**args):
    z=await s.call_tool('call_tool',dict(toolset_name=ts,tool_name=n,arguments=args));assert not z.is_error,str(z.content);return json.loads(z.content[0].text)['returnValue']
   async def cmd(t):await c(UI,'Type',ref='tb2',text=t,submit=True)
   await c(OB,'set_properties',instance={'refPath':'/Script/UnrealEd.Default__EditorPerformanceSettings'},values='{"bThrottleCPUWhenNotForeground":false}')
   assert not await c(ED,'IsPIERunning')
   await c(ED,'StartPIE',options={'bSimulate':False,'playMode':'PlayMode_InViewPort','warmupSeconds':2})
   for t in ['r.Editor.Viewport.OverridePIEScreenPercentage 0','r.DynamicRes.OperationMode 0','r.ScreenPercentage 100','r.VSync 0','t.MaxFPS 0']:await cmd(t)
   await asyncio.sleep(5);await cmd('csvprofile start');await cmd('py "'+str(R/'tools/orbit_impact_runtime.py').replace('\\','/')+'"');await asyncio.sleep(23);await cmd('csvprofile stop');await asyncio.sleep(3)
   await c(ED,'StopPIE');await cmd('r.Editor.Viewport.OverridePIEScreenPercentage 1');await cmd('r.ScreenPercentage 0')
   await c(OB,'set_properties',instance={'refPath':'/Script/UnrealEd.Default__EditorPerformanceSettings'},values='{"bThrottleCPUWhenNotForeground":true}')
   print('IMPACT_V2_FULL_RES_BENCHMARK_COMPLETE',flush=True)
asyncio.run(main())
