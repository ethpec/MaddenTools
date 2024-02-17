### MUST DELETE OUT 16 DIVISONAL GAMES PRIOR TO RUNNING CODE, THOSE WILL BE THE WEEK 18 MATCHUPS ###

import pandas as pd
from pulp import LpVariable, LpProblem, lpSum, LpMinimize

# Load the existing schedule from Excel
file_path = 'Files/Madden24/IE/Test/TestSeasonGame.xlsx'
output_file_path = 'Files/Madden24/IE/Test/TestNewSchedule.xlsx'

# Read existing schedule
df = pd.read_excel('Files/Madden24/IE/Test/TestSeasonGame.xlsx')

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
teams = set(df['Home']).union(set(df['Away']))
x = LpVariable.dicts("x", [(game, week) for game in games for week in weeks], 0, 1, cat='Binary')
team_week = LpVariable.dicts("team_week", [(team, week) for team in teams for week in weeks], 0, 1, cat='Binary')

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
        prob += lpSum([x[(game, week)] for game in games if df.at[game, 'Home'] == team or df.at[game, 'Away'] == team]) <= team_week[(team, week)]

# Solve the problem
prob.solve()

# Update NewSeasonWeek column with optimal assignment
for game, week in x:
    if x[(game, week)].varValue == 1:
        df.at[game, 'NewSeasonWeek'] = week

# Write updated schedule to a new Excel file
df.to_excel('Files/Madden24/IE/Test/TestNewSchedule.xlsx', index=False)