# Imports
import pandas as pd

# Your File Path
file_path = 'Files/Madden26/IE/Season0/Player.xlsx'

# Read the Excel file
df = pd.read_excel(file_path)

# Filter for players with ContractStatus = 'Expiring' or 'FreeAgent'
contract_filter = df['ContractStatus'].isin(['Expiring', 'FreeAgent'])
filtered_df = df[contract_filter]

# Sort by OverallRating descending and get top 10 per position
top_10_per_position = (
    filtered_df.sort_values(by='OverallRating', ascending=False)
    .groupby('Position')
    .head(10)
    .reset_index(drop=True)
)

# Select only the specified columns in the desired order
selected_columns = ['Position', 'OverallRating', 'FirstName', 'LastName', 'ContractStatus', 'Age', 'YearsPro']
top_10_per_position = top_10_per_position[selected_columns]

# Save the result to Excel
output_filename = 'Player_FreeAgentClass.xlsx'
top_10_per_position.to_excel(f'Files/Madden26/IE/Season0/{output_filename}', index=False)