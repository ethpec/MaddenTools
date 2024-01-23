# Imports
import pandas as pd

# Your File Path
file_path = 'Files/Madden24/IE/Season1/Player.xlsx'

# Read the Player.xlsx file into a DataFrame
df = pd.read_excel(file_path)

# Team Index Dictionary
team_dict = {0: 'CHI', 1: 'CIN', 2: 'BUF', 3: 'DEN', 4: 'CLE', 5: 'TB', 6: 'ARI', 7: 'LAC', 8: 'KC', 9: 'IND',
             10: 'DAL', 11: 'MIA', 12: 'PHI', 13: 'ATL', 14: 'SF', 15: 'NYG', 16: 'JAX', 17: 'NYJ', 18: 'DET',
             19: 'GB', 20: 'CAR', 21: 'NE', 22: 'LV', 23: 'LAR', 24: 'BAL', 25: 'WAS', 26: 'NO', 27: 'SEA',
             28: 'PIT', 29: 'TEN', 30: 'MIN', 31: 'HOU', 32: 'FA'}

# Define a function to count the number of void years for a player
def count_void_years(row):
    count = 0
    if row['ContractStatus'] == 'Signed':
        for i in range(7):
            bonus_column = f'ContractBonus{i}'
            salary_column = f'ContractSalary{i}'
            if row[bonus_column] != 0 and row[salary_column] == 0:
                count += 1
                break
            elif row[bonus_column] == 0 and row[salary_column] == 0 and row['ContractYear'] == i:
                count += 1
    return count

# Define a function to check for void years and return the first i when ContractBonus{i} != 0 and ContractSalary{i} = 0
def when_void(row):
    if row['ContractStatus'] == 'Signed':
        for i in range(7):
            bonus_column = f'ContractBonus{i}'
            salary_column = f'ContractSalary{i}'
            if row[bonus_column] != 0 and row[salary_column] == 0:
                return i
            if row[bonus_column] == 0 and row[salary_column] == 0 and row['ContractYear'] == i:
                return i
    return None

# Create a new DataFrame with the selected columns
selected_columns = ['FirstName', 'LastName', 'Position', 'TeamIndex', 'ContractLength', 'ContractYear']
result_df = df[selected_columns]

result_df = df[['FirstName', 'LastName', 'Position', 'TeamIndex', 'ContractLength', 'ContractYear']].copy()
result_df['ContractYear'] = df['ContractYear'] + 1
result_df['HasVoidYears'] = df.apply(lambda row: count_void_years(row) > 0, axis=1)
result_df['VoidYears'] = df.apply(count_void_years, axis=1)
result_df['WhenVoid'] = df.apply(when_void, axis=1)

# Add "VoidThisYear" column
result_df['VoidThisYear'] = result_df.apply(lambda row: row['ContractYear'] > row['WhenVoid'], axis=1)

# Filter the DataFrame to include only players with HasVoidYears = True
result_df = result_df[(result_df['HasVoidYears']) | (result_df['ContractYear'] > result_df['WhenVoid'])]

# Add a new column 'TeamName' based on 'TeamIndex' and 'team_dict'
result_df['TeamName'] = result_df['TeamIndex'].map(team_dict)

# Reorder the columns to place 'TeamName' after 'TeamIndex'
result_df = result_df[['FirstName', 'LastName', 'Position', 'TeamIndex', 'TeamName', 'ContractLength', 'ContractYear', 'HasVoidYears', 'VoidYears', 'WhenVoid', 'VoidThisYear']]

# Export the DataFrame to a new Excel file
output_filename = 'Files/Madden24/IE/Season1/Player_VoidYears.xlsx'
result_df.to_excel(output_filename, index=False)