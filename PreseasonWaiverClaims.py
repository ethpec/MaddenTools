# Imports
import pandas as pd
import random

# File Paths
player_file_path = 'Files/Madden26/IE/Season2/Player.xlsx'
draft_order_file_path = 'Files/Madden26/IE/Season2/DraftOrder.xlsx'

# Team Index Dictionary
team_dict = {0: 'CHI', 1: 'CIN', 2: 'BUF', 3: 'DEN', 4: 'CLE', 5: 'TB', 6: 'ARI', 7: 'LAC', 8: 'KC', 9: 'IND',
             10: 'DAL', 11: 'MIA', 12: 'PHI', 13: 'ATL', 14: 'SF', 15: 'NYG', 16: 'JAX', 17: 'NYJ', 18: 'DET',
             19: 'GB', 20: 'CAR', 21: 'NE', 22: 'LV', 23: 'LAR', 24: 'BAL', 25: 'WAS', 26: 'NO', 27: 'SEA',
             28: 'PIT', 29: 'TEN', 30: 'MIN', 31: 'HOU'}

# Draft Order Dictionary
team_draft_dict = {0: 'SF', 1: 'CHI', 2: 'CIN', 3: 'BUF', 4: 'DEN', 5: 'CLE', 6: 'TB', 7: 'ARI',
                   10: 'LAC', 11: 'KC', 12: 'IND', 13: 'WAS', 14: 'DAL', 15: 'MIA', 16: 'PHI', 17: 'ATL',
                   19: 'NYG', 21: 'JAX', 22: 'NYJ', 23: 'DET',
                   25: 'GB', 26: 'CAR', 27: 'NE', 28: 'LV', 29: 'LAR', 30: 'BAL', 31: 'NO', 32: 'SEA',
                   33: 'PIT', 34: 'HOU', 35: 'TEN', 36: 'MIN'}

# Load and filter to signed players
player_df = pd.read_excel(player_file_path)
signed_df = player_df[player_df['ContractStatus'] == 'Signed'].copy()

# --- Team Need Tier Logic ---
# Config maps group label → positions to pool + tier checks
# Tier checks: (tier, n_index_0based, ovr_threshold), ordered highest tier first
POSITION_TIER_CONFIG = {
    'CB':   {'positions': ['CB'],            'tiers': [(3, 2, 72), (2, 3, 70), (1, 4, 65)]},
    'WR':   {'positions': ['WR'],            'tiers': [(3, 2, 72), (2, 3, 70), (1, 4, 65)]},
    'T':    {'positions': ['LT', 'RT'],      'tiers': [(3, 1, 68), (2, 2, 67), (1, 2, 65)]},
    'G':    {'positions': ['LG', 'RG'],      'tiers': [(3, 1, 68), (2, 2, 67), (1, 2, 65)]},
    'C':    {'positions': ['C'],             'tiers': [(3, 0, 65), (2, 0, 68), (1, 1, 62)]},
    'OLB':  {'positions': ['LOLB', 'ROLB'],  'tiers': [(3, 1, 63), (2, 1, 65), (1, 2, 63)]},
    'MLB':  {'positions': ['MLB'],           'tiers': [(3, 0, 63), (2, 0, 66), (1, 1, 62)]},
    'HB':   {'positions': ['HB'],            'tiers': [(3, 1, 70), (2, 1, 73), (1, 2, 70)]},
    'FS':   {'positions': ['FS'],            'tiers': [(3, 0, 65), (2, 0, 70), (1, 1, 63)]},
    'SS':   {'positions': ['SS'],            'tiers': [(3, 0, 65), (2, 0, 70), (1, 1, 63)]},
    'TE':   {'positions': ['TE'],            'tiers': [(3, 1, 64), (2, 1, 67), (1, 2, 63)]},
    'EDGE': {'positions': ['LE', 'RE'],      'tiers': [(3, 2, 67), (2, 2, 69), (1, 3, 65)]},
    'DT':   {'positions': ['DT'],            'tiers': [(3, 2, 65), (2, 2, 67), (1, 3, 65)]},
    'QB':   {'positions': ['QB'],            'tiers': [(3, 1, 60), (2, 1, 64), (1, 2, 58)]},
}

def get_nth_rating(ratings_list, n):
    """Return nth best rating (0-indexed), or 0 if fewer than n+1 players."""
    return ratings_list[n] if n < len(ratings_list) else 0

def get_position_need_tier(team_df, group):
    """Return TeamNeedTier (1-3) for a position group on a team, or None if no need."""
    config = POSITION_TIER_CONFIG[group]
    ratings = (team_df[team_df['Position'].isin(config['positions'])]
               .sort_values('OverallRating', ascending=False)['OverallRating']
               .tolist())
    for tier, n, threshold in config['tiers']:
        if get_nth_rating(ratings, n) < threshold:
            return tier
    return None

need_positions = list(POSITION_TIER_CONFIG.keys())

# Build team needs DataFrame
team_needs_rows = []
for team_idx, team_name in team_dict.items():
    team_df = signed_df[signed_df['TeamIndex'] == team_idx]
    for position in need_positions:
        tier = get_position_need_tier(team_df, position)
        if tier is not None:
            team_needs_rows.append({
                'TeamIndex': team_idx,
                'Team': team_name,
                'Position': position,
                'TeamNeedTier': tier
            })

team_needs_df = pd.DataFrame(team_needs_rows, columns=['TeamIndex', 'Team', 'Position', 'TeamNeedTier'])

# Summarize needs per team: one row per team with tier position lists
def join_positions(series):
    return ', '.join(series.tolist())

tier_pivot = (team_needs_df.groupby(['TeamIndex', 'Team', 'TeamNeedTier'])['Position']
              .apply(join_positions)
              .unstack('TeamNeedTier')
              .rename(columns={3: 'Tier3Positions', 2: 'Tier2Positions', 1: 'Tier1Positions'})
              .reset_index())

# Ensure all tier columns exist even if no team has that tier
for col in ['Tier3Positions', 'Tier2Positions', 'Tier1Positions']:
    if col not in tier_pivot.columns:
        tier_pivot[col] = None

team_summary_df = tier_pivot[['TeamIndex', 'Team', 'Tier3Positions', 'Tier2Positions', 'Tier1Positions']]

# --- Draft Order / Waiver Priority ---
draft_order_df = pd.read_excel(draft_order_file_path)

# Filter to current year Round 0, sort by PickNumber to establish waiver claim order
waiver_order_df = (draft_order_df[(draft_order_df['YearOffset'] == 0) & (draft_order_df['Round'] == 0)]
                   .sort_values('PickNumber')
                   .reset_index(drop=True))

# Decode OriginalTeam: rightmost 16 bits of binary string → decimal → team name
def decode_team(binary_str):
    return team_draft_dict.get(int(str(binary_str)[-16:], 2), None)

waiver_order_df['Team'] = waiver_order_df['OriginalTeam'].apply(decode_team)

# --- Waiver Claim Simulation ---

team_highest_tier = team_needs_df.groupby('Team')['TeamNeedTier'].max().to_dict()

def get_tier_bonus(team):
    tier = team_highest_tier.get(team)
    if tier == 3:
        return 0.15
    elif tier == 2:
        return 0.10
    return 0.0

MAX_CLAIMS_PER_TEAM = 4
base_prob = 0.65
waiver_sim_rows = []

for _, row in waiver_order_df.iterrows():
    team = row['Team']
    if team is None:
        continue
    tier_bonus = get_tier_bonus(team)
    team_claims = 0
    while team_claims < MAX_CLAIMS_PER_TEAM:
        claim_prob = max(0.0, base_prob) + tier_bonus
        if random.random() < claim_prob:
            team_claims += 1
            base_prob -= 0.02
        else:
            break
    waiver_sim_rows.append({
        'PickNumber': row['PickNumber'],
        'Team': team,
        'TierBonus': tier_bonus,
        'ClaimsPlaced': team_claims
    })

waiver_sim_df = pd.DataFrame(waiver_sim_rows)
waiver_sim_df = waiver_sim_df.merge(
    team_summary_df[['Team', 'Tier3Positions', 'Tier2Positions', 'Tier1Positions']],
    on='Team', how='left'
)

# --- Waiver Claim Targets ---

eligible_df = player_df[
    (player_df['ContractStatus'].isin(['FreeAgent', 'PracticeSquad'])) &
    (player_df['YearsPro'] <= 3)
].copy()

waiver_targets_rows = []
for group, config in POSITION_TIER_CONFIG.items():
    pos_df = (eligible_df[eligible_df['Position'].isin(config['positions'])]
              .sort_values('OverallRating', ascending=False))
    if pos_df.empty:
        continue
    cutoff_rating = pos_df['OverallRating'].iloc[min(4, len(pos_df) - 1)]
    top_df = pos_df[pos_df['OverallRating'] >= cutoff_rating].copy()
    top_df['PositionGroup'] = group
    waiver_targets_rows.append(top_df)

waiver_targets_df = pd.concat(waiver_targets_rows)[
    ['FirstName', 'LastName', 'Position', 'PositionGroup', 'OverallRating', 'YearsPro', 'ContractStatus']
].reset_index(drop=True)

# Export
output_filename = 'Files/Madden26/IE/Season2/WaiverClaims.xlsx'
with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
    waiver_sim_df.to_excel(writer, sheet_name='WaiverSim', index=False)
    waiver_targets_df.to_excel(writer, sheet_name='WaiverTargets', index=False)

print(f"Exported to {output_filename}")