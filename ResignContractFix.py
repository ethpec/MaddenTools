import pandas as pd
import math
import random

# Your File Paths
resign_file_path = 'Files/Madden24/IE/Season1/PlayerExpiringContracts.xlsx'
player_file_path = 'Files/Madden24/IE/Season1/Player.xlsx'
expected_salary_file_path = 'Files/Madden24/IE/Season1/ExpectedSalary.xlsx'

# Read data from the specified Excel files
resign_df = pd.read_excel(resign_file_path)
player_df = pd.read_excel(player_file_path)
expected_salary_df = pd.read_excel(expected_salary_file_path)

# Create a new column 'StatusCheck' indicating if ContractStatus is 'Expiring' in PlayerExpiringContracts, 'Signed' in Player, and TeamIndex matches
player_df['StatusCheck'] = (player_df['ContractStatus'].eq('Signed')) & (resign_df['ContractStatus'].eq('Expiring')) & (player_df['TeamIndex'].eq(resign_df['TeamIndex']))

# Perform the lookup for Expected Contract Length
def calculate_expected_contract_length(row):
    position = row['Position']
    overall_rating = row['OverallRating']
    matching_row = expected_salary_df[(expected_salary_df['Position'] == position) & 
                                       (expected_salary_df['Rating Range Start'] <= overall_rating) &
                                       (expected_salary_df['Rating Range End'] >= overall_rating)]
    if not matching_row.empty:
        return matching_row.iloc[0]['Expected Contract Length']
    else:
        return None

# Calculate ExpectedContractLength for all players
player_df['ExpectedContractLength'] = player_df.apply(calculate_expected_contract_length, axis=1)

# Create a new column 'AddedYears' by subtracting 'ContractLength' from 'ExpectedContractLength'
player_df['AddedYears'] = player_df['ExpectedContractLength'] - player_df['ContractLength']

# Compute YearlySalary and YearlyBonus for players with True StatusCheck and AddedYears >= 1, round up to nearest integer
def compute_yearly_salary(row):
    if row['StatusCheck'] and row['AddedYears'] >= 1:
        non_zero_salaries = [row[f'ContractSalary{i}'] for i in range(8) if row[f'ContractSalary{i}'] != 0]
        non_zero_bonuses = [row[f'ContractBonus{i}'] for i in range(8) if row[f'ContractBonus{i}'] != 0]
        if non_zero_salaries and non_zero_bonuses:
            avg_salary = sum(non_zero_salaries) / len(non_zero_salaries)
            avg_bonus = sum(non_zero_bonuses) / len(non_zero_bonuses)
            return math.ceil(avg_salary), math.ceil(avg_bonus)  # Round up to nearest integer
    return None, None

# Apply compute_yearly_salary function to all players without filtering
player_df['YearlySalary'], player_df['YearlyBonus'] = zip(*player_df.apply(compute_yearly_salary, axis=1))

# Function to update the contract length for qualified players
def update_contractlength(row):
    if row['StatusCheck'] and row['AddedYears'] >= 1:
        new_contract_length = row['ExpectedContractLength']
        # Apply randomness (25% chance to subtract 1 from the contract length)
        if random.random() < 0.25:
            new_contract_length -= 1
        # Check if the new contract length is different from the original value and not NaN
        if not pd.isna(new_contract_length) and new_contract_length != row['ContractLength']:
            return new_contract_length, True  # Return the updated length and True for ContractLengthChanged
    return row['ContractLength'], False  # Keep the existing contract length and mark ContractLengthChanged as False

# Function to edit ContractSalary based on new ContractLength value
def edit_contract_salary(row):
    if row['ContractLengthChanged']:
        original_salaries = [row[f'ContractSalary{i}'] for i in range(8)]
        if not pd.isna(row['YearlySalary']):  # Check if 'YearlySalary' is not NaN
            if row['ContractLength'] == 1:
                row['ContractSalary0'] = int(0.95 * row['YearlySalary'])
            elif row['ContractLength'] == 2:
                row['ContractSalary0'] = int(0.95 * row['YearlySalary'])
                row['ContractSalary1'] = int(1.05 * row['YearlySalary'])
            elif row['ContractLength'] == 3:
                row['ContractSalary0'] = int(0.90 * row['YearlySalary'])
                row['ContractSalary1'] = row['YearlySalary']
                row['ContractSalary2'] = int(1.10 * row['YearlySalary'])
            elif row['ContractLength'] == 4:
                row['ContractSalary0'] = int(0.85 * row['YearlySalary'])
                row['ContractSalary1'] = int(0.95 * row['YearlySalary'])
                row['ContractSalary2'] = int(1.05 * row['YearlySalary'])
                row['ContractSalary3'] = int(1.15 * row['YearlySalary'])
            elif row['ContractLength'] == 5:
                row['ContractSalary0'] = int(0.80 * row['YearlySalary'])
                row['ContractSalary1'] = int(0.90 * row['YearlySalary'])
                row['ContractSalary2'] = row['YearlySalary']
                row['ContractSalary3'] = int(1.10 * row['YearlySalary'])
                row['ContractSalary4'] = int(1.20 * row['YearlySalary'])

        # Check if any ContractSalary(i) values were changed
        new_salaries = [row[f'ContractSalary{i}'] for i in range(8)]
        if original_salaries != new_salaries:
            row['DidSalaryChange'] = True
        else:
            row['DidSalaryChange'] = False
    return row

# Function to edit ContractBonus based on new ContractLength value
def edit_contract_bonus(row):
    if row['ContractLengthChanged']:
        if not pd.isna(row['YearlyBonus']):  # Check if 'YearlyBonus' is not NaN
            if row['ContractLength'] == 1:
                row['ContractBonus0'] = row['YearlyBonus']
            elif row['ContractLength'] == 2:
                row['ContractBonus0'] = row['YearlyBonus']
                row['ContractBonus1'] = row['YearlyBonus']
            elif row['ContractLength'] == 3:
                row['ContractBonus0'] = row['YearlyBonus']
                row['ContractBonus1'] = row['YearlyBonus']
                row['ContractBonus2'] = row['YearlyBonus']
            elif row['ContractLength'] == 4:
                row['ContractBonus0'] = row['YearlyBonus']
                row['ContractBonus1'] = row['YearlyBonus']
                row['ContractBonus2'] = row['YearlyBonus']
                row['ContractBonus3'] = row['YearlyBonus']
            elif row['ContractLength'] >= 5 and row['ContractLength'] <= 7:
                row['ContractBonus0'] = row['YearlyBonus']
                row['ContractBonus1'] = row['YearlyBonus']
                row['ContractBonus2'] = row['YearlyBonus']
                row['ContractBonus3'] = row['YearlyBonus']
                row['ContractBonus4'] = row['YearlyBonus']
    return row

# Apply the update_contractlength function to modify ContractLength column for qualified players and add ContractLengthChanged column
player_df['ContractLength'], player_df['ContractLengthChanged'] = zip(*player_df.apply(update_contractlength, axis=1))

# Apply edit_contract_salary function to players with ContractLengthChanged as True
player_df['DidSalaryChange'] = False  # Initialize the column with False
player_df.loc[player_df['ContractLengthChanged'], :] = player_df[player_df['ContractLengthChanged']].apply(edit_contract_salary, axis=1)

# Apply edit_contract_bonus function to players with ContractLengthChanged as True
player_df.loc[player_df['ContractLengthChanged'], :] = player_df[player_df['ContractLengthChanged']].apply(edit_contract_bonus, axis=1)

# Select only the columns you want to keep in the exported sheet
columns_to_export = ['FirstName', 'LastName', 'ContractStatus', 'DidSalaryChange', 'ContractLengthChanged', 'StatusCheck', 'ContractSalary0', 'ContractSalary1', 'ContractSalary2', 'ContractSalary3', 'ContractSalary4', 'ContractSalary5', 'ContractSalary6', 'ContractSalary7',
                    'ContractBonus0', 'ContractBonus1', 'ContractBonus2', 'ContractBonus3', 'ContractBonus4', 'ContractBonus5', 'ContractBonus6', 'ContractBonus7', 'ContractLength']

# Export the modified data to a new Excel file named "Player_ContractFix.xlsx"
output_filename = 'Files/Madden24/IE/Season1/Player_ResignContractFix.xlsx'
player_df[columns_to_export].to_excel(output_filename, index=False)