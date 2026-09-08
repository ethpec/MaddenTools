# Imports
from turtle import pos
import pandas as pd
import numpy as np 
import sqlite3
from config import season_path

# Your File Path
file_path = season_path('AllProgRegInfo.xlsm')

# Season
season = 12 ###Change This###

# Partial Qualifiers
# Players who miss the full playing time criteria but clear the lesser criteria below still get scored,
# then have their points divided by this and rounded toward zero (3 -> 1, -5 -> -2, 4 -> 2).
partial_point_divisor = 2 ###Change This###

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

def offense_qual_mask(df, touches, criteria, default_criteria):
    """
    Offensive qualification: (GamesPlayed OR DownsPlayed) AND Touches, with thresholds looked up per position
    """
    needed = pd.DataFrame(
        df['Position'].apply(lambda p: criteria.get(p, default_criteria)).tolist(),
        index=df.index, columns=['Games','Downs','Touches'])
    return ((df['GAMESPLAYED'] >= needed['Games']) | (df['DOWNSPLAYED'] >= needed['Downs'])) & (touches >= needed['Touches'])

def defense_qual_mask(df, criteria, default_criteria):
    """
    Defensive qualification: (GamesPlayed AND DownsPlayed) OR a heavy DownsPlayed count on its own, thresholds looked up per position
    """
    needed = pd.DataFrame(
        df['Position'].apply(lambda p: criteria.get(p, default_criteria)).tolist(),
        index=df.index, columns=['Games','Downs','DownsAlone'])
    return ((df['GAMESPLAYED'] >= needed['Games']) & (df['DOWNSPLAYED'] >= needed['Downs'])) | (df['DOWNSPLAYED'] >= needed['DownsAlone'])

def apply_qual_tiers(df, full_mask, partial_mask):
    """
    Keep both full and partial qualifiers, tagging each row with the divisor applied to its points
    """
    out = df[full_mask | partial_mask].copy()
    out['PointDivisor'] = np.where(full_mask[out.index], 1, partial_point_divisor)
    return out

def aggregate_points(df_points, point_column):
    """
    Sum a player's points across every stat check, then divide partial qualifiers down and round toward zero
    """
    agg = df_points.groupby(['FullName','Position','TeamName']).agg(
        **{point_column: (point_column, 'sum'), 'PointDivisor': ('PointDivisor', 'max')}
        ).reset_index() # max keeps the larger divisor if a player somehow lands in both tiers
    agg[point_column] = np.trunc(agg[point_column] / agg['PointDivisor']).astype(int) # trunc rounds toward zero so partials get fewer skill points AND fewer regression points
    return agg.drop(columns='PointDivisor')

def trim_all_columns(df):
    """
    Trim whitespace from ends of each value across all series in dataframe
    """
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)

# Excel Sheet Dataframes (Player Data)
df_players = pd.read_excel(file_path, sheet_name='PlayerInfo')
df_players['TeamName'] = df_players['TeamIndex'].apply(lambda x: team_dict[x]) # Create column with lambda (returns the key in our team_dict for every row. Say it sees a 0 in a row, it will make a column for that row and enter CHI into it.)
df_players['RatingTier'] = df_players['OverallRating'].apply(find_rating_tier) # applies our function to every row in the column and creates a new column based on its result
df_players.to_csv(season_path('PlayerTest.csv'), sep=',',index=False)

# Excel Sheets Dataframe (Logic)
df_logic = pd.read_excel(season_path('ProgRegLogicCheck.xlsx'), sheet_name='Sheet1')
df_logic['StatHigh'] = df_logic['StatValue'].apply(make_high)
df_logic['StatLow'] = df_logic['StatValue'].apply(make_low)
df_logic.to_csv(season_path('LogicTest.csv'), sep=',',index=False)

# Excel Sheet Dataframes (Stats) and JOINS
df_offensiveStats = pd.read_excel(file_path, sheet_name='Offensive Stats').merge(df_players, how='left', left_on=['FullName', 'Position', 'TeamPrefixName'], right_on=['FullName','Position','TeamName'])
df_defensiveStats = pd.read_excel(file_path, sheet_name='Defensive Stats').merge(df_players, how='left', left_on=['FullName', 'Position','TeamPrefixName'], right_on=['FullName','Position','TeamName'])
df_olineStats = pd.read_excel(file_path, sheet_name='OLine Stats').merge(df_players, how='left', left_on=['FullName', 'Position','TeamPrefixName'], right_on=['FullName','Position','TeamName'])
df_kickingStats = pd.read_excel(file_path, sheet_name='Kicking Stats').merge(df_players, how='left', left_on=['FullName', 'Position','TeamPrefixName'], right_on=['FullName','Position','TeamName'])
df_returnStats = pd.read_excel(file_path, sheet_name='Return Stats').merge(df_players, how='left', left_on=['FullName', 'Position','TeamPrefixName'], right_on=['FullName','Position','TeamName'])

# Filter Dataframes
# Each group builds a full mask (unchanged criteria = full points) and a partial mask (lesser criteria = points divided down).
# The '& ~full' on every partial mask keeps the two tiers mutually exclusive so nobody is tagged twice.

# Offense
# Thresholds per position as (GamesPlayed, DownsPlayed, Touches) ###Change This###
# A player qualifies by meeting (GamesPlayed OR DownsPlayed) AND Touches. QBs skip the check entirely.
full_off_criteria = {
    'HB': (12, 350, 100), 'RB': (12, 350, 100),
    'WR': (12, 500, 40),
    'TE': (12, 500, 25),
}
partial_off_criteria = {
    'HB': (8, 150, 50), 'RB': (8, 150, 50),
    'WR': (8, 300, 20),
    'TE': (8, 300, 15),
}
default_full_off_criteria = (12, 500, 25) # any offensive position not listed above (FB) falls back to the TE bar
default_partial_off_criteria = (8, 300, 15)

base_off = (df_offensiveStats['SEAS_YEAR'] == season) & (df_offensiveStats['ContractStatus'] == 'Signed')
touches_off = df_offensiveStats['RECEIVECATCHES'] + df_offensiveStats['RUSHATTEMPTS']
full_off = base_off & (
    offense_qual_mask(df_offensiveStats, touches_off, full_off_criteria, default_full_off_criteria) |
    (df_offensiveStats['Position'] == 'QB')
)
partial_off = base_off & ~full_off & offense_qual_mask(
    df_offensiveStats, touches_off, partial_off_criteria, default_partial_off_criteria)
df_offensiveStats = apply_qual_tiers(df_offensiveStats, full_off, partial_off)

# Defense
# Thresholds per position as (GamesPlayed, DownsPlayed, DownsPlayedAlone) ###Change This###
# A player qualifies by meeting (GamesPlayed AND DownsPlayed), or the DownsPlayedAlone count by itself.
full_def_criteria = {
    'LE': (12, 350, 400), 'RE': (12, 350, 400),
    'DT': (12, 300, 350),
    'LOLB': (12, 400, 500), 'MLB': (12, 400, 500), 'ROLB': (12, 400, 500),
    'CB': (12, 400, 450), 'FS': (12, 400, 450), 'SS': (12, 400, 450),
}
partial_def_criteria = {
    'LE': (8, 250, 300), 'RE': (8, 250, 300),
    'DT': (8, 200, 250),
    'LOLB': (8, 300, 400), 'MLB': (8, 300, 400), 'ROLB': (8, 300, 400),
    'CB': (8, 300, 350), 'FS': (8, 300, 350), 'SS': (8, 300, 350),
}
default_full_def_criteria = (12, 400, 500) # every defensive position in the data is listed above, so this only catches surprises
default_partial_def_criteria = (8, 300, 400)

base_def = (df_defensiveStats['SEAS_YEAR'] == season) & (df_defensiveStats['ContractStatus'] == 'Signed')
full_def = base_def & defense_qual_mask(df_defensiveStats, full_def_criteria, default_full_def_criteria)
partial_def = base_def & ~full_def & defense_qual_mask(df_defensiveStats, partial_def_criteria, default_partial_def_criteria)
df_defensiveStats = apply_qual_tiers(df_defensiveStats, full_def, partial_def)

# O-Line
base_ol = (df_olineStats['SEAS_YEAR'] == season) & (df_olineStats['ContractStatus'] == 'Signed')
full_ol = base_ol & ( # a heavy snap count alone qualifies, otherwise games and snaps together
    ((df_olineStats['GAMESPLAYED'] >= 12) & (df_olineStats['DOWNSPLAYED'] >= 500)) |
    (df_olineStats['DOWNSPLAYED'] >= 600)
)
partial_ol = base_ol & ~full_ol & (
    ((df_olineStats['GAMESPLAYED'] >= 8) & (df_olineStats['DOWNSPLAYED'] >= 350)) |
    (df_olineStats['DOWNSPLAYED'] >= 450)
)
df_olineStats = apply_qual_tiers(df_olineStats, full_ol, partial_ol)

# Kicking
base_kicking = (df_kickingStats['SEAS_YEAR'] == season)
full_kicking = base_kicking & (df_kickingStats['GAMESPLAYED'] >= 6) & ((df_kickingStats['KICKFGATTEMPTS'] >= 15) | (df_kickingStats['PUNTATTEMPTS'] >= 30))
partial_kicking = base_kicking & ~full_kicking & (df_kickingStats['GAMESPLAYED'] >= 3) & ((df_kickingStats['KICKFGATTEMPTS'] >= 10) | (df_kickingStats['PUNTATTEMPTS'] >= 20))
df_kickingStats = apply_qual_tiers(df_kickingStats, full_kicking, partial_kicking)

# Returners
base_return = (df_returnStats['SEAS_YEAR'] == season)
returns_total = df_returnStats['KRETATTEMPTS'] + df_returnStats['PRETATTEMPTS']
full_return = base_return & (returns_total >= 25)
partial_return = base_return & ~full_return & (returns_total >= 15)
df_returnStats = apply_qual_tiers(df_returnStats, full_return, partial_return)

# Add new DataFrame columns for Offense
df_offensiveStats['ScrimmageYardsPer1000DownsPlayed'] = ((df_offensiveStats['RUSHYARDS'] + df_offensiveStats['RECEIVEYARDS']) / (df_offensiveStats['DOWNSPLAYED'])) * 1000
df_offensiveStats['RBScrimmageYardsPer300Touches'] = ((df_offensiveStats['RUSHYARDS'] + (0.5 * df_offensiveStats['RECEIVEYARDS'])) / (df_offensiveStats['RECEIVECATCHES'] + df_offensiveStats['RUSHATTEMPTS'])) * 300
df_offensiveStats['RBScrimmageTDsPerGame'] = (df_offensiveStats['RUSHTDS'] + df_offensiveStats['RECEIVETDS']) / df_offensiveStats['GAMESPLAYED']
df_offensiveStats['TDsPer1000DownsPlayed'] = ((df_offensiveStats['RUSHTDS'] + df_offensiveStats['RECEIVETDS']) / (df_offensiveStats['DOWNSPLAYED'])) * 1000
# Calculate WRPercentageofTeamPassYards
# Team passing yards are summed from full qualifiers only, so adding the partial tier does not shift the denominator for players who already qualified
team_passing_ypg_map = df_offensiveStats[df_offensiveStats['PointDivisor'] == 1].groupby('TeamIndex')['PASSYARDS'].sum() / 17
team_passing_ypg = df_offensiveStats['TeamIndex'].map(team_passing_ypg_map)
df_offensiveStats['WRPercentageofTeamPassYards'] = (df_offensiveStats['RECEIVEYARDS'] / df_offensiveStats['GAMESPLAYED']) / team_passing_ypg

# Update the 'OffTest.csv' file
df_offensiveStats.to_csv(season_path('OffTest.csv'), sep=',', index=False)

# Add new DataFrame columns for OLine
df_olineStats['SacksPer1000Snaps'] = (df_olineStats['OLINESACKSALLOWED'] / df_olineStats['DOWNSPLAYED']) * 1000

# Add new DataFrame columns for Kicking
df_kickingStats['FGPercentage'] = df_kickingStats['KICKFGMADE'] / df_kickingStats['KICKFGATTEMPTS']
df_kickingStats['EPPercentage'] = df_kickingStats['KICKEPMADE'] / df_kickingStats['KICKEPATTEMPTS']
df_kickingStats['LongestFG'] = df_kickingStats['KICKFGLONGEST']
df_kickingStats['PuntTBPerIn20'] = df_kickingStats['PUNTTOUCHBACKS'] / df_kickingStats['PUNTIN20']
df_kickingStats['YardsPerPunt'] = df_kickingStats['PUNTYARDS'] / df_kickingStats['PUNTATTEMPTS']
df_kickingStats['NetYardsToPuntYards'] = df_kickingStats['PUNTNETYARDS'] / df_kickingStats['PUNTYARDS']

# Add new DataFrame columns for Returners
df_returnStats['KRYardsPerReturn'] = df_returnStats['KRETYARDS'] / df_returnStats['KRETATTEMPTS']
df_returnStats['PRYardsPerReturn'] = df_returnStats['PRETYARDS'] / df_returnStats['PRETATTEMPTS']
df_returnStats['TDsPerReturn'] = (df_returnStats['KRETTDS'] + df_returnStats['PRETTDS']) / (df_returnStats['KRETATTEMPTS'] + df_returnStats['PRETATTEMPTS'])

# Add new DataFrame columns for Defense
df_defensiveStats['DLSacksAndTFLPer1000Snaps'] = (((2.0 * df_defensiveStats['DLINESACKS']) + df_defensiveStats['DEFTACKLESFORLOSS']) / df_defensiveStats['DOWNSPLAYED']) * 1000
df_defensiveStats['DTSacksAndTFLPer1000Snaps'] = (((2.5 * df_defensiveStats['DLINESACKS']) + df_defensiveStats['DEFTACKLESFORLOSS']) / df_defensiveStats['DOWNSPLAYED']) * 1000
df_defensiveStats['TotalTurnoversPer1000Snaps'] = ((df_defensiveStats['DLINEFUMBLERECOVERIES'] + df_defensiveStats['DLINESAFETIES'] + df_defensiveStats['DSECINTS'] + df_defensiveStats['DSECINTTDS'] + df_defensiveStats['DLINEBLOCKS'] + df_defensiveStats['DLINEFORCEDFUMBLES'] + df_defensiveStats['DLINEFUMBLETDS'])/ df_defensiveStats['DOWNSPLAYED']) * 1000
df_defensiveStats['LBSacksTFLPassDeflPer1000Snaps'] = ((df_defensiveStats['DLINESACKS'] + df_defensiveStats['DEFTACKLESFORLOSS'] + df_defensiveStats['DEFPASSDEFLECTIONS']) / df_defensiveStats['DOWNSPLAYED']) * 1000
df_defensiveStats['TacklesPer1000Snaps'] = ((df_defensiveStats['ASSDEFTACKLES'] + df_defensiveStats['DEFTACKLES']) / df_defensiveStats['DOWNSPLAYED']) * 1000
df_defensiveStats['CBPassDeflPer1000Snaps'] = (df_defensiveStats['DEFPASSDEFLECTIONS'] / df_defensiveStats['DOWNSPLAYED']) * 1000
df_defensiveStats['CBCatchAllowPer100Snaps'] = (df_defensiveStats['CTHALLOWED'] / df_defensiveStats['DOWNSPLAYED']) * 100
df_defensiveStats['SafetiesCatchAllowMinusPDPerGame'] = (df_defensiveStats['CTHALLOWED'] - df_defensiveStats['DEFPASSDEFLECTIONS']) / df_defensiveStats['GAMESPLAYED']

# Melt (Unpivot) Offensive Dataframe
df_offensiveStats_unpivot = pd.melt(df_offensiveStats,id_vars=['FullName', 'Position', 'TeamName','RatingTier','PointDivisor'],value_vars=['ScrimmageYardsPer1000DownsPlayed','TDsPer1000DownsPlayed','RBScrimmageYardsPer300Touches','RBScrimmageTDsPerGame','RUSHFUMBLES','WRPercentageofTeamPassYards' ],var_name='StatCheck',value_name='value')
conn = sqlite3.connect(":memory:") # connect to Python memory to be able to query DataFrame variables as if they were tables
df_logic.to_sql("df_logic", conn, index=False)
df_offensiveStats_unpivot.to_sql("df_offensiveStats_unpivot", conn, index=False)
qry_off = '''
SELECT df2.SkillPoint AS SkillPointOff, df1.*, df2.StatTier, df2.StatHigh, df2.StatLow
FROM df_offensiveStats_unpivot df1
INNER JOIN df_logic df2 ON (df1.StatCheck = df2.StatCheck) AND (df1.Position = df2.Position) AND (df1.RatingTier = df2.RatingTier) AND ((df1.value >= df2.StatLow and df1.value < df2.StatHigh) OR df1.value = df2.StatLow);
''' # our query
df_off_points = pd.read_sql_query(qry_off,conn) # read query into a new DataFrame
df_off_points_agg = aggregate_points(df_off_points, 'SkillPointOff') # add all the skill points up, then divide partial qualifiers down
df_off_points_agg.to_csv(season_path('Points_off.csv'), sep=',',index=False)
df_offensiveStats = df_offensiveStats.merge(df_off_points_agg, how='left', left_on=['FullName', 'Position','TeamPrefixName'], right_on=['FullName','Position','TeamName'])

# Melt Defensive DataFrame
df_defensiveStats_unpivot = pd.melt(df_defensiveStats,id_vars=['FullName', 'Position', 'TeamName','RatingTier','PointDivisor'],value_vars=['DLSacksAndTFLPer1000Snaps','DTSacksAndTFLPer1000Snaps','TotalTurnoversPer1000Snaps','LBSacksTFLPassDeflPer1000Snaps','TacklesPer1000Snaps','CBPassDeflPer1000Snaps','CBCatchAllowPer100Snaps','SafetiesCatchAllowMinusPDPerGame'],var_name='StatCheck',value_name='value')
conn = sqlite3.connect(":memory:") # connect to Python memory to be able to query DataFrame variables as if they were tables
df_logic.to_sql("df_logic", conn, index=False)
df_defensiveStats_unpivot.to_sql("df_defensiveStats_unpivot", conn, index=False)
qry_def = '''
SELECT df2.SkillPoint AS SkillPointDef, df1.*, df2.StatTier, df2.StatHigh, df2.StatLow
FROM df_defensiveStats_unpivot df1
INNER JOIN df_logic df2 ON (df1.StatCheck = df2.StatCheck) AND (df1.Position = df2.Position) AND (df1.RatingTier = df2.RatingTier) AND ((df1.value >= df2.StatLow and df1.value < df2.StatHigh) OR df1.value = df2.StatLow);
''' # our query
df_def_points = pd.read_sql_query(qry_def,conn) # read query into a new DataFrame
df_def_points_agg = aggregate_points(df_def_points, 'SkillPointDef') # add all the skill points up, then divide partial qualifiers down
df_def_points_agg.to_csv(season_path('Points_def.csv'), sep=',',index=False)
df_defensiveStats = df_defensiveStats.merge(df_def_points_agg, how='left', left_on=['FullName', 'Position','TeamPrefixName'], right_on=['FullName','Position','TeamName'])

# Melt O-Line DataFrame
df_olineStats_unpivot = pd.melt(df_olineStats,id_vars=['FullName', 'Position', 'TeamName','RatingTier','PointDivisor'],value_vars=['SacksPer1000Snaps'],var_name='StatCheck',value_name='value')
conn = sqlite3.connect(":memory:") # connect to Python memory to be able to query DataFrame variables as if they were tables
df_logic.to_sql("df_logic", conn, index=False)
df_olineStats_unpivot.to_sql("df_olineStats_unpivot", conn, index=False)
qry_oline = '''
SELECT df2.SkillPoint AS SkillPointOL, df1.*, df2.StatTier, df2.StatHigh, df2.StatLow
FROM df_olineStats_unpivot df1
INNER JOIN df_logic df2 ON (df1.StatCheck = df2.StatCheck) AND (df1.Position = df2.Position) AND (df1.RatingTier = df2.RatingTier) AND ((df1.value >= df2.StatLow and df1.value < df2.StatHigh) OR df1.value = df2.StatLow);
''' # our query
df_oline_points = pd.read_sql_query(qry_oline,conn) # read query into a new DataFrame
df_oline_points_agg = aggregate_points(df_oline_points, 'SkillPointOL') # add all the skill points up, then divide partial qualifiers down
df_oline_points_agg.to_csv(season_path('Points_ol.csv'), sep=',',index=False)
df_olineStats = df_olineStats.merge(df_oline_points_agg, how='left', left_on=['FullName', 'Position','TeamPrefixName'], right_on=['FullName','Position','TeamName'])

# Melt Kicking DataFrame
df_kickingStats_unpivot = pd.melt(df_kickingStats,id_vars=['FullName', 'Position', 'TeamName','RatingTier','PointDivisor'],value_vars=['FGPercentage','EPPercentage','LongestFG','PuntTBPerIn20','YardsPerPunt','NetYardsToPuntYards'],var_name='StatCheck',value_name='value')
conn = sqlite3.connect(":memory:") # connect to Python memory to be able to query DataFrame variables as if they were tables
df_logic.to_sql("df_logic", conn, index=False)
df_kickingStats_unpivot.to_sql("df_kickingStats_unpivot", conn, index=False)
qry_kicking = '''
SELECT df2.SkillPoint AS SkillPointKick, df1.*, df2.StatTier, df2.StatHigh, df2.StatLow
FROM df_kickingStats_unpivot df1
INNER JOIN df_logic df2 ON (df1.StatCheck = df2.StatCheck) AND (df1.Position = df2.Position) AND (df1.RatingTier = df2.RatingTier) AND ((df1.value >= df2.StatLow and df1.value < df2.StatHigh) OR df1.value = df2.StatLow);
''' # our query
df_kicking_points = pd.read_sql_query(qry_kicking,conn) # read query into a new DataFrame
df_kicking_points_agg = aggregate_points(df_kicking_points, 'SkillPointKick') # add all the skill points up, then divide partial qualifiers down
df_kicking_points_agg.to_csv(season_path('Points_kick.csv'), sep=',',index=False)
df_kickingStats = df_kickingStats.merge(df_kicking_points_agg, how='left', left_on=['FullName', 'Position','TeamPrefixName'], right_on=['FullName','Position','TeamName'])

# Melt Return DataFrame
#df_returnStats_unpivot = pd.melt(df_returnStats,id_vars=['FullName', 'Position', 'TeamName','RatingTier','PointDivisor'],value_vars=['KRYardsPerReturn','PRYardsPerReturn','TDsPerReturn'],var_name='StatCheck',value_name='value')
#conn = sqlite3.connect(":memory:") # connect to Python memory to be able to query DataFrame variables as if they were tables
#df_logic.to_sql("df_logic", conn, index=False)
#df_returnStats_unpivot.to_sql("df_returnStats_unpivot", conn, index=False)
#qry_return = '''
#SELECT df2.SkillPoint AS SkillPointReturner, df1.*, df2.StatTier, df2.StatHigh, df2.StatLow
#FROM df_returnStats_unpivot df1
#INNER JOIN df_logic df2 ON (df1.StatCheck = df2.StatCheck) AND (df1.Position = df2.Position) AND (df1.RatingTier = df2.RatingTier) AND ((df1.value >= df2.StatLow and df1.value < df2.StatHigh) OR df1.value = df2.StatLow);
#''' # our query
#df_return_points = pd.read_sql_query(qry_return,conn) # read query into a new DataFrame
#df_return_points_agg = aggregate_points(df_return_points, 'SkillPointReturner') # add all the skill points up, then divide partial qualifiers down
#df_return_points_agg.to_csv(season_path('Points_return.csv'), sep=',',index=False)
#df_returnStats = df_returnStats.merge(df_return_points_agg, how='left', left_on=['FullName', 'Position','TeamPrefixName'], right_on=['FullName','Position','TeamName'])

# Join worksheet DataFrames to player DataFrame
df_final = df_players.merge(
    df_off_points_agg, how='left', left_on=['FullName', 'Position', 'TeamName'], right_on=['FullName','Position','TeamName']).merge(
        df_def_points_agg, how='left', left_on=['FullName', 'Position', 'TeamName'], right_on=['FullName','Position','TeamName']).merge(
            df_oline_points_agg, how='left', left_on=['FullName', 'Position', 'TeamName'], right_on=['FullName','Position','TeamName']).merge(
                df_kicking_points_agg, how='left', left_on=['FullName', 'Position', 'TeamName'], right_on=['FullName','Position','TeamName']
                )

# Update Regression and Skill Point columns
df_final['SkillPoints'] = df_final['SkillPointOff'].fillna(df_final['SkillPointDef']).fillna(df_final['SkillPointOL']).fillna(df_final['SkillPointKick']).fillna(0)
df_final.loc[df_final['SkillPoints'] < 0, 'RegressionPoints'] = abs(df_final['SkillPoints'])
df_final.loc[df_final['SkillPoints'] < 0, 'SkillPoints'] = 0
# The left joins above reintroduce NaN, which makes these columns float, so cast back to whole numbers
df_final['SkillPoints'] = df_final['SkillPoints'].fillna(0).astype(int)
df_final['RegressionPoints'] = df_final['RegressionPoints'].fillna(0).astype(int)

# # Export our DataFrames to various test files
df_offensiveStats.to_csv(season_path('OffTest.csv'), sep=',',index=False)
df_defensiveStats.to_csv(season_path('DefTest.csv'), sep=',',index=False)
df_olineStats.to_csv(season_path('OLTest.csv'), sep=',',index=False)
df_kickingStats.to_csv(season_path('KickingTest.csv'), sep=',',index=False)
df_returnStats.to_csv(season_path('ReturnTest.csv'), sep=',',index=False)
# df_defensiveStats_unpivot.to_csv(season_path('Defense_Unpivot.csv'), sep=',',index=False)

# Export our Final Player DataFrame with updated skills points/regression points
df_final.to_csv(season_path('Final_PreAdjustment.csv'), sep=',',index=False)