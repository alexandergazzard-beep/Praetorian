# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
import asyncio,json,base64
from pathlib import Path
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
ROOT=Path(__file__).resolve().parents[1];SC='editor_toolset.toolsets.scene.SceneTools';AT='editor_toolset.toolsets.actor.ActorTools';OB='editor_toolset.toolsets.object.ObjectTools';AS='editor_toolset.toolsets.asset.AssetTools';ED='EditorToolset.EditorAppToolset';MT='editor_toolset.toolsets.material.MaterialTools';D='/Game/LostVanguard/Environment/SpaceImpact'
async def main():
 async with streamable_http_client('http://127.0.0.1:8000/mcp') as (r,w):
  async with ClientSession(r,w) as s:
   await s.initialize()
   async def call(ts,tool,**args):
    r=await s.call_tool('call_tool',dict(toolset_name=ts,tool_name=tool,arguments=args))
    if r.is_error:raise RuntimeError(str(r.content))
    return json.loads(r.content[0].text)['returnValue']
   if await call(ED,'IsPIERunning'):await call(ED,'StopPIE')
   async def setp(obj,**props):return await call(OB,'set_properties',instance=obj,values=json.dumps(props))
   for name in ['M_EntryScarredMetal','M_WindPBR']:
    m={'refPath':D+'/Materials/'+name+'.'+name}
    for ex in await call(MT,'get_expressions',material_or_function=m):
     if 'TextureSample' in ex['refPath']:
      props=json.loads(await call(OB,'get_properties',instance=ex,properties=['SamplerType']))
      if props['SamplerType']=='SAMPLERTYPE_LinearColor':await setp(ex,SamplerType='SAMPLERTYPE_Masks')
    await call(MT,'recompile',material_or_function=m)
   candidates=[]
   for prefix in ['Impact_Heat','Impact_MetalSoftbox','Impact_DuskRim','Impact_Sky','Impact_Firelight','Impact_Grade']:
    candidates+=await call(SC,'find_actors',name=prefix,tag='',collision_channels=[])
   for a in candidates:
    label=await call(AT,'get_label',actor=a)
    if label.startswith('Impact_Heat'):await setp(a,bHidden=True)
    lights=await call(AT,'get_components',actor=a,component_type={'refPath':'/Script/Engine.LightComponent'})
    if lights:
     values={'Impact_MetalSoftbox':22000,'Impact_DuskRim':5,'Impact_Sky':1.5}
     if label in values:await setp(lights[0],Intensity=values[label])
     if label.startswith('Impact_Firelight'):await setp(lights[0],Intensity=500)
    if label=='Impact_Grade':await setp(a,Settings={'AutoExposureBias':-.7})
   await call(AS,'save_assets',asset_paths=[D+'/Maps/L_SpaceImpact_Cinematic',D+'/Materials/M_EntryScarredMetal',D+'/Materials/M_WindPBR'])
   pose={'location':{'x':-1050,'y':-1550,'z':300},'rotation':{'pitch':1,'yaw':60,'roll':0}}
   await call(ED,'SetCameraTransform',transform=pose);await asyncio.sleep(5)
   shot=await call(ED,'CaptureViewport',captureTransform=pose,bShowUI=False,annotations={'gridSpacing':0,'gridExtent':0,'gridHeight':0,'maxLabelDistance':0,'classFilter':{'refPath':'/Script/Engine.Actor'},'maxLabels':0})
   (ROOT/'reports/space_impact_preview.png').write_bytes(base64.b64decode(shot['image']['data']));print('IMPACT_REFINED',flush=True)
asyncio.run(main())
