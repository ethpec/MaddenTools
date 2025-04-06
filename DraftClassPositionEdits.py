# Imports
import pandas as pd

# Your File Path
file_path = 'Files/Madden25/IE/Season9/Player.xlsx'

df = pd.read_excel(file_path)

def update_position_ratings(row):
    # Check the player's position and apply changes to specific columns
    contract_status = row['ContractStatus']
    
    if contract_status in ['Draft']:
        # Change Edited Position Here
        '''if row['Position'] in ['QB'] and row['OverallRating'] <= 0:
            row['AwarenessRating'] += 1
            row['ThrowAccuracyDeepRating'] += 1
            row['ThrowAccuracyMidRating'] += 1
            row['ThrowAccuracyShortRating'] += 1
            row['ThrowPowerRating'] += 1
            row['ThrowOnTheRunRating'] += 1
            row['ThrowUnderPressureRating'] += 1'''

        '''if row['Position'] in ['HB']:
            row['AwarenessRating'] += 1
            row['CarryingRating'] += 1
            row['BreakTackleRating'] += 1
            row['ThrowAccuracyShortRating'] += 1
            row['StiffArmRating'] += 1
            row['TruckingRating'] += 1
            row['CatchingRating'] += 1'''

        if row['Position'] in ['WR'] and row['OverallRating'] >= 60:
            row['AwarenessRating'] -= 1
            row['CatchingRating'] -= 1
            row['DeepRouteRunningRating'] -= 1
            row['MediumRouteRunningRating'] -= 1
            row['ShortRouteRunningRating'] -= 1
            row['ReleaseRating'] -= 1
            row['CatchInTrafficRating'] -= 1
            row['SpectacularCatchRating'] -= 1

        '''if row['Position'] in ['TE'] and row['OverallRating'] >= 64:
            row['AwarenessRating'] -= 1
            row['CatchingRating'] -= 1
            row['DeepRouteRunningRating'] -= 1
            row['MediumRouteRunningRating'] -= 1
            row['ShortRouteRunningRating'] -= 1
            row['ReleaseRating'] -= 1
            row['CatchInTrafficRating'] -= 1
            row['SpectacularCatchRating'] -= 1'''

        '''if row['Position'] in ['LT'] and row['OverallRating'] <= 58:
            row['AwarenessRating'] += 1
            row['ImpactBlockingRating'] += 1
            row['LeadBlockRating'] += 1
            row['RunBlockFinesseRating'] += 1
            row['RunBlockPowerRating'] += 1
            row['RunBlockRating'] += 1
            row['PassBlockRating'] += 1
            row['PassBlockFinesseRating'] += 1
            row['PassBlockPowerRating'] += 1'''

        '''if row['Position'] in ['LG'] and row['OverallRating'] >= 61:
            row['AwarenessRating'] -= 1
            row['ImpactBlockingRating'] -= 1
            row['LeadBlockRating'] -= 1
            row['RunBlockFinesseRating'] -= 1
            row['RunBlockPowerRating'] -= 1
            row['RunBlockRating'] -= 1
            row['PassBlockRating'] -= 1
            row['PassBlockFinesseRating'] -= 1
            row['PassBlockPowerRating'] -= 1'''
        
        '''if row['Position'] in ['C']:
            row['AwarenessRating'] += 1
            row['ImpactBlockingRating'] += 1
            row['LeadBlockRating'] += 1
            row['RunBlockFinesseRating'] += 1
            row['RunBlockPowerRating'] += 1
            row['RunBlockRating'] += 1
            row['PassBlockRating'] += 1
            row['PassBlockFinesseRating'] += 1
            row['PassBlockPowerRating'] += 1'''

        '''if row['Position'] in ['RG'] and row['OverallRating'] <= 61:
            row['AwarenessRating'] += 1
            row['ImpactBlockingRating'] += 1
            row['LeadBlockRating'] += 1
            row['RunBlockFinesseRating'] += 1
            row['RunBlockPowerRating'] += 1
            row['RunBlockRating'] += 1
            row['PassBlockRating'] += 1
            row['PassBlockFinesseRating'] += 1
            row['PassBlockPowerRating'] += 1'''

        '''if row['Position'] in ['RT'] and row['OverallRating'] <= 59:
            row['AwarenessRating'] += 1
            row['ImpactBlockingRating'] += 1
            row['LeadBlockRating'] += 1
            row['RunBlockFinesseRating'] += 1
            row['RunBlockPowerRating'] += 1
            row['RunBlockRating'] += 1
            row['PassBlockRating'] += 1
            row['PassBlockFinesseRating'] += 1
            row['PassBlockPowerRating'] += 1'''

        '''if row['Position'] in ['LE'] and row['OverallRating'] >= 66:
            row['AwarenessRating'] -= 1
            row['BlockSheddingRating'] -= 1
            row['FinesseMovesRating'] -= 1
            row['PursuitRating'] -= 1
            row['TackleRating'] -= 1
            row['PlayRecognitionRating'] -= 1
            row['PowerMovesRating'] -= 1'''

        '''if row['Position'] in ['RE'] and row['OverallRating'] >= 62:
            row['AwarenessRating'] -= 1
            row['BlockSheddingRating'] -= 1
            row['FinesseMovesRating'] -= 1
            row['PursuitRating'] -= 1
            row['TackleRating'] -= 1
            row['PlayRecognitionRating'] -= 1
            row['PowerMovesRating'] -= 1'''

        '''if row['Position'] in ['DT'] and row['OverallRating'] <= 65:
            row['AwarenessRating'] += 1
            row['BlockSheddingRating'] += 1
            row['FinesseMovesRating'] += 1
            row['PursuitRating'] += 1
            row['TackleRating'] += 1
            row['PlayRecognitionRating'] += 1
            row['PowerMovesRating'] += 1'''

        '''if row['Position'] in ['LOLB'] and row['OverallRating'] <= 60:
            row['AwarenessRating'] += 1
            row['PursuitRating'] += 1
            row['TackleRating'] += 1
            row['PlayRecognitionRating'] += 1
            row['ManCoverageRating'] += 1
            row['ZoneCoverageRating'] += 1
            row['BlockSheddingRating'] += 1'''

        '''if row['Position'] in ['ROLB'] and row['OverallRating'] <= 60:
            row['AwarenessRating'] += 1
            row['PursuitRating'] += 1
            row['TackleRating'] += 1
            row['PlayRecognitionRating'] += 1
            row['ManCoverageRating'] += 1
            row['ZoneCoverageRating'] += 1
            row['BlockSheddingRating'] += 1'''

        '''if row['Position'] in ['MLB'] and row['OverallRating'] >= 67:
            row['AwarenessRating'] -= 2
            row['PursuitRating'] -= 1
            row['TackleRating'] -= 1
            row['PlayRecognitionRating'] -= 1
            row['ManCoverageRating'] -= 1
            row['ZoneCoverageRating'] -= 1
            row['BlockSheddingRating'] -= 1'''

        '''if row['Position'] in ['CB'] and row['OverallRating'] >= 64:
            row['AwarenessRating'] -= 1
            row['PursuitRating'] -= 1
            row['TackleRating'] -= 1
            row['PlayRecognitionRating'] -= 1
            row['ManCoverageRating'] -= 1
            row['PressRating'] -= 1
            row['ZoneCoverageRating'] -= 1'''

        '''if row['Position'] in ['FS'] and row['OverallRating'] >= 99:
            row['AwarenessRating'] -= 1
            row['PursuitRating'] -= 1
            row['TackleRating'] -= 1
            row['PlayRecognitionRating'] -= 1
            row['ManCoverageRating'] -= 1
            row['PressRating'] -= 1
            row['ZoneCoverageRating'] -= 1'''

        '''if row['Position'] in ['SS']:
            row['AwarenessRating'] -= 2
            row['PursuitRating'] -= 1
            row['TackleRating'] -= 1
            row['PlayRecognitionRating'] -= 1
            row['ManCoverageRating'] -= 1
            row['PressRating'] -= 1
            row['ZoneCoverageRating'] -= 1'''
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
df.to_excel('Files/Madden25/IE/Season9/DraftClassPositionEdits.xlsx', index=False)