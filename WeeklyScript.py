# Imports
import pandas as pd
import random

# Your File Path
file_path = 'Files/Madden26/IE/Season2/Player.xlsx'
coach_file_path = 'Files/Madden26/IE/Season2/CoachInfo.xlsx'

df = pd.read_excel(file_path)
coach_df = pd.read_excel(coach_file_path)

# Team Index Dictionary
team_dict = {0: 'CHI', 1: 'CIN', 2: 'BUF', 3: 'DEN', 4: 'CLE', 5: 'TB', 6: 'ARI', 7: 'LAC', 8: 'KC', 9: 'IND',
             10: 'DAL', 11: 'MIA', 12: 'PHI', 13: 'ATL', 14: 'SF', 15: 'NYG', 16: 'JAX', 17: 'NYJ', 18: 'DET',
             19: 'GB', 20: 'CAR', 21: 'NE', 22: 'LV', 23: 'LAR', 24: 'BAL', 25: 'WAS', 26: 'NO', 27: 'SEA',
             28: 'PIT', 29: 'TEN', 30: 'MIN', 31: 'HOU', 32: 'FA'}

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

    if row['ContractStatus'] in ['Signed', 'FreeAgent', 'PracticeSquad'] and row['InjuryStatus'] == 'Injured':

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

# Track the original DataFrame before applying updates
original_df = df.copy()

# Apply the update_injuries function to the DataFrame
df = df.apply(update_injuries, axis=1)
df = df.apply(update_def_tier_simstat, axis=1)

# Identify columns with no changes
columns_to_remove = [
    column for column in df.columns if df[column].equals(original_df[column])
]

# Drop columns with no edits
df.drop(columns=columns_to_remove, inplace=True)

# Save the updated DataFrame to Excel
output_filename = 'Files/Madden26/IE/Season2/Player_InjuryChanges.xlsx'
df.to_excel(output_filename, index=False)

print(df.dtypes)