# Imports
import pandas as pd
import random

# Your File Path
file_path = 'Files/Madden24/IE/Test/Player.xlsx'

df = pd.read_excel(file_path)

def update_traits(row):
    # Check the player's position and apply changes to specific columns
    contract_status = row['ContractStatus']
    
    if contract_status in ['FreeAgent', 'Signed', 'PracticeSquad']:

        # QB Edits
        if row['Position'] == 'QB':
            row['TRAIT_THROWAWAY'] = 'TRUE'  # Change Trait_ThrowAway column for QBs to 'TRUE'
            row['TRAIT_COVER_BALL'] = 'ForAllHits'
            if 'Pocket' in row['TRAIT_QBSTYLE']:
                row['TRAIT_QBSTYLE'] = 'Balanced'
            if row['SpeedRating'] < 80:
                row['TRAIT_QBSTYLE'] = 'Balanced'
            elif row['SpeedRating'] >= 85:
                row['TRAIT_QBSTYLE'] = 'Scrambler'
            if row['InjuryRating'] < 70:
                row['InjuryRating'] = 70

        # HB Edits
        elif row['Position'] == 'HB':
            # For HBs, set a minimum of 73 and a maximum of 85 for InjuryRating
            new_injury_rating = row['InjuryRating']
            # Ensure the new value is within the specified range
            if new_injury_rating < 73:
                new_injury_rating = 73
            elif new_injury_rating > 85:
                new_injury_rating = 85
            row['InjuryRating'] = new_injury_rating
            row['TRAIT_YACCATCH'] = 'TRUE'
            row['TRAIT_POSSESSIONCATCH'] = 'TRUE'
            row['TRAIT_HIGHPOINTCATCH'] = 'TRUE'

        # OFF Edits
        elif row['Position'] in ['WR', 'TE']:
            row['TRAIT_YACCATCH'] = 'TRUE'
            row['TRAIT_POSSESSIONCATCH'] = 'TRUE'
            row['TRAIT_HIGHPOINTCATCH'] = 'TRUE'

        # DEF Edits
        elif row['Position'] in ['LE', 'RE', 'DT']:
            row['TRAIT_DLSWIM'] = 'TRUE'
            row['TRAIT_DLSPIN'] = 'TRUE'
            row['TRAIT_DLBULLRUSH'] = 'TRUE'

        else:
            # For all other positions, set a minimum of 68 and a maximum of 80 for InjuryRating
            new_injury_rating = row['InjuryRating']
            # Ensure the new value is within the specified range
            if new_injury_rating < 68:
                new_injury_rating = 68
            elif new_injury_rating > 80:
                new_injury_rating = 80
            row['InjuryRating'] = new_injury_rating

    # Add more conditions and changes for other columns and positions as needed
    return row

# Apply the new function to update the DataFrame
df = df.apply(update_traits, axis=1)

output_filename = 'Player_PreseasonEdits.xlsx'
df.to_excel('Files/Madden24/IE/Test/Player_PreseasonEdits.xlsx', index=False)