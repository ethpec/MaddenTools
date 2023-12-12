import pandas as pd
import random

# Your File Path
file_path = 'Files/Madden24/IE/Season0/Final_AllStatBased.csv'

df = pd.read_csv(file_path)

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
            probabilities = [0.00, 0.10, 0.20, 0.40, 0.20, 0.10, 0.00]
            skill_points = random.choices(chances, probabilities)[0]
            return row['SkillPoints'] + skill_points  # Add skill points to the existing value
        elif development_trait == 'Superstar':
            chances = [0, 1, 2, 3, 4, 5, 6]
            probabilities = [0.00, 0.00, 0.00, 0.15, 0.35, 0.35, 0.15]
            skill_points = random.choices(chances, probabilities)[0]
            return row['SkillPoints'] + skill_points  # Add skill points to the existing value
        elif development_trait == 'XFactor':
            chances = [0, 1, 2, 3, 4, 5, 6]
            probabilities = [0.00, 0.00, 0.00, 0.15, 0.35, 0.35, 0.15]
            skill_points = random.choices(chances, probabilities)[0]
            return row['SkillPoints'] + skill_points  # Add skill points to the existing value
    return row['SkillPoints']  # Keep the existing skill points if conditions are not met

def calculate_freeagent_regression_points(row):
    if row['Age'] >= 26 and row['Position'] != 'QB' and row['ContractStatus'] == 'FreeAgent':
        return row['RegressionPoints'] + 3  # Add 3 points to the existing value
    return row['RegressionPoints']  # Keep the existing regression points if conditions are not met

df['RegressionPoints'] = df.apply(calculate_freeagent_regression_points, axis=1)

df['SkillPoints'] = df.apply(calculate_age_based_skill_points, axis=1)

output_filename = 'Final.csv'
df.to_csv('Files/Madden24/IE/Season0/Final.csv', index=False)
