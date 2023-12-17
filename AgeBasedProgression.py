import pandas as pd
import random

# Your File Path
file_path = 'Files/Madden24/IE/Test/Final_AllStatBased.csv'
regression_values_file_path = 'Files/Madden24/IE/Test/RegressionValues.xlsx'

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
        row['YearsPro'] in [0, 1, 2, 3]
        and row['ContractStatus'] in ['Signed', 'PracticeSquad']
        and row['Age'] in [20, 21, 22, 23, 24, 25]
        and row['Position'] not in ['QB', 'K', 'P']
    ):
        development_trait = row['TraitDevelopment']
        if development_trait == 'Normal':
            chances = [0, 1, 2, 3, 4, 5, 6]
            probabilities = [0.00, 0.635, 0.26, 0.085, 0.01, 0.01, 0.00]
            skill_points = random.choices(chances, probabilities)[0]
            return row['SkillPoints'] + skill_points  # Add skill points to the existing value
        elif development_trait == 'Star':
            chances = [0, 1, 2, 3, 4, 5, 6]
            probabilities = [0.00, 0.10, 0.40, 0.25, 0.15, 0.10, 0.00]
            skill_points = random.choices(chances, probabilities)[0]
            return row['SkillPoints'] + skill_points
        elif development_trait == 'Superstar':
            chances = [0, 1, 2, 3, 4, 5, 6]
            probabilities = [0.00, 0.00, 0.00, 0.20, 0.55, 0.20, 0.05]
            skill_points = random.choices(chances, probabilities)[0]
            return row['SkillPoints'] + skill_points
        elif development_trait == 'XFactor':
            chances = [0, 1, 2, 3, 4, 5, 6]
            probabilities = [0.00, 0.00, 0.00, 0.20, 0.55, 0.20, 0.05]
            skill_points = random.choices(chances, probabilities)[0]
            return row['SkillPoints'] + skill_points
    return row['SkillPoints']  # Keep the existing skill points if conditions are not met

def calculate_freeagent_regression_points(row):
    if row['Age'] >= 26 and row['Position'] != 'QB' and row['ContractStatus'] == 'FreeAgent':
        return row['RegressionPoints'] + 3  # Add 3 points to the existing value
    return row['RegressionPoints']  # Keep the existing regression points if conditions are not met

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
                elif age == age_range:
                    return row['RegressionPoints'] + regression_points

    return row['RegressionPoints']

# Apply the functions to the DataFrame
df['RegressionPoints'] = df.apply(calculate_freeagent_regression_points, axis=1)
df['SkillPoints'] = df.apply(calculate_age_based_skill_points, axis=1)
df['RegressionPoints'] = df.apply(calculate_age_based_regression, axis=1)

output_filename = 'Final.csv'
df.to_csv('Files/Madden24/IE/Test/Final.csv', index=False)
