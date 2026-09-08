# Imports
import pandas as pd
from config import season_path

# Your File Path
file_path = season_path('Player.xlsx')

df = pd.read_excel(file_path)

# Limit the run to specific positions, e.g. ['WR'] or ['WR', 'TE']
# Set to None to run every position block below
POSITIONS_TO_RUN = ['LOLB', 'ROLB']

def update_position_ratings(row):
    # Check the player's position and apply changes to specific columns
    contract_status = row['ContractStatus']

    if POSITIONS_TO_RUN is not None and row['Position'] not in POSITIONS_TO_RUN:
        return row

    if contract_status in ['Draft']:
        # Change Edited Position Here
        # row['AgilityRating'] -= 0
        # row['AccelerationRating'] += 0

        if row['Position'] in ['QB'] and row['OverallRating'] < 60:
            row['AwarenessRating'] += 1
            row['ThrowAccuracyDeepRating'] += 1
            row['ThrowAccuracyMidRating'] += 1
            row['ThrowAccuracyShortRating'] += 1
            row['ThrowPowerRating'] += 0
            row['ThrowOnTheRunRating'] += 1
            row['ThrowUnderPressureRating'] += 1
            row['BreakSackRating'] += 1

        if row['Position'] in ['HB'] and row['OverallRating'] < 62:
            row['AwarenessRating'] +=1
            row['CarryingRating'] +=1 ###Carrying for Base 26 Roster is really high###
            row['BCVisionRating'] +=1
            row['BreakTackleRating'] +=1
            row['ShortRouteRunningRating'] +=1
            row['StiffArmRating'] +=1
            row['TruckingRating'] +=1
            row['CatchingRating'] +=1
            row['PassBlockRating'] +=1

        if row['Position'] in ['WR'] and row['OverallRating'] > 0:
            row['AwarenessRating'] +=1
            row['CatchingRating'] +=1
            row['DeepRouteRunningRating'] +=1
            row['MediumRouteRunningRating'] +=1
            row['ShortRouteRunningRating'] +=1
            row['ReleaseRating'] +=1
            row['CatchInTrafficRating'] +=1
            row['SpectacularCatchRating'] +=1

        if row['Position'] in ['TE'] and row['OverallRating'] > 60:
            row['AwarenessRating'] -=1
            row['CatchingRating'] -=1
            row['DeepRouteRunningRating'] -=1
            row['MediumRouteRunningRating'] -=1
            row['ShortRouteRunningRating'] -=1
            row['ReleaseRating'] -=1
            row['CatchInTrafficRating'] -=1
            row['SpectacularCatchRating'] -=1

        if row['Position'] in ['LT'] and row['OverallRating'] < 60:
            row['AwarenessRating'] +=0
            row['ImpactBlockingRating'] +=1
            row['LeadBlockRating'] +=1
            row['RunBlockFinesseRating'] +=1
            row['RunBlockPowerRating'] +=1
            row['RunBlockRating'] +=1
            row['PassBlockRating'] +=1
            row['PassBlockFinesseRating'] +=1
            row['PassBlockPowerRating'] +=1

        if row['Position'] in ['LG'] and row['OverallRating'] < 0:
            row['AwarenessRating'] +=1
            row['ImpactBlockingRating'] +=1
            row['LeadBlockRating'] +=1
            row['RunBlockFinesseRating'] +=1
            row['RunBlockPowerRating'] +=1
            row['RunBlockRating'] +=1
            row['PassBlockRating'] +=1
            row['PassBlockFinesseRating'] +=1
            row['PassBlockPowerRating'] +=1
        
        if row['Position'] in ['C'] and row['OverallRating'] < 0:
            row['AwarenessRating'] +=1
            row['ImpactBlockingRating'] +=1
            row['LeadBlockRating'] +=1
            row['RunBlockFinesseRating'] +=1
            row['RunBlockPowerRating'] +=1
            row['RunBlockRating'] +=1
            row['PassBlockRating'] +=1
            row['PassBlockFinesseRating'] +=1
            row['PassBlockPowerRating'] +=1

        if row['Position'] in ['RG'] and row['OverallRating'] < 0:
            row['AwarenessRating'] +=1
            row['ImpactBlockingRating'] +=1
            row['LeadBlockRating'] +=1
            row['RunBlockFinesseRating'] +=1
            row['RunBlockPowerRating'] +=1
            row['RunBlockRating'] +=1
            row['PassBlockRating'] +=1
            row['PassBlockFinesseRating'] +=1
            row['PassBlockPowerRating'] +=1

        if row['Position'] in ['RT'] and row['OverallRating'] < 0:
            row['AwarenessRating'] +=1
            row['ImpactBlockingRating'] +=1
            row['LeadBlockRating'] +=1
            row['RunBlockFinesseRating'] +=1
            row['RunBlockPowerRating'] +=1
            row['RunBlockRating'] +=1
            row['PassBlockRating'] +=1
            row['PassBlockFinesseRating'] +=1
            row['PassBlockPowerRating'] +=1

        if row['Position'] in ['LE'] and row['OverallRating'] > 64:
            row['AwarenessRating'] -=1
            row['BlockSheddingRating'] -=1
            row['FinesseMovesRating'] -=1
            row['PursuitRating'] -=1
            row['TackleRating'] -=1
            row['PlayRecognitionRating'] -=1
            row['PowerMovesRating'] -=1

        if row['Position'] in ['RE'] and row['OverallRating'] > 64:
            row['AwarenessRating'] -=1
            row['BlockSheddingRating'] -=1
            row['FinesseMovesRating'] -=1
            row['PursuitRating'] -=1
            row['TackleRating'] -=1
            row['PlayRecognitionRating'] -=1
            row['PowerMovesRating'] -=1

        if row['Position'] in ['DT'] and row['OverallRating'] < 64:
            row['AwarenessRating'] +=1
            row['BlockSheddingRating'] +=1
            row['FinesseMovesRating'] +=1
            row['PursuitRating'] +=1
            row['TackleRating'] +=1
            row['PlayRecognitionRating'] +=1
            row['PowerMovesRating'] +=1

        if row['Position'] in ['LOLB'] and row['OverallRating'] < 75:
            row['AwarenessRating'] +=1
            row['PursuitRating'] +=1
            row['TackleRating'] +=1
            row['PlayRecognitionRating'] +=1
            row['ManCoverageRating'] +=3
            row['ZoneCoverageRating'] +=3
            row['BlockSheddingRating'] +=1

        if row['Position'] in ['ROLB'] and row['OverallRating'] < 75:
            row['AwarenessRating'] +=1
            row['PursuitRating'] +=1
            row['TackleRating'] +=1
            row['PlayRecognitionRating'] +=1
            row['ManCoverageRating'] +=3
            row['ZoneCoverageRating'] +=3
            row['BlockSheddingRating'] +=1

        if row['Position'] in ['MLB'] and row['OverallRating'] > 64:
            row['AwarenessRating'] -=1
            row['PursuitRating'] -=1
            row['TackleRating'] -=1
            row['PlayRecognitionRating'] -=1
            row['ManCoverageRating'] -=1
            row['ZoneCoverageRating'] -=1
            row['BlockSheddingRating'] -=1

        if row['Position'] in ['CB'] and row['OverallRating'] < 0:
            row['AwarenessRating'] -=1
            row['PursuitRating'] -=1
            row['TackleRating'] -=1
            row['PlayRecognitionRating'] -=1
            row['ManCoverageRating'] -=1
            row['PressRating'] -=1
            row['ZoneCoverageRating'] -=1

        if row['Position'] in ['FS'] and row['OverallRating'] < 65:
            row['AwarenessRating'] +=1
            row['PursuitRating'] +=1
            row['TackleRating'] +=1
            row['PlayRecognitionRating'] +=1
            row['ManCoverageRating'] +=1
            row['PressRating'] +=1
            row['ZoneCoverageRating'] +=1

        if row['Position'] in ['SS'] and row['OverallRating'] < 0:
            row['AwarenessRating'] -=1
            row['PursuitRating'] -=1
            row['TackleRating'] -=1
            row['PlayRecognitionRating'] -=1
            row['ManCoverageRating'] -=1
            row['PressRating'] -=1
            row['ZoneCoverageRating'] -=1

        if row['Position'] in ['K', 'P'] and row['OverallRating'] < 69:
            row['AwarenessRating'] +=1
            row['KickPowerRating'] +=1
            row['KickAccuracyRating'] +=1

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
df.to_excel(season_path('DraftClassPositionEdits.xlsx'), index=False)