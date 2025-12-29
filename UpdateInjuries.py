# Imports
import pandas as pd
import random

# Your File Path
file_path = 'Files/Madden25/IE/Season10/Player.xlsx'

df = pd.read_excel(file_path)

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

# Function to update injuries
def update_injuries(row):

    # Check if the player meets the criteria to reset injury duration
    if (row['ContractStatus'] in ['Signed', 'FreeAgent', 'PracticeSquad'] and
        row['InjuryStatus'] == 'Uninjured' and
        row['IsInjuredReserve'] == True and 
        row['MinInjuryDuration'] >= 55 and 
        row['MaxInjuryDuration'] >= 55):
        row['MinInjuryDuration'] = 0
        row['MaxInjuryDuration'] = 0
        row['InjuryType'] = 'Invalid_'

    if row['ContractStatus'] in ['Signed', 'FreeAgent', 'PracticeSquad'] and row['InjuryStatus'] == 'Injured':
            
        if 85 <= row['InjuryRating'] <= 99:
            # InjuryRating between 85-99 (higher chance to subtract)
            if 2 <= row['MaxInjuryDuration'] <= 4:
                row = adjust_durations(row, [10, 85, 5])
            elif row['MaxInjuryDuration'] >= 5:
                row = adjust_durations(row, [12, 80, 8])
            elif row['MaxInjuryDuration'] == 1:
                row = adjust_durations(row, [0, 97, 3])

        elif 80 <= row['InjuryRating'] <= 84:
            
            if 2 <= row['MaxInjuryDuration'] <= 4:
                row = adjust_durations(row, [8, 85, 7])
            elif row['MaxInjuryDuration'] >= 5:
                row = adjust_durations(row, [11, 80, 9])
            elif row['MaxInjuryDuration'] == 1:
                row = adjust_durations(row, [0, 95, 5])

        elif 75 <= row['InjuryRating'] <= 79:
            
            if 2 <= row['MaxInjuryDuration'] <= 4:
                row = adjust_durations(row, [7, 85, 8])
            elif row['MaxInjuryDuration'] >= 5:
                row = adjust_durations(row, [9, 80, 11])
            elif row['MaxInjuryDuration'] == 1:
                row = adjust_durations(row, [0, 93, 7])

        elif 1 <= row['InjuryRating'] <= 74:
            # InjuryRating between 1-74 (lower chance to subtract)
            if 2 <= row['MaxInjuryDuration'] <= 4:
                row = adjust_durations(row, [5, 85, 10])
            elif row['MaxInjuryDuration'] >= 5:
                row = adjust_durations(row, [8, 80, 12])
            elif row['MaxInjuryDuration'] == 1:
                row = adjust_durations(row, [0, 91, 9])

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
output_filename = 'Files/Madden25/IE/Season10/Player_InjuryChanges.xlsx'
df.to_excel(output_filename, index=False)

print(df.dtypes)