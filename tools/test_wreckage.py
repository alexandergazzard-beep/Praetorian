# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
"""Drive real PIE character inputs via test properties; record observed state."""
import asyncio
import base64
import json
import math
import sys
from pathlib import Path
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

sys.stdout.reconfigure(encoding='utf-8')
MAP=sys.argv[1] if len(sys.argv)>1 else '/Game/WreckagePrototype/Maps/L_Wreckage_Playable'
OPENING=MAP.endswith('L_Wreckage_Opening')
OUT=Path('reports/opening_playtest.json' if OPENING else 'reports/wreckage_playtest.json')
report={'map':MAP,'checks':[],'actions':[],'errors':[],'limitations':['Automated editor input properties used; physical keyboard/mouse feel needs a human pass.','Fresh 100-health start and normal 100-health death/restart are tested. Slow remote movement/combat uses temporary 5000 health, restored to 100 before the death check and by checkpoint restart; saved defaults remain unchanged. Normal-health encounter balance is not verified.']}
SCENE='editor_toolset.toolsets.scene.SceneTools'
OBJ='editor_toolset.toolsets.object.ObjectTools'
ACTOR='editor_toolset.toolsets.actor.ActorTools'
EDITOR='EditorToolset.EditorAppToolset'

def save():OUT.write_text(json.dumps(report,indent=2))

async def main():
    async with streamable_http_client('http://127.0.0.1:8000/mcp') as (reader,writer):
      async with ClientSession(reader,writer) as session:
        await session.initialize()
        async def call(toolset,tool,**args):
            result=await asyncio.wait_for(session.call_tool('call_tool',{'toolset_name':toolset,'tool_name':tool,'arguments':args}),25)
            if result.is_error:raise RuntimeError(str(result.content))
            value=json.loads(result.content[0].text)['returnValue'] if result.content and result.content[0].type=='text' else None
            return value
        if await call(EDITOR,'IsPIERunning'):
            await call(EDITOR,'StopPIE')
        await call(SCENE,'load_level',level_path=MAP)
        await call(EDITOR,'StartPIE',options={'bSimulate':False,'playMode':'PlayMode_InViewPort','warmupSeconds':.5})
        found=await call(SCENE,'find_actors',name='',tag='',collision_channels=[],actor_type={'refPath':'/Game/WreckagePrototype/Blueprints/BP_WreckagePlayer_Runtime.BP_WreckagePlayer_Runtime_C'})
        assert len(found)==1,found
        player=found[0]
        report['player']=player
        controllers=await call(SCENE,'find_actors',name='',tag='',collision_channels=[],actor_type={'refPath':'/Script/Engine.PlayerController'})
        controller=controllers[0]
        async def set_props(**props):
            await call(OBJ,'set_properties',instance=player,values=json.dumps(props))
        async def state(label):
            props=json.loads(await call(OBJ,'get_properties',instance=player,properties=['Step','Checkpoint','Health','Dead','HasWeapon','EvidenceRead','CommsRestored','Objective','Subtitle','SubtitleQueue','LookTotal','DebugMoveTime','bIsCrouched','Cue0','Cue5','Cue6','Cue8','Cue9']))
            transform=await call(ACTOR,'get_actor_transform',actor=player)
            item={'label':label,'properties':props,'transform':transform}
            report['actions'].append(item);save();print(json.dumps(item),flush=True)
            return props,transform
        async def check(name,condition,observed):
            report['checks'].append({'name':name,'passed':bool(condition),'observed':observed});save()
            assert condition,f'{name}: {observed}'
        async def input_action(label,seconds=.3,**props):
            await set_props(**props);await asyncio.sleep(seconds);return await state(label)
        async def move(label,forward,seconds,right=0,crouch=False,jump=False):
            return await input_action(label,seconds+.25,DebugForward=forward,DebugRight=right,DebugMoveTime=seconds,DebugCrouch=crouch,RequestJump=jump)
        async def face(yaw,pitch=0):
            # Exercise the same controller input as mouse look. Background editor
            # tick rates vary, so use observed heading rather than fixed timing.
            for _ in range(12):
                tr=await call(ACTOR,'get_actor_transform',actor=player)
                delta=(yaw-tr['rotation']['yaw']+180)%360-180
                if abs(delta)<.6:return
                await set_props(DebugLook=delta*.5,DebugMoveTime=.5)
                await asyncio.sleep(.85)
            raise AssertionError('Could not turn toward requested heading')
        async def capture(name):
            data=await call(EDITOR,'CaptureEditorImage')
            if OPENING:name='opening_'+name
            Path('reports/'+name+'.png').write_bytes(base64.b64decode(data['data']))
        async def go(label,x,y,tolerance=100,allow_dead=False,crouch=False):
            for attempt in range(12):
                tr=await call(ACTOR,'get_actor_transform',actor=player)
                dx=x-tr['location']['x'];dy=y-tr['location']['y'];dist=math.hypot(dx,dy)
                if dist<tolerance:return await state(label)
                await face(math.degrees(math.atan2(dy,dx)))
                speed=min(1.0,dist/500)
                seconds=min(2.0,max(1.0,dist/450))
                props,tr=await move(label+' segment '+str(attempt),speed,seconds,crouch=crouch)
                if props['Dead'] and allow_dead:return props,tr
                assert not props['Dead'],f'Died during {label}'
            raise AssertionError('Route did not reach '+label)
        props,tr=await state('Fresh PIE start')
        await check('Fresh start at recovery',props.get('Step')==0 and props['Health']==100,props)
        await capture('wreckage_recovery_play')
        props,tr=await input_action('Shift debris',RequestInteract=True)
        await check('Debris interaction',props.get('Step')==1,props)
        props,tr=await input_action('Look recovery',.6,DebugLook=40,DebugMoveTime=.5)
        await check('Look recovery',props.get('Step')==2,props)
        await face(0)
        props,tr=await go('Walk to passage',450,0,tolerance=65)
        await check('Walk recovery',props.get('Step')==3,props)
        props,tr=await go('Crouch under beam',1030,0,tolerance=25,crouch=True)
        await check('Crouch passage',props.get('Step')==4 and tr['location']['x']>940,{'state':props,'transform':tr})
        props,tr=await move('Approach break',1,.12)
        await set_props(Health=5000)
        props,tr=await move('Jump the break',1,2.0,jump=True)
        if props.get('Step')==4:
            props,tr=await move('Recover footing and finish the break',1,1.3,jump=True)
        await check('Break traversal',props.get('Step')==5 and tr['location']['z']>20,{'state':props,'transform':tr})
        await go('Weapon locker approach',1470,-80,tolerance=80)
        props,tr=await input_action('Weapon pickup',RequestInteract=True)
        await check('Weapon pickup',props.get('Step')==6 and props.get('HasWeapon'),props)
        await capture('wreckage_combat_play')
        await set_props(Health=100)
        await go('Enter bay',1730,0)
        props,tr=await go('Stand exposed to searcher fire',1840,-460,allow_dead=True)
        for _ in range(20):
            if props['Dead']:break
            await asyncio.sleep(1)
            props,tr=await state('Observe incoming fire')
            if props['Dead']:break
        await check('Combat can kill the player',props['Dead'] and props['Health']<=0,props)
        await capture('wreckage_death_play')
        props,tr=await input_action('Restart recovery checkpoint',RequestRestart=True)
        await check('Death/restart resets encounter',props['Health']==100 and props['Step']==5 and not props['Dead'],props)
        await check('Opening subtitles do not replay',props['Cue0'] and props['Subtitle']=='' and props['SubtitleQueue']==[],props)
        await set_props(Health=5000)
        props,tr=await input_action('Pickup after restart',RequestInteract=True)
        await go('Combat entrance after restart',1730,0)
        await go('South firing lane',1840,-470)
        async def shoot_at_enemy(target_x,target_y,label):
            tr=await call(ACTOR,'get_actor_transform',actor=player)
            await face(math.degrees(math.atan2(target_y-tr['location']['y'],target_x-tr['location']['x'])))
            for i in range(3):await input_action(label+' shot '+str(i+1),.45,RequestFire=True)
        await shoot_at_enemy(2480,-480,'First searcher')
        enemies=await call(SCENE,'find_actors',name='',tag='LV_Searcher',collision_channels=[])
        await check('Weapon trace defeats first searcher',len(enemies)==1,len(enemies))
        await go('South cover lane',2660,-430)
        await shoot_at_enemy(2780,150,'Second searcher')
        props,tr=await state('Combat clear')
        await check('First fight completes objective',props['Step']==7 and not props['Dead'],props)
        # Walk round the cover divider to the cyan record station.
        await go('East bay',3020,-200)
        await go('Search record access',3020,340)
        before=len(props['SubtitleQueue'])
        props,tr=await input_action('Read fresh search record',RequestInteract=True)
        await check('Evidence advances in order',props['EvidenceRead'] and props['Step']==8 and props['Checkpoint']==8,props)
        await capture('wreckage_evidence_play')
        first_cue=props['Cue8']
        props,tr=await input_action('Repeat evidence interaction',RequestInteract=True)
        await check('Evidence repeat does not replay cue',props['Step']==8 and props['Cue8']==first_cue,props)
        props,tr=await input_action('Restart after evidence checkpoint',RequestRestart=True)
        await check('Evidence remains available after restart',props['EvidenceRead'] and props['Step']==8 and props['Health']==100,props)
        # Try the exit before communications, with the actual blocking gate intact.
        await go('Approach locked exit',3980,0)
        props,tr=await input_action('Attempt early exit',RequestInteract=True)
        await check('Exit cannot bypass clue/communications',props['Step']==8 and not props['CommsRestored'] and tr['location']['x']<4040,{'state':props,'transform':tr})
        await go('Return to communications',3550,-240)
        props,tr=await input_action('Restore unidentified human signal',RequestInteract=True)
        await check('Communications advances after clue',props['Step']==9 and props['CommsRestored'],props)
        await go('Exit route',4230,0)
        props,tr=await input_action('Complete Wreckage',RequestInteract=True)
        await check('Complete route from fresh start',props['Step']==10 and props['EvidenceRead'] and props['CommsRestored'],props)
        await capture('wreckage_complete_play')
        await call(EDITOR,'StopPIE')
        await call(SCENE,'load_level',level_path='/Game/WreckagePrototype/Maps/L_Wreckage')
        await call(SCENE,'load_level',level_path='/Game/WreckagePrototype/Maps/L_Wreckage_Playable')
        current=await call(SCENE,'get_current_level')
        await call(SCENE,'load_level',level_path=MAP)
        current=await call(SCENE,'get_current_level')
        await check('Saved map reload',current==MAP,current)
        print('ALL_CHECKS_PASSED',flush=True)

try:asyncio.run(main())
except Exception as error:
    report['errors'].append(str(error));save();raise
