### ASSIGN WEEK 18 MATCHUPS (LINE 15) ###
### ASSIGN THE FIRST GAME OF THE SEASON BELOW IN THE CODE (LINE 105) ###

import pandas as pd
from pulp import LpVariable, LpProblem, lpSum, LpMinimize

# Load the existing schedule from Excel
file_path = 'Files/Madden24/IE/Test/TestSeasonGame.xlsx'
output_file_path = 'Files/Madden24/IE/Test/TestNewSchedule.xlsx'

# Read existing schedule
df = pd.read_excel(file_path)

### Assign Week 18 Matchups Here #################
week_18_games = df[
    (((df['HomeTeam'] == 'Jets') & (df['AwayTeam'] == 'Bills')) |
    ((df['HomeTeam'] == 'Dolphins') & (df['AwayTeam'] == 'Patriots'))) |
    (((df['HomeTeam'] == 'Browns') & (df['AwayTeam'] == 'Ravens')) |
    ((df['HomeTeam'] == 'Steelers') & (df['AwayTeam'] == 'Bengals'))) |
    (((df['HomeTeam'] == 'Texans') & (df['AwayTeam'] == 'Titans')) |
    ((df['HomeTeam'] == 'Jaguars') & (df['AwayTeam'] == 'Colts'))) |
    (((df['HomeTeam'] == 'Chiefs') & (df['AwayTeam'] == 'Chargers')) |
    ((df['HomeTeam'] == 'Broncos') & (df['AwayTeam'] == 'Raiders'))) |
    (((df['HomeTeam'] == 'Cowboys') & (df['AwayTeam'] == 'Giants')) |
    ((df['HomeTeam'] == 'Commanders') & (df['AwayTeam'] == 'Eagles'))) |
    (((df['HomeTeam'] == 'Lions') & (df['AwayTeam'] == 'Bears')) |
    ((df['HomeTeam'] == 'Vikings') & (df['AwayTeam'] == 'Packers'))) |
    (((df['HomeTeam'] == 'Panthers') & (df['AwayTeam'] == 'Buccaneers')) |
    ((df['HomeTeam'] == 'Falcons') & (df['AwayTeam'] == 'Saints'))) |
    (((df['HomeTeam'] == 'Rams') & (df['AwayTeam'] == 'Seahawks')) |
    ((df['HomeTeam'] == 'Cardinals') & (df['AwayTeam'] == '49ers')))
].copy()

# Create a new DataFrame for Week 18 Games
week_18_df = pd.DataFrame(columns=df.columns)
if not week_18_games.empty:
    week_18_df = pd.concat([week_18_df, week_18_games], ignore_index=True)

    # Drop the rows from the original DataFrame
    df = df.drop(week_18_games.index)

    # Write the modified DataFrame to a new Excel file with the Week18Games sheet
    week_18_df.to_excel('Files/Madden24/IE/Test/Week18Games.xlsx', index=False)

    print("Week 18 games have been moved to a new sheet successfully.")
else:
    print("No Week 18 games found for these matchups.")

# Define the number of games per week
games_per_week = {
    0: 16, 1: 16, 2: 16, 3: 16, 4: 14, 5: 15, 6: 13, 7: 16,
    8: 14, 9: 14, 10: 14, 11: 16, 12: 13, 13: 15, 14: 16,
    15: 16, 16: 16
}

# Define the divisional opponents for each team
divisional_opponents = {
    'Bills': ['Dolphins', 'Patriots', 'Jets'],
    'Dolphins': ['Bills', 'Patriots', 'Jets'],
    'Patriots': ['Bills', 'Dolphins', 'Jets'],
    'Jets': ['Bills', 'Dolphins', 'Patriots'],
    'Ravens': ['Bengals', 'Browns', 'Steelers'],
    'Bengals': ['Ravens', 'Browns', 'Steelers'],
    'Browns': ['Ravens', 'Bengals', 'Steelers'],
    'Steelers': ['Ravens', 'Bengals', 'Browns'],
    'Texans': ['Colts', 'Jaguars', 'Titans'],
    'Colts': ['Texans', 'Jaguars', 'Titans'],
    'Jaguars': ['Texans', 'Colts', 'Titans'],
    'Titans': ['Texans', 'Colts', 'Jaguars'],
    'Broncos': ['Chiefs', 'Raiders', 'Chargers'],
    'Chiefs': ['Broncos', 'Raiders', 'Chargers'],
    'Raiders': ['Broncos', 'Chiefs', 'Chargers'],
    'Chargers': ['Broncos', 'Chiefs', 'Raiders'],
    'Cowboys': ['Eagles', 'Giants', 'Commanders'],
    'Eagles': ['Cowboys', 'Giants', 'Commanders'],
    'Giants': ['Cowboys', 'Eagles', 'Commanders'],
    'Commanders': ['Cowboys', 'Eagles', 'Giants'],
    'Bears': ['Lions', 'Packers', 'Vikings'],
    'Lions': ['Bears', 'Packers', 'Vikings'],
    'Packers': ['Bears', 'Lions', 'Vikings'],
    'Vikings': ['Bears', 'Lions', 'Packers'],
    'Falcons': ['Panthers', 'Saints', 'Buccaneers'],
    'Panthers': ['Falcons', 'Saints', 'Buccaneers'],
    'Saints': ['Falcons', 'Panthers', 'Buccaneers'],
    'Buccaneers': ['Falcons', 'Panthers', 'Saints'],
    'Cardinals': ['Rams', '49ers', 'Seahawks'],
    'Rams': ['Cardinals', '49ers', 'Seahawks'],
    '49ers': ['Cardinals', 'Rams', 'Seahawks'],
    'Seahawks': ['Cardinals', 'Rams', '49ers']
}

# Add NewSeasonWeek column
df['NewSeasonWeek'] = 0  # Initialize with zeros

# Create optimization problem
prob = LpProblem("ScheduleOptimization", LpMinimize)

# Define decision variables
games = df.index
weeks = range(18)  # 18 weeks in the season
teams = set(df['HomeTeam']).union(set(df['AwayTeam']))
x = LpVariable.dicts("x", [(game, week) for game in games for week in weeks], 0, 1, cat='Binary')
team_week = LpVariable.dicts("team_week", [(team, week) for team in teams for week in weeks], 0, 1, cat='Binary')

##### Ensure SuperBowl Champs are HomeTeam for first game ###############################################
prob += lpSum([x[(game, 0)] for game in games if df.at[game, 'HomeTeam'] == 'Chiefs']) == 1

# Ensure Lions and Cowboys each are HomeTeam for a game on Thansgiving
prob += lpSum([x[(game, 11)] for game in games if df.at[game, 'HomeTeam'] == 'Lions']) == 1
prob += lpSum([x[(game, 11)] for game in games if df.at[game, 'HomeTeam'] == 'Cowboys']) == 1

# Define objective function
prob += lpSum([x[(game, week)] for game in games for week in weeks])

# Add constraints
for week, num_games in games_per_week.items():
    prob += lpSum([x[(game, week)] for game in games]) == num_games

# Each game must be assigned to exactly one week
for game in games:
    prob += lpSum([x[(game, week)] for week in weeks]) == 1

# Each team can be Home or Away for at most one game per week
for team in teams:
    for week in weeks:
        prob += lpSum([x[(game, week)] for game in games if df.at[game, 'HomeTeam'] == team or df.at[game, 'AwayTeam'] == team]) <= team_week[(team, week)]

# Solve the problem
prob.solve()

# Update NewSeasonWeek column with optimal assignment
for game, week in x:
    if x[(game, week)].varValue == 1:
        df.at[game, 'NewSeasonWeek'] = week

# Write updated schedule to a new Excel file
df.to_excel('Files/Madden24/IE/Test/TestNewSchedule.xlsx', index=False)