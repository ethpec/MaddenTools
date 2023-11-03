# Imports
import pandas as pd
import random

# Your File Path
file_path = 'Files/Madden24/IE/Test/Player.xlsx'

df = pd.read_excel(file_path)

def update_traits(row):
    # Check the player's position and apply changes to specific columns
    contract_status = row['ContractStatus']
    
    if contract_status in ['Draft']:

        # QB Edits
        if row['Position'] == 'QB':
            # For QBs, set a minimum of 70 and a maximum of 80 for InjuryRating
            new_injury_rating = row['InjuryRating'] - 15
            # Ensure the new value is within the specified range
            if new_injury_rating < 70:
                new_injury_rating = 70
            if new_injury_rating > 80:
                new_injury_rating = 80
            row['InjuryRating'] = new_injury_rating
            row['TRAIT_THROWAWAY'] = 'TRUE'  # Change Trait_ThrowAway column for QBs to 'TRUE'
            row['TRAIT_COVER_BALL'] = 'ForAllHits'
            if 'Pocket' in row['TRAIT_QBSTYLE']:
                row['TRAIT_QBSTYLE'] = 'Balanced'
            if row['SpeedRating'] < 80:
                row['TRAIT_QBSTYLE'] = 'Balanced'
            if row['SpeedRating'] >= 87:
                row['TRAIT_QBSTYLE'] = 'Scrambling'

        # HB Edits
        if row['Position'] == 'HB':
            # For HBs, set a minimum of 73 and a maximum of 85 for InjuryRating
            new_injury_rating = row['InjuryRating'] - 11
            # Ensure the new value is within the specified range
            if new_injury_rating < 73:
                new_injury_rating = 73
            if new_injury_rating > 85:
                new_injury_rating = 85
            row['InjuryRating'] = new_injury_rating
            row['TRAIT_YACCATCH'] = 'TRUE'
            row['TRAIT_POSSESSIONCATCH'] = 'TRUE'
            row['TRAIT_HIGHPOINTCATCH'] = 'TRUE'

        # OFF Edits
        if row['Position'] in ['WR', 'TE']:
            row['TRAIT_YACCATCH'] = 'TRUE'
            row['TRAIT_POSSESSIONCATCH'] = 'TRUE'
            row['TRAIT_HIGHPOINTCATCH'] = 'TRUE'

        # DEF Front Edits
        if row['Position'] in ['LE', 'RE', 'DT']:
            row['TRAIT_DLSWIM'] = 'TRUE'
            row['TRAIT_DLSPIN'] = 'TRUE'
            row['TRAIT_DLBULLRUSH'] = 'TRUE'

        # OLB Edits
        if row['Position'] in ['LOLB', 'ROLB']:
            if 'PassRush' in row['TRAIT_LBSTYLE']:
                row['TRAIT_LBSTYLE'] = 'Balanced'

            if row['FinesseMovesRating'] >= 70:
                row['FinesseMovesRating'] -= 10

            elif 55 <= row['FinesseMovesRating'] <= 69:
                row['FinesseMovesRating'] -= 7

            if row['PowerMovesRating'] >= 70:
                row['PowerMovesRating'] -= 12

            elif 55 <= row['PowerMovesRating'] <= 69:
                row['PowerMovesRating'] -= 8

            if row['ManCoverageRating'] < 45:
                row['ManCoverageRating'] = 45

            if row['ZoneCoverageRating'] < 45:
                row['ZoneCoverageRating'] = 45

        # For all other positions, set a minimum of 68 and a maximum of 80 for InjuryRating
        if row['Position'] not in ['HB', 'QB']:

            new_injury_rating = row['InjuryRating'] - 16
            # Ensure the new value is within the specified range
            if new_injury_rating < 68:
                new_injury_rating = 68
            if new_injury_rating > 80:
                new_injury_rating = 80
            row['InjuryRating'] = new_injury_rating

        # Set TraitDevelopment to "Normal" for all positions
        row['TraitDevelopment'] = 'Normal'

    # Add more conditions and changes for other columns and positions as needed
    return row

# Track the original DataFrame before applying updates
original_df = df.copy()

# Apply the new function to update the DataFrame
df = df.apply(update_traits, axis=1)

###
columns_to_remove = []

for column in df.columns:
    # Check if the column values are equal, considering data type differences
    if df[column].equals(original_df[column]):
        columns_to_remove.append(column)

# Drop columns with no edits
df.drop(columns=columns_to_remove, inplace=True)
###

output_filename = 'DraftClassEdit.xlsx'
df.to_excel('Files/Madden24/IE/Test/DraftClassEdit.xlsx', index=False)