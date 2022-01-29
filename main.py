# Imports
from turtle import pos
import pandas as pd
import xlrd


# Your File Path
file_path = 'Files/All.xlsm'

# Season
season = 2

# Rating Tiers
tier_0 = range(95,100)
tier_1 = range(90,95)
tier_2 = range(85,90)
tier_3 = range(80,85)
tier_4 = range(75,80)
tier_5 = range(70,75)
tier_6 = range(0,70)

# Position Groups
offense = ['HB', 'WR', 'TE']
defense = ['LE', 'RE', 'DT', 'LOLB','ROLB', 'MLB', 'CB', 'FS', 'SS']
oline = ['RT', 'LT', 'RG', 'LG', 'C']

# Team Index Dictionary
team_dict = {0:'CHI', 1:'CIN', 2:'BUF', 3:'DEN', 4:'CLE', 5:'TB', 6:'ARI', 7:'LAC', 8:'KC', 9:'IND', 10:'DAL', 11:'MIA', 12:'PHI', 13:'ATL', 14:'SF', 15:'NYG', 16:'JAX', 17:'NYJ', 18:'DET', 19:'GB', 20:'CAR', 21:'NE', 22:'LV', 23:'LAR', 24:'BAL', 25:'WAS', 26:'NO', 27:'SEA', 28:'PIT', 29:'TEN', 30:'MIN', 31:'HOU'}

# Excel Sheet Dataframes (Player Data & Statistical Data)
df_players = pd.read_excel(file_path, sheet_name='124 Stuff')
df_offensiveStats = pd.read_excel(file_path, sheet_name='Offensive Stats').merge(df_players, how='left', left_on=['FullName', 'Position'], right_on=['FullName','Position'])
df_defensiveStats = pd.read_excel(file_path, sheet_name='Defensive Stats').merge(df_players, how='left', left_on=['FullName', 'Position'], right_on=['FullName','Position'])
df_olineStats = pd.read_excel(file_path, sheet_name='OLine Stats').merge(df_players, how='left', left_on=['FullName', 'Position'], right_on=['FullName','Position'])
df_kickingStats = pd.read_excel(file_path, sheet_name='Kicking Stats').merge(df_players, how='left', left_on=['FullName', 'Position'], right_on=['FullName','Position'])

# Filter Dataframes
df_offensiveStats = df_offensiveStats[(df_offensiveStats['SEAS_YEAR'] == season) 
& (df_offensiveStats['ContractStatus'] == 'Signed') & (df_offensiveStats['GAMESPLAYED'] >= 10)]
df_defensiveStats = df_defensiveStats[(df_defensiveStats['SEAS_YEAR'] == season) 
& (df_defensiveStats['ContractStatus'] == 'Signed') & (df_defensiveStats['GAMESPLAYED'] >= 10) & (df_defensiveStats['DOWNSPLAYED'] >= 250)]
df_olineStats = df_olineStats[(df_olineStats['SEAS_YEAR'] == season) 
& (df_olineStats['ContractStatus'] == 'Signed') & (df_olineStats['GAMESPLAYED'] >= 10) & (df_olineStats['DOWNSPLAYED'] >= 250)]

# Add new DataFrame columns for Offense
df_offensiveStats['ScrimmmageYardsPerGame'] = (df_offensiveStats['RUSHYARDS'] + df_offensiveStats['RECEIVEYARDS']) / df_offensiveStats['GAMESPLAYED']
df_offensiveStats['ScrimmmageTDsPerGame'] = (df_offensiveStats['RUSHTDS'] + df_offensiveStats['RECEIVETDS']) / df_offensiveStats['GAMESPLAYED']

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



# Offensive Stats/Progression
print('Running Offensive Progression')
for idx, row in df_offensiveStats.iterrows():
# Running Backs
    if  df_offensiveStats.loc[idx,'Position'] == 'HB':
        # Tier 0
        if df_offensiveStats.loc[idx,'OverallRating'] in tier_0:
            df_offensiveStats.loc[idx,'SkillPoints'] += 1
        # Tier 1
        if int(df_offensiveStats.loc[idx,'OverallRating']) in tier_1:
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
df_offensiveStats.to_csv('Files/OffTest.csv', sep=',',index=False)
df_defensiveStats.to_csv('Files/DefTest.csv', sep=',',index=False)
df_olineStats.to_csv('Files/OLTest.csv', sep=',',index=False)
df_kickingStats.to_csv('Files/KickingTest.csv', sep=',',index=False)
print('File created')