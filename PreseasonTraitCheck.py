# Imports
import pandas as pd
import random
import math
from config import season_path

# Your File Path
player_file_path = season_path('Player.xlsx')

df = pd.read_excel(player_file_path)

def update_traits(row):
    # Check the player's position and apply changes to specific columns
    contract_status = row['ContractStatus']
    years_pro = row['YearsPro']
    
    #if contract_status in ['FreeAgent', 'Signed', 'PracticeSquad'] and years_pro == 0: ###USE FOR ROOKIES###
    #if contract_status in ['FreeAgent', 'Signed', 'PracticeSquad'] and years_pro >= 1: ###USE FOR NON-ROOKIES###
    if contract_status in ['FreeAgent', 'Signed', 'PracticeSquad'] and years_pro >= 0: ###All###

        # Set ExperiencePoints to 0 for these contract statuses
        row['ExperiencePoints'] = 0

        #row['PT_BIGHITTER'] = row['PT_HEADHUNTER']
        #row['PT_STRIPSBALL'] = row['PT_PUNCHITOUT']

        # QB Edits
        if row['Position'] == 'QB':

            # For QBs, set a minimum of 70 and a maximum of 90 for InjuryRating
            new_injury_rating = row['InjuryRating'] # - 10
            if new_injury_rating < 70:
                new_injury_rating = 70
            if new_injury_rating > 90:
                new_injury_rating = 90
            row['InjuryRating'] = new_injury_rating
            row['TRAIT_COVER_BALL'] = 'OnMediumHits'
            row['TRAIT_THROWAWAY'] = 'FALSE' # Keep this for Madden 25 #
            if row['SpeedRating'] <= 76:
                row['TRAIT_QBSTYLE'] = 'Pocket'
            if row['SpeedRating'] <= 79 and row['TRAIT_QBSTYLE'] == 'Scrambling':
                row['TRAIT_QBSTYLE'] = 'Balanced'
            if 'Conservative' in row['TRAIT_DECISION_MAKER']:
                row['ZoneCoverageRating'] = 65 + random.randint(0, 5)
            if 'Ideal' in row['TRAIT_DECISION_MAKER']:
                row['ZoneCoverageRating'] = 60 + random.randint(0, 5)
            if 'Aggressive' in row['TRAIT_DECISION_MAKER']:
                row['ZoneCoverageRating'] = 55 + random.randint(0, 5)
            if row['TRAIT_SENSE_PRESSURE'] == 'Ideal':
                row['ManCoverageRating'] = 80 + random.randint (-5, 10)
            if row['TRAIT_SENSE_PRESSURE'] == 'Average':
                row['ManCoverageRating'] = 70 + random.randint (-5, 10)
            if row['TRAIT_SENSE_PRESSURE'] == 'Paranoid':
                row['ManCoverageRating'] = 70 + random.randint (-5, 10)
            if row['TRAIT_SENSE_PRESSURE'] == 'TriggerHappy':
                row['ManCoverageRating'] = 60 + random.randint (-5, 10)
            if row['TRAIT_SENSE_PRESSURE'] == 'Oblivious':
                row['ManCoverageRating'] = 60 + random.randint (-5, 10)
            if row['TRAIT_QBSTYLE'] =='Pocket':
                row['FinesseMovesRating'] = 5
                row['PowerMovesRating'] = 60
            if row['TRAIT_QBSTYLE'] =='Balanced':
                row['FinesseMovesRating'] = 20
                row['PowerMovesRating'] = 40
            if row['TRAIT_QBSTYLE'] =='Scrambling' and row['Age'] >= 30:
                row['FinesseMovesRating'] = 40
                row['PowerMovesRating'] = 15
            if row['TRAIT_QBSTYLE'] =='Scrambling' and row['Age'] < 30:
                row['FinesseMovesRating'] = 50
                row['PowerMovesRating'] = 10
            if row['TRAIT_QBSTYLE'] =='Scrambling' and row['SpeedRating'] >= 88 and row['Age'] >= 30:
                row['FinesseMovesRating'] = 60
                row['PowerMovesRating'] = 5
            if row['TRAIT_QBSTYLE'] =='Scrambling' and row['SpeedRating'] >= 88 and row['Age'] < 30:
                row['FinesseMovesRating'] = 75
                row['PowerMovesRating'] = 1
            if row['Age'] >= 30:
                row['SpeedRating'] = max(50, row['SpeedRating'] - 1)
                row['AccelerationRating'] = max(50, row['AccelerationRating'] - 1)
                row['AgilityRating'] = max(50, row['AgilityRating'] - 1)
                row['ChangeOfDirectionRating'] = max(50, row['ChangeOfDirectionRating'] - 1)
            throw_accuracy_average = (row['ThrowAccuracyShortRating'] + row['ThrowAccuracyMidRating'] + row['ThrowAccuracyDeepRating']) / 3
            throw_accuracy_average = math.ceil(throw_accuracy_average)
            row['ThrowAccuracyRating'] = throw_accuracy_average
          
        # HB Edits
        if row['Position'] == 'HB':
            # For HBs, set a minimum of 70 and a maximum of 90 for InjuryRating
            new_injury_rating = row['InjuryRating'] # - 10
            if new_injury_rating < 70:
                new_injury_rating = 70
            if new_injury_rating > 90:
                new_injury_rating = 90
            row['InjuryRating'] = new_injury_rating
            row['TRAIT_YACCATCH'] = 'TRUE'
            row['TRAIT_POSSESSIONCATCH'] = 'TRUE'
            row['TRAIT_HIGHPOINTCATCH'] = 'TRUE'
            row['ThrowUnderPressureRating'] = 25
            row['PowerMovesRating'] = 25
            row['PlayActionRating'] = 25

            rb_targets = round((row['CatchingRating'] + row['CatchInTrafficRating'] + row['ShortRouteRunningRating']) / 3)
            if 75 <= rb_targets <= 99:
                adjusted_rbtargets = rb_targets + 5 + random.randint(0, 10) - random.randint(0, 5)
            elif 70 <= rb_targets <= 74:
                adjusted_rbtargets = rb_targets + random.randint(0, 9) - random.randint(0, 5)
            elif 65 <= rb_targets <= 69:
                adjusted_rbtargets = rb_targets - 10 + random.randint(0, 8) - random.randint(0, 5)
            elif 60 <= rb_targets <= 64:
                adjusted_rbtargets = rb_targets - 20 + random.randint(0, 7) - random.randint(0, 5)
            else:
                adjusted_rbtargets = rb_targets - 25 + random.randint(0, 6) - random.randint(0, 5)
            row['FinesseMovesRating'] = min(99, adjusted_rbtargets)

        # WR Edits
        if row['Position'] == 'WR':
            row['TRAIT_YACCATCH'] = 'TRUE'
            row['TRAIT_POSSESSIONCATCH'] = 'TRUE'
            row['TRAIT_HIGHPOINTCATCH'] = 'TRUE'            
            row['PowerMovesRating'] = 75
            row['PlayActionRating'] = 25
            overall_rating = row['OverallRating']
            if 95 <= overall_rating <= 99:
                row['FinesseMovesRating'] = overall_rating - 2 - random.randint(0, 2) + random.randint(0, 4)
            elif 90 <= overall_rating <= 94:
                row['FinesseMovesRating'] = overall_rating - 5 - random.randint(0, 4) + random.randint(0, 8)
            elif 85 <= overall_rating <= 89:
                row['FinesseMovesRating'] = overall_rating - 10 - random.randint(0, 6) + random.randint(0, 12)
            elif 80 <= overall_rating <= 84:
                row['FinesseMovesRating'] = overall_rating - 20 - random.randint(0, 8) + random.randint(0, 24)
            elif 75 <= overall_rating <= 79:
                row['FinesseMovesRating'] = overall_rating - 30 - random.randint(0, 12) + random.randint(0, 24)
            elif 70 <= overall_rating <= 74:
                row['FinesseMovesRating'] = overall_rating - 35 - random.randint(0, 14) + random.randint(0, 24)
            elif 1 <= overall_rating <= 69:
                row['FinesseMovesRating'] = 25 - random.randint(0, 15) + random.randint(0, 25)
            row['FinesseMovesRating'] = min(99, row['FinesseMovesRating'])

        # TE Edits
        if row['Position'] == 'TE':
            row['TRAIT_YACCATCH'] = 'TRUE'
            row['TRAIT_POSSESSIONCATCH'] = 'TRUE'
            row['TRAIT_HIGHPOINTCATCH'] = 'TRUE'
            row['PowerMovesRating'] = 50
            row['PlayActionRating'] = 25
            overall_rating = row['OverallRating']
            if 95 <= overall_rating <= 99:
                row['FinesseMovesRating'] = overall_rating - random.randint(0, 2) + random.randint(0, 4)
            elif 90 <= overall_rating <= 94:
                row['FinesseMovesRating'] = overall_rating - 2 - random.randint(0, 4) + random.randint(0, 8)
            elif 85 <= overall_rating <= 89:
                row['FinesseMovesRating'] = overall_rating - 5 - random.randint(0, 6) + random.randint(0, 12)
            elif 80 <= overall_rating <= 84:
                row['FinesseMovesRating'] = overall_rating - 10 - random.randint(0, 8) + random.randint(0, 24)
            elif 75 <= overall_rating <= 79:
                row['FinesseMovesRating'] = overall_rating - 20 - random.randint(0, 12) + random.randint(0, 26)
            elif 70 <= overall_rating <= 74:
                row['FinesseMovesRating'] = overall_rating - 20 - random.randint(0, 12) + random.randint(0, 30)
            elif 1 <= overall_rating <= 69:
                row['FinesseMovesRating'] = 35 - random.randint(0, 12) + random.randint(0, 32)
            row['FinesseMovesRating'] = min(99, row['FinesseMovesRating'])

        # REC Deep catch ability
        if row['Position'] in ['HB','FB','WR','TE']:
            deep_rec_rating = row['DeepRouteRunningRating']
            if 90 <= deep_rec_rating <= 99:
                row['BlockSheddingRating'] = deep_rec_rating
            elif 85 <= deep_rec_rating <= 89:
                row['BlockSheddingRating'] = deep_rec_rating - 5 - random.randint(0, 3) + random.randint(0, 3)
            elif 80 <= deep_rec_rating <= 84:
                row['BlockSheddingRating'] = deep_rec_rating - 10 - random.randint(0, 3) + random.randint(0, 3)
            elif 75 <= deep_rec_rating <= 79:
                row['BlockSheddingRating'] = deep_rec_rating - 15 - random.randint(0, 4) + random.randint(0, 4)
            elif 70 <= deep_rec_rating <= 74:
                row['BlockSheddingRating'] = deep_rec_rating - 20 - random.randint(0, 4) + random.randint(0, 4)
            elif 1 <= deep_rec_rating <= 69:
                row['BlockSheddingRating'] = deep_rec_rating - 25 - random.randint(0, 5) + random.randint(0, 5)
            row['BlockSheddingRating'] = max(1, row['BlockSheddingRating'])

        # DEF Edits
        if row['Position'] in ['LE', 'RE']:
            row['TRAIT_DLSWIM'] = 'TRUE'
            row['TRAIT_DLSPIN'] = 'TRUE'
            row['TRAIT_DLBULLRUSH'] = 'TRUE'
            row['PlayActionRating'] = 45 + random.randint(0, 15)
            row['BreakSackRating'] = 1 # Positional Tackle modifier (SIM STATS)
            overall_rating = row['OverallRating']
            if 95 <= overall_rating <= 99:
                row['ThrowOnTheRunRating'] = overall_rating
            elif 90 <= overall_rating <= 94:
                row['ThrowOnTheRunRating'] = overall_rating - random.randint(0, 4) + random.randint(0, 5)
            elif 85 <= overall_rating <= 89:
                row['ThrowOnTheRunRating'] = overall_rating - random.randint(0, 6) + random.randint(0, 8)
            elif 80 <= overall_rating <= 84:
                row['ThrowOnTheRunRating'] = overall_rating - random.randint(0, 8) + random.randint(0, 10)
            elif 75 <= overall_rating <= 79:
                row['ThrowOnTheRunRating'] = overall_rating - random.randint(0, 10) + random.randint(0, 12)
            elif 70 <= overall_rating <= 74:
                row['ThrowOnTheRunRating'] = overall_rating - random.randint(0, 12) + random.randint(0, 15)
            elif 1 <= overall_rating <= 69:
                row['ThrowOnTheRunRating'] = overall_rating - random.randint(0, 15) + random.randint(0, 15)

        if row['Position'] in ['DT']:
            row['TRAIT_DLSWIM'] = 'TRUE'
            row['TRAIT_DLSPIN'] = 'TRUE'
            row['TRAIT_DLBULLRUSH'] = 'TRUE'
            row['PlayActionRating'] = 30 + random.randint(0, 15)
            row['BreakSackRating'] = 9
            overall_rating = row['OverallRating']
            overall_pass_rush_rating = max(row['FinesseMovesRating'], row['PowerMovesRating'])
            dt_true_weight = row['Weight'] + 160
            if 95 <= overall_pass_rush_rating <= 99:
                row['ThrowOnTheRunRating'] = max(1, overall_pass_rush_rating - 40 - random.randint(0, 2) + random.randint(0, 4))
            elif 90 <= overall_pass_rush_rating <= 94:
                row['ThrowOnTheRunRating'] = max(1, overall_pass_rush_rating - 45 - random.randint(0, 4) + random.randint(0, 6))
            elif 85 <= overall_pass_rush_rating <= 89:
                row['ThrowOnTheRunRating'] = max(1, overall_pass_rush_rating - 50 - random.randint(0, 6) + random.randint(0, 8))
            elif 80 <= overall_pass_rush_rating <= 84:
                row['ThrowOnTheRunRating'] = max(1, overall_pass_rush_rating - 55 - random.randint(0, 8) + random.randint(0, 10))
            elif 75 <= overall_pass_rush_rating <= 79:
                row['ThrowOnTheRunRating'] = max(1, overall_pass_rush_rating - 60 - random.randint(0, 10) + random.randint(0, 12))
            elif 70 <= overall_pass_rush_rating <= 74:
                row['ThrowOnTheRunRating'] = max(1, overall_pass_rush_rating - 65 - random.randint(0, 12) + random.randint(0, 15))
            elif 1 <= overall_pass_rush_rating <= 69:
                row['ThrowOnTheRunRating'] = max(1, overall_pass_rush_rating - 58 - random.randint(0, 12) + random.randint(0, 15))

            # Nose Tackle Logic #
            if dt_true_weight >= 325:
                row['ThrowAccuracyDeepRating'] = min(overall_rating + 5, 99)
            elif 310 <= dt_true_weight < 325:
                row['ThrowAccuracyDeepRating'] = max(overall_rating - 5, 1)
            elif 300 <= dt_true_weight < 310:
                row['ThrowAccuracyDeepRating'] = max(overall_rating - 15, 1)
            elif 290 <= dt_true_weight < 300:
                row['ThrowAccuracyDeepRating'] = max(overall_rating - 25, 1)
            else:
                row['ThrowAccuracyDeepRating'] = 25            

        if row['Position'] in ['LOLB', 'MLB', 'ROLB']:
            row['ThrowOnTheRunRating'] = 45 + random.randint(0, 20)
            row['ThrowUnderPressureRating'] = 1 + random.randint(0, 19)
            row['PlayActionRating'] = 50 + random.randint(0, 15)
            row['BreakSackRating'] = 65

        if row['Position'] in ['CB']:
            row['ThrowOnTheRunRating'] = 75 + random.randint(0, 20)          
            row['ThrowUnderPressureRating'] = 6 + random.randint(0, 24)
            row['PlayActionRating'] = 15 + random.randint(0, 15)
            row['BreakSackRating'] = 70

        if row['Position'] in ['FS', 'SS']:
            row['ThrowOnTheRunRating'] = 75 + random.randint(0, 20)      
            row['ThrowUnderPressureRating'] = 75 + random.randint(0, 24)
            row['PlayActionRating'] = 80 + random.randint(0, 15)
            row['BreakSackRating'] = 70

        # For all other positions, set a minimum of 70 and a maximum of 90 for InjuryRating
        if row['Position'] not in ['HB', 'QB']:

            new_injury_rating = row['InjuryRating'] # - 10
            if new_injury_rating < 70:
                new_injury_rating = 70
            if new_injury_rating > 90:
                new_injury_rating = 90
            row['InjuryRating'] = new_injury_rating

    # Add more conditions and changes for other columns and positions as needed
    return row

# Define target values for ContractSalary0 and ContractSalary1 based on years_pro
min_salary_values = {
    0: 89,
    1: 100,
    2: 108,
    3: 115,
}

# Set the same values for players with 4 through 6 YearsPro
for years_pro in range(4, 7):
    min_salary_values[years_pro] = 122  # Minimum for years_pro >= 4

# Set the same values for players with 7 through 25 YearsPro
for years_pro in range(7, 26):
    min_salary_values[years_pro] = 130  # Minimum for years_pro >= 7

# Function to adjust Salary to league minimum
def adjust_contract_salary(row):
    contract_status = row['ContractStatus']
    years_pro = row['YearsPro']
    contract_salary_0 = row['ContractSalary0']
    contract_salary_1 = row['ContractSalary1']
    contract_salary_2 = row['ContractSalary2']
    contract_salary_3 = row['ContractSalary3']

    if contract_status == 'Signed':
        if years_pro in min_salary_values:
            target_salary = min_salary_values[years_pro]
            if contract_salary_0 != 0 and contract_salary_0 < target_salary:
                row['ContractSalary0'] = target_salary
            if contract_salary_1 != 0 and contract_salary_1 < target_salary:
                row['ContractSalary1'] = target_salary
            if contract_salary_2 != 0 and contract_salary_2 < target_salary:
                row['ContractSalary2'] = target_salary
            if contract_salary_3 != 0 and contract_salary_3 < target_salary:
                row['ContractSalary3'] = target_salary

    return row

def player_tag_updates(row):
    tag1 = row['Tag1']
    tag2 = row['Tag2']
    contract_status = row['ContractStatus']
    years_pro = row['YearsPro']
    overall_rating = row['OverallRating']
    position = row['Position']

    # Set ExperiencePoints = 0 for all players
    row['ExperiencePoints'] = 0
    
    # Check if Tag1 and Tag2 have "NoRole"
    if tag1 == 'NoRole' and tag2 == 'NoRole' and contract_status == 'Signed':
        # General Young Player Checks
        if 0 <= years_pro <= 1 and overall_rating >= 73 and position not in ['QB', 'HB', 'FB', 'WR', 'CB', 'K', 'P']:
            row['Tag1'] = 'Day1Starter'

        if 0 <= years_pro <= 1 and 68 <= overall_rating <= 72 and position not in ['QB', 'HB', 'FB', 'WR', 'CB', 'K', 'P']:
            row['Tag1'] = 'FutureStarter'

        # HB, WR, CB Young Player Checks
        if 0 <= years_pro <= 1 and overall_rating >= 75 and position in ['HB', 'WR', 'CB']:
            row['Tag1'] = 'Day1Starter'

        if 0 <= years_pro <= 1 and 70 <= overall_rating <= 74 and position in ['HB', 'WR', 'CB']:
            row['Tag1'] = 'FutureStarter'

        # Veteran Checks
        if 4 <= years_pro <= 9 and 65 <= overall_rating <= 79 and position not in ['QB', 'FB', 'K', 'P']:
            row['Tag1'] = 'BridgePlayer'

        if years_pro >= 10 and overall_rating >= 75 and position not in ['QB', 'FB', 'K', 'P']:
            row['Tag1'] = 'Mentor'

        # QB Checks
        if 1 <= years_pro <= 2 and position == 'QB' and 74 <= overall_rating <= 79:
            row['Tag1'] = 'QBofTheFuture'

        if years_pro == 0 and position == 'QB' and 67 <= overall_rating <= 79:
            row['Tag1'] = 'QBofTheFuture'

        if position == 'QB' and overall_rating >= 80:
            row['Tag1'] = 'FranchiseQB'

        if years_pro >= 4 and position == 'QB' and 68 <= overall_rating <= 72:
            row['Tag1'] = 'BridgeQB'
    
    return row

def player_personality_change(row):
    # 1% chance to gain 15 PersonalityRating, 1% chance to lose 15 (clamped 60-90)
    contract_status = row['ContractStatus']
    personality_rating = row['PersonalityRating']

    if contract_status not in ['FreeAgent', 'Signed', 'PracticeSquad']:
        return row

    if pd.isna(personality_rating):
        return row

    roll = random.randint(1, 100)
    if roll == 1:
        new_personality_rating = personality_rating + 15
    elif roll == 2:
        new_personality_rating = personality_rating - 15
    else:
        return row

    if new_personality_rating < 60:
        new_personality_rating = 60
    if new_personality_rating > 90:
        new_personality_rating = 90
    row['PersonalityRating'] = new_personality_rating

    return row

def player_ego_change(row):
    # Chance to gain or lose 20 PLYR_EGO based on OverallRating (clamped 15-95)
    contract_status = row['ContractStatus']
    overall_rating = row['OverallRating']
    ego_rating = row['PLYR_EGO']

    if contract_status not in ['FreeAgent', 'Signed', 'PracticeSquad']:
        return row

    if pd.isna(ego_rating):
        return row

    if overall_rating >= 90:
        increase_chance = 8
        decrease_chance = 2
    elif 80 <= overall_rating <= 89:
        increase_chance = 7
        decrease_chance = 3
    elif 70 <= overall_rating <= 79:
        increase_chance = 5
        decrease_chance = 5
    else:
        increase_chance = 4
        decrease_chance = 6

    roll = random.randint(1, 100)
    if roll <= increase_chance:
        new_ego_rating = ego_rating + 20
    elif roll <= increase_chance + decrease_chance:
        new_ego_rating = ego_rating - 20
    else:
        return row

    if new_ego_rating < 15:
        new_ego_rating = 15
    if new_ego_rating > 95:
        new_ego_rating = 95
    row['PLYR_EGO'] = new_ego_rating

    return row


# Track the original DataFrame before applying updates
original_df = df.copy()

# Apply the update_traits function to update the DataFrame
df = df.apply(update_traits, axis=1)

# Apply the adjust_contract_salary function to update the DataFrame
df = df.apply(adjust_contract_salary, axis=1)

# Apply the player_tag_updates function to update the DataFrame
df = df.apply(player_tag_updates, axis=1)

# Apply the player_personality_change function to update the DataFrame
df = df.apply(player_personality_change, axis=1)

# Apply the player_ego_change function to update the DataFrame
df = df.apply(player_ego_change, axis=1)

# Create a set to store column names with edits
columns_with_edits = set()

# Check if the column values in df are equal to original_df, considering data type differences
for column in df.columns:
    if not df[column].equals(original_df[column]):
        columns_with_edits.add(column)

# Create a list to store columns to be removed
columns_to_remove = []

# Check if a column doesn't have any edits, then add it to the list of columns to be removed
for column in df.columns:
    if column not in columns_with_edits:
        columns_to_remove.append(column)

# Drop columns with no edits
df.drop(columns=columns_to_remove, inplace=True)

output_filename = 'Player_PreseasonEdits.xlsx'
df.to_excel(season_path('Player_PreseasonEdits.xlsx'), index=False)
