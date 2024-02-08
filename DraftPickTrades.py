import pandas as pd
import numpy as np
import random

# Your File Paths
pick_file_path = 'Files/Madden24/IE/Test/DraftPicks.xlsx'
index_file_path = 'Files/Madden24/IE/Test/DraftTeamIndex.xlsx'
value_file_path = 'Files/Madden24/IE/Test/DraftPickValue.xlsx'
output_file_path = 'Files/Madden24/IE/Test/Draft_Trades.xlsx'

# Read DraftTeamIndex Excel file
team_index_df = pd.read_excel(index_file_path)

# Extract TeamName and TeamIndex columns
team_picks_df = team_index_df[['Team Name', 'Team Index', 'Binary']]

# Convert the 'Binary' column to string and pad with leading zeros
team_picks_df['Binary'] = team_picks_df['Binary'].astype(str).str.zfill(16)

# Read DraftPicks Excel file
draft_picks_df = pd.read_excel(pick_file_path)

# Filter the DataFrame to include only the picks with YearOffset = 0
draft_picks_df_year_0 = draft_picks_df[draft_picks_df['YearOffset'] == 0]

# Extract right 16 digits of the 'CurrentTeam' column and convert to string
draft_picks_df_year_0['CurrentTeam'] = draft_picks_df_year_0['CurrentTeam'].astype(str).str[-16:]

# Count the number of picks with YearOffset = 0 each team has
num_draft_picks_year_0 = draft_picks_df_year_0.groupby('CurrentTeam').size().reset_index(name='PicksThisYear')

# Merge with team_picks_df
team_picks_df = pd.merge(team_picks_df, num_draft_picks_year_0, how='left', left_on='Binary', right_on='CurrentTeam')

# Fill NaN values with 0 (teams with no picks this year)
team_picks_df['PicksThisYear'].fillna(0, inplace=True)

# Drop the 'CurrentTeam' column
team_picks_df.drop(columns='CurrentTeam', inplace=True)

# Read DraftPickValue Excel file
pick_value_df = pd.read_excel(value_file_path)

# Merge draft_picks_df_year_0 with pick_value_df based on 'PickNumber'
draft_picks_df_year_0 = pd.merge(draft_picks_df_year_0, pick_value_df[['Pick', 'Value']], how='left', left_on='PickNumber', right_on='Pick')

# Group by 'CurrentTeam' and sum up the 'Value' for each team
team_pick_values = draft_picks_df_year_0.groupby('CurrentTeam')['Value'].sum().reset_index()

# Merge with team_picks_df to add the total pick value for each team
team_picks_df = pd.merge(team_picks_df, team_pick_values, how='left', left_on='Binary', right_on='CurrentTeam')

# Fill NaN values with 0 (teams with no picks this year)
team_picks_df['Value'].fillna(0, inplace=True)

# Drop the 'CurrentTeam' column
team_picks_df.drop(columns='CurrentTeam', inplace=True)

# Filter out rows/teams with total pick value of 0
team_picks_df = team_picks_df[team_picks_df['Value'] != 0]

# Read DraftPicks Excel file and write it to a new tab called 'DraftPicks'
draft_picks_df = pd.read_excel(pick_file_path)
with pd.ExcelWriter(output_file_path) as writer:
    team_picks_df.to_excel(writer, sheet_name='TeamPicks', index=False)
    draft_picks_df.to_excel(writer, sheet_name='DraftPicks', index=False)

# Filter draft picks for YearOffset = 0
draft_picks_year_0 = draft_picks_df[draft_picks_df['YearOffset'] == 0]

# Merge with pick_value_df to get pick values
draft_order_df = pd.merge(draft_picks_year_0, pick_value_df[['Pick', 'Value']], how='left', left_on='PickNumber', right_on='Pick')

# Select relevant columns
draft_order_df = draft_order_df[['CurrentTeam', 'PickNumber', 'Value']]

# Rename columns
draft_order_df.columns = ['Team', 'PickNumber', 'Value']

# Extract right 16 digits of the 'Team' column and convert to string
draft_order_df['Binary'] = draft_order_df['Team'].astype(str).str[-16:]

# Retrieve Team Names
team_names = team_picks_df[['Binary', 'Team Name', 'PicksThisYear']]

# Merge with draft_order_df to add the actual Team Name
draft_order_df = pd.merge(draft_order_df, team_names, how='left', left_on='Binary', right_on='Binary')

# Select only relevant columns
draft_order_df = draft_order_df[['Team Name', 'Binary', 'PickNumber', 'Value', 'PicksThisYear']]

# Sort by PickNumber
draft_order_df.sort_values(by='PickNumber', inplace=True)

# Reset index
draft_order_df.reset_index(drop=True, inplace=True)

# Define the multipliers using conditional statements
def get_multiplier(num_picks):
    if num_picks >= 9:
        return 0.5
    elif num_picks == 8:
        return 0.75
    elif num_picks == 7:
        return 1
    elif num_picks == 6:
        return 1.25
    elif num_picks <= 5:
        return 1.5
    else:
        return 1

# Function to calculate trade down probability with adjusted multiplier
def calculate_trade_down(row):
    multiplier = get_multiplier(row['PicksThisYear'])
    if np.random.rand() < 0.05 * multiplier:  # 5% chance of "Yes"
        return 'Yes'
    else:
        return 'No'

# Add TradeDown column with adjusted probabilities
draft_order_df['TradeDown'] = draft_order_df.apply(calculate_trade_down, axis=1)

# Filter rows where TradeDown is Yes
trade_down_rows = draft_order_df[draft_order_df['TradeDown'] == 'Yes']

# Seed the random number generator for reproducibility
random.seed()

# Loop through each row where TradeDown is Yes
for index, row in trade_down_rows.iterrows():
    # Find the minimum value for selecting trade team
    min_trade_value = row['Value'] * 0.4
    
    # Filter rows where Value is at least 40% of the current pick value
    potential_trade_teams = draft_order_df[(draft_order_df['Value'] >= min_trade_value) & (draft_order_df['TradeDown'] != 'Yes')]
    
    # Randomly select a trade team
    if not potential_trade_teams.empty:
        trade_team = random.choice(potential_trade_teams['Team Name'])
    else:
        trade_team = None

    # Assign the selected trade team to the current row
    draft_order_df.at[index, 'TradeTeam'] = trade_team

# Write to Excel under 'DraftOrder' tab
with pd.ExcelWriter(output_file_path, mode='a') as writer:
    draft_order_df.to_excel(writer, sheet_name='DraftOrder', index=False)
