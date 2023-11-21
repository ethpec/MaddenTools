# Imports
import pandas as pd

# Your File Paths
player_value_file = 'Files/Madden24/IE/Test/CompPickPlayerValue.xlsx'
expiring_contracts_file = 'Files/Madden24/IE/Test/Player_ExpiringContracts.xlsx'
output_filename = 'Files/Madden24/IE/Test/CompPicksAwarded.xlsx'

# Read the "CompPickPlayerValue.xlsx" and "Player_ExpiringContracts.xlsx" sheets into DataFrames
player_value_df = pd.read_excel(player_value_file)
expiring_contracts_df = pd.read_excel(expiring_contracts_file)

# Merge the two dataframes on the specified columns
merged_df = pd.merge(player_value_df, expiring_contracts_df, on=['FirstName', 'LastName', 'Position', 'YearDrafted'], suffixes=('_Current', '_Former'))

# Filter for rows where the TeamIndex values are different and not equal to 32
different_team_indices = merged_df[
    (merged_df['TeamIndex_Current'] != merged_df['TeamIndex_Former']) &
    (merged_df['TeamIndex_Current'] != 32) &
    (merged_df['TeamIndex_Former'] != 32)
]

# Filter for CompPickValue values of 3, 4, 5, 6, 7
filtered_players = different_team_indices.query('CompPickValue in [3, 4, 5, 6, 7]')

# Create the "PlayerValue" sheet with the required columns
player_value_sheet = filtered_players[['FirstName', 'LastName', 'Position', 'YearsPro_Current', 'TeamIndex_Former', 'TeamIndex_Current', 'CompPickValue']]
player_value_sheet.columns = ['FirstName', 'LastName', 'Position', 'YearsPro', 'FormerTeam', 'CurrentTeam', 'CompPickValue']

# Add the "TotalPoints" column from the CompPickPlayerValue document
total_points_df = pd.read_excel(player_value_file, usecols=['FirstName', 'LastName', 'Position', 'TotalPoints'])
player_value_sheet = player_value_sheet.merge(total_points_df, on=['FirstName', 'LastName', 'Position'])

# Read the "CompPickPlayerValue.xlsx" file to extract the "CompRank" column
comp_rank_df = pd.read_excel(player_value_file, usecols=['FirstName', 'LastName', 'Position', 'CompRank'])

# Merge the "CompRank" column into the "player_value_sheet" DataFrame based on "FirstName," "LastName," and "Position"
player_value_sheet = player_value_sheet.merge(comp_rank_df, on=['FirstName', 'LastName', 'Position'], how='left')

# Ensure uniqueness based on FirstName, LastName, and Position
player_value_sheet.drop_duplicates(subset=['FirstName', 'LastName', 'Position'], inplace=True)

# Create an Excel writer object and save the result to "CompPicksAwarded.xlsx"
with pd.ExcelWriter(output_filename) as writer:
    player_value_sheet.to_excel(writer, sheet_name='PlayerValue', index=False)

# Calculate the counts of PlayersLost and PlayersGained for each TeamIndex, excluding TeamIndex = 32
team_counts = player_value_sheet[
    (player_value_sheet['FormerTeam'] != 32) &
    (player_value_sheet['CurrentTeam'] != 32)
]
team_counts = team_counts.groupby('FormerTeam')['FirstName'].count().reset_index()
team_counts.columns = ['TeamIndex', 'PlayersLost']

# Create a DataFrame with all possible TeamIndex values
all_team_indices = pd.DataFrame({'TeamIndex': range(32)})

# Merge the team_counts DataFrame with all_team_indices to include all TeamIndex values
team_counts = all_team_indices.merge(team_counts, on='TeamIndex', how='left')

# Fill missing values with 0 for PlayersLost
team_counts['PlayersLost'].fillna(0, inplace=True)

# Calculate PlayersGained by grouping the CurrentTeam column, excluding TeamIndex = 32
players_gained = team_counts[
    (team_counts['TeamIndex'] != 32) &
    (team_counts['TeamIndex'].isin(player_value_sheet['CurrentTeam'].unique()))
]
players_gained = player_value_sheet.groupby('CurrentTeam')['FirstName'].count().reset_index()
players_gained.columns = ['TeamIndex', 'PlayersGained']

# Merge the PlayersGained DataFrame with team_counts to include all TeamIndex values
team_counts = team_counts.merge(players_gained, on='TeamIndex', how='left')

# Fill missing values with 0 for PlayersGained
team_counts['PlayersGained'].fillna(0, inplace=True)

# Calculate the NetPlayersLost by subtracting PlayersGained from PlayersLost
team_counts['NetPlayersLost'] = team_counts['PlayersLost'] - team_counts['PlayersGained']

# Create the "TeamGainedLost" sheet with the required columns
team_gained_lost_sheet = team_counts[['TeamIndex', 'PlayersLost', 'PlayersGained', 'NetPlayersLost']]

# Append the "TeamGainedLost" sheet to "CompPicksAwarded.xlsx" after removing the existing sheet if it exists
with pd.ExcelWriter(output_filename, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
    try:
        # Try to delete the existing "TeamGainedLost" sheet if it exists
        writer.book.remove(writer.sheets['TeamGainedLost'])
    except KeyError:
        pass  # If the sheet doesn't exist, do nothing
    player_value_sheet.to_excel(writer, sheet_name='PlayerValue', index=False)
    team_gained_lost_sheet.to_excel(writer, sheet_name='TeamGainedLost', index=False)

# Create an empty DataFrame for the report of teams with NetPlayersLost >= 1
report_df_picks = pd.DataFrame(columns=['TeamIndex', 'Status', 'PlayerName', 'Position', 'YearsPro', 'CompRank', 'CompPickValue'])

# Create an empty DataFrame for the report of teams with NetPlayersLost <= 0
report_df_nopicks = pd.DataFrame(columns=['TeamIndex', 'Status', 'PlayerName', 'Position','YearsPro', 'CompRank', 'CompPickValue'])

# Loop through each TeamIndex and calculate CompPickEligible
for team_index in team_gained_lost_sheet['TeamIndex']:
    players_lost = player_value_sheet[
        (player_value_sheet['FormerTeam'] == team_index)
    ]

    players_gained = player_value_sheet[
        (player_value_sheet['CurrentTeam'] == team_index)
    ]

    # Check if CompPickEligible is 'Yes' for this team
    comp_pick_eligible = 'Yes' if (
        (players_lost['CompPickValue'].isin([3, 4, 5, 6, 7])).any()
    ) else 'No'

    if comp_pick_eligible == 'Yes':
        # Iterate through players lost and add them to the respective report with "PlayersLost" status
        for _, player in players_lost.iterrows():
            if team_counts.loc[team_counts['TeamIndex'] == team_index, 'NetPlayersLost'].values[0] >= 1:
                report_df_picks = pd.concat([report_df_picks, pd.DataFrame({
                    'TeamIndex': [team_index],
                    'Status': ['PlayersLost'],
                    'PlayerName': [f"{player['FirstName']} {player['LastName']}"],
                    'Position': [player['Position']],
                    'YearsPro': [player['YearsPro']],
                    'CompRank': [player['CompRank']],
                    'CompPickValue': [player['CompPickValue']]
                })], ignore_index=True)
            else:
                report_df_nopicks = pd.concat([report_df_nopicks, pd.DataFrame({
                    'TeamIndex': [team_index],
                    'Status': ['PlayersLost'],
                    'PlayerName': [f"{player['FirstName']} {player['LastName']}"],
                    'Position': [player['Position']],
                    'YearsPro': [player['YearsPro']],
                    'CompRank': [player['CompRank']],
                    'CompPickValue': [player['CompPickValue']]
                })], ignore_index=True)

        # Iterate through players gained and add them to the respective report with "PlayersGained" status
        for _, player in players_gained.iterrows():
            if team_counts.loc[team_counts['TeamIndex'] == team_index, 'NetPlayersLost'].values[0] >= 1:
                report_df_picks = pd.concat([report_df_picks, pd.DataFrame({
                    'TeamIndex': [team_index],
                    'Status': ['PlayersGained'],
                    'PlayerName': [f"{player['FirstName']} {player['LastName']}"],
                    'Position': [player['Position']],
                    'YearsPro': [player['YearsPro']],
                    'CompRank': [player['CompRank']],
                    'CompPickValue': [player['CompPickValue']]
                })], ignore_index=True)
            else:
                report_df_nopicks = pd.concat([report_df_nopicks, pd.DataFrame({
                    'TeamIndex': [team_index],
                    'Status': ['PlayersGained'],
                    'PlayerName': [f"{player['FirstName']} {player['LastName']}"],
                    'Position': [player['Position']],
                    'YearsPro': [player['YearsPro']],
                    'CompRank': [player['CompRank']],
                    'CompPickValue': [player['CompPickValue']]
                })], ignore_index=True)

# Export the picks and nopicks reports to separate sheets in the Excel file
with pd.ExcelWriter(output_filename, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
    report_df_picks.to_excel(writer, sheet_name='CompPickReport_picks', index=False)
    report_df_nopicks.to_excel(writer, sheet_name='CompPickReport_nopicks', index=False)
