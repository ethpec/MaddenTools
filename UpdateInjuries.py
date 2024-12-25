# Imports
import pandas as pd
import random

# Your File Path
file_path = 'Files/Madden25/IE/Season8/Player.xlsx'

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
    if row['ContractStatus'] in ['Signed', 'FreeAgent', 'PracticeSquad'] and row['InjuryStatus'] == 'Injured':
        
        # Check for players with Position 'HB' or 'RB'
        if row['Position'] in ['HB', 'RB']:
            # Apply logic based on InjuryRating for 'HB' and 'RB'
            if 85 <= row['InjuryRating'] <= 99:
                # InjuryRating between 85-99 (higher chance to subtract)
                if 2 <= row['MaxInjuryDuration'] <= 4:
                    row = adjust_durations(row, [7, 90, 3])
                elif row['MaxInjuryDuration'] >= 5:
                    row = adjust_durations(row, [6, 92, 2])

            elif 80 <= row['InjuryRating'] <= 84:
                # InjuryRating between 80-84
                if 2 <= row['MaxInjuryDuration'] <= 4:
                    row = adjust_durations(row, [5, 90, 5])
                elif row['MaxInjuryDuration'] >= 5:
                    row = adjust_durations(row, [4, 92, 4])

            elif 1 <= row['InjuryRating'] <= 79:
                # InjuryRating between 1-79 (lower chance to subtract)
                if 2 <= row['MaxInjuryDuration'] <= 4:
                    row = adjust_durations(row, [3, 90, 7])
                elif row['MaxInjuryDuration'] >= 5:
                    row = adjust_durations(row, [2, 92, 6])

        # Apply the same logic for other positions (non-HB/RB)
        else:
            # Apply logic based on InjuryRating for other positions
            if 80 <= row['InjuryRating'] <= 99:
                # InjuryRating between 80-99 (higher chance to subtract)
                if 2 <= row['MaxInjuryDuration'] <= 4:
                    row = adjust_durations(row, [7, 90, 3])
                elif row['MaxInjuryDuration'] >= 5:
                    row = adjust_durations(row, [6, 92, 2])

            elif 75 <= row['InjuryRating'] <= 79:
                # InjuryRating between 75-79
                if 2 <= row['MaxInjuryDuration'] <= 4:
                    row = adjust_durations(row, [5, 90, 5])
                elif row['MaxInjuryDuration'] >= 5:
                    row = adjust_durations(row, [4, 92, 4])

            elif 1 <= row['InjuryRating'] <= 74:
                # InjuryRating between 1-74 (lower chance to subtract)
                if 2 <= row['MaxInjuryDuration'] <= 4:
                    row = adjust_durations(row, [3, 90, 7])
                elif row['MaxInjuryDuration'] >= 5:
                    row = adjust_durations(row, [2, 92, 6])

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
output_filename = 'Files/Madden25/IE/Season8/Player_InjuryChanges.xlsx'
df.to_excel(output_filename, index=False)