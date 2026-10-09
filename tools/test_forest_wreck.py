# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
"""Reuse the established route test; preserve its historical reports."""
import sys,asyncio
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import test_wreckage as test
test.MAP='/Game/LostVanguard/Environment/OpeningReview/Maps/L_ForestWreck_Review'
test.OPENING=True
test.OUT=Path('reports/forest_wreck_playtest.json')
test.CAPTURE_PREFIX='forest_wreck_'
test.CAPTURE_VIEWPORT=True
test.report['map']=test.MAP
try:asyncio.run(test.main())
except Exception as error:
 test.report['errors'].append(str(error));test.save();raise
