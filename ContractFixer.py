# Imports
import pandas as pd
import random
import math
import numpy as np

# File Paths
player_file_path = 'Files/Madden25/IE/Test/Player.xlsx'
salary_expectation_file_path = 'Files/Madden25/IE/Test/Expected Salary Sheet.xlsx'

# Load DataFrames
df = pd.read_excel(player_file_path)
salary_df = pd.read_excel(salary_expectation_file_path, sheet_name='Import (Values Only) (279)')

# Parse Salary Table
def parse_salary_table(salary_df):
    salary_data = {}

    # Group rows by Position (last column)
    for pos, group in salary_df.groupby('Position'):
        pos = str(pos).strip().upper()

        # Extract numeric values for each Type ignoring first column (Type) and last (Position)
        overall = group[group['Type'] == 'OverallRating'].iloc[0, 1:-1].astype(float).tolist()
        aav = group[group['Type'] == 'AAV'].iloc[0, 1:-1].astype(float).tolist()
        bonus = group[group['Type'] == 'Bonus'].iloc[0, 1:-1].astype(float).tolist()
        length = group[group['Type'] == 'Length'].iloc[0, 1:-1].astype(float).tolist()

        salary_data[pos] = {
            'Overall': overall,
            'AAV': aav,
            'Bonus': bonus,
            'Length': length
        }

    return salary_data

salary_lookup = parse_salary_table(salary_df)

# Salary Interpolation
def salary_interpolation(position, overall, salary_lookup):
    if position not in salary_lookup:
        return None, None, None

    data = salary_lookup[position]
    x = data['Overall']

    def interpolate(y_values):
        return float(np.interp(overall, x, y_values))

    aav = round(interpolate(data['AAV']))
    bonus = round(interpolate(data['Bonus']))
    length = round(interpolate(data['Length']))

    return aav, bonus, length

# Apply to Each Row
def assign_salaryinfo(row):
    position = str(row['Position']).strip().upper()
    overall = row['OverallRating']

    aav, bonus, length = salary_interpolation(position, overall, salary_lookup)

    row['ExpectedAAV'] = aav
    row['ExpectedBonus'] = bonus
    row['ExpectedContractLength'] = length
    row['SalaryCheck'] = 'Updated' if aav is not None else 'Position Missing'

    return row

def fix_contract_salaries(row):
    salary_changed = False  # Flag to check if any salary value changes
    
    if row['YearsPro'] >= 4 and row['ContractYear'] == 0 and row['ContractStatus'] == 'Signed':
        total_salary = sum(row[f'ContractSalary{i}'] for i in range(7))
        total_bonus = sum(row[f'ContractBonus{i}'] for i in range(7))
        contract_length = sum(1 for i in range(7) if row.get(f'ContractSalary{i}', 0) > 0)
        contract_length = contract_length if contract_length > 0 else 1  # prevent divide by zero


        # Calculate current AAV and Bonus
        current_aav = round((total_salary + total_bonus) / contract_length)
        current_bonus = round(total_bonus / contract_length)

        row['CurrentAAV'] = current_aav
        row['CurrentBonus'] = current_bonus
        
        # Calculate the leftover salary once
        leftover = total_salary
        
        if row['ContractLength'] == 2 and row['ContractSalary0'] >= 0.45 * total_salary and row['ContractSalary1'] > 0:
            
            if row['CurrentAAV'] >= row['ExpectedAAV']:
                base_salary = total_salary
            elif row['CurrentAAV'] < row['ExpectedAAV'] and row['CurrentBonus'] > row['ExpectedBonus']:
                base_salary = (row['ExpectedAAV'] - row['ExpectedBonus']) * row['ContractLength']
                row['ContractBonus0'] = row['ExpectedBonus']
                row['ContractBonus1'] = row['ExpectedBonus']
            else:
                base_salary = (row['ExpectedAAV'] - row['ExpectedBonus']) * row['ContractLength']

            new_salary_0 = math.ceil(random.uniform(0.33, 0.44) * base_salary / 5) * 5

            if new_salary_0 != row['ContractSalary0']:
                salary_changed = True

            leftover = base_salary - new_salary_0
            row['ContractSalary0'] = new_salary_0
            row['ContractSalary1'] = leftover - sum(row[f'ContractSalary{i}'] for i in range(2, 7))

        elif row['ContractLength'] == 3 and row['ContractSalary0'] >= 0.27 * total_salary and row['ContractSalary2'] > 0:

            if row['CurrentAAV'] >= row['ExpectedAAV']:
                base_salary = total_salary
            elif row['CurrentAAV'] < row['ExpectedAAV'] and row['CurrentBonus'] > row['ExpectedBonus']:
                base_salary = (row['ExpectedAAV'] - row['ExpectedBonus']) * row['ContractLength']
                row['ContractBonus0'] = row['ExpectedBonus']
                row['ContractBonus1'] = row['ExpectedBonus']
            else:
                base_salary = (row['ExpectedAAV'] - row['ExpectedBonus']) * row['ContractLength']

            leftover = base_salary
            
            new_salary_0 = math.ceil(random.uniform(0.22, 0.26) * base_salary / 5) * 5
            if new_salary_0 != row['ContractSalary0']:
                salary_changed = True
            leftover -= new_salary_0
            new_salary_1 = math.ceil(random.uniform(0.33, 0.37) * base_salary / 5) * 5
            if new_salary_1 != row['ContractSalary1']:
                salary_changed = True
            leftover -= new_salary_1
            row['ContractSalary0'] = new_salary_0
            row['ContractSalary1'] = new_salary_1
            row['ContractSalary2'] = leftover - sum(row[f'ContractSalary{i}'] for i in range(3, 7))

        elif row['ContractLength'] == 4 and row['ContractSalary0'] >= 0.22 * total_salary and row['ContractSalary3'] > 0:
            
            if row['CurrentAAV'] >= row['ExpectedAAV']:
                base_salary = total_salary
            elif row['CurrentAAV'] < row['ExpectedAAV'] and row['CurrentBonus'] > row['ExpectedBonus']:
                base_salary = (row['ExpectedAAV'] - row['ExpectedBonus']) * row['ContractLength']
                row['ContractBonus0'] = row['ExpectedBonus']
                row['ContractBonus1'] = row['ExpectedBonus']
            else:
                base_salary = (row['ExpectedAAV'] - row['ExpectedBonus']) * row['ContractLength']

            leftover = base_salary

            new_salary_0 = math.ceil(random.uniform(0.17, 0.21) * base_salary / 5) * 5
            if new_salary_0 != row['ContractSalary0']:
                salary_changed = True
            leftover -= new_salary_0
            new_salary_1 = math.ceil(0.25 * base_salary / 5) * 5
            if new_salary_1 != row['ContractSalary1']:
                salary_changed = True
            leftover -= new_salary_1
            new_salary_2 = math.ceil(0.27 * base_salary / 5) * 5
            if new_salary_2 != row['ContractSalary2']:
                salary_changed = True
            leftover -= new_salary_2
            row['ContractSalary0'] = new_salary_0
            row['ContractSalary1'] = new_salary_1
            row['ContractSalary2'] = new_salary_2
            row['ContractSalary3'] = leftover - sum(row[f'ContractSalary{i}'] for i in range(4, 7))

    row['StatusCheck'] = salary_changed  # Add StatusCheck column

    if row['YearsPro'] == 1 and row['ContractYear'] == 0 and row['ContractStatus'] == 'Signed':
        row['ContractLength'] = 1
        row['ContractSalary0'] = 96
        row['ContractBonus0'] = 0
        row['ContractSalary1'] = 0
        row['ContractSalary2'] = 0
        row['ContractSalary3'] = 0
        row['ContractSalary4'] = 0
        row['ContractBonus1'] = 0
        row['ContractBonus2'] = 0
        row['ContractBonus3'] = 0
        row['ContractBonus4'] = 0
        row['PLYR_CAPSALARY'] = 96
        row['StatusCheck'] = 'Young_Adjusted'

    if row['YearsPro'] == 2 and row['ContractYear'] == 0 and row['ContractStatus'] == 'Signed':
        row['ContractLength'] = 1
        row['ContractSalary0'] = 103
        row['ContractBonus0'] = 0
        row['ContractSalary1'] = 0
        row['ContractSalary2'] = 0
        row['ContractSalary3'] = 0
        row['ContractSalary4'] = 0
        row['ContractBonus1'] = 0
        row['ContractBonus2'] = 0
        row['ContractBonus3'] = 0
        row['ContractBonus4'] = 0
        row['PLYR_CAPSALARY'] = 103
        row['StatusCheck'] = 'Young_Adjusted'

    ### Veteran Age 29 ###
    if row['Age'] >= 29 and row['Position'] in ['RB', 'HB'] and row['ContractSalary0'] >= 225 and row['ContractYear'] == 0 and row['ContractStatus'] == 'Signed':
        # Adjust salaries
        salary_multiplier = random.uniform(0.65, 0.9)

        for i in range(7):
            col = f'ContractSalary{i}'
            if col in row:
                row[col] = round((row[col] * salary_multiplier) / 5) * 5

        # Adjust bonuses
        bonus_multiplier = random.uniform(0.75, 0.95)
        for i in range(5):
            col = f'ContractBonus{i}'
            if col in row:
                row[col] = round((row[col] * bonus_multiplier) / 5) * 5

        row['StatusCheck'] = 'Vet_Adjusted'

    ### Veteran Age 30 ###
    if row['Age'] >= 30 and row['Position'] in ['CB'] and row['ContractSalary0'] >= 225 and row['ContractYear'] == 0 and row['ContractStatus'] == 'Signed':
        # Adjust salaries
        salary_multiplier = random.uniform(0.65, 0.9)

        for i in range(7):
            col = f'ContractSalary{i}'
            if col in row:
                row[col] = round((row[col] * salary_multiplier) / 5) * 5

        row['StatusCheck'] = 'Vet_Adjusted'

        # Adjust bonuses
        bonus_multiplier = random.uniform(0.75, 0.95)
        for i in range(5):
            col = f'ContractBonus{i}'
            if col in row:
                row[col] = round((row[col] * bonus_multiplier) / 5) * 5

    ### Veteran Age 31 ###
    if row['Age'] >= 31 and row['Position'] in ['WR', 'LOLB', 'MLB', 'ROLB', 'FS', 'SS'] and row['ContractSalary0'] >= 225 and row['ContractYear'] == 0 and row['ContractStatus'] == 'Signed':
        # Adjust salaries
        salary_multiplier = random.uniform(0.65, 0.9)

        for i in range(7):
            col = f'ContractSalary{i}'
            if col in row:
                row[col] = round((row[col] * salary_multiplier) / 5) * 5

        row['StatusCheck'] = 'Vet_Adjusted'

        # Adjust bonuses
        bonus_multiplier = random.uniform(0.75, 0.95)
        for i in range(5):
            col = f'ContractBonus{i}'
            if col in row:
                row[col] = round((row[col] * bonus_multiplier) / 5) * 5

    ### Veteran Age 32 ###
    if row['Age'] >= 32 and row['Position'] in ['TE', 'DT', 'LE', 'RE'] and row['ContractSalary0'] >= 225 and row['ContractYear'] == 0 and row['ContractStatus'] == 'Signed':
        # Adjust salaries
        salary_multiplier = random.uniform(0.65, 0.9)

        for i in range(7):
            col = f'ContractSalary{i}'
            if col in row:
                row[col] = round((row[col] * salary_multiplier) / 5) * 5

        row['StatusCheck'] = 'Vet_Adjusted'

        # Adjust bonuses
        bonus_multiplier = random.uniform(0.75, 0.95)
        for i in range(5):
            col = f'ContractBonus{i}'
            if col in row:
                row[col] = round((row[col] * bonus_multiplier) / 5) * 5

    ### Veteran Age 33 ###
    if row['Age'] >= 33 and row['Position'] in ['LT', 'LG', 'C', 'RG', 'RT'] and row['ContractSalary0'] >= 225 and row['ContractYear'] == 0 and row['ContractStatus'] == 'Signed':
        # Adjust salaries
        salary_multiplier = random.uniform(0.65, 0.9)

        for i in range(7):
            col = f'ContractSalary{i}'
            if col in row:
                row[col] = round((row[col] * salary_multiplier) / 5) * 5

        row['StatusCheck'] = 'Vet_Adjusted'

        # Adjust bonuses
        bonus_multiplier = random.uniform(0.75, 0.95)
        for i in range(5):
            col = f'ContractBonus{i}'
            if col in row:
                row[col] = round((row[col] * bonus_multiplier) / 5) * 5
                    
    return row

# Apply function to DataFrame
result_df = df.apply(fix_contract_salaries, axis=1)

# Ensure StatusCheck is the first column
cols = ['StatusCheck'] + [col for col in result_df.columns if col != 'StatusCheck']
result_df = result_df[cols]

# Export the DataFrame to a new Excel file
output_filename = 'Files/Madden25/IE/Test/Player_ContractsFixed.xlsx'
result_df.to_excel(output_filename, index=False)