# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
import asyncio,base64,json
from pathlib import Path
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
ROOT=Path(__file__).resolve().parents[1]
async def main():
 async with streamable_http_client('http://127.0.0.1:8000/mcp') as (r,w):
  async with ClientSession(r,w) as s:
   await s.initialize()
   async def call(ts,tool,**args):
    r=await s.call_tool('call_tool',{'toolset_name':ts,'tool_name':tool,'arguments':args})
    if r.is_error:raise RuntimeError(str(r.content))
    return json.loads(r.content[0].text).get('returnValue')
   ED='EditorToolset.EditorAppToolset';SC='editor_toolset.toolsets.scene.SceneTools';AT='editor_toolset.toolsets.actor.ActorTools';OB='editor_toolset.toolsets.object.ObjectTools';AS='editor_toolset.toolsets.asset.AssetTools'
   await call(SC,'load_level',level_path='/Game/LostVanguard/Art/Review/L_Debris_FirstPair_Review')
   await call(ED,'SelectActors',actors=[])
   for a in await call(SC,'find_actors',name='',tag='',collision_channels=[]):
    label=await call(AT,'get_label',actor=a)
    if label in ['Key','Fill','Rim']:
     for c in await call(AT,'get_components',actor=a,component_type={'refPath':'/Script/Engine.LightComponent'}):
      await call(OB,'set_properties',instance=c,values=json.dumps({'intensity':{'Key':500,'Fill':350,'Rim':500}[label]}))
    if label=='Review_Exposure':
     for c in await call(AT,'get_components',actor=a,component_type={'refPath':'/Script/Engine.BrushComponent'}):
      await call(OB,'set_properties',instance=c,values=json.dumps({'bVisible':False}))
    for c in await call(AT,'get_components',actor=a,component_type={'refPath':'/Script/Engine.BillboardComponent'}):
     await call(OB,'set_properties',instance=c,values=json.dumps({'bVisible':False}))
   camera={'location':{'x':190,'y':-270,'z':150},'rotation':{'pitch':-18,'yaw':132,'roll':0}}
   await call(ED,'SetCameraTransform',transform=camera)
   await asyncio.sleep(4)
   shot=await call(ED,'CaptureViewport',captureTransform=camera,bShowUI=False,annotations={'gridSpacing':0,'gridExtent':0,'gridHeight':0,'maxLabelDistance':0,'classFilter':{'refPath':'/Script/Engine.Actor'},'maxLabels':0})
   (ROOT/'reports/debris_pair_studio.png').write_bytes(base64.b64decode(shot['image']['data']))
   await call(AS,'save_assets',asset_paths=['/Game/LostVanguard/Art/Review/L_Debris_FirstPair_Review'])
   print('REVIEW_SAVED',flush=True)
asyncio.run(main())
