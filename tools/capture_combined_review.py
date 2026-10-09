# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
import asyncio,base64
from movement_mcp import session,ROOT,EDITOR
async def main():
 async with session() as call:
  pose={'location':{'x':-4300,'y':-5500,'z':2200},'rotation':{'pitch':-13,'yaw':51,'roll':0}}
  await call(EDITOR,'SetCameraTransform',transform=pose)
  await asyncio.sleep(3)
  shot=await call(EDITOR,'CaptureViewport',captureTransform=pose,bShowUI=False,annotations={'gridSpacing':0,'gridExtent':0,'gridHeight':0,'maxLabelDistance':0,'classFilter':{'refPath':'/Script/Engine.Actor'},'maxLabels':0})
  (ROOT/'reports/combined_orison_overview.png').write_bytes(base64.b64decode(shot['image']['data']))
  print('Combined review screenshot saved')
asyncio.run(main())
