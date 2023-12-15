# Imports
import pandas as pd
import random

# Your File Path
file_path = 'Files/Madden24/IE/Season1/Player.xlsx'

df = pd.read_excel(file_path)

def calculate_skill_points(row):
    if row['YearsPro'] == 0 and row['ContractStatus'] in ['FreeAgent', 'Signed', 'PracticeSquad'] and 'QB' not in row['Position']:
        development_trait = row['TraitDevelopment']
        if development_trait == 'Normal':
            chances = [0, 1, 2, 3, 4, 5, 6, 8, 10]
            probabilities = [0.20, 0.41, 0.20, 0.12, 0.04, 0.017, 0.008, 0.004, 0.001] ### Average = 1.5 ###
            skill_points = random.choices(chances, probabilities)[0]
            return skill_points
        elif development_trait == 'Star':
             chances = [0, 1, 2, 3, 4, 5, 6, 8, 10]
             probabilities = [0.00, 0.125, 0.45, 0.125, 0.125, 0.075, 0.05, 0.035, 0.015] ### Average = 3 ###
             skill_points = random.choices(chances, probabilities)[0]
             return skill_points
        elif development_trait == 'Superstar':
             chances = [0, 1, 2, 3, 4, 5, 6, 8, 10]
             probabilities = [0.00, 0.00, 0.00, 0.40, 0.25, 0.125, 0.10, 0.075, 0.05] ### Average = 4.5 ###
             skill_points = random.choices(chances, probabilities)[0]
             return skill_points
    return row['SkillPoints']  # Keep the existing skill points if conditions are not met

df['SkillPoints'] = df.apply(calculate_skill_points, axis=1)

output_filename = 'Player_RookieProgression.xlsx'
df.to_excel('Files/Madden24/IE/Season1/Player_RookieProgression.xlsx', index=False)