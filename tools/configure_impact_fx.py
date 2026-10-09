# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
import asyncio,json
from pathlib import Path
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
ROOT=Path(__file__).resolve().parents[1];TS='NiagaraToolsets.NiagaraToolset_System';system={'refPath':'/Game/LostVanguard/Environment/SpaceImpact/FX/NS_ImpactAtmosphere.NS_ImpactAtmosphere'}
def ref(e,s='',m='',i=None):return dict(system=system,emitterName=e,scriptName=s,moduleName=m,rendererIndex=0,inputNameStack=[] if i is None else [i])
async def main():
 async with streamable_http_client('http://127.0.0.1:8000/mcp') as (r,w):
  async with ClientSession(r,w) as session:
   await session.initialize()
   async def call(name,**args):
    r=await session.call_tool('call_tool',dict(toolset_name=TS,tool_name=name,arguments=args))
    if r.is_error:raise RuntimeError(str(r.content))
    return json.loads(r.content[0].text)['returnValue']
   async def setval(e,s,m,i,v):
    if isinstance(v,tuple):typ='/Script/CoreUObject.Vector3f';value=dict(zip('xyz',v))
    elif isinstance(v,bool):typ='/Script/Niagara.NiagaraBool';value={'value':-1 if v else 0}
    else:typ='/Script/Niagara.NiagaraFloat';value={'value':v}
    return await call('SetStackInputData',stackInputRef=ref(e,s,m,i),inputData={'struct':{'refPath':typ},'value':value})
   summary=await call('GetSystemSummary',system=system);existing={e['emitterName'] for e in summary['emitters']}
   for e in ['Smoke','Sparks']:
    if e not in existing:await call('AddEmitter',system=system,templateEmitter={'refPath':'/Niagara/DefaultAssets/Templates/Emitters/Fountain.Fountain'},emitterName=e)
   specs={'Fire':(15,.75,1.2,160,225,28,14,(0,0,0),.3,65),'Smoke':(3,5,7,160,260,80,18,(12,4,8),.15,70),'Sparks':(10,2,3.8,2,4,210,50,(18,7,-55),.22,80)}
   changes=[]
   for e,(rate,lmin,lmax,smin,smax,speed,angle,grav,drag,radius) in specs.items():
    vals=[('EmitterUpdateScript','SpawnRate','SpawnRate',rate),('ParticleSpawnScript','InitializeParticle','Lifetime Min',lmin),('ParticleSpawnScript','InitializeParticle','Lifetime Max',lmax),('ParticleSpawnScript','InitializeParticle','Uniform Sprite Size Min',smin),('ParticleSpawnScript','InitializeParticle','Uniform Sprite Size Max',smax),('ParticleSpawnScript','InitializeParticle','Adjust Hue',False),('ParticleSpawnScript','InitializeParticle','Sprite Rotation Angle Min',0),('ParticleSpawnScript','InitializeParticle','Sprite Rotation Angle Max',0 if e=='Fire' else 360),('ParticleSpawnScript','ShapeLocation','Sphere Radius',radius),('ParticleSpawnScript','AddVelocity','Velocity Speed',speed),('ParticleSpawnScript','AddVelocity','Cone Angle',angle),('ParticleUpdateScript','GravityForce','Gravity',grav),('ParticleUpdateScript','Drag','Drag',drag)]
    vals=[(s,m,i,v) for s,m,i,v in vals if i!='Adjust Hue']
    for s,m,i,v in vals:
     try:await setval(e,s,m,i,v);changes.append([e,m,i,v])
     except Exception as ex:raise RuntimeError(str((e,m,i,v,ex)))
    material='M_'+('Ember' if e=='Sparks' else e)
    await call('SetRendererData',renderer=ref(e),rendererData={'propertyValues':json.dumps({'material':{'refPath':'/Game/LostVanguard/Environment/SpaceImpact/Materials/'+material+'.'+material},'alignment':'Unaligned','facingMode':'FaceCamera','sortMode':'ViewDepth','pivotInUVSpace':{'x':.5,'y':.5}})})
   result=await session.call_tool('call_tool',{'toolset_name':'editor_toolset.toolsets.asset.AssetTools','tool_name':'save_assets','arguments':{'asset_paths':[system['refPath'].split('.')[0]]}});assert not result.is_error
   compile=await call('GetSystemCompileState',system=system);issues=await call('GetStackIssues',system=system)
   (ROOT/'reports/space_impact_fx.json').write_text(json.dumps({'compile':compile,'issues':issues,'changes':changes,'estimated_max_particles_per_site':77,'sites':3},indent=2));print('IMPACT_FX_COMPLETE',compile['aggregateStatus'],flush=True)
asyncio.run(main())
