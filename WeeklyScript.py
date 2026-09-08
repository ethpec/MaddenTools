# Imports
import pandas as pd
import random
from config import season_path

# Your File Path
file_path = season_path('Player.xlsx')
coach_schemes_file_path = season_path('CoachSchemes.xlsx') # Update at beginning of each season
coach_info_file_path = season_path('CoachInfo.xlsx')
coach_file_path = season_path('Coach.xlsx')

df = pd.read_excel(file_path)
coach_df = pd.read_excel(coach_info_file_path)

# Team Index Dictionary
team_dict = {0: 'CHI', 1: 'CIN', 2: 'BUF', 3: 'DEN', 4: 'CLE', 5: 'TB', 6: 'ARI', 7: 'LAC', 8: 'KC', 9: 'IND',
             10: 'DAL', 11: 'MIA', 12: 'PHI', 13: 'ATL', 14: 'SF', 15: 'NYG', 16: 'JAX', 17: 'NYJ', 18: 'DET',
             19: 'GB', 20: 'CAR', 21: 'NE', 22: 'LV', 23: 'LAR', 24: 'BAL', 25: 'WAS', 26: 'NO', 27: 'SEA',
             28: 'PIT', 29: 'TEN', 30: 'MIN', 31: 'HOU', 32: 'FA'}

# --- User Settings (update each week) ---
User_Team = 28          # PIT — the user's franchise team (index into team_dict)
User_Opponent_This_Week = 21  # Change this to the opponent's team index each week (e.g. 24 = BAL)
# -----------------------------------------

def get_confidence_modifier(confidence_rating):
    if confidence_rating <= 30:
        return -40
    elif confidence_rating <= 45:
        return -20
    elif confidence_rating <= 55:
        return 0
    elif confidence_rating <= 70:
        return 10
    else:
        return 20

def adjust_confidence_by_ego(row):
    if row['ContractStatus'] not in ['Signed', 'FreeAgent', 'PracticeSquad']:
        return row

    ego = row['PLYR_EGO']

    # [chance_decrease, chance_keep, chance_increase]
    if ego <= 34:
        weights = [5, 90, 5]
    elif ego <= 54:
        weights = [7, 87, 6]
    elif ego <= 74:
        weights = [9, 84, 7]
    elif ego <= 94:
        weights = [11, 81, 8]
    else:
        weights = [13, 78, 9]

    action = random.choices(['decrease', 'keep', 'increase'], weights=weights, k=1)[0]

    if action == 'decrease':
        row['ConfidenceRating'] = max(0, row['ConfidenceRating'] - random.randint(1, 5))
    elif action == 'increase':
        row['ConfidenceRating'] = min(99, row['ConfidenceRating'] + random.randint(1, 5))

    return row

# Apply the ConfidenceRating to the modification weights   
def apply_confidence_to_weights(weights, conf_mod):
    """
    weights = [decrease, no_change, increase]
    conf_mod shifts probability toward decrease (+) or increase (-)
    """
    dec, same, inc = weights

    dec = max(0, dec + conf_mod)
    inc = max(0, inc - conf_mod)

    # Normalize so total stays reasonable
    total = dec + same + inc
    if total == 0:
        return weights

    scale = sum(weights) / total
    return [dec * scale, same * scale, inc * scale]
    
# Function to adjust injury durations
def adjust_durations(row, probability_weights):
    adjustment = random.choices(
        [-1, 0, 1],
        weights=probability_weights,
        k=1
    )[0]
    row['MinInjuryDuration'] = max(0, row['MinInjuryDuration'] + adjustment)
    row['MaxInjuryDuration'] = max(0, row['MaxInjuryDuration'] + adjustment)
    row['TotalInjuryDuration'] = max(0, row['TotalInjuryDuration'] + adjustment)
    return row

def adjust_with_confidence(row, base_weights, conf_mod):
    weights = apply_confidence_to_weights(base_weights, conf_mod)
    return adjust_durations(row, weights)

team_def_tier = coach_df.set_index('TeamIndex')['DEF Tier'].to_dict()

# Function to update injuries
def update_injuries(row):

    # Check if the player meets the criteria to reset injury duration
    if row['ContractStatus'] in ['Signed', 'FreeAgent', 'PracticeSquad'] and row['InjuryStatus'] == 'Uninjured':
        #row['IsInjuredReserve'] == True and 
        #row['MinInjuryDuration'] >= 55 and 
        #row['MaxInjuryDuration'] >= 55):
        row['MinInjuryDuration'] = 0
        row['MaxInjuryDuration'] = 0
        row['TotalInjuryDuration'] = 0
        row['InjuryType'] = 'Invalid_'
        row['InjurySeverity'] = 'Invalid_'

    # Suspensions are stored as injuries with InjuryType 'DoNotUse' — leave their durations alone
    if (row['ContractStatus'] in ['Signed', 'FreeAgent', 'PracticeSquad'] and row['InjuryStatus'] == 'Injured'
            and row['InjuryType'] != 'DoNotUse'):

        conf_mod = get_confidence_modifier(row['ConfidenceRating'])

        if 85 <= row['InjuryRating'] <= 99:
            # InjuryRating between 85-99 (higher chance to subtract)
            if 2 <= row['MaxInjuryDuration'] <= 4:
                row = adjust_with_confidence(row, [10, 85, 5], conf_mod)
            elif row['MaxInjuryDuration'] >= 5:
                row = adjust_with_confidence(row, [12, 80, 8], conf_mod)
            elif row['MaxInjuryDuration'] == 1:
                row = adjust_with_confidence(row, [0, 97, 3], conf_mod)

        elif 80 <= row['InjuryRating'] <= 84:
            if 2 <= row['MaxInjuryDuration'] <= 4:
                row = adjust_with_confidence(row, [8, 85, 7], conf_mod)
            elif row['MaxInjuryDuration'] >= 5:
                row = adjust_with_confidence(row, [11, 80, 9], conf_mod)
            elif row['MaxInjuryDuration'] == 1:
                row = adjust_with_confidence(row, [0, 95, 5], conf_mod)

        elif 75 <= row['InjuryRating'] <= 79:
            if 2 <= row['MaxInjuryDuration'] <= 4:
                row = adjust_with_confidence(row, [7, 85, 8], conf_mod)
            elif row['MaxInjuryDuration'] >= 5:
                row = adjust_with_confidence(row, [9, 80, 11], conf_mod)
            elif row['MaxInjuryDuration'] == 1:
                row = adjust_with_confidence(row, [0, 93, 7], conf_mod)

        elif 1 <= row['InjuryRating'] <= 74:
            # InjuryRating between 1-74 (lower chance to subtract)
            if 2 <= row['MaxInjuryDuration'] <= 4:
                row = adjust_with_confidence(row, [5, 85, 10], conf_mod)
            elif row['MaxInjuryDuration'] >= 5:
                row = adjust_with_confidence(row, [8, 80, 12], conf_mod)
            elif row['MaxInjuryDuration'] == 1:
                row = adjust_with_confidence(row, [0, 91, 9], conf_mod)

    if row['ContractStatus'] in ['Signed', 'FreeAgent', 'PracticeSquad'] and row['InjuryStatus'] == 'Uninjured':
            
        for col in row.index:
            if 'WearAndTear' in col:
                row[col] = 10

    return row

def apply_suspensions(row):
    if row['ContractStatus'] not in ['Signed', 'FreeAgent', 'PracticeSquad']:
        return row
    if row['InjuryStatus'] != 'Uninjured':
        return row

    personality = row['PersonalityRating']

    if personality <= 60:
        suspension_chance = 0.0005  # 0.05%
    elif personality <= 89:
        suspension_chance = 0.0035  # 0.35%
    else:
        suspension_chance = 0.0065  # 0.65%

    if random.random() >= suspension_chance:
        return row

    length = random.choices(
        [1, 2, 6, 25],
        weights=[83, 10, 5, 2],
        k=1
    )[0]

    row['InjuryStatus'] = 'Injured'
    row['InjuryType'] = 'DoNotUse'
    row['InjurySeverity'] = 'CoupleGames'
    row['MinInjuryDuration'] = length
    row['MaxInjuryDuration'] = length
    row['TotalInjuryDuration'] = length

    return row

def update_def_tier_simstat(row):

    if row['ContractStatus'] in ['Signed', 'PracticeSquad'] and row['Position'] in ['LE', 'RE', 'DT', 'LOLB', 'MLB', 'ROLB', 'CB', 'FS', 'SS']:

        team_index = row['TeamIndex']

        if team_index in team_def_tier:

            tier = int(team_def_tier[team_index])

            tier_to_rating = {
                1: 90,
                2: 70,
                3: 50,
                4: 30,
                5: 10
            }

            if tier in tier_to_rating:
                row['ThrowAccuracyMidRating'] = tier_to_rating[tier]

    return row

def adjust_hb_stamina(df):
    """
    Set StaminaRating for signed HBs.

    User's team and this week's opponent get a flat 80-95 roll so their depth
    charts stay realistic. Every other team gets a sim-oriented spread based on
    how far the best healthy HB is ahead of the second-best healthy HB.
    """
    hb_mask = (df['Position'] == 'HB') & (df['ContractStatus'] == 'Signed')

    for team_index, team_hbs in df[hb_mask].groupby('TeamIndex'):

        if team_index in [User_Team, User_Opponent_This_Week]:
            for idx in team_hbs.index:
                df.at[idx, 'StaminaRating'] = random.randint(80, 95)
            continue

        healthy = team_hbs[team_hbs['InjuryStatus'] == 'Uninjured']

        # No healthy HB to build around — rank the whole group instead
        ranked = healthy if not healthy.empty else team_hbs
        ranked = ranked.sort_values('OverallRating', ascending=False)

        if len(ranked) >= 2:
            difference = ranked.iloc[0]['OverallRating'] - ranked.iloc[1]['OverallRating']
        else:
            # A lone healthy HB is the clear feature back
            difference = 10

        if difference <= 2:
            for idx in team_hbs.index:
                df.at[idx, 'StaminaRating'] = random.randint(40, 60)
            continue

        if difference >= 10:
            best_stamina = random.randint(85, 98)
        elif difference >= 6:
            best_stamina = random.randint(75, 90)
        else:
            best_stamina = random.randint(65, 80)

        best_idx = ranked.index[0]
        for idx in team_hbs.index:
            df.at[idx, 'StaminaRating'] = best_stamina if idx == best_idx else 50

    # Talented backs shouldn't be buried at the bottom of the stamina range
    low_stamina = hb_mask & (df['StaminaRating'] < 60)
    df.loc[low_stamina & (df['OverallRating'] >= 80), 'StaminaRating'] += 10
    df.loc[low_stamina & df['OverallRating'].between(75, 79), 'StaminaRating'] += 5

    return df

def update_coach_schemes():
    coach_full_df = pd.read_excel(coach_file_path)
    schemes_df = pd.read_excel(coach_schemes_file_path)

    key_cols = ['Position', 'FirstName', 'LastName', 'ContractStatus', 'TeamIndex']

    def make_key(row):
        return '_'.join(str(row[c]) for c in key_cols)

    schemes_df['_key'] = schemes_df.apply(make_key, axis=1)
    schemes_lookup = schemes_df.set_index('_key')[['DefensivePlaybook', 'DefensiveScheme']]

    original_coach_df = coach_full_df.copy()

    def apply_scheme(row):
        key = make_key(row)
        if key in schemes_lookup.index:
            row['DefensivePlaybook'] = schemes_lookup.at[key, 'DefensivePlaybook']
            row['DefensiveScheme'] = schemes_lookup.at[key, 'DefensiveScheme']
        return row

    updated_df = coach_full_df.apply(apply_scheme, axis=1)

    matched_keys = set(schemes_lookup.index)

    def apply_sim_scheme(row):
        key = make_key(row)
        if key in matched_keys and row['TeamIndex'] not in [User_Team, User_Opponent_This_Week]:
            row['DefensivePlaybook'] = '10000000000000011001100000100010'
            row['DefensiveScheme'] = '10000000000000011001100010000101'
        return row

    updated_df = updated_df.apply(apply_sim_scheme, axis=1)

    changed_cols = [col for col in updated_df.columns if not updated_df[col].equals(original_coach_df[col])]
    updated_df[changed_cols].to_excel(season_path('Coach_Updated.xlsx'), index=False)
    print(f"Coach schemes updated. Changed columns: {changed_cols}")

update_coach_schemes()

# Track the original DataFrame before applying updates
original_df = df.copy()

# Apply the update_injuries function to the DataFrame
df = df.apply(adjust_confidence_by_ego, axis=1)
df = df.apply(update_injuries, axis=1)
df = df.apply(apply_suspensions, axis=1)
df = df.apply(update_def_tier_simstat, axis=1)
df = adjust_hb_stamina(df)

# Identify columns with no changes
columns_to_remove = [
    column for column in df.columns if df[column].equals(original_df[column])
]

# Drop columns with no edits
df.drop(columns=columns_to_remove, inplace=True)

# Save the updated DataFrame to Excel
output_filename = season_path('Player_InjuryChanges.xlsx')
df.to_excel(output_filename, index=False)

print(df.dtypes)