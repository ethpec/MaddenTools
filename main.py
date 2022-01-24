# Imports
from turtle import pos
import pandas as pd
import xlrd
from pandasql import sqldf

# Your File Path
file_path = 'Files/All.xlsm'

# Rating Tiers
tier_0 = range(95,100)
tier_1 = range(90,94)
tier_2 = range(85,89)
tier_3 = range(80,84)
tier_4 = range(75,79)
tier_5 = range(70,74)
tier_6 = range(0,69)

# Position Groups
offense = ['HB', 'WR', 'TE']
defense = ['LE', 'RE', 'DT', 'LOLB','ROLB', 'MLB', 'CB', 'FS', 'SS']
oline = ['RT', 'LT', 'RG', 'LG', 'C']

# Excel Sheet Dataframes (Player Data & Statistical Data)
df_players = pd.read_excel(file_path, sheet_name='124 Stuff')
df_offensiveStats = pd.read_excel(file_path, sheet_name='Offensive Stats').merge(df_players, how='right', left_on=['FullName', 'Position'], right_on=['FullName','Position'])
df_defensiveStats = pd.read_excel(file_path, sheet_name='Defensive Stats').merge(df_players, how='right', left_on=['FullName', 'Position'], right_on=['FullName','Position'])
df_olineStats = pd.read_excel(file_path, sheet_name='OLine Stats').merge(df_players, how='right', left_on=['FullName', 'Position'], right_on=['FullName','Position'])


# Test Function for looking at ratings in the tiers
# def checkrating(rating):
#     if rating in tier_0:
#         print(str(rating) + ' is in tier 0')
#     elif rating in tier_1:
#         print(str(rating) + ' is in tier 1')
#     elif rating in tier_2:
#         print(str(rating) + ' is in tier 2')
#     elif rating in tier_3:
#         print(str(rating) + ' is in tier 3')
#     elif rating in tier_4:
#         print(str(rating) + ' is in tier 4')
#     elif rating in tier_5:
#         print(str(rating) + ' is in tier 5')
#     elif rating in tier_6:
#         print(str(rating) + ' is in tier 6')
#     else:
#         print('This is not a valid rating!')

# Progression Function to be used on every row of Player Dataframe
def progression(df_players):
    if df_players.Position == 'HB':
        pass        

# # Apply the function to our Player Dataframe "row by row" (axis = 1)
# df_players.apply(progression, axis=1)

# Export our new sheet to a file
df_offensiveStats.to_csv('Files/Test.csv', sep=',',index=False)