import pandas as pd
import random

# Your File Path
file_path = 'Files/Madden24/IE/Season6/Final_AllStatBased.csv'
regression_values_file_path = 'Files/Madden24/IE/Season6/RegressionValues.xlsx'

df = pd.read_csv(file_path)

# Read position-specific age and regression point thresholds from an Excel file
regression_values_df = pd.read_excel(regression_values_file_path)

# Convert age range strings to tuples
regression_values_df['Age'] = regression_values_df['Age'].apply(lambda x: eval(x) if isinstance(x, str) and '-' in x else int(x))

# Create a dictionary of position and age thresholds
position_age_thresholds = {}
for _, row in regression_values_df.iterrows():
    position = row['Position']
    age = row['Age']
    regression_points = row['RegressionPoints']

    if position not in position_age_thresholds:
        position_age_thresholds[position] = []

    position_age_thresholds[position].append((age, regression_points))

def calculate_age_based_skill_points(row):
    if (
        row['YearsPro'] in [2] ### SEASON 6 IS LAST SEASON WHERE WE NEED THIS, ONLY NEED POTENTIAL AFTER THIS ###
        and row['ContractStatus'] in ['Signed', 'PracticeSquad']
        and row['Age'] in [20, 21, 22, 23, 24, 25]
        and row['Position'] not in ['QB', 'K', 'P']
    ):
        development_trait = row['TraitDevelopment']
        if development_trait == 'Normal':
            chances = [0, 1, 2, 3, 4, 5, 6, 8, 10]
            probabilities = [0.00, 0.70, 0.20, 0.05, 0.025, 0.01, 0.01, 0.005, 0.00] # Avg = 1.5 #
            skill_points = random.choices(chances, probabilities)[0]
            return row['SkillPoints'] + skill_points  # Add skill points to the existing value
        elif development_trait == 'Star':
            chances = [0, 1, 2, 3, 4, 5, 6, 8, 10]
            probabilities = [0.00, 0.10, 0.20, 0.45, 0.15, 0.05, 0.03, 0.015, 0.005] # Avg ~ 3 #
            skill_points = random.choices(chances, probabilities)[0]
            return row['SkillPoints'] + skill_points
        elif development_trait in ['Superstar', 'XFactor']:
            chances = [0, 1, 2, 3, 4, 5, 6, 8, 10]
            probabilities = [0.00, 0.00, 0.00, 0.20, 0.54, 0.15, 0.08, 0.02, 0.01] # Avg = 4.25 #
            skill_points = random.choices(chances, probabilities)[0]
            return row['SkillPoints'] + skill_points
    return row['SkillPoints']  # Keep the existing skill points if conditions are not met

def calculate_freeagent_regression_points(row):
    # Check the common conditions first
    if row['YearsPro'] >= 3 and row['ContractStatus'] == 'FreeAgent':
        if row['Position'] == 'QB':
            return row['RegressionPoints'] + 1
        elif row['OverallRating'] <= 64:
            return row['RegressionPoints'] + 6
        elif row['OverallRating'] >= 65:
            return row['RegressionPoints'] + 3
    return row['RegressionPoints']

def calculate_age_based_regression(row):
    contract_status = row['ContractStatus']
    position = row['Position']
    age = row['Age']

    # Apply regression only for specific contract statuses
    if contract_status in ['Signed', 'PracticeSquad', 'FreeAgent']:
        if position in position_age_thresholds:
            for age_range, regression_points in position_age_thresholds[position]:
                if isinstance(age_range, tuple):
                    start_age, end_age = age_range
                    if start_age <= age <= end_age:
                        return row['RegressionPoints'] + regression_points
                elif isinstance(age_range, str) and '-' in age_range:
                    range_parts = age_range.split('-')
                    if len(range_parts) == 2:
                        start_age, end_age = map(int, range_parts)
                        if start_age <= age <= end_age:
                            return row['RegressionPoints'] + regression_points
                elif age == age_range:
                    return row['RegressionPoints'] + regression_points

    return row['RegressionPoints']

# Apply the functions to the DataFrame
df['RegressionPoints'] = df.apply(calculate_freeagent_regression_points, axis=1)
df['SkillPoints'] = df.apply(calculate_age_based_skill_points, axis=1)
df['RegressionPoints'] = df.apply(calculate_age_based_regression, axis=1)

def zero_out_points(row):
    position_age_threshold = {
        'QB': 38,
        'RB': 30,
        'HB': 30,
        'FB': 32,
        'WR': 31,
        'TE': 32,
        'LT': 34,
        'LG': 34,
        'C': 34,
        'RG': 34,
        'RT': 34,
        'LE': 32,
        'RE': 32,
        'DT': 32,
        'LOLB': 32,
        'MLB': 32,
        'ROLB': 32,
        'CB': 30,
        'FS': 31,
        'SS': 31,
        'K': 38,
        'P': 38,
    }

    position = row['Position']
    age_threshold = position_age_threshold.get(position)

    if age_threshold is not None and row['Age'] >= age_threshold and row['SkillPoints'] > row['RegressionPoints']:
        row['SkillPoints'] = 0
        row['RegressionPoints'] = 0

    return row

# Apply the functions to the DataFrame
df = df.apply(zero_out_points, axis=1)

output_filename = 'Final.csv'
df.to_csv('Files/Madden24/IE/Season6/Final.csv', index=False)
