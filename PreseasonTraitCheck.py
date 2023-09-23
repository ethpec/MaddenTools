# Imports
import pandas as pd
import random

# Your File Path
file_path = 'Files/Madden24/IE/Test/Player.xlsx'

df = pd.read_excel(file_path)

def update_traits(row):
    # Check the player's position and apply changes to specific columns
    contract_status = row['ContractStatus']
    
    if contract_status in ['FreeAgent', 'Signed', 'PracticeSquad']:

        # QB Edits
        if row['Position'] == 'QB':
            # For QBs, set a minimum of 70 and a maximum of 80 for InjuryRating
            new_injury_rating = row['InjuryRating'] - 18
            # Ensure the new value is within the specified range
            if new_injury_rating < 70:
                new_injury_rating = 70
            if new_injury_rating > 80:
                new_injury_rating = 80
            row['InjuryRating'] = new_injury_rating
            row['TRAIT_THROWAWAY'] = 'TRUE'  # Change Trait_ThrowAway column for QBs to 'TRUE'
            row['TRAIT_COVER_BALL'] = 'ForAllHits'
            if 'Pocket' in row['TRAIT_QBSTYLE']:
                row['TRAIT_QBSTYLE'] = 'Balanced'
            if row['SpeedRating'] < 80:
                row['TRAIT_QBSTYLE'] = 'Balanced'
            if row['SpeedRating'] >= 87:
                row['TRAIT_QBSTYLE'] = 'Scrambler'

        # HB Edits
        if row['Position'] == 'HB':
            # For HBs, set a minimum of 73 and a maximum of 85 for InjuryRating
            new_injury_rating = row['InjuryRating'] - 13
            # Ensure the new value is within the specified range
            if new_injury_rating < 73:
                new_injury_rating = 73
            if new_injury_rating > 85:
                new_injury_rating = 85
            row['InjuryRating'] = new_injury_rating
            row['TRAIT_YACCATCH'] = 'TRUE'
            row['TRAIT_POSSESSIONCATCH'] = 'TRUE'
            row['TRAIT_HIGHPOINTCATCH'] = 'TRUE'

        # OFF Edits
        if row['Position'] in ['WR', 'TE']:
            row['TRAIT_YACCATCH'] = 'TRUE'
            row['TRAIT_POSSESSIONCATCH'] = 'TRUE'
            row['TRAIT_HIGHPOINTCATCH'] = 'TRUE'

        # DEF Edits
        if row['Position'] in ['LE', 'RE', 'DT']:
            row['TRAIT_DLSWIM'] = 'TRUE'
            row['TRAIT_DLSPIN'] = 'TRUE'
            row['TRAIT_DLBULLRUSH'] = 'TRUE'

        # For all other positions, set a minimum of 68 and a maximum of 80 for InjuryRating
        if row['Position'] not in ['HB', 'QB']:

            new_injury_rating = row['InjuryRating'] - 18
            # Ensure the new value is within the specified range
            if new_injury_rating < 68:
                new_injury_rating = 68
            if new_injury_rating > 80:
                new_injury_rating = 80
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
            if contract_salary_0 < target_salary:
                row['ContractSalary0'] = target_salary
            if contract_salary_1 < target_salary:
                row['ContractSalary1'] = target_salary

    return row

# Track the original DataFrame before applying updates
original_df = df.copy()

# Apply the update_traits function to update the DataFrame
df = df.apply(update_traits, axis=1)

# Apply the adjust_contract_salary function to update the DataFrame
df = df.apply(adjust_contract_salary, axis=1)

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
df.to_excel('Files/Madden24/IE/Test/Player_PreseasonEdits.xlsx', index=False)

### REWRITE DEF ADJUST_CONTRACT_SALARY TO ONLY CHANGE SALARY IF UNDER CONTRACT THAT YEAR (DON'T CHANGE IF CONTRACT_SALARY = 0) ###