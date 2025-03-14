# Imports
import pandas as pd

# Your File Path
file_path = 'Files/Madden25/IE/Season8/Player.xlsx'

df = pd.read_excel(file_path)

def update_position_ratings(row):
    # Check the player's position and apply changes to specific columns
    contract_status = row['ContractStatus']
    
    if contract_status in ['Draft']:
        # Change Edited Position Here
        if row['Position'] in ['CB'] and row['OverallRating'] >= 64:
            row['AwarenessRating'] -= 1
            row['PlayRecognitionRating'] -= 1
            row['TackleRating'] -= 1
            row['PursuitRating'] -= 1
            row['PressRating'] -= 1
            row['ZoneCoverageRating'] -= 2
            row['ManCoverageRating'] -= 2
    # Add more conditions and changes for other columns and positions as needed
    return row

# Track the original DataFrame before applying updates
original_df = df.copy()

# Apply the new function to update the DataFrame
df = df.apply(update_position_ratings, axis=1)

columns_to_remove = []

for column in df.columns:
    # Check if the column values are equal, considering data type differences
    if df[column].equals(original_df[column]):
        columns_to_remove.append(column)

# Drop columns with no edits
df.drop(columns=columns_to_remove, inplace=True)

output_filename = 'DraftClassPositionEdits.xlsx'
df.to_excel('Files/Madden25/IE/Season8/DraftClassPositionEdits.xlsx', index=False)