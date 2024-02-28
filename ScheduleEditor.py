### Assign Week 18 Matchups, Number of Games Per Week (Match Existing Schedule), & Super Bowl Champion Week 1 Home Game ###

import pandas as pd
from pulp import LpVariable, LpProblem, lpSum, LpMinimize
import random

# Load the existing schedule from Excel
file_path = 'Files/Madden24/IE/Season3/SeasonGame.xlsx'

# Define a function to generate a schedule
def generate_schedule(file_path):
    # Read existing schedule
    df = pd.read_excel(file_path)

    ### Assign Week 18 Matchups Here #################
    week_18_games = df[
        (((df['HomeTeam'] == 'Jets') & (df['AwayTeam'] == 'Bills')) |
        ((df['HomeTeam'] == 'Dolphins') & (df['AwayTeam'] == 'Patriots'))) |
        (((df['HomeTeam'] == 'Ravens') & (df['AwayTeam'] == 'Browns')) |
        ((df['HomeTeam'] == 'Steelers') & (df['AwayTeam'] == 'Bengals'))) |
        (((df['HomeTeam'] == 'Texans') & (df['AwayTeam'] == 'Titans')) |
        ((df['HomeTeam'] == 'Jaguars') & (df['AwayTeam'] == 'Colts'))) |
        (((df['HomeTeam'] == 'Chiefs') & (df['AwayTeam'] == 'Chargers')) |
        ((df['HomeTeam'] == 'Broncos') & (df['AwayTeam'] == 'Raiders'))) |
        (((df['HomeTeam'] == 'Cowboys') & (df['AwayTeam'] == 'Giants')) |
        ((df['HomeTeam'] == 'Commanders') & (df['AwayTeam'] == 'Eagles'))) |
        (((df['HomeTeam'] == 'Packers') & (df['AwayTeam'] == 'Bears')) |
        ((df['HomeTeam'] == 'Vikings') & (df['AwayTeam'] == 'Lions'))) |
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

    # Define the number of games per week ############ Match what EA produces for the schedule
    games_per_week = {
        0: 16, 1: 16, 2: 16, 3: 16, 4: 16, 5: 14, 6: 13, 7: 15,
        8: 14, 9: 14, 10: 15, 11: 15, 12: 14, 13: 14, 14: 16,
        15: 16, 16: 16
    }

    # Shuffle the order of teams
    teams = list(set(df['HomeTeam']).union(set(df['AwayTeam'])))
    random.shuffle(teams)

    # Add NewSeasonWeek column
    df['NewSeasonWeek'] = 0  # Initialize with zeros

    # Create optimization problem
    prob = LpProblem("ScheduleOptimization", LpMinimize)

    # Define decision variables
    games = df.index
    weeks = range(18)  # 18 weeks in the season
    x = LpVariable.dicts("x", [(game, week) for game in games for week in weeks], 0, 1, cat='Binary')

    ##### Ensure SuperBowl Champs are HomeTeam for first game ###############################################
    prob += lpSum([x[(game, 0)] for game in games if df.at[game, 'HomeTeam'] == 'Jets']) == 1

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
            prob += lpSum([x[(game, week)] for game in games if df.at[game, 'HomeTeam'] == team or df.at[game, 'AwayTeam'] == team]) <= 1

    # Solve the problem
    prob.solve()

    # Update NewSeasonWeek column with optimal assignment
    for game, week in x:
        if x[(game, week)].varValue == 1:
            df.at[game, 'NewSeasonWeek'] = week

    return df, week_18_df

# Generate three schedules with differences
schedules = [generate_schedule(file_path) for _ in range(3)]

# Combine schedules into the same Excel document with each on a different tab
with pd.ExcelWriter('Files/Madden24/IE/Season3/CombinedSchedules.xlsx') as writer:
    for i, (schedule, week_18_df) in enumerate(schedules):
        schedule.to_excel(writer, sheet_name=f'Schedule_{i+1}', index=False)
    week_18_df.to_excel(writer, sheet_name='Week18Games', index=False)
