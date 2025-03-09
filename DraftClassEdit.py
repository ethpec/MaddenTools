# Imports
import pandas as pd
import random

# Your File Path
file_path = 'Files/Madden25/IE/Season8/Player.xlsx'

df = pd.read_excel(file_path)

def update_traits(row):
    # Check the player's position and apply changes to specific columns
    contract_status = row['ContractStatus']
    
    if contract_status in ['Draft']:
        if row['Position'] not in ['K', 'P']:
            row['AwarenessRating'] = row['OverallRating']

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
            row['TRAIT_THROWAWAY'] = 'TRUE'
            row['TRAIT_COVER_BALL'] = 'ForAllHits'
            if row['SpeedRating'] <= 76:
                row['TRAIT_QBSTYLE'] = 'Pocket'
            if 77 <= row['SpeedRating'] <= 79:
                qbstyle_value = random.choice(['Pocket', 'Balanced'])
                row['TRAIT_TUCK_RUN'] = qbstyle_value
            if 80 <= row['SpeedRating'] <= 82:
                row['TRAIT_QBSTYLE'] = 'Balanced'
            if 83 <= row['SpeedRating'] <= 84:
                qbstyle_value = random.choice(['Scrambling', 'Balanced'])
                row['TRAIT_TUCK_RUN'] = qbstyle_value
            if row['SpeedRating'] >= 85:
                row['TRAIT_QBSTYLE'] = 'Scrambling'
            if row['SpeedRating'] >= 90:
                row['TRAIT_TUCK_RUN'] = '2'
            if 85 <= row['SpeedRating'] <= 89:
                tuck_run_value = random.choice(['1', '2'])
                row['TRAIT_TUCK_RUN'] = tuck_run_value
            if 80 <= row['SpeedRating'] <= 84:
                tuck_run_value = random.choice(['0', '1', '2'])
                row['TRAIT_TUCK_RUN'] = tuck_run_value
            if 77 <= row['SpeedRating'] <= 79:
                tuck_run_value = random.choice(['0', '1'])
                row['TRAIT_TUCK_RUN'] = tuck_run_value
            if row['SpeedRating'] <= 76:
                row['TRAIT_TUCK_RUN'] = '0'
            if 'Conservative' in row['TRAIT_DECISION_MAKER']:
                qbforcepass_value = random.choice(['Ideal', 'Conservative'])
                row['TRAIT_DECISION_MAKER'] = qbforcepass_value
            if row['OverallRating'] <= 60:
                row['AwarenessRating'] = min(row['AwarenessRating'] + 1, 99)
                row['ShortAccuracyRating'] = min(row['ShortAccuracyRating'] + 1, 99)
                row['MediumAccuracyRating'] = min(row['MediumAccuracyRating'] + 1, 99)
                row['DeepAccuracyRating'] = min(row['DeepAccuracyRating'] + 1, 99)

                
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
            if row['OverallRating'] <= 60:
                row['AwarenessRating'] = min(row['AwarenessRating'] + 1, 99)
                row['BCVisionRating'] = min(row['BCVisionRating'] + 1, 99)
                row['BreakTackleRating'] = min(row['BreakTackleRating'] + 1, 99)
                row['CarryingRating'] = min(row['CarryingRating'] + 1, 99)


        # OFF Edits
        if row['Position'] in ['WR', 'TE']:
            row['TRAIT_YACCATCH'] = 'TRUE'
            row['TRAIT_POSSESSIONCATCH'] = 'TRUE'
            row['TRAIT_HIGHPOINTCATCH'] = 'TRUE'
            if row['OverallRating'] <= 60:
                row['AwarenessRating'] = min(row['AwarenessRating'] + 1, 99)
                row['CatchingRating'] = min(row['CatchingRating'] + 1, 99)
                row['ShortRouteRunningRating'] = min(row['ShortRouteRunningRating'] + 1, 99)
                row['MediumRouteRunningRating'] = min(row['MediumRouteRunningRating'] + 1, 99)
                row['DeepRouteRunningRating'] = min(row['DeepRouteRunningRating'] + 1, 99)
            if row['KickReturnRating'] >= 90:
                row['BCVisionRating'] = min(99, max(row['BCVisionRating'] + 2, 68))
                row['JukeMoveRating'] = min(99, max(row['JukeMoveRating'] + 3, 72))
                row['SpinMoveRating'] = min(99, max(row['SpinMoveRating'] + 3, 70))
                row['CarryingRating'] = min(99, max(row['CarryingRating'] + 3, 65))
                row['BreakTackleRating'] = min(99, max(row['BreakTackleRating'] + 2, 60))


        # DEF Front Edits
        if row['Position'] in ['LE', 'RE', 'DT']:
            row['TRAIT_DLSWIM'] = 'TRUE'
            row['TRAIT_DLSPIN'] = 'TRUE'
            row['TRAIT_DLBULLRUSH'] = 'TRUE'
            if row['OverallRating'] <= 60:
                row['AwarenessRating'] = min(row['AwarenessRating'] + 1, 99)
                row['FinesseMovesRating'] = min(row['FinesseMovesRating'] + 1, 99)
                row['PowerMovesRating'] = min(row['PowerMovesRating'] + 1, 99)
                row['PursuitRating'] = min(row['PursuitRating'] + 1, 99)
                row['TackleRating'] = min(row['TackleRating'] + 1, 99)
                row['BlockSheddingRating'] = min(row['BlockSheddingRating'] + 1, 99)


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

            if row['ManCoverageRating'] >= 50:
                row['ManCoverageRating'] = min(99, 50 + random.randint(0, 5))

            if row['ZoneCoverageRating'] >= 50:
                row['ZoneCoverageRating'] = min(99, 50 + random.randint(0, 5))

            if row['ManCoverageRating'] < 50:
                row['ManCoverageRating'] = 50 + random.randint(0, 10)

            if row['ZoneCoverageRating'] < 50:
                row['ZoneCoverageRating'] = 50 + random.randint(0, 10)

            if row['SpeedRating'] <= 90:
                row['SpeedRating'] += 2

            if row['OverallRating'] <= 60:
                row['AwarenessRating'] = min(row['AwarenessRating'] + 1, 99)
                row['PlayRecognitionRating'] = min(row['PlayRecognitionRating'] + 1, 99)
                row['HitPowerRating'] = min(row['HitPowerRating'] + 1, 99)
                row['PursuitRating'] = min(row['PursuitRating'] + 1, 99)
                row['TackleRating'] = min(row['TackleRating'] + 1, 99)
                row['BlockSheddingRating'] = min(row['BlockSheddingRating'] + 1, 99)


        # OLB Edits
        if row['Position'] in ['MLB']:
            if row['SpeedRating'] <= 90:
                row['SpeedRating'] += 1

            if row['ManCoverageRating'] >= 50:
                row['ManCoverageRating'] = min(99, 50 + random.randint(0, 5))

            if row['ZoneCoverageRating'] >= 50:
                row['ZoneCoverageRating'] = min(99, 50 + random.randint(0, 5))

            if row['ManCoverageRating'] < 50:
                row['ManCoverageRating'] = 50 + random.randint(0, 10)

            if row['ZoneCoverageRating'] < 50:
                row['ZoneCoverageRating'] = 50 + random.randint(0, 10)
            
            if row['OverallRating'] <= 60:
                row['AwarenessRating'] = min(row['AwarenessRating'] + 1, 99)
                row['PlayRecognitionRating'] = min(row['PlayRecognitionRating'] + 1, 99)
                row['HitPowerRating'] = min(row['HitPowerRating'] + 1, 99)
                row['PursuitRating'] = min(row['PursuitRating'] + 1, 99)
                row['TackleRating'] = min(row['TackleRating'] + 1, 99)
                row['BlockSheddingRating'] = min(row['BlockSheddingRating'] + 1, 99)

        # CB Edits
        if row['Position'] in ['CB']:
            if row['OverallRating'] <= 60:
                row['AwarenessRating'] = min(row['AwarenessRating'] + 1, 99)
                row['PlayRecognitionRating'] = min(row['PlayRecognitionRating'] + 1, 99)
                row['ZoneCoverageRating'] = min(row['ZoneCoverageRating'] + 1, 99)
                row['ManCoverageRating'] = min(row['ManCoverageRating'] + 1, 99)
                row['PressRating'] = min(row['PressRating'] + 1, 99)
            if row['KickReturnRating'] >= 90:
                row['BCVisionRating'] = min(99, max(row['BCVisionRating'] + 5, 68))
                row['JukeMoveRating'] = min(99, max(row['JukeMoveRating'] + 5, 72))
                row['SpinMoveRating'] = min(99, max(row['SpinMoveRating'] + 5, 70))
                row['CarryingRating'] = min(99, max(row['CarryingRating'] + 5, 64))
                row['BreakTackleRating'] = min(99, max(row['BreakTackleRating'] + 10, 60))

        # S Edits
        if row['Position'] in ['FS', 'SS']:
            if row['OverallRating'] <= 60:
                row['AwarenessRating'] = min(row['AwarenessRating'] + 1, 99)
                row['PlayRecognitionRating'] = min(row['PlayRecognitionRating'] + 1, 99)
                row['ZoneCoverageRating'] = min(row['ZoneCoverageRating'] + 1, 99)
                row['PursuitRating'] = min(row['PursuitRating'] + 1, 99)
                row['TackleRating'] = min(row['TackleRating'] + 1, 99)
                row['ManCoverageRating'] = min(row['ManCoverageRating'] + 1, 99)
            if row['KickReturnRating'] >= 90:
                row['BCVisionRating'] = min(99, max(row['BCVisionRating'] + 5, 68))
                row['JukeMoveRating'] = min(99, max(row['JukeMoveRating'] + 5, 72))
                row['SpinMoveRating'] = min(99, max(row['SpinMoveRating'] + 5, 70))
                row['CarryingRating'] = min(99, max(row['CarryingRating'] + 5, 64))
                row['BreakTackleRating'] = min(99, max(row['BreakTackleRating'] + 10, 60))

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

    # Default value if no conditions are met
    return 0

# Track the original DataFrame before applying updates
original_df = df.copy()

# Apply the new function to update the DataFrame
df = df.apply(update_traits, axis=1)
df['PLYR_SLEEVETEMPERATURE'] = df.apply(lambda row: update_sleevetemp(row), axis=1)

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
df.to_excel('Files/Madden25/IE/Season8/DraftClassEdit.xlsx', index=False)