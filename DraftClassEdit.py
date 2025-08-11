# Imports
import pandas as pd
import random
import numpy as np

# Your File Path
file_path = 'Files/Madden25/IE/Season10/Player.xlsx'

df = pd.read_excel(file_path)

def update_traits(row):
    # Check the player's position and apply changes to specific columns
    contract_status = row['ContractStatus']
    
    if contract_status in ['Draft']:
        # Non-Specialists
        if row['Position'] not in ['K', 'P']:
            row['AwarenessRating'] = row['OverallRating']
            row['KickPowerRating'] = max(row['KickPowerRating'] - 5, 15)
            row['KickAccuracyRating'] = max(row['KickPowerRating'] - 10, 10)

        # Non-LongSnappers
        if row['Position'] not in ['LS']:
            row['LongSnapRating'] = 10

        # Kick-Returning
        if row['Position'] not in ['X']:
            row['KickReturnRating'] = max(row['KickReturnRating'] - 5, 5)

        # Non-QBs
        if row['Position'] not in ['QB']:
            row['ThrowPowerRating'] = min(row['ThrowPowerRating'] + 5, 90)

        if row['Position'] in ['WR', 'TE']:
            # List of tuples: (ThrowPower, ThrowUnderPressure, ThrowOnTheRun, ThrowAccuracy, ThrowAccuracyShort, ThrowAccuracyMedium, ThrowAccuracyDeep, chance)
            throw_rating_changes = [
                (65, 50, 55, 60, 65, 60, 55, 0.005),   # 0.5% chance to set these values
                (75, 55, 60, 65, 70, 65, 60, 0.003),
                (80, 60, 70, 70, 75, 70, 65, 0.002),
            ]

            for power, under_pressure, on_run, accuracy, acc_short, acc_med, acc_deep, chance in throw_rating_changes:
                if random.random() <= chance:
                    row['ThrowPowerRating'] = power
                    row['ThrowUnderPressureRating'] = under_pressure
                    row['ThrowOnTheRunRating'] = on_run
                    row['ThrowAccuracyRating'] = accuracy
                    row['ThrowAccuracyShortRating'] = acc_short
                    row['ThrowAccuracyMediumRating'] = acc_med
                    row['ThrowAccuracyDeepRating'] = acc_deep
                    break

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
                row['ThrowAccuracyShortRating'] = min(row['ThrowAccuracyShortRating'] + 1, 99)
                row['ThrowAccuracyMidRating'] = min(row['ThrowAccuracyMidRating'] + 1, 99)
                row['ThrowAccuracyDeepRating'] = min(row['ThrowAccuracyDeepRating'] + 1, 99)
                
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
                row['BCVisionRating'] = min(98, max(row['BCVisionRating'] + 2, 68))
                row['JukeMoveRating'] = min(98, max(row['JukeMoveRating'] + 3, 72))
                row['SpinMoveRating'] = min(98, max(row['SpinMoveRating'] + 3, 70))
                row['CarryingRating'] = min(98, max(row['CarryingRating'] + 3, 65))
                row['BreakTackleRating'] = min(98, max(row['BreakTackleRating'] + 2, 60))

            long_snap_te_chances = [
                (20, 0.005),
                (30, 0.005),
                (40, 0.005),
                (50, 0.005),
                (60, 0.005),
            ]

            if row['Position'] == 'TE':
                for value, chance in long_snap_te_chances:
                    if random.random() <= chance:
                        row['LongSnapRating'] = value
                        break

        # OL LS Edits
        if row['Position'] in ['LT', 'LG', 'C', 'RG', 'RT']:
            long_snap_ol_chances = [
                (20, 0.003),
                (30, 0.002),
                (40, 0.001),
                (50, 0.001),
                (60, 0.001),
            ]
            for value, chance in long_snap_ol_chances:
                if random.random() <= chance:
                    row['LongSnapRating'] = value
                    break

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

            if row['ManCoverageRating'] < 50:
                row['ManCoverageRating'] = 48 + random.randint(0, 5)

            if row['ZoneCoverageRating'] < 50:
                row['ZoneCoverageRating'] = 48 + random.randint(0, 5)

            if row['OverallRating'] <= 60:
                row['AwarenessRating'] = min(row['AwarenessRating'] + 1, 99)
                row['PlayRecognitionRating'] = min(row['PlayRecognitionRating'] + 1, 99)
                row['HitPowerRating'] = min(row['HitPowerRating'] + 1, 99)
                row['PursuitRating'] = min(row['PursuitRating'] + 1, 99)
                row['TackleRating'] = min(row['TackleRating'] + 1, 99)
                row['BlockSheddingRating'] = min(row['BlockSheddingRating'] + 1, 99)

        # MLB Edits
        if row['Position'] in ['MLB']:
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

            if row['ManCoverageRating'] < 50:
                row['ManCoverageRating'] = 48 + random.randint(0, 5)

            if row['ZoneCoverageRating'] < 50:
                row['ZoneCoverageRating'] = 48 + random.randint(0, 5)
            
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
                row['BCVisionRating'] = min(99, max(row['BCVisionRating'] + 6, 68))
                row['JukeMoveRating'] = min(99, max(row['JukeMoveRating'] + 6, 72))
                row['SpinMoveRating'] = min(99, max(row['SpinMoveRating'] + 6, 70))
                row['CarryingRating'] = min(99, max(row['CarryingRating'] + 6, 65))
                row['BreakTackleRating'] = min(99, max(row['BreakTackleRating'] + 20, 60))
            if 89 >= row['KickReturnRating'] >= 85:
                row['BCVisionRating'] = min(99, max(row['BCVisionRating'] + 3, 65))
                row['JukeMoveRating'] = min(99, max(row['JukeMoveRating'] + 3, 70))
                row['SpinMoveRating'] = min(99, max(row['SpinMoveRating'] + 3, 68))
                row['CarryingRating'] = min(99, max(row['CarryingRating'] + 3, 62))
                row['BreakTackleRating'] = min(99, max(row['BreakTackleRating'] + 15, 55))

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
                row['BCVisionRating'] = min(99, max(row['BCVisionRating'] + 6, 68))
                row['JukeMoveRating'] = min(99, max(row['JukeMoveRating'] + 6, 72))
                row['SpinMoveRating'] = min(99, max(row['SpinMoveRating'] + 6, 70))
                row['CarryingRating'] = min(99, max(row['CarryingRating'] + 6, 65))
                row['BreakTackleRating'] = min(99, max(row['BreakTackleRating'] + 20, 60))
            if 89 >= row['KickReturnRating'] >= 85:
                row['BCVisionRating'] = min(99, max(row['BCVisionRating'] + 3, 65))
                row['JukeMoveRating'] = min(99, max(row['JukeMoveRating'] + 3, 70))
                row['SpinMoveRating'] = min(99, max(row['SpinMoveRating'] + 3, 68))
                row['CarryingRating'] = min(99, max(row['CarryingRating'] + 3, 62))
                row['BreakTackleRating'] = min(99, max(row['BreakTackleRating'] + 15, 55))

        # Non-Kicker/Punter Kicking Edits
        if row['Position'] in ['WR', 'SS', 'FS']:
            # Example list of tuples: (KickAccuracyRating value, KickPowerRating value, chance)
            kick_rating_changes = [
                (50, 55, 0.002),  # 0.2% chance to set Accuracy=50 and Power=55
                (55, 65, 0.001),
                (60, 75, 0.001),
                (65, 85, 0.001),
            ]

            for acc_value, power_value, chance in kick_rating_changes:
                if random.random() <= chance:
                    row['KickAccuracyRating'] = acc_value
                    row['KickPowerRating'] = power_value
                    break

        # WR Coverage Edits
        if row['Position'] in ['WR'] and row['Height'] <= 74:
            # Example list of tuples: (ManCoverageRating value, ZoneCoverageRating value, PressRating value, chance)
            wr_cover_changes = [
                (50, 50, 50, 0.003),  # 0.3% chance to set Man=50 and Zone=55
                (55, 60, 50, 0.003),
                (60, 55, 55, 0.003),
                (60, 65, 55, 0.003),
                (65, 60, 60, 0.003),
                (65, 70, 60, 0.002),
                (70, 65, 65, 0.002),
                (75, 75, 70, 0.001),
            ]

            for mancov_value, zonecove_value, presscov_value, chance in wr_cover_changes:
                if random.random() <= chance:
                    row['ManCoverageRating'] = mancov_value
                    row['ZoneCoverageRating'] = zonecove_value
                    row['PressRating'] = presscov_value
                    break

        # CB Route-Running Edits
        if row['Position'] in ['CB'] and row['JukeMoveRating'] >= 75:
            # Example list of tuples: (ShortRouteRunningRating value, MediumRouteRunningRating value, DeepRouteRunningRating value, chance)
            cb_route_changes = [
                (50, 50, 50, 0.002),
                (60, 60, 60, 0.001),
                (60, 55, 50, 0.001),
                (65, 60, 55, 0.001),
                (70, 65, 60, 0.001),
                (75, 60, 60, 0.001),
                (55, 50, 60, 0.001),
                (60, 55, 65, 0.001),
                (65, 60, 70, 0.001),
            ]

            for shortroutecb_value, medroutecb_value, deeproutecb_Value , chance in cb_route_changes:
                if random.random() <= chance:
                    row['ShortRouteRunningRating'] = shortroutecb_value
                    row['MediumRouteRunningRating'] = medroutecb_value
                    row['DeepRouteRunningRating'] = deeproutecb_Value
                    break

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

def assign_home_states(row):
    if row['ContractStatus'] == 'Draft' and row['Position'] not in ['K', 'P']:
        states = [
            "Alaska", "Alabama", "Arizona", "Arkansas", "California", "CanadaAlberta",
            "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii",
            "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
            "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
            "Missouri", "Montana", "Nebraska", "Nevada", "NewHampshire", "NewJersey",
            "NewMexico", "NewYork", "NonUS", "NorthCarolina", "NorthDakota", "Ohio",
            "Oklahoma", "Oregon", "Pennsylvania", "RhodeIsland", "SouthCarolina",
            "SouthDakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia",
            "Washington", "WestVirginia", "Wisconsin", "Wyoming"
        ]

        probabilities = np.array([
            0.3, 3, 2, 2, 6.5, 0.3, 2, 1.5, 0.6, 5, 4, 0.6, 0.6, 3, 2, 2, 2, 2, 2, 0.6, 
            2, 1.5, 2, 2, 2, 2, 0.6, 1.5, 1.5, 0.6, 2, 2, 4, 0.1, 2, 1.5, 2, 2, 2, 2, 
            0.6, 2, 1.5, 2, 5, 2, 0.6, 2, 2, 2, 2, 1
        ]) / 100  # Convert to decimal probabilities

        # Randomly select a state based on the probabilities
        row['PLYR_HOME_STATE'] = np.random.choice(states, p=probabilities)
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
df = df.apply(assign_home_states, axis=1)
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
df.to_excel('Files/Madden25/IE/Season10/DraftClassEdit.xlsx', index=False)