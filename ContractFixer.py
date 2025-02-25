# Imports
import pandas as pd
import random
import math

# Your File Path
player_file_path = 'Files/Madden25/IE/Season8/Player.xlsx'

# Load DataFrame
df = pd.read_excel(player_file_path)

def fix_contract_salaries(row):
    salary_changed = False  # Flag to check if any salary value changes
    
    if row['YearsPro'] >= 4 and row['ContractYear'] == 0 and row['ContractStatus'] == 'Signed':
        total_salary = sum(row[f'ContractSalary{i}'] for i in range(7))
        
        # Calculate the leftover salary once
        leftover = total_salary
        
        if row['ContractLength'] == 2 and row['ContractSalary0'] >= 0.45 * total_salary and row['ContractSalary1'] > 0:
            new_salary_0 = math.ceil(random.uniform(0.3, 0.4) * total_salary / 5) * 5
            if new_salary_0 != row['ContractSalary0']:
                salary_changed = True
            leftover -= new_salary_0
            row['ContractSalary0'] = new_salary_0
            row['ContractSalary1'] = leftover - sum(row[f'ContractSalary{i}'] for i in range(2, 7))
        
        elif row['ContractLength'] == 3 and row['ContractSalary0'] >= 0.3 * total_salary and row['ContractSalary2'] > 0:
            new_salary_0 = math.ceil(random.uniform(0.15, 0.20) * total_salary / 5) * 5
            if new_salary_0 != row['ContractSalary0']:
                salary_changed = True
            leftover -= new_salary_0
            new_salary_1 = math.ceil(random.uniform(0.35, 0.40) * total_salary / 5) * 5
            if new_salary_1 != row['ContractSalary1']:
                salary_changed = True
            leftover -= new_salary_1
            row['ContractSalary0'] = new_salary_0
            row['ContractSalary1'] = new_salary_1
            row['ContractSalary2'] = leftover - sum(row[f'ContractSalary{i}'] for i in range(3, 7))
        
        elif row['ContractLength'] == 4 and row['ContractSalary0'] >= 0.3 * total_salary and row['ContractSalary3'] > 0:
            new_salary_0 = math.ceil(random.uniform(0.15, 0.2) * total_salary / 5) * 5
            if new_salary_0 != row['ContractSalary0']:
                salary_changed = True
            leftover -= new_salary_0
            
            new_salary_1 = math.ceil(0.25 * total_salary / 5) * 5
            if new_salary_1 != row['ContractSalary1']:
                salary_changed = True
            leftover -= new_salary_1
            
            new_salary_2 = math.ceil(0.28 * total_salary / 5) * 5
            if new_salary_2 != row['ContractSalary2']:
                salary_changed = True
            leftover -= new_salary_2
            
            new_salary_3 = math.ceil(0.32 * total_salary / 5) * 5
            if new_salary_3 != row['ContractSalary3']:
                salary_changed = True
            leftover -= new_salary_3
            
            row['ContractSalary0'] = new_salary_0
            row['ContractSalary1'] = new_salary_1
            row['ContractSalary2'] = new_salary_2
            row['ContractSalary3'] = new_salary_3
    
    row['StatusCheck'] = salary_changed  # Add StatusCheck column
    return row

# Apply function to DataFrame
result_df = df.apply(fix_contract_salaries, axis=1)

# Ensure StatusCheck is the first column
cols = ['StatusCheck'] + [col for col in result_df.columns if col != 'StatusCheck']
result_df = result_df[cols]

# Export the DataFrame to a new Excel file
output_filename = 'Files/Madden25/IE/Season8/Player_ContractsFixed.xlsx'
result_df.to_excel(output_filename, index=False)