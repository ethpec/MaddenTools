# Imports
import pandas as pd
import random
import numpy as np

# Your File Path
file_path = 'Files/Madden26/IE/Season0/Player.xlsx'

df = pd.read_excel(file_path)

def update_traits(row):
    # Check the player's position and apply changes to specific columns
    contract_status = row['ContractStatus']
    
    if contract_status in ['Draft']:
        # Assign out-of-position attributes initially (so they can be changed later)
        # Non-Specialists

        # Initially set all traits to FALSE
        for col in row.index:
            if col.startswith('PT_'):
                row[col] = False

        if row['Position'] not in ['K', 'P', 'QB']:
            row['AwarenessRating'] = row['OverallRating']
            row['KickPowerRating'] = max(row['KickPowerRating'] - 5, 15)
            row['KickAccuracyRating'] = max(row['KickAccuracyRating'] - 10, 10)

        # Non-LongSnappers
        if row['Position'] not in ['LS']:
            row['LongSnapRating'] = 5

        # Kick-Returning
        if row['Position'] not in ['X']:
            row['KickReturnRating'] = max(row['KickReturnRating'] - 3, 5)
            if random.random() < 0.10:
                row['PT_UNDISCIPLINED'] = True
            if not row['PT_UNDISCIPLINED'] and random.random() < 0.10:
                row['PT_DISCIPLINED'] = True

        # Non-QBs throwing Edits
        if row['Position'] not in ['QB']:
            row['ThrowPowerRating'] = min(row['ThrowPowerRating'] + 5, 90)

        # HB/WR/TE general traits
        if row['Position'] in ['RB', 'HB', 'WR', 'TE', 'FB']:
            if row['JukeMoveRating'] >= 90 and random.random() < 0.66:
                row['PT_ELUSIVEINSTINCT'] = True
            elif 80 <= row['JukeMoveRating'] <= 89 and random.random() < 0.33:
                row['PT_ELUSIVEINSTINCT'] = True
            elif row['JukeMoveRating'] <= 79 and random.random() < 0.1:
                row['PT_ELUSIVEINSTINCT'] = True
            if row['SpinMoveRating'] >= 90 and random.random() < 0.66:
                row['PT_SPINCYCLE'] = True
            elif 80 <= row['SpinMoveRating'] <= 89 and random.random() < 0.25:
                row['PT_SPINCYCLE'] = True
            elif row['SpinMoveRating'] <= 79 and random.random() < 0.05:
                row['PT_SPINCYCLE'] = True
            if row['TruckingRating'] >= 90 and random.random() < 0.66:
                row['PT_RUNOVER'] = True
            elif 80 <= row['TruckingRating'] <= 89 and random.random() < 0.33:
                row['PT_RUNOVER'] = True
            elif row['TruckingRating'] <= 79 and random.random() < 0.1:
                row['PT_RUNOVER'] = True
            if row['StiffArmRating'] >= 90 and random.random() < 0.66:
                row['PT_STRONGARM'] = True
            elif 80 <= row['StiffArmRating'] <= 89 and random.random() < 0.33:
                row['PT_STRONGARM'] = True
            elif row['StiffArmRating'] <= 79 and random.random() < 0.1:
                row['PT_STRONGARM'] = True            

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

            # QB Generic Trait Chances   
            qb_trait_chances = {
                'PT_LOOKFORSTARS': 0.50,
                'PT_EYESUP': 0.15,
                'PT_TRIGGERHAPPY': 0.10,
                'PT_QUICKCLOCK': 0.15,
                'PT_QUICKTRIGGER': 0.15,
                'PT_SEEINGGHOSTS': 0.10,
                'PT_SETUPTIME': 0.10,
                'PT_THROWAWAY': 0.25,
                'PT_UNUSEDTRAIT1': 0.10, #Throw It Up
                'PT_COVERBALL': 0.15,
                'PT_HAPPYFEET': 0.05
            }
            for trait, chance in qb_trait_chances.items():
                if random.random() < chance:
                    row[trait] = True

            # QB attribute dependent traits    
            if row['ThrowPowerRating'] >= 96 and random.random() < 0.15:
                row['PT_CANNON'] = True
            elif 95 >= row['ThrowPowerRating'] >= 92 and random.random() < 0.1:
                row['PT_CANNON'] = True
            elif 88 <= row['ThrowPowerRating'] <= 91 and random.random() < 0.05:
                row['PT_CANNON'] = True
            if row['PT_CANNON'] == False and random.random() < 0.1:
                row['PT_UPANDOVER'] = True
            if row['SpeedRating'] <= 74:
                row['PT_SEDENTARY'] = True
            elif 75 <= row['SpeedRating'] <= 79:
                row['PT_SEDENTARY'] = random.choice([True, False])
            elif row['SpeedRating'] >= 85:
                row['PT_HEROBALL'] = True
            elif 80 <= row['SpeedRating'] <= 84:
                row['PT_HEROBALL'] = random.choice([True, False])
            if random.random() < 0.15:
                row['PT_RISKTAKER'] = True
            if random.random() < 0.15 and row['PT_RISKTAKER'] == False:
                row['PT_CONSERVATIVE'] = True
            if row['ThrowOnTheRunRating'] >= 85  and random.random() < 0.75:
                row['PT_DOUBLEBACK'] = True
            elif 80 <= row['ThrowOnTheRunRating'] <= 84 and random.random() < 0.2:
                row['PT_DOUBLEBACK'] = True
            elif row['ThrowOnTheRunRating'] <= 79 and random.random() < 0.05:
                row['PT_DOUBLEBACK'] = True
            if random.random() < 0.1:
                row['PT_OBLIVIOUS'] = True
            elif row['PT_OBLIVIOUS'] == False and random.random() < 0.07:
                row['PT_PARANOID'] = True
            if row['SpeedRating'] >= 85 and random.random() < 0.5:
                row['PT_ELUSIVEINSTINCT'] = True
            elif 84 >= row['SpeedRating'] >= 80 and random.random() < 0.25:
                row['PT_ELUSIVEINSTINCT'] = True
            elif row['SpeedRating'] <= 79 and random.random() < 0.075:
                row['PT_ELUSIVEINSTINCT'] = True
            if row['SpeedRating'] >= 85 and random.random() < 0.1:
                row['PT_SPINCYCLE'] = True
            elif 84 >= row['SpeedRating'] >= 80 and random.random() < 0.05:
                row['PT_SPINCYCLE'] = True
            elif row['SpeedRating'] <= 79 and random.random() < 0.01:
                row['PT_SPINCYCLE'] = True
            if row['SpeedRating'] >= 85 and random.random() < 0.2:
                row['PT_RUNOVER'] = True
            elif 84 >= row['SpeedRating'] >= 80 and random.random() < 0.1:
                row['PT_RUNOVER'] = True
            elif row['SpeedRating'] <= 79 and random.random() < 0.05:
                row['PT_RUNOVER'] = True
            if row['SpeedRating'] >= 85 and random.random() < 0.1:
                row['PT_STRONGARM'] = True
            elif 84 >= row['SpeedRating'] >= 80 and random.random() < 0.05:
                row['PT_STRONGARM'] = True
            elif row['SpeedRating'] <= 79 and random.random() < 0.01:
                row['PT_STRONGARM'] = True
            if not row['PT_ELUSIVEINSTINCT'] and not row['PT_STRONGARM'] and not row['PT_SPINCYCLE'] and not row['PT_RUNOVER']:
                row['PT_STEERINGCLEAR'] = True

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

            # HB Generic Trait Chances   
            hb_trait_chances = {
                'PT_AGGRESSIVE': 0.10,
                'PT_COVERBALL': 0.15,
                'PT_HIGHLIGHTREEL': 0.05,
                'PT_POSSESSION': 0.15,
                'PT_RAC': 0.20,
                'PT_EARLYCELEBRATION': 0.15
            }
            for trait, chance in hb_trait_chances.items():
                if random.random() < chance:
                    row[trait] = True

            if not row['PT_ELUSIVEINSTINCT'] and not row['PT_STRONGARM'] and not row['PT_SPINCYCLE'] and not row['PT_RUNOVER'] and random.random() < 0.05:
                row['PT_STEERINGCLEAR'] = True

            if row['OverallRating'] <= 60:
                row['AwarenessRating'] = min(row['AwarenessRating'] + 1, 99)
                row['BCVisionRating'] = min(row['BCVisionRating'] + 1, 99)
                row['BreakTackleRating'] = min(row['BreakTackleRating'] + 1, 99)
                row['CarryingRating'] = min(row['CarryingRating'] + 1, 99)

        # OFF Edits
        if row['Position'] in ['WR', 'TE']:

            # WR/TE Generic Trait Chances   
            rec_trait_chances = {
                'PT_COVERBALL': 0.15,
                'PT_POSSESSION': 0.15,
                'PT_RAC': 0.25,
                'PT_EARLYCELEBRATION': 0.20
            }
            for trait, chance in rec_trait_chances.items():
                if random.random() < chance:
                    row[trait] = True

            if not row['PT_ELUSIVEINSTINCT'] and not row['PT_STRONGARM'] and not row['PT_SPINCYCLE'] and not row['PT_RUNOVER'] and random.random() < 0.25:
                row['PT_STEERINGCLEAR'] = True
            if row['SpectacularCatchRating'] >= 90 and random.random() < 0.66:
                row['PT_HIGHLIGHTREEL'] = True
            elif 80 <= row['SpectacularCatchRating'] <= 89 and random.random() < 0.25:
                row['PT_HIGHLIGHTREEL'] = True
            elif row['SpectacularCatchRating'] <= 79 and random.random() < 0.075:
                row['PT_HIGHLIGHTREEL'] = True
            if row['CatchInTrafficRating'] >= 90 and random.random() < 0.75:
                row['PT_AGGRESSIVE'] = True
            elif 80 <= row['CatchInTrafficRating'] <= 89 and random.random() < 0.33:
                row['PT_AGGRESSIVE'] = True
            elif row['CatchInTrafficRating'] <= 79 and random.random() < 0.10:
                row['PT_AGGRESSIVE'] = True        

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

        # DEF General Trait Edits
        if row['Position'] in ['LE', 'RE', 'DT', 'LOLB', 'MLB', 'ROLB', 'CB', 'FS', 'SS']:
            if row['HitPowerRating'] >= 90 and random.random() < 0.66:
                row['PT_HEADHUNTER'] = True
            elif 80 <= row['HitPowerRating'] <= 89 and random.random() < 0.15:
                row['PT_HEADHUNTER'] = True
            elif row['HitPowerRating'] <= 79 and random.random() < 0.05:
                row['PT_HEADHUNTER'] = True 
            if random.random() < 0.05:
                row['PT_PUNCHITOUT'] = True
            if not row['PT_HEADHUNTER'] and not row['PT_PUNCHITOUT'] and random.random() < 0.10:
                row['PT_SAFETACKLER'] = True

        # DEF Front Edits
        if row['Position'] in ['LE', 'RE', 'DT']:
        
            if (row['BlockSheddingRating'] + row['PowerMovesRating'])/2 >= 85 and random.random() < 0.75:
                row['PT_BOUNCER'] = True
            elif 75 <= (row['BlockSheddingRating'] + row['PowerMovesRating'])/2 <= 84 and random.random() < 0.25:
                row['PT_BOUNCER'] = True
            elif (row['BlockSheddingRating'] + row['PowerMovesRating'])/2 <= 74 and random.random() < 0.05:
                row['PT_BOUNCER'] = True      
            if row['StrengthRating'] >= 85 and random.random() < 0.75:
                row['PT_BULL'] = True
            elif 75 <= row['StrengthRating'] <= 84 and random.random() < 0.25:
                row['PT_BULL'] = True
            elif row['StrengthRating'] <= 74 and random.random() < 0.05:
                row['PT_BULL'] = True  
            if row['FinesseMovesRating'] >= 85 and random.random() < 0.75:
                row['PT_FINESSERUSHER'] = True
            elif 75 <= row['FinesseMovesRating'] <= 84 and random.random() < 0.25:
                row['PT_FINESSERUSHER'] = True
            elif row['FinesseMovesRating'] <= 74 and random.random() < 0.05:
                row['PT_FINESSERUSHER'] = True 
            if (row['PowerMovesRating'] + row['FinesseMovesRating'])/2 >= 85 and random.random() < 0.75:
                row['PT_OLE'] = True
            elif 75 <= (row['PowerMovesRating'] + row['FinesseMovesRating'])/2 <= 84 and random.random() < 0.25:
                row['PT_OLE'] = True
            elif (row['PowerMovesRating'] + row['FinesseMovesRating'])/2 <= 74 and random.random() < 0.05:
                row['PT_OLE'] = True  
            if row['PowerMovesRating'] >= 85 and random.random() < 0.75:
                row['PT_POWERRUSHER'] = True
            elif 75 <= row['PowerMovesRating'] <= 84 and random.random() < 0.25:
                row['PT_POWERRUSHER'] = True
            elif row['PowerMovesRating'] <= 74 and random.random() < 0.05:
                row['PT_POWERRUSHER'] = True  
            if (row['AgilityRating'] + row['FinesseMovesRating'])/2 >= 85 and random.random() < 0.75:
                row['PT_SPINRUSHER'] = True
            elif 75 <= (row['AgilityRating'] + row['FinesseMovesRating'])/2 <= 84 and random.random() < 0.25:
                row['PT_SPINRUSHER'] = True
            elif (row['AgilityRating'] + row['FinesseMovesRating'])/2 <= 74 and random.random() < 0.05:
                row['PT_SPINRUSHER'] = True
            if (row['StrengthRating'] + row['PowerMovesRating'])/2 >= 85 and random.random() < 0.75:
                row['PT_HAMMERHEAD'] = True
            elif 75 <= (row['StrengthRating'] + row['PowerMovesRating'])/2 <= 84 and random.random() < 0.25:
                row['PT_HAMMERHEAD'] = True
            elif (row['StrengthRating'] + row['PowerMovesRating'])/2 <= 74 and random.random() < 0.05:
                row['PT_HAMMERHEAD'] = True 
            if random.random() < 0.075:
                row['PT_FLYSWATTER'] = True
            if random.random() < 0.075:
                row['PT_GASGUZZLER'] = True

            if row['OverallRating'] <= 60:
                row['AwarenessRating'] = min(row['AwarenessRating'] + 1, 99)
                row['FinesseMovesRating'] = min(row['FinesseMovesRating'] + 1, 99)
                row['PowerMovesRating'] = min(row['PowerMovesRating'] + 1, 99)
                row['PursuitRating'] = min(row['PursuitRating'] + 1, 99)
                row['TackleRating'] = min(row['TackleRating'] + 1, 99)
                row['BlockSheddingRating'] = min(row['BlockSheddingRating'] + 1, 99)

        # OLB Edits
        if row['Position'] in ['LOLB', 'ROLB']:

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

        # DB Edits
        if row['Position'] in ['CB', 'FS', 'SS']:
            if row['PressRating'] >= 85 and random.random() < 0.75:
                row['PT_JAMMER'] = True
            elif 75 <= row['PressRating'] <= 84 and random.random() < 0.15:
                row['PT_JAMMER'] = True
            elif row['PressRating'] <= 74 and random.random() < 0.05:
                row['PT_JAMMER'] = True 
            if random.random() < 0.10:
                row['PT_PLAYBALL'] = True
            if not row['PT_PLAYBALL'] and random.random() < 0.10:
                row['PT_PLAYRECEIVER'] = True  

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
    if row['ContractStatus'] == 'Draft' and row['Position'] not in ['K', 'P']:
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
df.to_excel('Files/Madden26/IE/Season0/DraftClassEdit.xlsx', index=False)