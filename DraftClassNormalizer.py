# Imports
import pandas as pd
import random
import numpy as np

# Your File Path
file_path = 'Files/Madden25/IE/Season9/Player.xlsx'

df = pd.read_excel(file_path)

def update_ratings(row):
    # Check the player's position and apply changes to specific columns
    contract_status = row['ContractStatus']
    
    if contract_status in ['Draft']:

        # QB Edits
        if row['Position'] == 'QB':
            row['ThrowAccuracyDeepRating'] = max(0, min(row['ThrowAccuracyDeepRating'] + random.randint(-6, 5), 99))
            row['ThrowAccuracyMidRating'] = max(0, min(row['ThrowAccuracyMidRating'] + random.randint(-6, 5), 99))
            row['ThrowAccuracyShortRating'] = max(0, min(row['ThrowAccuracyShortRating'] + random.randint(-5, 5), 99))
            row['ThrowPowerRating'] = max(0, min(row['ThrowPowerRating'] + random.randint(-6, 5), 99))
            row['ThrowOnTheRunRating'] = max(0, min(row['ThrowOnTheRunRating'] + random.randint(-5, 5), 99))
            row['ThrowUnderPressureRating'] = max(0, min(row['ThrowUnderPressureRating'] + random.randint(-5, 5), 99))

        # HB Edits
        if row['Position'] == 'HB':
            row['AgilityRating'] = max(0, min(row['AgilityRating'] + random.randint(-1, 2), 99))
            row['AccelerationRating'] = max(0, min(row['AccelerationRating'] + random.randint(-2, 1), 99))
            row['CarryingRating'] = max(0, min(row['CarryingRating'] + random.randint(-4, 3), 99))
            row['BreakTackleRating'] = max(0, min(row['BreakTackleRating'] + random.randint(-4, 3), 99))
            row['ChangeOfDirectionRating'] = max(0, min(row['ChangeOfDirectionRating'] + random.randint(-3, 4), 99))
            row['CatchingRating'] = max(0, min(row['CatchingRating'] + random.randint(-4, 3), 99))
            row['DeepRouteRunningRating'] = max(0, min(row['DeepRouteRunningRating'] + random.randint(-3, 4), 99))
            row['JukeMoveRating'] = max(0, min(row['JukeMoveRating'] + random.randint(-3, 3), 99))
            row['MediumRouteRunningRating'] = max(0, min(row['MediumRouteRunningRating'] + random.randint(-3, 3), 99))
            row['SpinMoveRating'] = max(0, min(row['SpinMoveRating'] + random.randint(-3, 4), 99))
            row['ShortRouteRunningRating'] = max(0, min(row['ShortRouteRunningRating'] + random.randint(-3, 3), 99))
            row['SpeedRating'] = max(0, min(row['SpeedRating'] + random.randint(-1, 1), 99))
            row['StiffArmRating'] = max(0, min(row['StiffArmRating'] + random.randint(-4, 3), 99))
            row['ReleaseRating'] = max(0, min(row['ReleaseRating'] + random.randint(1, 4), 99))

    # Add more conditions and changes for other columns and positions as needed
    return row

# Track the original DataFrame before applying updates
original_df = df.copy()

# Apply the new function to update the DataFrame
df = df.apply(update_ratings, axis=1)

###
columns_to_remove = []

for column in df.columns:
    # Check if the column values are equal, considering data type differences
    if df[column].equals(original_df[column]):
        columns_to_remove.append(column)

# Drop columns with no edits
df.drop(columns=columns_to_remove, inplace=True)
###

output_filename = 'Player_DraftClassNormalized.xlsx'
df.to_excel('Files/Madden25/IE/Season9/Player_DraftClassNormalized.xlsx', index=False)