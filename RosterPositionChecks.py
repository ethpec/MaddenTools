import pandas as pd

# Your File Paths
player_file_path = 'Files/Madden24/IE/Season5/Player.xlsx'

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

# Filter contracts for players with "ContractStatus" as "Signed"
signed_contracts = player_df[player_df['ContractStatus'] == 'Signed']

# Calculate AAV and Signing Bonus columns
contract_salary_columns = ['ContractSalary0', 'ContractSalary1', 'ContractSalary2', 'ContractSalary3',
                           'ContractSalary4', 'ContractSalary5', 'ContractSalary6', 'ContractSalary7']

contract_bonus_columns = ['ContractBonus0', 'ContractBonus1', 'ContractBonus2', 'ContractBonus3',
                          'ContractBonus4', 'ContractBonus5', 'ContractBonus6', 'ContractBonus7']

# Calculate AAV and Signing Bonus columns for signed contracts
signed_contracts['AAV'] = (signed_contracts[contract_salary_columns].sum(axis=1) + signed_contracts[contract_bonus_columns].sum(axis=1)) / signed_contracts['ContractLength']
signed_contracts['AAV'] = round(signed_contracts['AAV'] / 100, 2)  # Round to nearest 100th and divide by 100

signed_contracts['SigningBonus'] = signed_contracts[contract_bonus_columns].sum(axis=1)
signed_contracts['SigningBonus'] = round(signed_contracts['SigningBonus'] / 100, 2)  # Round to nearest 100th and divide by 100

contract_year_column = signed_contracts.pop('ContractYear') 
signed_contracts.insert(signed_contracts.columns.get_loc('Position') + 1, 'ContractYear', contract_year_column)  # Insert at the desired position

# Concatenate all relevant columns at once using pd.concat() for 'Contracts' sheet
contracts_data = pd.concat([
    signed_contracts[['FirstName', 'LastName', 'Position', 'YearsPro', 'OverallRating', 'ContractLength', 'AAV', 'SigningBonus', 'TeamIndex']],
    signed_contracts['ContractYear'],  # Use only 'ContractYear' here
], axis=1)

# Add 'TeamName' to 'contracts_data' based on 'TeamIndex'
contracts_data['TeamName'] = contracts_data['TeamIndex'].map(team_dict)

# Reorder columns for the final 'contracts_data' DataFrame
contracts_data = contracts_data[['FirstName', 'LastName', 'Position', 'YearsPro' , 'OverallRating' , 'ContractYear' , 'ContractLength', 'AAV', 'SigningBonus', 'TeamIndex', 'TeamName']]

# Export the differences to a new sheet named "Differences" and add "Team Position Depth"
output_file_path = 'Files/Madden24/IE/Season5/Position_Report.xlsx'
with pd.ExcelWriter(output_file_path) as writer:
    report_data.to_excel(writer, index=False, sheet_name='Counts')
    differences.to_excel(writer, sheet_name='Differences')
    contracts_data.to_excel(writer, index=False, sheet_name='Contracts')

    # Add the 'Team Position Depth' sheet
    contracts_data_team_depth = contracts_data[['TeamIndex', 'TeamName', 'FirstName', 'LastName', 'Position', 'YearsPro' , 'OverallRating' , 'ContractYear' , 'ContractLength', 'AAV', 'SigningBonus']]
    
    # Add a 'Rank' column based on 'OverallRating' within each group of 'TeamIndex' and 'Position'
    contracts_data_team_depth['Rank'] = contracts_data_team_depth.sort_values(by=['OverallRating', 'YearsPro', 'AAV'], ascending=[False, True, True]) \
                                      .groupby(['TeamIndex', 'Position']) \
                                      .cumcount() + 1
    
    # Convert 'ContractYear' and 'ContractLength' columns to numeric, handling errors
    contracts_data_team_depth[['ContractYear', 'ContractLength']] = contracts_data_team_depth[['ContractYear', 'ContractLength']].apply(pd.to_numeric, errors='coerce')

    # Calculate the ContractYearsLeft column
    contracts_data_team_depth['ContractYearsLeft'] = contracts_data_team_depth['ContractLength'] - contracts_data_team_depth['ContractYear']

    # Reorder columns for the 'Team Position Depth' DataFrame
    contracts_data_team_depth = contracts_data_team_depth[['Rank', 'TeamIndex', 'TeamName', 'FirstName', 'LastName', 'Position', 'YearsPro' , 'OverallRating' , 'ContractYear' , 'ContractLength', 'ContractYearsLeft', 'AAV', 'SigningBonus']]
    contracts_data_team_depth.to_excel(writer, index=False, sheet_name='Team Position Depth')