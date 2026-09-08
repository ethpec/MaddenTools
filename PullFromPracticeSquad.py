# Imports
import pandas as pd
import random
import math
import numpy as np
from itertools import product
from config import season_path

# File Paths
player_file_path = season_path('Player.xlsx')

# Load DataFrames
df = pd.read_excel(player_file_path)

# Team Index Dictionary
team_dict = {0:'CHI', 1:'CIN', 2:'BUF', 3:'DEN', 4:'CLE', 5:'TB', 6:'ARI', 7:'LAC', 8:'KC', 9:'IND', 
10:'DAL', 11:'MIA', 12:'PHI', 13:'ATL', 14:'SF', 15:'NYG', 16:'JAX', 17:'NYJ', 18:'DET', 19:'GB', 
20:'CAR', 21:'NE', 22:'LV', 23:'LAR', 24:'BAL', 25:'WAS', 26:'NO', 27:'SEA', 28:'PIT', 29:'TEN', 
30:'MIN', 31:'HOU', 32:'FA'}

# Position Requirement Dictionary (Active players required per team per position)
position_requirements = {
    'QB': 3,
    'HB': 3,
    'WR': 4,
    'TE': 3,
    'LT': 1,
    'LG': 1,
    'C': 1,
    'RG': 1,
    'RT': 1,
    'LE': 1,
    'RE': 1,
    'DT': 3,
    'LOLB': 1,
    'MLB': 1,
    'ROLB': 1,
    'CB': 4,
    'FS': 1,
    'SS': 1,
    'K': 1,
    'P': 1
}

# Filter for active players (Signed and Uninjured)
active_players = df[
    (df['ContractStatus'] == 'Signed') &
    (df['InjuryStatus'] == 'Uninjured')
]

# Build complete cross-product of all teams x positions (excluding FA team 32)
all_teams = [k for k in team_dict.keys() if k != 32]
all_positions = list(position_requirements.keys())
complete_index = pd.DataFrame(list(product(all_teams, all_positions)), columns=['TeamIndex', 'Position'])

# Count active players per team/position and merge onto complete index (missing = 0)
actual_counts = (
    active_players
    .groupby(['TeamIndex', 'Position'])
    .size()
    .reset_index(name='ActiveCount')
)
position_counts = complete_index.merge(actual_counts, on=['TeamIndex', 'Position'], how='left')
position_counts['ActiveCount'] = position_counts['ActiveCount'].fillna(0).astype(int)

# Convert TeamIndex to abbreviation
position_counts['Team'] = position_counts['TeamIndex'].map(team_dict)

# Add required counts and compare
position_counts['RequiredCount'] = position_counts['Position'].map(position_requirements)
position_counts['NotEnoughActivePlayers'] = position_counts['ActiveCount'] < position_counts['RequiredCount']

# === NEW: Check for Practice Squad backups ===
# Get set of (TeamIndex, Position) combinations that have PracticeSquad players
ps_players = df[df['ContractStatus'] == 'PracticeSquad']
ps_player_groups = set(zip(ps_players['TeamIndex'], ps_players['Position']))

# Apply function to compute HasPracticeSquadPlayer only when needed
def has_ps_player(row):
    if row['NotEnoughActivePlayers']:
        return (row['TeamIndex'], row['Position']) in ps_player_groups
    return None  # or np.nan if you prefer

position_counts['HasPracticeSquadPlayer'] = position_counts.apply(has_ps_player, axis=1)

# Final cleanup
position_counts = position_counts[['Team', 'Position', 'ActiveCount', 'NotEnoughActivePlayers', 'HasPracticeSquadPlayer']]

# Export to Excel
position_counts.to_excel(season_path('ActivePlayerCounts.xlsx'), index=False)