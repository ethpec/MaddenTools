import pandas as pd

# Your File Paths
player_file_path = 'Files/Madden24/IE/Test/Player.xlsx'

# Read data from the specified Excel files
player_df = pd.read_excel(player_file_path)

# Team Index Dictionary
team_dict = {0: 'CHI', 1: 'CIN', 2: 'BUF', 3: 'DEN', 4: 'CLE', 5: 'TB', 6: 'ARI', 7: 'LAC', 8: 'KC', 9: 'IND',
             10: 'DAL', 11: 'MIA', 12: 'PHI', 13: 'ATL', 14: 'SF', 15: 'NYG', 16: 'JAX', 17: 'NYJ', 18: 'DET',
             19: 'GB', 20: 'CAR', 21: 'NE', 22: 'LV', 23: 'LAR', 24: 'BAL', 25: 'WAS', 26: 'NO', 27: 'SEA',
             28: 'PIT', 29: 'TEN', 30: 'MIN', 31: 'HOU', 32: 'FA'}

# Group by 'TeamIndex' and 'Position' and count occurrences
position_counts = player_df.groupby(['TeamIndex', 'Position']).size().reset_index(name='Count')

# Map TeamIndex to team names using the team_dict
position_counts['TeamName'] = position_counts['TeamIndex'].map(team_dict)

# Filter specific positions: LT, RT, LG, RG, LE, RE, LOLB, ROLB
desired_positions = ['LT', 'RT', 'LG', 'RG', 'LE', 'RE', 'LOLB', 'ROLB']
filtered_positions = position_counts[position_counts['Position'].isin(desired_positions)]

# Extract relevant columns for the report
report_data = filtered_positions[['TeamIndex', 'TeamName', 'Position', 'Count']]

# Calculate differences in counts: LT - RT, LG - RG, LOLB - ROLB, LE - RE for each team
differences = report_data.pivot_table(index=['TeamIndex', 'TeamName'], columns='Position', values='Count', fill_value=0)
differences['LT-RT'] = differences['LT'] - differences['RT']
differences['LG-RG'] = differences['LG'] - differences['RG']
differences['LOLB-ROLB'] = differences['LOLB'] - differences['ROLB']
differences['LE-RE'] = differences['LE'] - differences['RE']

# Export the differences to a new sheet named "Differences" within the same Excel file
output_file_path = 'Files/Madden24/IE/Test/Position_Report.xlsx'
with pd.ExcelWriter(output_file_path) as writer:
    report_data.to_excel(writer, index=False, sheet_name='Counts')
    differences.to_excel(writer, sheet_name='Differences')