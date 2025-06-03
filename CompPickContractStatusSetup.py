# Imports
import pandas as pd

# Your File Paths
expiring_contract_file = 'Files/Madden25/IE/Season9/LastSeason_ExpiringContracts.xlsx'

# Read the "LastSeason_ExpiringContracts.xlsx" sheet into DataFrame
expiring_contracts_df = pd.read_excel(expiring_contract_file)

# Check if ContractSalary(i) = 0 and ContractBonus(i) != 0
# or ContractSalary(i) = 0 and ContractBonus(i) = 0, for the specific i value based on ContractYear
for _, row in expiring_contracts_df[expiring_contracts_df['ContractStatus'] == 'Signed'].iterrows():
    contract_year = row['ContractYear']
    contract_length = row['ContractLength']
    
    # Ensure i_value_to_check is within the valid range [0, contract_length - 1]
    i_value_to_check = max(0, min(contract_length - 1, contract_year))

    criteria_salary = (
        row.get(f'ContractSalary{i_value_to_check}', 0) == 0 and
        row.get(f'ContractBonus{i_value_to_check}', 0) != 0
    )

    criteria_both_zero = (
        row.get(f'ContractSalary{i_value_to_check}', 0) == 0 and
        row.get(f'ContractBonus{i_value_to_check}', 0) == 0
    )

    # Update ContractStatus if any of the conditions are met
    if criteria_salary or criteria_both_zero:
        expiring_contracts_df.at[_, 'ContractStatus'] = 'Expiring'

# Define the output filename in the same directory as the import
output_filename = 'Files/Madden25/IE/Season9/CompPick_ContractStatusUpdated.xlsx'

# Export the updated DataFrame to Excel in the same directory
expiring_contracts_df.to_excel(output_filename, index=False)