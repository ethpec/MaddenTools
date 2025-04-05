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

        # WR Edits
        if row['Position'] == 'WR':
            row['AgilityRating'] = max(0, min(row['AgilityRating'] + random.randint(-2, 2), 99))
            row['AccelerationRating'] = max(0, min(row['AccelerationRating'] + random.randint(-2, 2), 99))
            row['CatchingRating'] = max(0, min(row['CatchingRating'] + random.randint(-7, 4), 99))
            row['DeepRouteRunningRating'] = max(0, min(row['DeepRouteRunningRating'] + random.randint(-6, 4), 99))
            row['MediumRouteRunningRating'] = max(0, min(row['MediumRouteRunningRating'] + random.randint(-6, 4), 99))
            row['ShortRouteRunningRating'] = max(0, min(row['ShortRouteRunningRating'] + random.randint(-6, 4), 99))
            row['SpeedRating'] = max(0, min(row['SpeedRating'] + random.randint(-1, 1), 99))
            row['ReleaseRating'] = max(0, min(row['ReleaseRating'] + random.randint(-5, 5), 99))
            row['CatchInTrafficRating'] = max(0, min(row['CatchInTrafficRating'] + random.randint(-6, 4), 99))
            row['SpectacularCatchRating'] = max(0, min(row['SpectacularCatchRating'] + random.randint(-8, 4), 99))

        # TE Edits
        if row['Position'] == 'TE':
            row['AgilityRating'] = max(0, min(row['AgilityRating'] + random.randint(-2, 2), 99))
            row['AccelerationRating'] = max(0, min(row['AccelerationRating'] + random.randint(-2, 2), 99))
            row['CatchingRating'] = max(0, min(row['CatchingRating'] + random.randint(-6, 4), 99))
            row['DeepRouteRunningRating'] = max(0, min(row['DeepRouteRunningRating'] + random.randint(-4, 5), 99))
            row['MediumRouteRunningRating'] = max(0, min(row['MediumRouteRunningRating'] + random.randint(-4, 4), 99))
            row['ShortRouteRunningRating'] = max(0, min(row['ShortRouteRunningRating'] + random.randint(-5, 4), 99))
            row['SpeedRating'] = max(0, min(row['SpeedRating'] + random.randint(-1, 1), 99))
            row['ReleaseRating'] = max(0, min(row['ReleaseRating'] + random.randint(-4, 5), 99))
            row['CatchInTrafficRating'] = max(0, min(row['CatchInTrafficRating'] + random.randint(-4, 4), 99))
            row['SpectacularCatchRating'] = max(0, min(row['SpectacularCatchRating'] + random.randint(-4, 4), 99))
            row['BreakTackleRating'] = max(0, min(row['BreakTackleRating'] + random.randint(-2, 5), 99))
            row['StiffArmRating'] = max(0, min(row['StiffArmRating'] + random.randint(-2, 2), 99))
            row['TruckingRating'] = max(0, min(row['TruckingRating'] + random.randint(-3, 3), 99))

        #OL Edits
        if row['Position'] in ['LT', 'RT']:
            row['ImpactBlockingRating'] = max(0, min(row['ImpactBlockingRating'] + random.randint(-4, 4), 99))
            row['LeadBlockRating'] = max(0, min(row['LeadBlockRating'] + random.randint(-4, 4), 99))
            row['RunBlockFinesseRating'] = max(0, min(row['RunBlockFinesseRating'] + random.randint(-4, 5), 99))
            row['RunBlockPowerRating'] = max(0, min(row['RunBlockPowerRating'] + random.randint(-4, 4), 99))
            row['RunBlockRating'] = max(0, min(row['RunBlockRating'] + random.randint(-4, 4), 99))
            row['StrengthRating'] = max(0, min(row['StrengthRating'] + random.randint(-2, 2), 99))
            row['PassBlockRating'] = max(0, min(row['PassBlockRating'] + random.randint(-4, 5), 99))
            row['PassBlockFinesseRating'] = max(0, min(row['PassBlockFinesseRating'] + random.randint(-4, 4), 99))
            row['PassBlockPowerRating'] = max(0, min(row['PassBlockPowerRating'] + random.randint(-4, 4), 99))

        if row['Position'] in ['LG', 'RG']:
            row['ImpactBlockingRating'] = max(0, min(row['ImpactBlockingRating'] + random.randint(-4, 4), 99))
            row['LeadBlockRating'] = max(0, min(row['LeadBlockRating'] + random.randint(-4, 4), 99))
            row['RunBlockFinesseRating'] = max(0, min(row['RunBlockFinesseRating'] + random.randint(-4, 5), 99))
            row['RunBlockPowerRating'] = max(0, min(row['RunBlockPowerRating'] + random.randint(-4, 4), 99))
            row['RunBlockRating'] = max(0, min(row['RunBlockRating'] + random.randint(-4, 4), 99))
            row['StrengthRating'] = max(0, min(row['StrengthRating'] + random.randint(-3, 2), 99))
            row['PassBlockRating'] = max(0, min(row['PassBlockRating'] + random.randint(-4, 4), 99))
            row['PassBlockFinesseRating'] = max(0, min(row['PassBlockFinesseRating'] + random.randint(-4, 4), 99))
            row['PassBlockPowerRating'] = max(0, min(row['PassBlockPowerRating'] + random.randint(-4, 4), 99))

        if row['Position'] in ['C']:
            row['ImpactBlockingRating'] = max(0, min(row['ImpactBlockingRating'] + random.randint(-4, 5), 99))
            row['LeadBlockRating'] = max(0, min(row['LeadBlockRating'] + random.randint(-4, 4), 99))
            row['RunBlockFinesseRating'] = max(0, min(row['RunBlockFinesseRating'] + random.randint(-4, 5), 99))
            row['RunBlockPowerRating'] = max(0, min(row['RunBlockPowerRating'] + random.randint(-4, 5), 99))
            row['RunBlockRating'] = max(0, min(row['RunBlockRating'] + random.randint(-5, 4), 99))
            row['StrengthRating'] = max(0, min(row['StrengthRating'] + random.randint(-2, 3), 99))
            row['PassBlockRating'] = max(0, min(row['PassBlockRating'] + random.randint(-4, 4), 99))
            row['PassBlockFinesseRating'] = max(0, min(row['PassBlockFinesseRating'] + random.randint(-4, 4), 99))
            row['PassBlockPowerRating'] = max(0, min(row['PassBlockPowerRating'] + random.randint(-4, 4), 99))

        # DL Edits
        if row['Position'] in ['LE', 'RE']:
            row['AgilityRating'] = max(0, min(row['AgilityRating'] + random.randint(-2, 3), 99))
            row['AccelerationRating'] = max(0, min(row['AccelerationRating'] + random.randint(-2, 3), 99))
            row['BlockSheddingRating'] = max(0, min(row['BlockSheddingRating'] + random.randint(-4, 5), 99))
            row['ChangeOfDirectionRating'] = max(0, min(row['ChangeOfDirectionRating'] + random.randint(-3, 4), 99))
            row['FinesseMovesRating'] = max(0, min(row['FinesseMovesRating'] + random.randint(-4, 4), 99))
            row['SpeedRating'] = max(0, min(row['SpeedRating'] + random.randint(-1, 2), 99))
            row['StrengthRating'] = max(0, min(row['StrengthRating'] + random.randint(-3, 3), 99))
            row['PursuitRating'] = max(0, min(row['PursuitRating'] + random.randint(-5, 4), 99))
            row['TackleRating'] = max(0, min(row['TackleRating'] + random.randint(-5, 4), 99))
            row['PlayRecognitionRating'] = max(0, min(row['PlayRecognitionRating'] + random.randint(-4, 6), 99))
            row['PowerMovesRating'] = max(0, min(row['PowerMovesRating'] + random.randint(-5, 4), 99))

        if row['Position'] in ['DT']:
            row['AgilityRating'] = max(0, min(row['AgilityRating'] + random.randint(-2, 4), 99))
            row['AccelerationRating'] = max(0, min(row['AccelerationRating'] + random.randint(-2, 2), 99))
            row['BlockSheddingRating'] = max(0, min(row['BlockSheddingRating'] + random.randint(-4, 4), 99))
            row['ChangeOfDirectionRating'] = max(0, min(row['ChangeOfDirectionRating'] + random.randint(-2, 5), 99))
            row['FinesseMovesRating'] = max(0, min(row['FinesseMovesRating'] + random.randint(-4, 6), 99))
            row['SpeedRating'] = max(0, min(row['SpeedRating'] + random.randint(-1, 3), 99))
            row['StrengthRating'] = max(0, min(row['StrengthRating'] + random.randint(-3, 3), 99))
            row['PursuitRating'] = max(0, min(row['PursuitRating'] + random.randint(-4, 4), 99))
            row['TackleRating'] = max(0, min(row['TackleRating'] + random.randint(-4, 4), 99))
            row['PlayRecognitionRating'] = max(0, min(row['PlayRecognitionRating'] + random.randint(-4, 5), 99))
            row['PowerMovesRating'] = max(0, min(row['PowerMovesRating'] + random.randint(-4, 4), 99))

        # LB Edits ############################################# (Have to figure out how to work with other script - when/what to run when)

        if row['Position'] in ['LOLB', 'ROLB', 'MLB']:
            row['AgilityRating'] = max(0, min(row['AgilityRating'] + random.randint(-2, 2), 99))
            row['AccelerationRating'] = max(0, min(row['AccelerationRating'] + random.randint(-2, 2), 99))
            row['ChangeOfDirectionRating'] = max(0, min(row['ChangeOfDirectionRating'] + random.randint(-2, 2), 99))
            row['SpeedRating'] = max(0, min(row['SpeedRating'] + random.randint(-2, 2), 99))
            row['StrengthRating'] = max(0, min(row['StrengthRating'] + random.randint(-2, 2), 99))
            row['PursuitRating'] = max(0, min(row['PursuitRating'] + random.randint(-6, 4), 99))
            row['TackleRating'] = max(0, min(row['TackleRating'] + random.randint(-4, 4), 99))
            row['PlayRecognitionRating'] = max(0, min(row['PlayRecognitionRating'] + random.randint(-4, 4), 99))
            row['CatchingRating'] = max(0, min(row['CatchingRating'] + random.randint(-4, 4), 99))
            row['CatchInTrafficRating'] = max(0, min(row['CatchInTrafficRating'] + random.randint(-3, 5), 99))
            row['ManCoverageRating'] = max(0, min(row['ManCoverageRating'] + random.randint(-7, 4), 99))
            row['PressRating'] = max(0, min(row['PressRating'] + random.randint(-5, 4), 99))
            row['ZoneCoverageRating'] = max(0, min(row['ZoneCoverageRating'] + random.randint(-6, 4), 99))
            row['HitPowerRating'] = max(0, min(row['HitPowerRating'] + random.randint(-4, 5), 99))

        # DB Edits
        if row['Position'] == 'CB':
            row['AgilityRating'] = max(0, min(row['AgilityRating'] + random.randint(-2, 2), 99))
            row['AccelerationRating'] = max(0, min(row['AccelerationRating'] + random.randint(-2, 2), 99))
            row['ChangeOfDirectionRating'] = max(0, min(row['ChangeOfDirectionRating'] + random.randint(-2, 2), 99))
            row['SpeedRating'] = max(0, min(row['SpeedRating'] + random.randint(-2, 2), 99))
            row['StrengthRating'] = max(0, min(row['StrengthRating'] + random.randint(-2, 3), 99))
            row['PursuitRating'] = max(0, min(row['PursuitRating'] + random.randint(-3, 2), 99))
            row['TackleRating'] = max(0, min(row['TackleRating'] + random.randint(-3, 3), 99))
            row['PlayRecognitionRating'] = max(0, min(row['PlayRecognitionRating'] + random.randint(-3, 3), 99))
            row['CatchingRating'] = max(0, min(row['CatchingRating'] + random.randint(-3, 4), 99))
            row['CatchInTrafficRating'] = max(0, min(row['CatchInTrafficRating'] + random.randint(-3, 5), 99))
            row['ManCoverageRating'] = max(0, min(row['ManCoverageRating'] + random.randint(-7, 4), 99))
            row['PressRating'] = max(0, min(row['PressRating'] + random.randint(-4, 4), 99))
            row['ZoneCoverageRating'] = max(0, min(row['ZoneCoverageRating'] + random.randint(-4, 4), 99))

        if row['Position'] in ['FS', 'SS']:
            row['AgilityRating'] = max(0, min(row['AgilityRating'] + random.randint(-2, 2), 99))
            row['AccelerationRating'] = max(0, min(row['AccelerationRating'] + random.randint(-2, 2), 99))
            row['ChangeOfDirectionRating'] = max(0, min(row['ChangeOfDirectionRating'] + random.randint(-2, 2), 99))
            row['SpeedRating'] = max(0, min(row['SpeedRating'] + random.randint(-2, 2), 99))
            row['StrengthRating'] = max(0, min(row['StrengthRating'] + random.randint(-2, 2), 99))
            row['PursuitRating'] = max(0, min(row['PursuitRating'] + random.randint(-6, 4), 99))
            row['TackleRating'] = max(0, min(row['TackleRating'] + random.randint(-4, 4), 99))
            row['PlayRecognitionRating'] = max(0, min(row['PlayRecognitionRating'] + random.randint(-4, 4), 99))
            row['CatchingRating'] = max(0, min(row['CatchingRating'] + random.randint(-4, 4), 99))
            row['CatchInTrafficRating'] = max(0, min(row['CatchInTrafficRating'] + random.randint(-3, 5), 99))
            row['ManCoverageRating'] = max(0, min(row['ManCoverageRating'] + random.randint(-7, 4), 99))
            row['PressRating'] = max(0, min(row['PressRating'] + random.randint(-5, 4), 99))
            row['ZoneCoverageRating'] = max(0, min(row['ZoneCoverageRating'] + random.randint(-6, 4), 99))
            row['HitPowerRating'] = max(0, min(row['HitPowerRating'] + random.randint(-4, 5), 99))

        # K and P Edits
        if row['Position'] in ['K']:
            row['KickAccuracyRating'] = max(0, min(row['KickAccuracyRating'] + random.randint(-3, 6), 99))
            row['KickPowerRating'] = max(0, min(row['KickPowerRating'] + random.randint(-3, 4), 99))

        if row['Position'] in ['K']:
            row['KickAccuracyRating'] = max(0, min(row['KickAccuracyRating'] + random.randint(-3, 5), 99))
            row['KickPowerRating'] = max(0, min(row['KickPowerRating'] + random.randint(-3, 4), 99))

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