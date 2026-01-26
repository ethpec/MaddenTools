# Imports
import pandas as pd
import random
import math

# Your File Path
file_path = 'Files/Madden26/IE/Season1/Player.xlsx'

df = pd.read_excel(file_path)

def update_traits(row):
    # Check the player's position and apply changes to specific columns
    contract_status = row['ContractStatus']
    years_pro = row['YearsPro']
    
    #if contract_status in ['FreeAgent', 'Signed', 'PracticeSquad'] and years_pro == 0: ###USE FOR ROOKIES###
    #if contract_status in ['FreeAgent', 'Signed', 'PracticeSquad'] and years_pro >= 1: ###USE FOR NON-ROOKIES###
    if contract_status in ['FreeAgent', 'Signed', 'PracticeSquad'] and years_pro >= 0: ###All###

        # Set ExperiencePoints to 0 for these contract statuses
        row['ExperiencePoints'] = 0

        row['PT_BIGHITTER'] = row['PT_HEADHUNTER']
        row['PT_STRIPSBALL'] = row['PT_PUNCHITOUT']

        # QB Edits
        if row['Position'] == 'QB':

            # QB Generic Trait Chances   
            qb_trait_chances = {
                'PT_LOOKFORSTARS': 0.01,
                'PT_EYESUP': 0.01,
                'PT_TRIGGERHAPPY': 0.01,
                'PT_QUICKCLOCK': 0.01,
                'PT_QUICKTRIGGER': 0.01,
                'PT_SEEINGGHOSTS': 0.01,
                'PT_SETUPTIME': 0.01,
                'PT_THROWAWAY': 0.01,
                'PT_UNUSEDTRAIT1': 0.01,  # Throw It Up
                'PT_COVERBALL': 0.01,
                'PT_HAPPYFEET': 0.01
            }

            for trait, chance in qb_trait_chances.items():
                roll = random.random()
                if roll < chance:          # 1% chance to force True
                    row[trait] = True
                elif roll > 1 - chance:    # 1% chance to force False
                    row[trait] = False

            # For QBs, set a minimum of 70 and a maximum of 90 for InjuryRating
            new_injury_rating = row['InjuryRating'] # - 10
            if new_injury_rating < 70:
                new_injury_rating = 70
            if new_injury_rating > 90:
                new_injury_rating = 90
            row['InjuryRating'] = new_injury_rating
            row['PT_AGGRESSIVEQB'] = row['PT_RISKTAKER']
            row['PT_POCKETPASSER'] = row['PT_SEDENTARY']
            row['PT_SCRAMBLER'] = row['PT_HEROBALL']
            row['PT_SNAPMISCHIEF'] = 'FALSE'
            if row['PT_CONSERVATIVE'] is True:
                row['ZoneCoverageRating'] = 63 + random.randint(0, 5)
            if row['PT_CONSERVATIVE'] is False and row['PT_RISKTAKER'] is False:
                row['ZoneCoverageRating'] = 60 + random.randint(0, 5)
            if row['PT_RISKTAKER'] is True:
                row['ZoneCoverageRating'] = 57 + random.randint(0, 5)
            if row['PT_PARANOID'] is False and row['PT_OBLIVIOUS'] is False:
                row['ManCoverageRating'] = 70 + random.randint (-5, 10)
            if row['PT_PARANOID'] is True:
                row['ManCoverageRating'] = 75 + random.randint (-5, 10)
            if row['PT_OBLIVIOUS'] is True:
                row['ManCoverageRating'] = 65 + random.randint (-5, 10)
            if row['PT_POCKETPASSER'] is True and row['SpeedRating'] < 80:
                row['FinesseMovesRating'] = 5
                row['PowerMovesRating'] = 65
            if row['PT_POCKETPASSER'] is True and row['SpeedRating'] >= 80:
                row['FinesseMovesRating'] = 15
                row['PowerMovesRating'] = 55
            if row['PT_POCKETPASSER'] is False and row['PT_SCRAMBLER'] is False and row['SpeedRating'] < 85:
                row['FinesseMovesRating'] = 20
                row['PowerMovesRating'] = 50
            if row['PT_POCKETPASSER'] is False and row['PT_SCRAMBLER'] is False and row['SpeedRating'] >= 85:
                row['FinesseMovesRating'] = 30
                row['PowerMovesRating'] = 35
            if row['PT_SCRAMBLER'] is True and row['Age'] >= 30:
                row['FinesseMovesRating'] = 40
                row['PowerMovesRating'] = 15
            if row['PT_SCRAMBLER'] is True and row['Age'] < 30:
                row['FinesseMovesRating'] = 50
                row['PowerMovesRating'] = 10
            if row['PT_SCRAMBLER'] is True and row['SpeedRating'] >= 85 and row['Age'] >= 30:
                row['FinesseMovesRating'] = 60
                row['PowerMovesRating'] = 5
            if row['PT_SCRAMBLER'] is True and row['SpeedRating'] >= 85 and row['Age'] < 30:
                row['FinesseMovesRating'] = 75
                row['PowerMovesRating'] = 1
            if row['PT_PARANOID'] is True and row['OverallRating'] >= 85:
                row['PT_PARANOID'] ='FALSE'
            if row['PT_OBLIVIOUS'] is True and row['OverallRating'] >= 85:
                row['PT_OBLIVIOUS'] ='FALSE'
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
                row['FinesseMovesRating'] = overall_rating - 25 - random.randint(0, 12) + random.randint(0, 24)
            elif 70 <= overall_rating <= 74:
                row['FinesseMovesRating'] = overall_rating - 35 - random.randint(0, 14) + random.randint(0, 24)
            elif 1 <= overall_rating <= 69:
                row['FinesseMovesRating'] = 25 - random.randint(0, 15) + random.randint(0, 25)
            row['FinesseMovesRating'] = min(99, row['FinesseMovesRating'])

        # TE Edits
        if row['Position'] == 'TE':
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
                row['FinesseMovesRating'] = overall_rating - 20 - random.randint(0, 12) + random.randint(0, 28)
            elif 1 <= overall_rating <= 69:
                row['FinesseMovesRating'] = 35 - random.randint(0, 12) + random.randint(0, 30)
            row['FinesseMovesRating'] = min(99, row['FinesseMovesRating'])

        # DEF Edits
        if row['Position'] in ['LE', 'RE']:
            row['PlayActionRating'] = 45 + random.randint(0, 15)
            row['BreakSackRating'] = 1
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
            row['PlayActionRating'] = 30 + random.randint(0, 15)
            row['BreakSackRating'] = 9
            overall_rating = row['OverallRating']
            overall_pass_rush_rating = max(row['FinesseMovesRating'], row['PowerMovesRating'])
            dt_true_weight = row['Weight'] + 160
            if 95 <= overall_pass_rush_rating <= 99:
                row['ThrowOnTheRunRating'] = overall_pass_rush_rating - 20 + random.randint(0, 5)
            elif 90 <= overall_pass_rush_rating <= 94:
                row['ThrowOnTheRunRating'] = overall_pass_rush_rating - 25 - random.randint(0, 4) + random.randint(0, 6)
            elif 85 <= overall_pass_rush_rating <= 89:
                row['ThrowOnTheRunRating'] = overall_pass_rush_rating - 30 - random.randint(0, 6) + random.randint(0, 8)
            elif 80 <= overall_pass_rush_rating <= 84:
                row['ThrowOnTheRunRating'] = overall_pass_rush_rating - 35 - random.randint(0, 8) + random.randint(0, 10)
            elif 75 <= overall_pass_rush_rating <= 79:
                row['ThrowOnTheRunRating'] = overall_pass_rush_rating - 40 - random.randint(0, 10) + random.randint(0, 12)
            elif 70 <= overall_pass_rush_rating <= 74:
                row['ThrowOnTheRunRating'] = overall_pass_rush_rating - 45 - random.randint(0, 12) + random.randint(0, 15)
            elif 1 <= overall_pass_rush_rating <= 69:
                row['ThrowOnTheRunRating'] = max(1, overall_pass_rush_rating - 48 - random.randint(0, 12) + random.randint(0, 15))

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
            row['ThrowUnderPressureRating'] = 1 + random.randint(0, 24)
            row['PlayActionRating'] = 50 + random.randint(0, 15)
            row['BreakSackRating'] = 65

        if row['Position'] in ['CB']:
            row['ThrowOnTheRunRating'] = 75 + random.randint(0, 20)          
            row['ThrowUnderPressureRating'] = 1 + random.randint(0, 24)
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
    0: 84,
    1: 96,
    2: 103,
    3: 110,
}

# Set the same values for players with 4 through 6 YearsPro
for years_pro in range(4, 7):
    min_salary_values[years_pro] = 117  # Minimum for years_pro >= 4

# Set the same values for players with 7 through 25 YearsPro
for years_pro in range(7, 26):
    min_salary_values[years_pro] = 125  # Minimum for years_pro >= 7

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


# Track the original DataFrame before applying updates
original_df = df.copy()

# Apply the update_traits function to update the DataFrame
df = df.apply(update_traits, axis=1)

# Apply the adjust_contract_salary function to update the DataFrame
df = df.apply(adjust_contract_salary, axis=1)

# Apply the player_tag_updates function to update the DataFrame
df = df.apply(player_tag_updates, axis=1)

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
df.to_excel('Files/Madden26/IE/Season1/Player_PreseasonEdits.xlsx', index=False)
