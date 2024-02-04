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
            # For QBs, set a minimum of 73 and a maximum of 85 for InjuryRating
            new_injury_rating = row['InjuryRating'] - 10
            # Ensure the new value is within the specified range
            if new_injury_rating < 73:
                new_injury_rating = 73
            if new_injury_rating > 85:
                new_injury_rating = 85
            row['InjuryRating'] = new_injury_rating
            row['TRAIT_THROWAWAY'] = 'TRUE'  # Change Trait_ThrowAway column for QBs to 'TRUE'
            row['TRAIT_COVER_BALL'] = 'ForAllHits'
            if 'Pocket' in row['TRAIT_QBSTYLE']:
                row['TRAIT_QBSTYLE'] = 'Balanced'
            if row['SpeedRating'] < 80:
                row['TRAIT_QBSTYLE'] = 'Balanced'
            if row['SpeedRating'] >= 87:
                row['TRAIT_QBSTYLE'] = 'Scrambling'
            if row['SpeedRating'] >= 90:
                row['TRAIT_TUCK_RUN'] = '2'
            if 85 <= row['SpeedRating'] <= 89:
                tuck_run_value = random.choice(['1', '2'])
            if 80 <= row['SpeedRating'] <= 84:
                tuck_run_value = random.choice(['0', '1', '2'])
                row['TRAIT_TUCK_RUN'] = tuck_run_value
            if 77 <= row['SpeedRating'] <= 79:
                tuck_run_value = random.choice(['0', '1'])
                row['TRAIT_TUCK_RUN'] = tuck_run_value
            if row['SpeedRating'] <= 76:
                row['TRAIT_TUCK_RUN'] = '0'
            if 'Conservative' in row['TRAIT_FORCE_PASS']:
                row['TRAIT_FORCE_PASS'] = 'Ideal'

        # HB Edits
        if row['Position'] == 'HB':
            # For HBs, set a minimum of 78 and a maximum of 90 for InjuryRating
            new_injury_rating = row['InjuryRating'] - 5
            # Ensure the new value is within the specified range
            if new_injury_rating < 78:
                new_injury_rating = 78
            if new_injury_rating > 90:
                new_injury_rating = 90
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
                row['FinesseMovesRating'] -= 8

            elif 55 <= row['FinesseMovesRating'] <= 69:
                row['FinesseMovesRating'] -= 7

            if row['PowerMovesRating'] >= 70:
                row['PowerMovesRating'] -= 10

            elif 55 <= row['PowerMovesRating'] <= 69:
                row['PowerMovesRating'] -= 8

            if row['ManCoverageRating'] < 45:
                row['ManCoverageRating'] = 45

            if row['ZoneCoverageRating'] < 45:
                row['ZoneCoverageRating'] = 45

        # For all other positions, set a minimum of 73 and a maximum of 85 for InjuryRating
        if row['Position'] not in ['HB', 'QB']:

            new_injury_rating = row['InjuryRating'] - 10
            # Ensure the new value is within the specified range
            if new_injury_rating < 73:
                new_injury_rating = 73
            if new_injury_rating > 85:
                new_injury_rating = 85
            row['InjuryRating'] = new_injury_rating

        # Set TraitDevelopment to "Normal" for all positions
        row['TraitDevelopment'] = 'Normal'

    # Add more conditions and changes for other columns and positions as needed
    return row

def update_sleevetemp(row):
    # Check the player's position and apply changes to specific columns
    if row['ContractStatus'] in ['Draft']:
        # Change SleeveTemp for all players
        if row['Position'] in ['QB', 'K', 'P']:
            chances = [0, 10, 20, 30, 40, 50, 60]
            probabilities = [0.05, 0.10, 0.20, 0.30, 0.20, 0.10, 0.05] ### Average = 30 ###
            sleeve_temp = random.choices(chances, probabilities)[0]
            return sleeve_temp
        elif row['Position'] in ['RB', 'HB', 'FB']:
            chances = [0, 10, 20, 30, 40, 50, 60]
            probabilities = [0.30, 0.10, 0.25, 0.15, 0.10, 0.05, 0.05] ### Average = 20 ###
            sleeve_temp = random.choices(chances, probabilities)[0]
            return sleeve_temp
        elif row['Position'] in ['WR', 'TE', 'CB', 'FS', 'SS']:
            chances = [0, 10, 20, 30, 40, 50, 60]
            probabilities = [0.15, 0.10, 0.25, 0.25, 0.15, 0.05, 0.05] ### Average = 25 ###
            sleeve_temp = random.choices(chances, probabilities)[0]
            return sleeve_temp
        elif row['Position'] in ['LT', 'LG', 'C', 'RG', 'RT', 'LE', 'RE', 'DT']:
            chances = [0, 10, 20, 30, 40, 50, 60]
            probabilities = [0.40, 0.10, 0.20, 0.15, 0.10, 0.025, 0.025] ### Average = 16.25 ###
            sleeve_temp = random.choices(chances, probabilities)[0]
            return sleeve_temp
        elif row['Position'] in ['LOLB', 'MLB', 'ROLB']:
            chances = [0, 10, 20, 30, 40, 50, 60]
            probabilities = [0.50, 0.20, 0.05, 0.15, 0.05, 0.025, 0.025] ### Average = 12.25 ###
            sleeve_temp = random.choices(chances, probabilities)[0]
            return sleeve_temp
    return row['PLYR_SLEEVETEMPERATURE']

# Track the original DataFrame before applying updates
original_df = df.copy()

# Apply the new function to update the DataFrame
df = df.apply(update_traits, axis=1)
df['PLYR_SLEEVETEMPERATURE'] = df.apply(update_sleevetemp, axis=1)

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