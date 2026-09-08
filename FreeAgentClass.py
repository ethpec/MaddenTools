# Imports
import pandas as pd
from config import season_path

# Your File Path
file_path = season_path('Player.xlsx')

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
top_10_per_position.to_excel(season_path(output_filename), index=False)