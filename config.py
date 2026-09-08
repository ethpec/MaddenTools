import os
from pathlib import Path

# Anchored to this file's location, so scripts work from any working directory
REPO_ROOT = Path(__file__).resolve().parent

# Update these two values when rolling the franchise forward to a new season.
GAME = 'Madden25'
SEASON = 'Season13'

# Defaults to Files/ inside the repo. Set MADDEN_DATA_DIR to keep exports elsewhere.
DATA_DIR = Path(os.environ.get('MADDEN_DATA_DIR', REPO_ROOT / 'Files'))

# Where the Madden import/export files for the current season live
def season_path(filename):
    return str(DATA_DIR / GAME / 'IE' / SEASON / filename)
