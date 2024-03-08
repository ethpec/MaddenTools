# Imports
import pandas as pd
import random
import math

# Your File Path
file_path = 'Files/Madden24/IE/Season3/Player.xlsx'

df = pd.read_excel(file_path)

def update_traits(row):
    # Check the player's position and apply changes to specific columns
    contract_status = row['ContractStatus']
    
    if contract_status in ['FreeAgent', 'Signed', 'PracticeSquad']:

        # QB Edits
        if row['Position'] == 'QB':
            # For QBs, set a minimum of 73 and a maximum of 85 for InjuryRating
            new_injury_rating = row['InjuryRating'] # - 10
            # Ensure the new value is within the specified range
            if new_injury_rating < 73:
                new_injury_rating = 73
            if new_injury_rating > 85:
                new_injury_rating = 85
            row['InjuryRating'] = new_injury_rating
            row['TRAIT_THROWAWAY'] = 'TRUE'
            row['TRAIT_COVER_BALL'] = 'OnMediumHits'
            if row['SpeedRating'] <= 76:
                row['TRAIT_QBSTYLE'] = 'Pocket'
            if 'Conservative' in row['TRAIT_FORCE_PASS']:
                row['ZoneCoverageRating'] = 63 + random.randint(0, 5)
            if 'Ideal' in row['TRAIT_FORCE_PASS']:
                row['ZoneCoverageRating'] = 60 + random.randint(0, 5)
            if 'Aggressive' in row['TRAIT_FORCE_PASS']:
                row['ZoneCoverageRating'] = 57 + random.randint(0, 5)
            throw_accuracy_average = (row['ThrowAccuracyShortRating'] + row['ThrowAccuracyMidRating'] + row['ThrowAccuracyDeepRating']) / 3
            throw_accuracy_average = math.ceil(throw_accuracy_average)
            row['ThrowAccuracyRating'] = throw_accuracy_average
          
        # HB Edits
        if row['Position'] == 'HB':
            # For HBs, set a minimum of 78 and a maximum of 90 for InjuryRating
            new_injury_rating = row['InjuryRating'] # - 5
            # Ensure the new value is within the specified range
            if new_injury_rating < 78:
                new_injury_rating = 78
            if new_injury_rating > 90:
                new_injury_rating = 90
            row['InjuryRating'] = new_injury_rating
            row['TRAIT_YACCATCH'] = 'TRUE'
            row['TRAIT_POSSESSIONCATCH'] = 'TRUE'
            row['TRAIT_HIGHPOINTCATCH'] = 'TRUE'
            rb_targets = row['CatchingRating']
            adjusted_rbtargets = rb_targets + 5
            row['ZoneCoverageRating'] = min(99, adjusted_rbtargets)

        # WR Edits
        if row['Position'] == 'WR':
            row['TRAIT_YACCATCH'] = 'TRUE'
            row['TRAIT_POSSESSIONCATCH'] = 'TRUE'
            row['TRAIT_HIGHPOINTCATCH'] = 'TRUE'
            overall_rating = row['OverallRating']
            if 95 <= overall_rating <= 99:
                row['ZoneCoverageRating'] = 99
            elif 90 <= overall_rating <= 94:
                row['ZoneCoverageRating'] = overall_rating
            elif 85 <= overall_rating <= 89:
                row['ZoneCoverageRating'] = overall_rating - 10 + random.randint(0, 5)
            elif 80 <= overall_rating <= 84:
                row['ZoneCoverageRating'] = overall_rating - 20 + random.randint(0, 5)
            elif 75 <= overall_rating <= 79:
                row['ZoneCoverageRating'] = overall_rating - 35 + random.randint(0, 5)
            elif 70 <= overall_rating <= 74:
                row['ZoneCoverageRating'] = overall_rating - 40 + random.randint(0, 5)
            elif 1 <= overall_rating <= 69:
                row['ZoneCoverageRating'] = 20 + random.randint(0, 10)

        # TE Edits
        if row['Position'] == 'TE':
            row['TRAIT_YACCATCH'] = 'TRUE'
            row['TRAIT_POSSESSIONCATCH'] = 'TRUE'
            row['TRAIT_HIGHPOINTCATCH'] = 'TRUE'
            overall_rating = row['OverallRating']
            if 95 <= overall_rating <= 99:
                row['ZoneCoverageRating'] = overall_rating - 5 + random.randint(0, 2)
            elif 90 <= overall_rating <= 94:
                row['ZoneCoverageRating'] = overall_rating - 5 + random.randint(0, 5)
            elif 85 <= overall_rating <= 89:
                row['ZoneCoverageRating'] = overall_rating - 15 + random.randint(0, 5)
            elif 80 <= overall_rating <= 84:
                row['ZoneCoverageRating'] = overall_rating - 25 + random.randint(0, 5)
            elif 75 <= overall_rating <= 79:
                row['ZoneCoverageRating'] = overall_rating - 40 + random.randint(0, 5)
            elif 70 <= overall_rating <= 74:
                row['ZoneCoverageRating'] = overall_rating - 45 + random.randint(0, 5)
            elif 1 <= overall_rating <= 69:
                row['ZoneCoverageRating'] = 15 + random.randint(0, 10)

        # DEF Edits
        if row['Position'] in ['LE', 'RE']:
            row['TRAIT_DLSWIM'] = 'TRUE'
            row['TRAIT_DLSPIN'] = 'TRUE'
            row['TRAIT_DLBULLRUSH'] = 'TRUE'
            overall_rating = row['OverallRating']
            row['ThrowOnTheRunRating'] = overall_rating

        if row['Position'] in ['DT']:
            row['TRAIT_DLSWIM'] = 'TRUE'
            row['TRAIT_DLSPIN'] = 'TRUE'
            row['TRAIT_DLBULLRUSH'] = 'TRUE'
            overall_rating = row['OverallRating']
            row['ThrowOnTheRunRating'] = overall_rating

        # For all other positions, set a minimum of 73 and a maximum of 85 for InjuryRating
        if row['Position'] not in ['HB', 'QB']:

            new_injury_rating = row['InjuryRating'] # - 10
            # Ensure the new value is within the specified range
            if new_injury_rating < 73:
                new_injury_rating = 73
            if new_injury_rating > 85:
                new_injury_rating = 85
            row['InjuryRating'] = new_injury_rating

    # Add more conditions and changes for other columns and positions as needed
    return row

# Define target values for ContractSalary0 and ContractSalary1 based on years_pro
min_salary_values = {
    0: 75,
    1: 87,
    2: 94,
    3: 101,
}

# Set the same values for players with 4 through 6 YearsPro
for years_pro in range(4, 7):
    min_salary_values[years_pro] = 108  # Minimum for years_pro >= 4

# Set the same values for players with 7 through 25 YearsPro
for years_pro in range(7, 26):
    min_salary_values[years_pro] = 116  # Minimum for years_pro >= 7

# Function to adjust Salary to league minimum
def adjust_contract_salary(row):
    contract_status = row['ContractStatus']
    years_pro = row['YearsPro']
    contract_salary_0 = row['ContractSalary0']
    contract_salary_1 = row['ContractSalary1']

    if contract_status == 'Signed':
        if years_pro in min_salary_values:
            target_salary = min_salary_values[years_pro]
            if contract_salary_0 != 0 and contract_salary_0 < target_salary:
                row['ContractSalary0'] = target_salary
            if contract_salary_1 != 0 and contract_salary_1 < target_salary:
                row['ContractSalary1'] = target_salary

    return row

def player_tag_updates(row):
    tag1 = row['Tag1']
    tag2 = row['Tag2']
    contract_status = row['ContractStatus']
    years_pro = row['YearsPro']
    overall_rating = row['OverallRating']
    position = row['Position']
    
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
df.to_excel('Files/Madden24/IE/Season3/Player_PreseasonEdits.xlsx', index=False)

### CoverBall might get changed ###