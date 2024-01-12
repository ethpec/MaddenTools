# Imports
import pandas as pd

# Your File Path
file_path = 'Files/Madden24/IE/Test/Player.xlsx'

df = pd.read_excel(file_path)

# Define target values for ContractSalary0 and ContractSalary1 based on years_pro
min_salary_values = {
    0: 75,
    1: 87,
    2: 94
}

def update_pscontracts(row):
    contract_status = row['ContractStatus']
    years_pro = int(row['YearsPro'])
    contract_length = int(row['ContractLength'])
    contract_salary_0 = row['ContractSalary0']
    contract_salary_1 = row['ContractSalary1']
    contract_salary_2 = row['ContractSalary2']

    if contract_status == 'Signed' and years_pro in [0, 1] and contract_length == 1:
        row['ContractLength'] = 3
        row['ContractYear'] = str(years_pro)

        if years_pro in min_salary_values:
            target_salary = min_salary_values[years_pro]
            if contract_salary_0 == 0:
                row['ContractSalary0'] = target_salary
            if contract_salary_1 == 0:
                row['ContractSalary1'] = target_salary
            if contract_salary_2 == 0:
                row['ContractSalary2'] = target_salary

    return row

# Track the original DataFrame before applying updates
original_df = df.copy()

# Apply the function to each row
df = df.apply(update_pscontracts, axis=1)

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

# Save the updated DataFrame to a new Excel file
output_filename = 'PracticeSquad_Contracts.xlsx'
df.to_excel('Files/Madden24/IE/Test/PracticeSquad_Contracts.xlsx', index=False)