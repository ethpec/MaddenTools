# Imports
import pandas as pd
import random

# Your File Path
file_path = 'Files/Madden26/IE/Season1/Player.xlsx'

df = pd.read_excel(file_path)

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

# Track the original DataFrame before applying updates
original_df = df.copy()

# Apply the update_injuries function to the DataFrame
df = df.apply(update_injuries, axis=1)

# Identify columns with no changes
columns_to_remove = [
    column for column in df.columns if df[column].equals(original_df[column])
]

# Drop columns with no edits
df.drop(columns=columns_to_remove, inplace=True)

# Save the updated DataFrame to Excel
output_filename = 'Files/Madden26/IE/Season1/Player_InjuryChanges.xlsx'
df.to_excel(output_filename, index=False)

print(df.dtypes)