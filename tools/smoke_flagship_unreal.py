# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
"""Check replacement meshes in actual PIE without altering shared gameplay."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/wreck_trio_smoke.py').read_text().replace('wreck_trio_unreal','wreck_flagship71_unreal')
source=source.replace('three LODs','four LODs')
exec(compile(source,str(ROOT/'tools/wreck_trio_smoke.py'),'exec'))
