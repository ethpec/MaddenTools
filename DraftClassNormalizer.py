# Imports
import pandas as pd
import random
import numpy as np

# Your File Path
file_path = 'Files/Madden25/IE/Season9/Player.xlsx'

df = pd.read_excel(file_path)

# Position Strengths: can adjust as needed
position_strength = {
    'QB': 'Weak',
    'HB': 'Strong',
    'WR': 'Weak',
    'TE': 'Normal',
    'LT': 'Weak',
    'LG': 'Strong',
    'C': 'Strong',
    'RG': 'Weak',
    'RT': 'Weak',
    'LE': 'Weak',
    'DT': 'Normal',
    'RE': 'Strong',
    'LOLB': 'Strong',
    'MLB': 'Weak',
    'ROLB': 'Normal',
    'CB': 'Normal',
    'FS': 'Normal',
    'SS': 'Normal',
}

# Map strength label to numerical modifier
def get_strength_modifier(position):
    strength = position_strength.get(position, 'Normal')
    if strength == 'Weak':
        return -1
    elif strength == 'Strong':
        return 1
    return 0

def update_ratings(row):
    # Check the player's position and apply changes to specific columns
    contract_status = row['ContractStatus']
    
    if contract_status in ['Draft']:
        mod = get_strength_modifier(row['Position'])

        if row['Position'] not in ['K', 'P']:
            row['AwarenessRating'] = row['OverallRating']

        # QB Edits
        if row['Position'] == 'QB':
            row['ThrowAccuracyDeepRating'] = max(0, min(row['ThrowAccuracyDeepRating'] + random.randint(-6, 4) + mod, 99))
            row['ThrowAccuracyMidRating'] = max(0, min(row['ThrowAccuracyMidRating'] + random.randint(-6, 4) + mod, 99))
            row['ThrowAccuracyShortRating'] = max(0, min(row['ThrowAccuracyShortRating'] + random.randint(-8, 4) + mod, 99))
            row['ThrowPowerRating'] = max(0, min(row['ThrowPowerRating'] + random.randint(-5, 4) + mod, 99))
            row['ThrowOnTheRunRating'] = max(0, min(row['ThrowOnTheRunRating'] + random.randint(-5, 4) + mod, 99))
            row['ThrowUnderPressureRating'] = max(0, min(row['ThrowUnderPressureRating'] + random.randint(-5, 4) + mod, 99))
            row['PlayActionRating'] = max(0, min(row['PlayActionRating'] + random.randint(-5, 4) + mod, 99))
            row['SpeedRating'] = max(0, min(row['SpeedRating'] + random.randint(0, 2), 99))
            row['JukeMoveRating'] = max(0, min(row['JukeMoveRating'] + random.randint(0, 2) + mod, 99))
            row['SpinMoveRating'] = max(0, min(row['SpinMoveRating'] + random.randint(0, 2) + mod, 99))

            # Boost Top 4 QB Ratings
            rating_columns = [
                'ThrowAccuracyDeepRating', 'ThrowAccuracyMidRating', 'ThrowAccuracyShortRating',
                'ThrowOnTheRunRating', 'ThrowUnderPressureRating', 'PlayActionRating'
            ]

            for col in rating_columns:
                top_qbs = df[df['Position'] == 'QB'][col].nlargest(4)
                if row[col] in top_qbs.values:
                    row[col] = max(0, min(row[col] + random.randint(1, 5), 99))

        # HB Edits
        if row['Position'] == 'HB':
            row['AgilityRating'] = max(0, min(row['AgilityRating'] + random.randint(-1, 2), 99))
            row['AccelerationRating'] = max(0, min(row['AccelerationRating'] + random.randint(-2, 2), 99))
            row['CarryingRating'] = max(0, min(row['CarryingRating'] + random.randint(-5, 3) + mod, 99))
            row['BreakTackleRating'] = max(0, min(row['BreakTackleRating'] + random.randint(-4, 4) + mod, 99))
            row['ChangeOfDirectionRating'] = max(0, min(row['ChangeOfDirectionRating'] + random.randint(-3, 4), 99))
            row['CatchingRating'] = max(0, min(row['CatchingRating'] + random.randint(-5, 3) + mod, 99))
            row['DeepRouteRunningRating'] = max(0, min(row['DeepRouteRunningRating'] + random.randint(-4, 4) + mod, 99))
            row['JukeMoveRating'] = max(0, min(row['JukeMoveRating'] + random.randint(-4, 3) + mod, 99))
            row['MediumRouteRunningRating'] = max(0, min(row['MediumRouteRunningRating'] + random.randint(-4, 3) + mod, 99))
            row['SpinMoveRating'] = max(0, min(row['SpinMoveRating'] + random.randint(-4, 4) + mod, 99))
            row['ShortRouteRunningRating'] = max(0, min(row['ShortRouteRunningRating'] + random.randint(-4, 3) + mod, 99))
            row['SpeedRating'] = max(0, min(row['SpeedRating'] + random.randint(-1, 1), 99))
            row['StiffArmRating'] = max(0, min(row['StiffArmRating'] + random.randint(-4, 4) + mod, 99))
            row['TruckingRating'] = max(0, min(row['TruckingRating'] + random.randint(-3, 4) + mod, 99))
            row['ReleaseRating'] = max(0, min(row['ReleaseRating'] + random.randint(0, 3) + mod, 99))
            row['BCVisionRating'] = max(0, min(row['BCVisionRating'] + random.randint(-4, 3) + mod, 99))
            row['PassBlockingRating'] = max(0, min(row['PassBlockingRating'] + random.randint(-3, 3) + mod, 99))
            row['KickReturnRating'] = max(0, min(row['KickReturnRating'] + random.randint(-5, 3) + mod, 99))

        # Boost Top 5 HB Ratings
            rating_columns = [
                'CarryingRating', 'BreakTackleRating', 'CatchingRating', 'DeepRouteRunningRating', 'JukeMoveRating',
                'MediumRouteRunningRating', 'SpinMoveRating', 'ShortRouteRunningRating', 'StiffArmRating', 
                'TruckingRating', 'ReleaseRating', 'BCVisionRating', 'PassBlockingRating', 'KickReturnRating'
            ]

            for col in rating_columns:
                # Rank all HBs by this rating column, descending (higher is better)
                top_hbs = df[df['Position'] == 'HB'][col].nlargest(5)

                # If this player is in the top 3, give random boost
                if row[col] in top_hbs.values:
                    row[col] = max(0, min(row[col] + random.randint(1, 5), 99))


        # WR Edits
        if row['Position'] == 'WR':
            row['AgilityRating'] = max(0, min(row['AgilityRating'] + random.randint(-2, 2), 99))
            row['AccelerationRating'] = max(0, min(row['AccelerationRating'] + random.randint(-2, 2), 99))
            row['CatchingRating'] = max(0, min(row['CatchingRating'] + random.randint(-6, 4) + mod, 99))
            row['DeepRouteRunningRating'] = max(0, min(row['DeepRouteRunningRating'] + random.randint(-6, 4) + mod, 99))
            row['MediumRouteRunningRating'] = max(0, min(row['MediumRouteRunningRating'] + random.randint(-6, 4) + mod, 99))
            row['ShortRouteRunningRating'] = max(0, min(row['ShortRouteRunningRating'] + random.randint(-6, 4) + mod, 99))
            row['SpeedRating'] = max(0, min(row['SpeedRating'] + random.randint(-1, 1), 99))
            row['ReleaseRating'] = max(0, min(row['ReleaseRating'] + random.randint(-4, 4) + mod, 99))
            row['CatchInTrafficRating'] = max(0, min(row['CatchInTrafficRating'] + random.randint(-7, 4) + mod, 99))
            row['SpectacularCatchRating'] = max(0, min(row['SpectacularCatchRating'] + random.randint(-8, 4) + mod, 99))
            row['RunBlockingRating'] = max(0, min(row['RunBlockingRating'] + random.randint(-3, 3) + mod, 99))
            row['KickReturnRating'] = max(0, min(row['KickReturnRating'] + random.randint(-5, 3) + mod, 99))

            # Boost Top 8 WR Ratings
            rating_columns = [
                'CatchingRating', 'DeepRouteRunningRating', 'MediumRouteRunningRating',
                'ShortRouteRunningRating', 'ReleaseRating', 'CatchInTrafficRating',
                'SpectacularCatchRating', 'RunBlockingRating', 'KickReturnRating'
            ]

            for col in rating_columns:
                top_wrs = df[df['Position'] == 'WR'][col].nlargest(8)
                if row[col] in top_wrs.values:
                    row[col] = max(0, min(row[col] + random.randint(1, 5), 99))

        # TE Edits
        if row['Position'] == 'TE':
            row['AgilityRating'] = max(0, min(row['AgilityRating'] + random.randint(-2, 2), 99))
            row['AccelerationRating'] = max(0, min(row['AccelerationRating'] + random.randint(-2, 2), 99))
            row['CatchingRating'] = max(0, min(row['CatchingRating'] + random.randint(-7, 4) + mod, 99))
            row['DeepRouteRunningRating'] = max(0, min(row['DeepRouteRunningRating'] + random.randint(-5, 5) + mod, 99))
            row['MediumRouteRunningRating'] = max(0, min(row['MediumRouteRunningRating'] + random.randint(-5, 4) + mod, 99))
            row['ShortRouteRunningRating'] = max(0, min(row['ShortRouteRunningRating'] + random.randint(-6, 4) + mod, 99))
            row['SpeedRating'] = max(0, min(row['SpeedRating'] + random.randint(-1, 1), 99))
            row['ReleaseRating'] = max(0, min(row['ReleaseRating'] + random.randint(-5, 5) + mod, 99))
            row['CatchInTrafficRating'] = max(0, min(row['CatchInTrafficRating'] + random.randint(-5, 4) + mod, 99))
            row['SpectacularCatchRating'] = max(0, min(row['SpectacularCatchRating'] + random.randint(-4, 4) + mod, 99))
            row['BreakTackleRating'] = max(0, min(row['BreakTackleRating'] + random.randint(-3, 5) + mod, 99))
            row['StiffArmRating'] = max(0, min(row['StiffArmRating'] + random.randint(-3, 4) + mod, 99))
            row['TruckingRating'] = max(0, min(row['TruckingRating'] + random.randint(-3, 4) + mod, 99))
            row['JukeMoveRating'] = max(0, min(row['JukeMoveRating'] + random.randint(-2, 4) + mod, 99))
            row['SpinMoveRating'] = max(0, min(row['SpinMoveRating'] + random.randint(-2, 4) + mod, 99))
            row['ImpactBlockingRating'] = max(0, min(row['ImpactBlockingRating'] + random.randint(-3, 4) + mod, 99))
            row['LeadBlockRating'] = max(0, min(row['LeadBlockRating'] + random.randint(-3, 4) + mod, 99))
            row['RunBlockFinesseRating'] = max(0, min(row['RunBlockFinesseRating'] + random.randint(-3, 4) + mod, 99))
            row['RunBlockPowerRating'] = max(0, min(row['RunBlockPowerRating'] + random.randint(-3, 4) + mod, 99))
            row['RunBlockRating'] = max(0, min(row['RunBlockRating'] + random.randint(-3, 4) + mod, 99))

            # Boost Top 4 TE Ratings
            rating_columns = [
                'CatchingRating', 'DeepRouteRunningRating', 'MediumRouteRunningRating',
                'ShortRouteRunningRating', 'ReleaseRating', 'CatchInTrafficRating', 'SpectacularCatchRating',
                'BreakTackleRating', 'StiffArmRating', 'TruckingRating', 'JukeMoveRating',
                'ImpactBlockingRating', 'LeadBlockRating', 'RunBlockFinesseRating', 'RunBlockPowerRating', 'RunBlockRating'
            ]

            for col in rating_columns:
                top_tes = df[df['Position'] == 'TE'][col].nlargest(4)
                if row[col] in top_tes.values:
                    row[col] = max(0, min(row[col] + random.randint(1, 5), 99))

        #OL Edits
        if row['Position'] in ['LT', 'RT']:
            row['ImpactBlockingRating'] = max(0, min(row['ImpactBlockingRating'] + random.randint(-7, 4) + mod, 99))
            row['LeadBlockRating'] = max(0, min(row['LeadBlockRating'] + random.randint(-5, 4) + mod, 99))
            row['RunBlockFinesseRating'] = max(0, min(row['RunBlockFinesseRating'] + random.randint(-5, 5) + mod, 99))
            row['RunBlockPowerRating'] = max(0, min(row['RunBlockPowerRating'] + random.randint(-5, 4) + mod, 99))
            row['RunBlockRating'] = max(0, min(row['RunBlockRating'] + random.randint(-5, 4) + mod, 99))
            row['StrengthRating'] = max(0, min(row['StrengthRating'] + random.randint(-2, 2), 99))
            row['PassBlockRating'] = max(0, min(row['PassBlockRating'] + random.randint(-5, 5) + mod, 99))
            row['PassBlockFinesseRating'] = max(0, min(row['PassBlockFinesseRating'] + random.randint(-5, 4) + mod, 99))
            row['PassBlockPowerRating'] = max(0, min(row['PassBlockPowerRating'] + random.randint(-5, 4) + mod, 99))

            # Boost Top 6 LT/RT Ratings
            rating_columns = [
                'ImpactBlockingRating', 'LeadBlockRating', 'RunBlockFinesseRating', 'RunBlockPowerRating',
                'RunBlockRating', 'PassBlockRating', 'PassBlockFinesseRating', 'PassBlockPowerRating'
            ]

            for col in rating_columns:
                top_tackles = df[df['Position'].isin(['LT', 'RT'])][col].nlargest(6)
                if row[col] in top_tackles.values:
                    row[col] = max(0, min(row[col] + random.randint(1, 5), 99))

        if row['Position'] in ['LG', 'RG']:
            row['ImpactBlockingRating'] = max(0, min(row['ImpactBlockingRating'] + random.randint(-5, 4) + mod, 99))
            row['LeadBlockRating'] = max(0, min(row['LeadBlockRating'] + random.randint(-5, 4) + mod, 99))
            row['RunBlockFinesseRating'] = max(0, min(row['RunBlockFinesseRating'] + random.randint(-5, 5) + mod, 99))
            row['RunBlockPowerRating'] = max(0, min(row['RunBlockPowerRating'] + random.randint(-5, 4) + mod, 99))
            row['RunBlockRating'] = max(0, min(row['RunBlockRating'] + random.randint(-5, 4) + mod, 99))
            row['StrengthRating'] = max(0, min(row['StrengthRating'] + random.randint(-3, 2), 99))
            row['PassBlockRating'] = max(0, min(row['PassBlockRating'] + random.randint(-5, 4) + mod, 99))
            row['PassBlockFinesseRating'] = max(0, min(row['PassBlockFinesseRating'] + random.randint(-5, 4) + mod, 99))
            row['PassBlockPowerRating'] = max(0, min(row['PassBlockPowerRating'] + random.randint(-5, 4) + mod, 99))

            # Boost Top 6 LG/RG Ratings
            rating_columns = [
                'ImpactBlockingRating', 'LeadBlockRating', 'RunBlockFinesseRating', 'RunBlockPowerRating',
                'RunBlockRating', 'PassBlockRating', 'PassBlockFinesseRating', 'PassBlockPowerRating'
            ]

            for col in rating_columns:
                top_guards = df[df['Position'].isin(['LG', 'RG'])][col].nlargest(6)
                if row[col] in top_guards.values:
                    row[col] = max(0, min(row[col] + random.randint(1, 5), 99))

        if row['Position'] in ['C']:
            row['ImpactBlockingRating'] = max(0, min(row['ImpactBlockingRating'] + random.randint(-5, 5) + mod, 99))
            row['LeadBlockRating'] = max(0, min(row['LeadBlockRating'] + random.randint(-5, 4) + mod, 99))
            row['RunBlockFinesseRating'] = max(0, min(row['RunBlockFinesseRating'] + random.randint(-5, 5) + mod, 99))
            row['RunBlockPowerRating'] = max(0, min(row['RunBlockPowerRating'] + random.randint(-5, 5) + mod, 99))
            row['RunBlockRating'] = max(0, min(row['RunBlockRating'] + random.randint(-6, 4) + mod, 99))
            row['StrengthRating'] = max(0, min(row['StrengthRating'] + random.randint(-2, 3), 99))
            row['PassBlockRating'] = max(0, min(row['PassBlockRating'] + random.randint(-5, 4) + mod, 99))
            row['PassBlockFinesseRating'] = max(0, min(row['PassBlockFinesseRating'] + random.randint(-5, 4) + mod, 99))
            row['PassBlockPowerRating'] = max(0, min(row['PassBlockPowerRating'] + random.randint(-5, 4) + mod, 99))

            # Boost Top 3 C Ratings
            rating_columns = [
                'ImpactBlockingRating', 'LeadBlockRating', 'RunBlockFinesseRating', 'RunBlockPowerRating',
                'RunBlockRating', 'PassBlockRating', 'PassBlockFinesseRating', 'PassBlockPowerRating'
            ]

            for col in rating_columns:
                top_centers = df[df['Position'] == 'C'][col].nlargest(3)
                if row[col] in top_centers.values:
                    row[col] = max(0, min(row[col] + random.randint(1, 5), 99))

        # DL Edits
        if row['Position'] in ['LE', 'RE']:
            row['AgilityRating'] = max(0, min(row['AgilityRating'] + random.randint(-2, 3), 99))
            row['AccelerationRating'] = max(0, min(row['AccelerationRating'] + random.randint(-2, 2), 99))
            row['BlockSheddingRating'] = max(0, min(row['BlockSheddingRating'] + random.randint(-5, 5) + mod, 99))
            row['ChangeOfDirectionRating'] = max(0, min(row['ChangeOfDirectionRating'] + random.randint(-3, 4), 99))
            row['FinesseMovesRating'] = max(0, min(row['FinesseMovesRating'] + random.randint(-5, 4) + mod, 99))
            row['SpeedRating'] = max(0, min(row['SpeedRating'] + random.randint(-1, 2), 99))
            row['StrengthRating'] = max(0, min(row['StrengthRating'] + random.randint(-3, 3), 99))
            row['PursuitRating'] = max(0, min(row['PursuitRating'] + random.randint(-6, 4) + mod, 99))
            row['TackleRating'] = max(0, min(row['TackleRating'] + random.randint(-6, 4) + mod, 99))
            row['PlayRecognitionRating'] = max(0, min(row['PlayRecognitionRating'] + random.randint(-5, 6) + mod, 99))
            row['PowerMovesRating'] = max(0, min(row['PowerMovesRating'] + random.randint(-6, 4) + mod, 99))

            # Boost Top 8 Edge Ratings
            rating_columns = [
                'BlockSheddingRating', 'FinesseMovesRating', 'PursuitRating',
                'TackleRating', 'PlayRecognitionRating', 'PowerMovesRating'
            ]

            for col in rating_columns:
                top_edges = df[df['Position'].isin(['LE', 'RE'])][col].nlargest(8)
                if row[col] in top_edges.values:
                    row[col] = max(0, min(row[col] + random.randint(1, 5), 99))

        if row['Position'] in ['DT']:
            row['AgilityRating'] = max(0, min(row['AgilityRating'] + random.randint(-2, 4), 99))
            row['AccelerationRating'] = max(0, min(row['AccelerationRating'] + random.randint(-2, 2), 99))
            row['BlockSheddingRating'] = max(0, min(row['BlockSheddingRating'] + random.randint(-5, 4) + mod, 99))
            row['ChangeOfDirectionRating'] = max(0, min(row['ChangeOfDirectionRating'] + random.randint(-2, 5), 99))
            row['FinesseMovesRating'] = max(0, min(row['FinesseMovesRating'] + random.randint(-5, 5) + mod, 99))
            row['SpeedRating'] = max(0, min(row['SpeedRating'] + random.randint(-1, 3), 99))
            row['StrengthRating'] = max(0, min(row['StrengthRating'] + random.randint(-3, 3), 99))
            row['PursuitRating'] = max(0, min(row['PursuitRating'] + random.randint(-5, 4) + mod, 99))
            row['TackleRating'] = max(0, min(row['TackleRating'] + random.randint(-5, 4) + mod, 99))
            row['PlayRecognitionRating'] = max(0, min(row['PlayRecognitionRating'] + random.randint(-5, 5) + mod, 99))
            row['PowerMovesRating'] = max(0, min(row['PowerMovesRating'] + random.randint(-5, 4) + mod, 99))

            # Boost Top 5 DT Ratings
            rating_columns = [
                'BlockSheddingRating', 'FinesseMovesRating', 'PursuitRating', 
                'TackleRating', 'PlayRecognitionRating', 'PowerMovesRating'
            ]

            for col in rating_columns:
                top_dts = df[df['Position'] == 'DT'][col].nlargest(5)
                if row[col] in top_dts.values:
                    row[col] = max(0, min(row[col] + random.randint(1, 5), 99))

        # LB Edits

        if row['Position'] in ['LOLB', 'ROLB']:
            row['AgilityRating'] = max(0, min(row['AgilityRating'] + random.randint(-2, 2), 99))
            row['AccelerationRating'] = max(0, min(row['AccelerationRating'] + random.randint(-3, 2), 99))
            row['ChangeOfDirectionRating'] = max(0, min(row['ChangeOfDirectionRating'] + random.randint(-3, 2), 99))
            row['SpeedRating'] = max(0, min(row['SpeedRating'] + random.randint(-1, 3), 99))
            row['StrengthRating'] = max(0, min(row['StrengthRating'] + random.randint(-2, 2), 99))
            row['PursuitRating'] = max(0, min(row['PursuitRating'] + random.randint(-7, 4) + mod, 99))
            row['TackleRating'] = max(0, min(row['TackleRating'] + random.randint(-7, 4) + mod, 99))
            row['PlayRecognitionRating'] = max(0, min(row['PlayRecognitionRating'] + random.randint(-7, 4) + mod, 99))
            row['CatchingRating'] = max(0, min(row['CatchingRating'] + random.randint(-3, 3) + mod, 99))
            row['CatchInTrafficRating'] = max(0, min(row['CatchInTrafficRating'] + random.randint(-3, 3) + mod, 99))
            row['ManCoverageRating'] = max(0, min(row['ManCoverageRating'] + random.randint(-5, 7) + mod, 99))
            row['ZoneCoverageRating'] = max(0, min(row['ZoneCoverageRating'] + random.randint(-4, 5) + mod, 99))
            row['HitPowerRating'] = max(0, min(row['HitPowerRating'] + random.randint(-5, 4) + mod, 99))
            row['BlockSheddingRating'] = max(0, min(row['BlockSheddingRating'] + random.randint(-5, 4) + mod, 99))

            # Boost Top 5 OLB Ratings
            rating_columns = [
                'PursuitRating', 'TackleRating', 'PlayRecognitionRating',
                'ManCoverageRating', 'ZoneCoverageRating', 'HitPowerRating', 'BlockSheddingRating'
            ]

            for col in rating_columns:
                top_olbs = df[df['Position'].isin(['LOLB', 'ROLB'])][col].nlargest(5)
                if row[col] in top_olbs.values:
                    row[col] = max(0, min(row[col] + random.randint(1, 5), 99))

        if row['Position'] in ['MLB']:
            row['AgilityRating'] = max(0, min(row['AgilityRating'] + random.randint(-2, 2), 99))
            row['AccelerationRating'] = max(0, min(row['AccelerationRating'] + random.randint(-3, 2), 99))
            row['ChangeOfDirectionRating'] = max(0, min(row['ChangeOfDirectionRating'] + random.randint(-2, 4), 99))
            row['SpeedRating'] = max(0, min(row['SpeedRating'] + random.randint(-2, 3), 99))
            row['StrengthRating'] = max(0, min(row['StrengthRating'] + random.randint(-2, 2), 99))
            row['PursuitRating'] = max(0, min(row['PursuitRating'] + random.randint(-5, 4) + mod, 99))
            row['TackleRating'] = max(0, min(row['TackleRating'] + random.randint(-5, 5) + mod, 99))
            row['PlayRecognitionRating'] = max(0, min(row['PlayRecognitionRating'] + random.randint(-5, 6) + mod, 99))
            row['CatchingRating'] = max(0, min(row['CatchingRating'] + random.randint(-3, 3) + mod, 99))
            row['CatchInTrafficRating'] = max(0, min(row['CatchInTrafficRating'] + random.randint(-3, 3) + mod, 99))
            row['ManCoverageRating'] = max(0, min(row['ManCoverageRating'] + random.randint(-4, 6) + mod, 99))
            row['ZoneCoverageRating'] = max(0, min(row['ZoneCoverageRating'] + random.randint(-4, 5) + mod, 99))
            row['HitPowerRating'] = max(0, min(row['HitPowerRating'] + random.randint(-5, 4) + mod, 99))
            row['BlockSheddingRating'] = max(0, min(row['BlockSheddingRating'] + random.randint(-5, 5) + mod, 99))

            # Boost Top 3 MLB Ratings
            rating_columns = [
                'PursuitRating', 'TackleRating', 'PlayRecognitionRating',
                'ManCoverageRating', 'ZoneCoverageRating', 'HitPowerRating', 'BlockSheddingRating'
            ]

            for col in rating_columns:
                top_mlbs = df[df['Position'] == 'MLB'][col].nlargest(3)
                if row[col] in top_mlbs.values:
                    row[col] = max(0, min(row[col] + random.randint(1, 5), 99))

        # DB Edits
        if row['Position'] == 'CB':
            row['AgilityRating'] = max(0, min(row['AgilityRating'] + random.randint(-2, 2), 99))
            row['AccelerationRating'] = max(0, min(row['AccelerationRating'] + random.randint(-2, 2), 99))
            row['ChangeOfDirectionRating'] = max(0, min(row['ChangeOfDirectionRating'] + random.randint(-2, 2), 99))
            row['SpeedRating'] = max(0, min(row['SpeedRating'] + random.randint(-2, 2), 99))
            row['StrengthRating'] = max(0, min(row['StrengthRating'] + random.randint(-2, 3), 99))
            row['PursuitRating'] = max(0, min(row['PursuitRating'] + random.randint(-4, 2) + mod, 99))
            row['TackleRating'] = max(0, min(row['TackleRating'] + random.randint(-4, 3) + mod, 99))
            row['PlayRecognitionRating'] = max(0, min(row['PlayRecognitionRating'] + random.randint(-4, 5) + mod, 99))
            row['CatchingRating'] = max(0, min(row['CatchingRating'] + random.randint(-4, 4) + mod, 99))
            row['CatchInTrafficRating'] = max(0, min(row['CatchInTrafficRating'] + random.randint(-4, 5) + mod, 99))
            row['ManCoverageRating'] = max(0, min(row['ManCoverageRating'] + random.randint(-8, 4) + mod, 99))
            row['PressRating'] = max(0, min(row['PressRating'] + random.randint(-5, 4) + mod, 99))
            row['ZoneCoverageRating'] = max(0, min(row['ZoneCoverageRating'] + random.randint(-5, 4) + mod, 99))
            row['KickReturnRating'] = max(0, min(row['KickReturnRating'] + random.randint(-5, 3) + mod, 99))

            # Boost Top 8 CB Ratings
            rating_columns = [
                'PursuitRating', 'TackleRating', 'PlayRecognitionRating', 'CatchingRating',
                'CatchInTrafficRating', 'ManCoverageRating', 'PressRating', 'ZoneCoverageRating', 'KickReturnRating'
            ]

            for col in rating_columns:
                top_cbs = df[df['Position'] == 'CB'][col].nlargest(8)
                if row[col] in top_cbs.values:
                    row[col] = max(0, min(row[col] + random.randint(1, 5), 99))

        if row['Position'] in ['FS', 'SS']:
            row['AgilityRating'] = max(0, min(row['AgilityRating'] + random.randint(-2, 2), 99))
            row['AccelerationRating'] = max(0, min(row['AccelerationRating'] + random.randint(-2, 2), 99))
            row['ChangeOfDirectionRating'] = max(0, min(row['ChangeOfDirectionRating'] + random.randint(-2, 2), 99))
            row['SpeedRating'] = max(0, min(row['SpeedRating'] + random.randint(-2, 2), 99))
            row['StrengthRating'] = max(0, min(row['StrengthRating'] + random.randint(-2, 2), 99))
            row['PursuitRating'] = max(0, min(row['PursuitRating'] + random.randint(-6, 4) + mod, 99))
            row['TackleRating'] = max(0, min(row['TackleRating'] + random.randint(-5, 4) + mod, 99))
            row['PlayRecognitionRating'] = max(0, min(row['PlayRecognitionRating'] + random.randint(-4, 10) + mod, 99))
            row['CatchingRating'] = max(0, min(row['CatchingRating'] + random.randint(-5, 4) + mod, 99))
            row['CatchInTrafficRating'] = max(0, min(row['CatchInTrafficRating'] + random.randint(-4, 5) + mod, 99))
            row['ManCoverageRating'] = max(0, min(row['ManCoverageRating'] + random.randint(-8, 4) + mod, 99))
            row['PressRating'] = max(0, min(row['PressRating'] + random.randint(-6, 4) + mod, 99))
            row['ZoneCoverageRating'] = max(0, min(row['ZoneCoverageRating'] + random.randint(-8, 4) + mod, 99))
            row['HitPowerRating'] = max(0, min(row['HitPowerRating'] + random.randint(-5, 5) + mod, 99))
            row['KickReturnRating'] = max(0, min(row['KickReturnRating'] + random.randint(-5, 3) + mod, 99))

            # Boost Top 6 FS/SS Ratings
            rating_columns = [
                'PursuitRating', 'TackleRating', 'PlayRecognitionRating', 'CatchingRating', 'CatchInTrafficRating',
                'ManCoverageRating', 'PressRating', 'ZoneCoverageRating', 'HitPowerRating', 'KickReturnRating'
            ]

            for col in rating_columns:
                top_safeties = df[df['Position'].isin(['FS', 'SS'])][col].nlargest(6)
                if row[col] in top_safeties.values:
                    row[col] = max(0, min(row[col] + random.randint(1, 5), 99))

        # K and P Edits
        if row['Position'] in ['K']:
            row['KickAccuracyRating'] = max(0, min(row['KickAccuracyRating'] + random.randint(-4, 6), 99))
            row['KickPowerRating'] = max(0, min(row['KickPowerRating'] + random.randint(-4, 4), 99))

            # Boost Top 2 K Ratings
            rating_columns = [
                'KickAccuracyRating', 'KickPowerRating'
            ]

            for col in rating_columns:
                top_kickers = df[df['Position'] == 'K'][col].nlargest(2)
                if row[col] in top_kickers.values:
                    row[col] = max(0, min(row[col] + random.randint(1, 2), 99))

        if row['Position'] in ['P']:
            row['KickAccuracyRating'] = max(0, min(row['KickAccuracyRating'] + random.randint(-4, 5), 99))
            row['KickPowerRating'] = max(0, min(row['KickPowerRating'] + random.randint(-4, 4), 99))

            # Boost Top 2 P Ratings
            rating_columns = [
                'KickAccuracyRating', 'KickPowerRating'
            ]

            for col in rating_columns:
                top_punters = df[df['Position'] == 'P'][col].nlargest(2)
                if row[col] in top_punters.values:
                    row[col] = max(0, min(row[col] + random.randint(1, 2), 99))

        if row['Position'] in ['LS']:
            row['LongSnapRating'] = max(0, min(row['KickAccuracyRating'] + random.randint(-4, 3), 99))

            # Boost Top 1 LS Ratings
            rating_columns = [
                'LongSnapRating'
            ]

            for col in rating_columns:
                top_ls = df[df['Position'] == 'LS'][col].nlargest(1)
                if row[col] in top_ls.values:
                    row[col] = max(0, min(row[col] + random.randint(1, 3), 99))

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