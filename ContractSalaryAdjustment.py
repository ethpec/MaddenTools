import pandas as pd

# Set the multiplier for adjusting salaries and bonuses
adjustment_multiplier = 0.918  # You can change this value to adjust salaries and bonuses

# Your File Paths
player_file_path = 'Files/Madden24/IE/Season2/Player.xlsx'
output_filename = 'Files/Madden24/IE/Season2/Contracts_Adjusted.xlsx'

# Read player data from the Excel file
df = pd.read_excel(player_file_path)

# Adjust salaries, bonuses, and PLYR_CAPSALARY for players with ContractStatus = 'Signed'
mask = df['ContractStatus'] == 'Signed'
columns_to_adjust = [f'ContractSalary{i}' for i in range(8)] + [f'ContractBonus{i}' for i in range(8)] + ['PLYR_CAPSALARY']

# Create a new DataFrame with only the impacted columns and all rows
impacted_df = df[columns_to_adjust].copy()

# Check if any changes occurred in the impacted columns
changes_occurred = (impacted_df.loc[mask] * adjustment_multiplier).astype(int).round() != impacted_df.loc[mask]

# Adjust salaries, bonuses, and PLYR_CAPSALARY in the impacted columns
impacted_df.loc[mask] = (impacted_df.loc[mask] * adjustment_multiplier).astype(int).round()

# Export only the columns that have changes to Excel
impacted_df.loc[:, changes_occurred.any()].to_excel(output_filename, index=False)
print(f"Impacted columns of adjusted DataFrame (rounded) exported to {output_filename}")
