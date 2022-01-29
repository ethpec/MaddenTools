# Imports
from turtle import pos
import pandas as pd
import xlrd


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

# Team Index Dictionary
team_dict = {0:'CHI', 1:'CIN', 2:'BUF', 3:'DEN', 4:'CLE', 5:'TB', 6:'ARI', 7:'LAC', 8:'KC', 9:'IND', 10:'DAL', 11:'MIA', 12:'PHI', 13:'ATL', 14:'SF', 15:'NYG', 16:'JAX', 17:'NYJ', 18:'DET', 19:'GB', 20:'CAR', 21:'NE', 22:'LV', 23:'LAR', 24:'BAL', 25:'WAS', 26:'NO', 27:'SEA', 28:'PIT', 29:'TEN', 30:'MIN', 31:'HOU'}

# Excel Sheet Dataframes (Player Data & Statistical Data)
df_players = pd.read_excel(file_path, sheet_name='124 Stuff')
df_offensiveStats = pd.read_excel(file_path, sheet_name='Offensive Stats').merge(df_players, how='right', left_on=['FullName', 'Position'], right_on=['FullName','Position'])
df_defensiveStats = pd.read_excel(file_path, sheet_name='Defensive Stats').merge(df_players, how='right', left_on=['FullName', 'Position'], right_on=['FullName','Position'])
df_olineStats = pd.read_excel(file_path, sheet_name='OLine Stats').merge(df_players, how='right', left_on=['FullName', 'Position'], right_on=['FullName','Position'])

# Add new DataFrame columns


# Offensive Stats/Progression

for idx, row in df_offensiveStats.iterrows():
    # Running Backs
    if  df_offensiveStats.loc[idx,'Position'] == 'WR':
        # Tier 0
        if df_offensiveStats.loc[idx,'OverallRating'] in tier_0:
            df_offensiveStats.loc[idx,'SkillPoints'] += 1
        # Tier 1
        if df_offensiveStats.loc[idx,'OverallRating'] in tier_1:
            df_offensiveStats.loc[idx,'SkillPoints'] += 1
        # Tier 2
        if df_offensiveStats.loc[idx,'OverallRating'] in tier_2:
            df_offensiveStats.loc[idx,'SkillPoints'] += 1
        # Tier 3
        if df_offensiveStats.loc[idx,'OverallRating'] in tier_3:
            df_offensiveStats.loc[idx,'SkillPoints'] += 1
        # Tier 4
        if df_offensiveStats.loc[idx,'OverallRating'] in tier_4:
            df_offensiveStats.loc[idx,'SkillPoints'] += 1
        # Tier 5
        if df_offensiveStats.loc[idx,'OverallRating'] in tier_5:
            df_offensiveStats.loc[idx,'SkillPoints'] += 1
        # Tier 6
        if df_offensiveStats.loc[idx,'OverallRating'] in tier_6:
            df_offensiveStats.loc[idx,'SkillPoints'] += 1

    if  df_offensiveStats.loc[idx,'Position'] == 'HB':
        df_offensiveStats.loc[idx,'SkillPoints'] = 1
    if  df_offensiveStats.loc[idx,'Position'] == 'TE':
        df_offensiveStats.loc[idx,'SkillPoints'] = 1


# Join worksheet DataFrames to player DataFrame

# Export our new sheet to a file
df_offensiveStats.to_csv('Files/Test.csv', sep=',',index=False)