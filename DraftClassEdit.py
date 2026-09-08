# Imports
import pandas as pd
import random
import numpy as np
from config import season_path

# Your File Path
file_path = season_path('Player.xlsx')

df = pd.read_excel(file_path)

# Set the draftclass phase
draftclass_phase = "Traits"  ### Change this to "No_Traits"" or "Traits" ###

def update_traits(row):
    # Check the player's position and apply changes to specific columns
    contract_status = row['ContractStatus']
    
    if draftclass_phase == "Traits" and contract_status in ['Draft']:
        # Assign out-of-position attributes initially (so they can be changed later)

        # Initially set all traits to FALSE
        for col in row.index:
            if col.startswith('PT_'):
                row[col] = False

        # DISCIPLINED vs UNDISCIPLINED
        if row['Position'] not in ['X']:

            if random.random() < 0.10:
                row['TRAIT_PENALTY'] = 'Undisciplined'
            if 0.10 < random.random() < 0.20:
                row['TRAIT_PENALTY'] = 'Disciplined'       

        # QB Edits
        if row['Position'] == 'QB':

            row['TRAIT_THROWAWAY'] = 'FALSE'
            row['TRAIT_COVER_BALL'] = 'ForAllHits'

            # QB attribute dependent traits    
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
                        
        # HB Edits
        if row['Position'] == 'HB':

            row['TRAIT_YACCATCH'] = 'TRUE'
            row['TRAIT_POSSESSIONCATCH'] = 'TRUE'
            row['TRAIT_HIGHPOINTCATCH'] = 'TRUE'

        # OFF Edits
        if row['Position'] in ['WR', 'TE']:

            row['TRAIT_YACCATCH'] = 'TRUE'
            row['TRAIT_POSSESSIONCATCH'] = 'TRUE'
            row['TRAIT_HIGHPOINTCATCH'] = 'TRUE'

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

        # OLB Edits
        if row['Position'] in ['LOLB', 'ROLB', 'MLB']:
            if 'PassRush' in row['TRAIT_LBSTYLE']:
                row['TRAIT_LBSTYLE'] = 'Balanced'

    # Add more conditions and changes for other columns and positions as needed
    return row

def update_attributes(row):
    # Check the player's position and apply changes to specific columns
    contract_status = row['ContractStatus']
    
    if draftclass_phase == "No_Traits" and contract_status in ['Draft']:
        # Assign out-of-position attributes initially (so they can be changed later)
        # Non-Specialists

        if row['Position'] not in ['K', 'P', 'QB', 'LS']:
            row['AwarenessRating'] = row['OverallRating']
            row['KickPowerRating'] = max(row['KickPowerRating'] - 5, 15)
            row['KickAccuracyRating'] = max(row['KickAccuracyRating'] - 10, 10)

        # Non-LongSnappers
        if row['Position'] not in ['LS']:
            row['LongSnapRating'] = 5

        # Kick-Returning
        if row['Position'] not in ['X']:
            row['KickReturnRating'] = max(row['KickReturnRating'] - 5, 5)

        # Non-QBs throwing Edits
        if row['Position'] not in ['QB']:
            row['ThrowPowerRating'] = min(row['ThrowPowerRating'] + 5, 90)

        # Ego Rating
        if row['Position'] in ['WR', 'CB'] and str(row['GenericHeadAssetName']).lower() in ['gen_5', 'gen_6', 'gen_7']:
            roll = random.random()
            if roll < 0.15:
                row['PLYR_EGO'] = 15
            elif roll < 0.30:
                row['PLYR_EGO'] = 35
            elif roll < 0.55:
                row['PLYR_EGO'] = 55
            elif roll < 0.80:
                row['PLYR_EGO'] = 75
            else:
                row['PLYR_EGO'] = 95
        if row['Position'] not in ['WR', 'CB'] and str(row['GenericHeadAssetName']).lower() in ['gen_5', 'gen_6', 'gen_7']:
            roll = random.random()
            if roll < 0.20:
                row['PLYR_EGO'] = 15
            elif roll < 0.45:
                row['PLYR_EGO'] = 35
            elif roll < 0.60:
                row['PLYR_EGO'] = 55
            elif roll < 0.85:
                row['PLYR_EGO'] = 75
            else:
                row['PLYR_EGO'] = 95
        if str(row['GenericHeadAssetName']).lower() not in ['gen_5', 'gen_6', 'gen_7']:
            roll = random.random()
            if roll < 0.25:
                row['PLYR_EGO'] = 15
            elif roll < 0.5:
                row['PLYR_EGO'] = 35
            elif roll < 0.75:
                row['PLYR_EGO'] = 55
            elif roll < 0.95:
                row['PLYR_EGO'] = 75
            else:
                row['PLYR_EGO'] = 95

        # Personality(Character Concerns) Rating
        if str(row['GenericHeadAssetName']).lower() in ['gen_5', 'gen_6', 'gen_7']:
            roll = random.random()
            if roll < 0.95:
                row['PersonalityRating'] = 60
            elif roll < 0.995:
                row['PersonalityRating'] = 75
            else:
                row['PersonalityRating'] = 90
        if str(row['GenericHeadAssetName']).lower() not in ['gen_5', 'gen_6', 'gen_7']:
            roll = random.random()
            if roll < 0.97:
                row['PersonalityRating'] = 60
            elif roll < 0.999:
                row['PersonalityRating'] = 75
            else:
                row['PersonalityRating'] = 90        

        # QB Edits
        if row['Position'] == 'QB':
            # For QBs, set a minimum of 70 and a maximum of 90 for InjuryRating
            new_injury_rating = row['InjuryRating'] - 10
            # Ensure the new value is within the specified range
            if new_injury_rating < 70:
                new_injury_rating = 70
            if new_injury_rating > 90:
                new_injury_rating = 90
            row['InjuryRating'] = new_injury_rating

            if row['OverallRating'] <= 60:
                row['AwarenessRating'] = min(row['AwarenessRating'] + 1, 99)
                row['ThrowAccuracyShortRating'] = min(row['ThrowAccuracyShortRating'] + 1, 99)
                row['ThrowAccuracyMidRating'] = min(row['ThrowAccuracyMidRating'] + 1, 99)
                row['ThrowAccuracyDeepRating'] = min(row['ThrowAccuracyDeepRating'] + 1, 99)
                        
        # HB Edits
        if row['Position'] == 'HB':
            # For HBs, set a minimum of 70 and a maximum of 90 for InjuryRating
            new_injury_rating = row['InjuryRating'] - 10
            # Ensure the new value is within the specified range
            if new_injury_rating < 70:
                new_injury_rating = 70
            if new_injury_rating > 90:
                new_injury_rating = 90
            row['InjuryRating'] = new_injury_rating

            if row['OverallRating'] <= 60:
                row['AwarenessRating'] = min(row['AwarenessRating'] + 1, 99)
                row['BCVisionRating'] = min(row['BCVisionRating'] + 1, 99)
                row['BreakTackleRating'] = min(row['BreakTackleRating'] + 1, 99)
                row['CarryingRating'] = min(row['CarryingRating'] + 1, 99)

        # OFF Edits
        if row['Position'] in ['WR', 'TE']:      

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

        # Stamina Edits
        if row['Position'] in ['TE']:
              row['StaminaRating'] = max(row['StaminaRating'] - 15, 1)
        if row['Position'] in ['DT']:
              row['StaminaRating'] = max(row['StaminaRating'] - 10, 1)

        # OL Edits
        if row['Position'] in ['LT', 'LG', 'C', 'RG', 'RT']:
            row['CarryingRating'] = random.randint(20, 45)
            row['CatchingRating'] = random.randint(15, 40)

            carrying_ol_chances = [
                (50, 0.015),
                (55, 0.006),
                (60, 0.003),
                (65, 0.001),
            ]
            for value, chance in carrying_ol_chances:
                if random.random() <= chance:
                    row['CarryingRating'] = value
                    break    

            catching_ol_chances = [
                (45, 0.015),
                (50, 0.004),
                (55, 0.003),
                (60, 0.002),
                (65, 0.001),
            ]
            for value, chance in catching_ol_chances:
                if random.random() <= chance:
                    row['CatchingRating'] = value
                    break 

        # DT Nose Tackle logic
        if row['Position'] in ['DT']:
            dt_true_weight = row['Weight'] + 160
            overall_rating = row['OverallRating']
            if dt_true_weight >= 325:
                row['ThrowAccuracyDeepRating'] = 99 if overall_rating >= 80 else min(overall_rating + 15, 90)
            elif 310 <= dt_true_weight < 325:
                row['ThrowAccuracyDeepRating'] = min(overall_rating, 85) if overall_rating >= 80 else overall_rating
            elif 300 <= dt_true_weight < 310:
                row['ThrowAccuracyDeepRating'] = 35 if overall_rating >= 80 else 30
            elif 290 <= dt_true_weight < 300:
                row['ThrowAccuracyDeepRating'] = 20 if overall_rating >= 80 else 10
            else:
                row['ThrowAccuracyDeepRating'] = 1

        # DEF Front Edits
        if row['Position'] in ['LE', 'RE', 'DT']:

            if row['OverallRating'] <= 60:
                row['AwarenessRating'] = min(row['AwarenessRating'] + 1, 99)
                row['FinesseMovesRating'] = min(row['FinesseMovesRating'] + 1, 99)
                row['PowerMovesRating'] = min(row['PowerMovesRating'] + 1, 99)
                row['PursuitRating'] = min(row['PursuitRating'] + 1, 99)
                row['TackleRating'] = min(row['TackleRating'] + 1, 99)
                row['BlockSheddingRating'] = min(row['BlockSheddingRating'] + 1, 99)

        # LB Edits
        if row['Position'] in ['LOLB', 'ROLB', 'MLB']:

            if row['ManCoverageRating'] < 50:
                row['ManCoverageRating'] = 48 + random.randint(0, 5)

            if row['ZoneCoverageRating'] < 50:
                row['ZoneCoverageRating'] = 48 + random.randint(0, 5)

            if row['FinesseMovesRating'] > 60:
                row['FinesseMovesRating'] = row['FinesseMovesRating'] - random.randint(0, 5)

            if row['PowerMovesRating'] > 60:
                row['PowerMovesRating'] = row['PowerMovesRating'] - random.randint(0, 5)

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

        # K/P Edits
        if row['Position'] in ['K', 'P']:
                row['TackleRating'] = max(min(row['TackleRating'] - 5, 99), 5)

        # Non-Kicker/Punter Kicking Edits
        if row['Position'] in ['WR', 'SS', 'FS']:
            # Example list of tuples: (KickAccuracyRating value, KickPowerRating value, chance)
            kick_rating_changes = [
                (50, 55, 0.002),
                (55, 65, 0.001),
                (60, 75, 0.002),
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
                (50, 50, 50, 0.01),
                (60, 60, 60, 0.007),
                (60, 55, 50, 0.007),
                (65, 60, 55, 0.007),
                (70, 65, 60, 0.005),
                (75, 65, 60, 0.005),
                (55, 50, 60, 0.003),
                (60, 55, 65, 0.003),
                (65, 60, 70, 0.003),
            ]

            for shortroutecb_value, medroutecb_value, deeproutecb_Value , chance in cb_route_changes:
                if random.random() <= chance:
                    row['ShortRouteRunningRating'] = shortroutecb_value
                    row['MediumRouteRunningRating'] = medroutecb_value
                    row['DeepRouteRunningRating'] = deeproutecb_Value
                    break

        # Off Weapons Passing Edits
        if row['Position'] in ['WR', 'TE']:
            # List of tuples: (ThrowPower, ThrowUnderPressure, ThrowOnTheRun, ThrowAccuracy, ThrowAccuracyShort, ThrowAccuracyMedium, ThrowAccuracyDeep, chance)
            throw_rating_changes = [
                (65, 50, 55, 60, 65, 60, 55, 0.007),
                (75, 55, 60, 65, 70, 65, 60, 0.005),
                (80, 60, 70, 70, 75, 70, 65, 0.003),
            ]

            for power, under_pressure, on_run, accuracy, acc_short, acc_med, acc_deep, chance in throw_rating_changes:
                if random.random() <= chance:
                    row['ThrowPowerRating'] = power
                    row['ThrowUnderPressureRating'] = under_pressure
                    row['ThrowOnTheRunRating'] = on_run
                    row['ThrowAccuracyRating'] = accuracy
                    row['ThrowAccuracyShortRating'] = acc_short
                    row['ThrowAccuracyMidRating'] = acc_med
                    row['ThrowAccuracyDeepRating'] = acc_deep
                    break

        # For all other positions, set a minimum of 70 and a minimum of 90 for InjuryRating
        if row['Position'] not in ['HB', 'QB']:

            new_injury_rating = row['InjuryRating'] - 10
            # Ensure the new value is within the specified range
            if new_injury_rating < 70:
                new_injury_rating = 70
            if new_injury_rating > 90:
                new_injury_rating = 90
            row['InjuryRating'] = new_injury_rating

        # Set TraitDevelopment to "Normal" for all positions
        row['TraitDevelopment'] = 'Normal'

    # Add more conditions and changes for other columns and positions as needed
    return row

def assign_home_states(row):
        
    if draftclass_phase == "Traits" and row['ContractStatus'] == 'Draft' and row['Position'] not in ['K', 'P']:
            states = [
                "Alabama", "Alaska", "Arizona", "Arkansas", "California", "CanadaAlberta",
                "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii",
                "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
                "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
                "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "NewHampshire",
                "NewJersey", "NewMexico", "NewYork", "NorthCarolina", "NorthDakota", "Ohio",
                "Oklahoma", "Oregon", "Pennsylvania", "RhodeIsland", "SouthCarolina", "SouthDakota",
                "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
                "WestVirginia", "Wisconsin", "Wyoming"
            ]

            chances = np.array([
                3.27, 0.03, 1.34, 0.32, 9.39, 0.04,
                0.98, 0.67, 0.28, 9.90, 8.79, 0.79,
                0.32, 2.97, 1.58, 1.06, 0.63, 0.75,
                3.72, 0.04, 2.99, 0.71, 3.19, 0.98,
                2.09, 1.65, 0.20, 0.35, 0.87, 0.04,
                2.99, 0.04, 1.58, 4.02, 0.20, 3.90,
                0.95, 0.75, 2.99, 0.12, 2.21, 0.20,
                2.13, 11.37, 1.18, 0.03, 2.21, 1.34,
                0.32, 1.43, 0.12
            ])

            # Normalize to probabilities
            probabilities = chances / chances.sum()

            # Randomly select a state based on the probabilities
            row['PLYR_HOME_STATE'] = np.random.choice(states, p=probabilities)
    return row

def update_sleevetemp(row):
    if draftclass_phase == "Traits" and row['ContractStatus'] in ['Draft']:
        if row['Position'] in ['QB', 'K', 'P']: # Avg 30
            chances = [0, 10, 20, 30, 40, 50, 60]
            probabilities = [0.05, 0.10, 0.20, 0.30, 0.20, 0.10, 0.05]
            row['PLYR_SLEEVETEMPERATURE'] = random.choices(chances, probabilities)[0]
        elif row['Position'] in ['RB', 'HB', 'FB']: # Avg 20
            chances = [0, 10, 20, 30, 40, 50, 60]
            probabilities = [0.30, 0.10, 0.25, 0.15, 0.10, 0.05, 0.05]
            row['PLYR_SLEEVETEMPERATURE'] = random.choices(chances, probabilities)[0]
        elif row['Position'] in ['WR', 'TE', 'CB', 'FS', 'SS']: # Avg 25
            chances = [0, 10, 20, 30, 40, 50, 60]
            probabilities = [0.15, 0.10, 0.25, 0.25, 0.15, 0.05, 0.05]
            row['PLYR_SLEEVETEMPERATURE'] = random.choices(chances, probabilities)[0]
        elif row['Position'] in ['LT', 'LG', 'C', 'RG', 'RT', 'LE', 'RE', 'DT']: # Avg 16.25
            chances = [0, 10, 20, 30, 40, 50, 60]
            probabilities = [0.40, 0.10, 0.20, 0.15, 0.10, 0.025, 0.025]
            row['PLYR_SLEEVETEMPERATURE'] = random.choices(chances, probabilities)[0]
        elif row['Position'] in ['LOLB', 'MLB', 'ROLB']: # Avg 12.25
            chances = [0, 10, 20, 30, 40, 50, 60]
            probabilities = [0.50, 0.20, 0.05, 0.15, 0.05, 0.025, 0.025]
            row['PLYR_SLEEVETEMPERATURE'] = random.choices(chances, probabilities)[0]
    return row

# Track the original DataFrame before applying updates
original_df = df.copy()

# Apply the new function to update the DataFrame
df = df.apply(update_traits, axis=1)
df = df.apply(update_attributes, axis=1)
df = df.apply(assign_home_states, axis=1)
df = df.apply(update_sleevetemp, axis=1)
#df['PLYR_SLEEVETEMPERATURE'] = df.apply(lambda row: update_sleevetemp(row), axis=1)

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
df.to_excel(season_path('DraftClassEdit.xlsx'), index=False)