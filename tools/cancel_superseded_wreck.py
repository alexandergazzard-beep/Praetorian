# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
"""Cancel only the known superseded Very Large candidate following user's correction."""
import asyncio,json,tempfile
from pathlib import Path
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
ROOT=Path(__file__).resolve().parents[1];LEDGER=ROOT/'reports/forest_wreck_spending.json'
async def main():
 d=json.loads(LEDGER.read_text());item=next(x for x in reversed(d['operations']) if x['asset']=='VeryLarge_HullFace' and x.get('task_id'))
 params=StdioServerParameters(command='C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe',args=['-NoProfile','-ExecutionPolicy','Bypass','-File',str(ROOT/'tools/start_meshy_mcp.ps1')])
 with tempfile.TemporaryFile(mode='w+',encoding='utf-8') as err:
  async with stdio_client(params,errlog=err) as (r,w):
   async with ClientSession(r,w) as s:
    await s.initialize()
    state=await s.call_tool('meshy_get_task_status',{'task_id':item['task_id'],'task_type':'image-to-3d','wait':False,'timeout_seconds':20,'response_format':'json'})
    assert not state.is_error
    data=state.structured_content or json.loads(next(b.text for b in state.content if b.type=='text'))
    item['outcome']=data['status'];item['superseded_by_user']='Large instead of Very Large'
    if item['outcome'] not in ['SUCCEEDED','FAILED','CANCELED','CANCELLED']:
     before=await s.call_tool('meshy_check_balance',{});assert not before.is_error
     result=await s.call_tool('meshy_cancel_task',{'task_id':item['task_id'],'task_type':'image-to-3d'})
     item['cancellation_requested']=not result.is_error
     item['cancellation_response']=[b.text for b in result.content if b.type=='text']
     after=await s.call_tool('meshy_check_balance',{});assert not after.is_error
     item['cancellation_balance_before']=[b.text for b in before.content if b.type=='text']
     item['cancellation_balance_after']=[b.text for b in after.content if b.type=='text']
    LEDGER.write_text(json.dumps(d,indent=2))
    print(json.dumps({'asset':item['asset'],'task_id':item['task_id'],'status_before_cancellation':item['outcome'],'cancellation_requested':item.get('cancellation_requested'),'cancellation_response':item.get('cancellation_response'),'balance_after':item.get('cancellation_balance_after')}))
asyncio.run(main())
