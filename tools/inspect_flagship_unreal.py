# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
"""Verify flagship assets with four controlled detail levels and simple collision."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/inspect_wreck_trio_live.py').read_text()
for old,new in [('wreck_trio_unreal','wreck_flagship71_unreal'),('triangle_percents=[.5,.22]','triangle_percents=[.5,.22,.08]'),('thresholds=[1,.35,.14]','thresholds=[1,.4,.18,.07]')]:source=source.replace(old,new)
exec(compile(source,str(ROOT/'tools/inspect_wreck_trio_live.py'),'exec'))
