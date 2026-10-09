import csv,json,statistics,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1];src=max((R/'Unreal/LostVanguard 5.8/Saved/Profiling/CSV').glob('*.csv'),key=lambda p:p.stat().st_mtime)
rows=list(csv.DictReader(src.open(newline='',encoding='utf-8-sig')));out={'source_csv':str(src),'hardware':{'cpu':'Ryzen 7 5800X','gpu':'RTX 3080 Ti'},'viewport_pixels':[1526,862],'screen_percentage_command':100,'kind':'Actual PIE with continuously moving camera, three GPU fluid volumes, embers and wind','historical_material_edit_crash':True,'background_throttle_restored':True,'sample_frames':0}
for key in ['FrameTime','GPUTime','GameThreadTime','RenderThreadTime','RHI/DrawCalls']:
 vals=[]
 for row in rows[10:-10]:
  try:v=float(row[key])
  except (KeyError,ValueError,TypeError):continue
  if v>0:vals.append(v)
 if vals:
  vals.sort();out[key]={'mean':statistics.mean(vals),'median':statistics.median(vals),'p95':vals[int(.95*(len(vals)-1))]}
  if key=='FrameTime':out['sample_frames']=len(vals);out['average_fps']=1000/statistics.mean(vals)
assert out['sample_frames']>100
shutil.copy2(src,R/'reports/space_impact_v2_performance.csv');(R/'reports/space_impact_v2_performance.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
