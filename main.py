# Imports
from turtle import pos
import pandas as pd
import numpy as np
import sqlite3


# Your File Path
file_path = 'Files/All.xlsm'

# Season
season = 2

# Rating Tier
tier_0 = range(95,100)
tier_1 = range(90,95)
tier_2 = range(85,90)
tier_3 = range(80,85)
tier_4 = range(75,80)
tier_5 = range(70,75)
tier_6 = range(0,70)

# Team Index Dictionary
team_dict = {0:'CHI', 1:'CIN', 2:'BUF', 3:'DEN', 4:'CLE', 5:'TB', 6:'ARI', 7:'LAC', 8:'KC', 9:'IND', 
10:'DAL', 11:'MIA', 12:'PHI', 13:'ATL', 14:'SF', 15:'NYG', 16:'JAX', 17:'NYJ', 18:'DET', 19:'GB', 
20:'CAR', 21:'NE', 22:'LV', 23:'LAR', 24:'BAL', 25:'WAS', 26:'NO', 27:'SEA', 28:'PIT', 29:'TEN', 
30:'MIN', 31:'HOU', 32:'FA'}

# Functions (Can be expanded and collapsed)

def find_rating_tier(rating):
    if rating in tier_0:
        return 'tier_0'
    elif rating in tier_1:
        return 'tier_1'
    elif rating in tier_2:
        return 'tier_2'
    elif rating in tier_3:
        return 'tier_3'
    elif rating in tier_4:
        return 'tier_4'
    elif rating in tier_5:
        return 'tier_5'
    elif rating in tier_6:
        return 'tier_6'

def make_high(range_string):
    if '>' in range_string: # for any negative ranges we must use > instead of - to not split twice
        return float(range_string.split('>')[1]) + 1
    if '-' not in range_string:
        return range_string
    if '.' in range_string:
        return ((float(range_string.split('-')[1]) * 100) + 1) / 100
    else:
        return int(range_string.split('-')[1]) + 1

def make_low(range_string):
    if '>' in range_string: # for any negative ranges we must use > instead of - to not split twice
        return range_string.split('>')[0]
    if '-' not in range_string:
        return range_string
    else:
        return range_string.split('-')[0]

def trim_all_columns(df):
    """
    Trim whitespace from ends of each value across all series in dataframe
    """
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)

# Excel Sheet Dataframes (Player Data)
df_players = pd.read_excel(file_path, sheet_name='124 Stuff')
df_players['TeamName'] = df_players['TeamIndex'].apply(lambda x: team_dict[x]) # Create column with lambda (returns the key in our team_dict for every row. Say it sees a 0 in a row, it will make a column for that row and enter CHI into it.)
df_players['RatingTier'] = df_players['OverallRating'].apply(find_rating_tier) # applies our function to every row in the column and creates a new column based on its result
df_players.to_csv('Files/PlayerTest.csv', sep=',',index=False)

# Excel Sheets Dataframe (Logic)
df_logic = pd.read_excel('Files/ProgRegLogicCheck.xlsx', sheet_name='Sheet1')
df_logic['StatHigh'] = df_logic['StatValue'].apply(make_high)
df_logic['StatLow'] = df_logic['StatValue'].apply(make_low)
df_logic.to_csv('Files/LogicTest.csv', sep=',',index=False)

# Excel Sheet Dataframes (Stats) and JOINS
df_offensiveStats = pd.read_excel(file_path, sheet_name='Offensive Stats').merge(df_players, how='left', left_on=['FullName', 'Position', 'TeamPrefixName'], right_on=['FullName','Position','TeamName'])
df_defensiveStats = pd.read_excel(file_path, sheet_name='Defensive Stats').merge(df_players, how='left', left_on=['FullName', 'Position','TeamPrefixName'], right_on=['FullName','Position','TeamName'])
df_olineStats = pd.read_excel(file_path, sheet_name='OLine Stats').merge(df_players, how='left', left_on=['FullName', 'Position','TeamPrefixName'], right_on=['FullName','Position','TeamName'])
df_kickingStats = pd.read_excel(file_path, sheet_name='Kicking Stats').merge(df_players, how='left', left_on=['FullName', 'Position','TeamPrefixName'], right_on=['FullName','Position','TeamName'])

# Filter Dataframes
df_offensiveStats = df_offensiveStats[(df_offensiveStats['SEAS_YEAR'] == season) 
& (df_offensiveStats['ContractStatus'] == 'Signed') & (df_offensiveStats['GAMESPLAYED'] >= 10)]
df_defensiveStats = df_defensiveStats[(df_defensiveStats['SEAS_YEAR'] == season) 
& (df_defensiveStats['ContractStatus'] == 'Signed') & (df_defensiveStats['GAMESPLAYED'] >= 10) & (df_defensiveStats['DOWNSPLAYED'] >= 250)]
df_olineStats = df_olineStats[(df_olineStats['SEAS_YEAR'] == season) 
& (df_olineStats['ContractStatus'] == 'Signed') & (df_olineStats['GAMESPLAYED'] >= 10) & (df_olineStats['DOWNSPLAYED'] >= 400)]
df_kickingStats = df_kickingStats[(df_kickingStats['SEAS_YEAR'] == season) 
& (df_kickingStats['ContractStatus'] == 'Signed')]

# Add new DataFrame columns for Offense
df_offensiveStats['ScrimmageYardsPerGame'] = (df_offensiveStats['RUSHYARDS'] + df_offensiveStats['RECEIVEYARDS']) / df_offensiveStats['GAMESPLAYED']
df_offensiveStats['ScrimmageTDsPerGame'] = (df_offensiveStats['RUSHTDS'] + df_offensiveStats['RECEIVETDS']) / df_offensiveStats['GAMESPLAYED']

# Add new DataFrame columns for OLine
df_olineStats['SacksPer1000Snaps'] = (df_olineStats['OLINESACKSALLOWED'] / df_olineStats['DOWNSPLAYED']) * 1000

# Add new DataFrame columns for Kicking
df_kickingStats['FGPercentage'] = df_kickingStats['KICKFGMADE'] / df_kickingStats['KICKFGATTEMPTS']
df_kickingStats['EPPercentage'] = df_kickingStats['KICKEPMADE'] / df_kickingStats['KICKEPATTEMPTS']
df_kickingStats['Over40YardPercentage'] = (df_kickingStats['KICKFGMADE40TO49'] + df_kickingStats['KICKFGMADE50ORMORE']) / (df_kickingStats['KICKFGATTEMPTS40TO49'] + df_kickingStats['KICKFGATTEMPTS50ORMORE'])
df_kickingStats['PuntTBPerIn20'] = df_kickingStats['PUNTTOUCHBACKS'] / df_kickingStats['PUNTIN20']
df_kickingStats['YardsPerPunt'] = df_kickingStats['PUNTYARDS'] / df_kickingStats['PUNTATTEMPTS']
df_kickingStats['NetYardsToPuntYards'] = df_kickingStats['PUNTNETYARDS'] / df_kickingStats['PUNTYARDS']

# Add new DataFrame columns for Defense
df_defensiveStats['DLSacksAndTFLPerGame'] = (df_defensiveStats['DLINESACKS'] + df_defensiveStats['DEFTACKLESFORLOSS']) / df_defensiveStats['GAMESPLAYED']
df_defensiveStats['TotalTurnovers'] = df_defensiveStats['DLINEFUMBLERECOVERIES'] + df_defensiveStats['DLINESAFETIES'] + df_defensiveStats['DSECINTS'] + df_defensiveStats['DSECINTTDS'] + df_defensiveStats['DLINEBLOCKS'] + df_defensiveStats['DLINEFORCEDFUMBLES'] + df_defensiveStats['DLINEFUMBLETDS']
df_defensiveStats['LBSacksTFLPassDeflPerGame'] = (df_defensiveStats['DLINESACKS'] + df_defensiveStats['DEFTACKLESFORLOSS'] + df_defensiveStats['DEFPASSDEFLECTIONS']) / df_defensiveStats['GAMESPLAYED']
df_defensiveStats['TacklesPerGame'] = (df_defensiveStats['ASSDEFTACKLES'] + df_defensiveStats['DEFTACKLES']) / df_defensiveStats['GAMESPLAYED']
df_defensiveStats['CBPassDeflPerGame'] = df_defensiveStats['DEFPASSDEFLECTIONS'] / df_defensiveStats['GAMESPLAYED']
df_defensiveStats['CBCatchAllowPer100Snaps'] = (df_defensiveStats['CTHALLOWED'] / df_defensiveStats['DOWNSPLAYED']) *100
df_defensiveStats['SafetiesCatchAllowMinusPDPerGame'] = (df_defensiveStats['CTHALLOWED'] - df_defensiveStats['DEFPASSDEFLECTIONS']) / df_defensiveStats['GAMESPLAYED']

# Melt (Unpivot) Offensive Dataframe
df_offensiveStats_unpivot = pd.melt(df_offensiveStats,id_vars=['FullName', 'Position', 'TeamName','RatingTier'],value_vars=['ScrimmageYardsPerGame','ScrimmageTDsPerGame','RUSHFUMBLES'],var_name='StatCheck',value_name='value')
conn = sqlite3.connect(":memory:") # connect to Python memory to be able to query DataFrame variables as if they were tables
df_logic.to_sql("df_logic", conn, index=False)
df_offensiveStats_unpivot.to_sql("df_offensiveStats_unpivot", conn, index=False)
qry_off = '''
SELECT df2.SkillPoint AS SkillPointOff, df1.*, df2.StatTier, df2.StatHigh, df2.StatLow
FROM df_offensiveStats_unpivot df1
INNER JOIN df_logic df2 ON (df1.StatCheck = df2.StatCheck) AND (df1.Position = df2.Position) AND (df1.RatingTier = df2.RatingTier) AND ((df1.value >= df2.StatLow and df1.value < df2.StatHigh) OR df1.value = df2.StatLow);
''' # our query
df_off_points = pd.read_sql_query(qry_off,conn) # read query into a new DataFrame
df_off_points_agg = df_off_points.groupby(['FullName','Position','TeamName'])['SkillPointOff'].sum().reset_index() # add all the skill points up
df_off_points_agg.to_csv('Files/Points_off.csv', sep=',',index=False)
df_offensiveStats = df_offensiveStats.merge(df_off_points_agg, how='left', left_on=['FullName', 'Position','TeamPrefixName'], right_on=['FullName','Position','TeamName'])

# Melt Defensive DataFrame
df_defensiveStats_unpivot = pd.melt(df_defensiveStats,id_vars=['FullName', 'Position', 'TeamName','RatingTier'],value_vars=['DLSacksAndTFLPerGame','TotalTurnovers','LBSacksTFLPassDeflPerGame','TacklesPerGame','CBPassDeflPerGame','CBCatchAllowPer100Snaps','SafetiesCatchAllowMinusPDPerGame'],var_name='StatCheck',value_name='value')
conn = sqlite3.connect(":memory:") # connect to Python memory to be able to query DataFrame variables as if they were tables
df_logic.to_sql("df_logic", conn, index=False)
df_defensiveStats_unpivot.to_sql("df_defensiveStats_unpivot", conn, index=False)
qry_def = '''
SELECT df2.SkillPoint AS SkillPointDef, df1.*, df2.StatTier, df2.StatHigh, df2.StatLow
FROM df_defensiveStats_unpivot df1
INNER JOIN df_logic df2 ON (df1.StatCheck = df2.StatCheck) AND (df1.Position = df2.Position) AND (df1.RatingTier = df2.RatingTier) AND ((df1.value >= df2.StatLow and df1.value < df2.StatHigh) OR df1.value = df2.StatLow);
''' # our query
df_def_points = pd.read_sql_query(qry_def,conn) # read query into a new DataFrame
df_def_points_agg = df_def_points.groupby(['FullName','Position','TeamName'])['SkillPointDef'].sum().reset_index() # add all the skill points up
df_def_points_agg.to_csv('Files/Points_def.csv', sep=',',index=False)
df_defensiveStats = df_defensiveStats.merge(df_def_points_agg, how='left', left_on=['FullName', 'Position','TeamPrefixName'], right_on=['FullName','Position','TeamName'])

# Melt O-Line DataFrame
df_olineStats_unpivot = pd.melt(df_olineStats,id_vars=['FullName', 'Position', 'TeamName','RatingTier'],value_vars=['SacksPer1000Snaps'],var_name='StatCheck',value_name='value')
conn = sqlite3.connect(":memory:") # connect to Python memory to be able to query DataFrame variables as if they were tables
df_logic.to_sql("df_logic", conn, index=False)
df_olineStats_unpivot.to_sql("df_olineStats_unpivot", conn, index=False)
qry_oline = '''
SELECT df2.SkillPoint AS SkillPointOL, df1.*, df2.StatTier, df2.StatHigh, df2.StatLow
FROM df_olineStats_unpivot df1
INNER JOIN df_logic df2 ON (df1.StatCheck = df2.StatCheck) AND (df1.Position = df2.Position) AND (df1.RatingTier = df2.RatingTier) AND ((df1.value >= df2.StatLow and df1.value < df2.StatHigh) OR df1.value = df2.StatLow);
''' # our query
df_oline_points = pd.read_sql_query(qry_oline,conn) # read query into a new DataFrame
df_oline_points_agg = df_oline_points.groupby(['FullName','Position','TeamName'])['SkillPointOL'].sum().reset_index() # add all the skill points up
df_oline_points_agg.to_csv('Files/Points_ol.csv', sep=',',index=False)
df_olineStats = df_olineStats.merge(df_oline_points_agg, how='left', left_on=['FullName', 'Position','TeamPrefixName'], right_on=['FullName','Position','TeamName'])

# Melt Kicking DataFrame
df_kickingStats_unpivot = pd.melt(df_kickingStats,id_vars=['FullName', 'Position', 'TeamName','RatingTier'],value_vars=['FGPercentage','EPPercentage','Over40YardPercentage','PuntTBPerIn20','YardsPerPunt','NetYardsToPuntYards'],var_name='StatCheck',value_name='value')
conn = sqlite3.connect(":memory:") # connect to Python memory to be able to query DataFrame variables as if they were tables
df_logic.to_sql("df_logic", conn, index=False)
df_kickingStats_unpivot.to_sql("df_kickingStats_unpivot", conn, index=False)
qry_kicking = '''
SELECT df2.SkillPoint AS SkillPointKick, df1.*, df2.StatTier, df2.StatHigh, df2.StatLow
FROM df_kickingStats_unpivot df1
INNER JOIN df_logic df2 ON (df1.StatCheck = df2.StatCheck) AND (df1.Position = df2.Position) AND (df1.RatingTier = df2.RatingTier) AND ((df1.value >= df2.StatLow and df1.value < df2.StatHigh) OR df1.value = df2.StatLow);
''' # our query
df_kicking_points = pd.read_sql_query(qry_kicking,conn) # read query into a new DataFrame
df_kicking_points_agg = df_kicking_points.groupby(['FullName','Position','TeamName'])['SkillPointKick'].sum().reset_index() # add all the skill points up
df_kicking_points_agg.to_csv('Files/Points_kick.csv', sep=',',index=False)
df_kickingStats = df_kickingStats.merge(df_kicking_points_agg, how='left', left_on=['FullName', 'Position','TeamPrefixName'], right_on=['FullName','Position','TeamName'])

# Join worksheet DataFrames to player DataFrame
df_final = df_players.merge(
    df_off_points_agg, how='left', left_on=['FullName', 'Position', 'TeamName'], right_on=['FullName','Position','TeamName']).merge(
        df_def_points_agg, how='left', left_on=['FullName', 'Position', 'TeamName'], right_on=['FullName','Position','TeamName']).merge(
            df_oline_points_agg, how='left', left_on=['FullName', 'Position', 'TeamName'], right_on=['FullName','Position','TeamName']).merge(
                df_kicking_points_agg, how='left', left_on=['FullName', 'Position', 'TeamName'], right_on=['FullName','Position','TeamName'])

# Update Regression and Skill Point columns
df_final['SkillPoints'] = df_final['SkillPointOff'].fillna(df_final['SkillPointDef']).fillna(df_final['SkillPointOL']).fillna(df_final['SkillPointKick']).fillna(0)
df_final.loc[df_final['SkillPoints'] < 0, 'RegressionPoints'] = abs(df_final['SkillPoints'])
df_final.loc[df_final['SkillPoints'] < 0, 'SkillPoints'] = 0

# # Export our DataFrames to various test files
# df_offensiveStats.to_csv('Files/OffTest.csv', sep=',',index=False)
# df_defensiveStats.to_csv('Files/DefTest.csv', sep=',',index=False)
# df_olineStats.to_csv('Files/OLTest.csv', sep=',',index=False)
# df_kickingStats.to_csv('Files/KickingTest.csv', sep=',',index=False)
# df_defensiveStats_unpivot.to_csv('Files/Defense_Unpivot.csv', sep=',',index=False)

# Export our Final Player DataFrame with updated skills points/regression points
df_final.to_csv('Files/Final.csv', sep=',',index=False)