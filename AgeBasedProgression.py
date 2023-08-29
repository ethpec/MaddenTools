# Imports
import pandas as pd
import random

# Your File Path
file_path = 'Files/Madden24/IE/Test/Player.xlsx'

df = pd.read_excel(file_path)

def calculate_age_based_skill_points(row):
    if row['YearsPro'] in [0, 1, 2, 3] and row['ContractStatus'] in ['Signed', 'PracticeSquad'] and row['Age'] in [20, 21, 22, 23, 24, 25] and row['Position'] not in ['QB', 'K', 'P']:
        development_trait = row['TraitDevelopment']
        if development_trait == 'Normal':
            chances = [0, 1, 2, 3, 4, 5, 6]
            probabilities = [0.00, 0.625, 0.275, 0.075, 0.025, 0.00, 0.00]
            skill_points = random.choices(chances, probabilities)[0]
            return skill_points
        elif development_trait == 'Star':
             chances = [0, 1, 2, 3, 4, 5, 6]
             probabilities = [0.00, 0.10, 0.20, 0.40, 0.20, 0.10, 0.00]
             skill_points = random.choices(chances, probabilities)[0]
             return skill_points
        elif development_trait == 'Superstar':
             chances = [0, 1, 2, 3, 4, 5, 6]
             probabilities = [0.00, 0.00, 0.00, 0.15, 0.35, 0.35, 0.15]
             skill_points = random.choices(chances, probabilities)[0]
             return skill_points
        elif development_trait == 'XFactor':
             chances = [0, 1, 2, 3, 4, 5, 6]
             probabilities = [0.00, 0.00, 0.00, 0.15, 0.35, 0.35, 0.15]
             skill_points = random.choices(chances, probabilities)[0]
             return skill_points
        else:
            return 0  # Handle other cases if needed
    else:
        return 0  # No skill points for other players

df['SkillPoints'] = df.apply(calculate_age_based_skill_points, axis=1)

output_filename = 'Player_AgeBasedProgression.xlsx'
df.to_excel('Files/Madden24/IE/Test/Player_AgeBasedProgression.xlsx', index=False)