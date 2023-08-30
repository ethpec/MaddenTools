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
    return row['SkillPoints']  # Keep the existing skill points if conditions are not met
    
def calculate_freeagent_regression_points(row):
    if row['Age'] >= 26 and row['Position'] != 'QB' and row['ContractStatus'] == 'FreeAgent':
        return row['RegressionPoints'] + 3  # Add 3 points to the existing value
    return row['RegressionPoints']  # Keep the existing regression points if conditions are not met

def update_trait_development(row):
    position = row['Position']
    overall_rating = row['OverallRating']
    years_pro = row['YearsPro']
    trait_development = row['TraitDevelopment']
    contract_status = row['ContractStatus']

    # Create a dictionary to specify the rating threshold for "Superstar" for each position
    position_thresholds = {
        'QB': 88, 'RB': 88, 'WR': 88, 'TE': 88, 'LT': 88, 'LG': 88, 'C': 88, 'RG': 88, 'RT': 88, 'LE': 88, 'RE': 88, 'DT': 88, 'LOLB': 88, 'ROLB': 88, 'MLB': 88, 'CB': 88, 'FS': 88, 'SS': 88, 'FB': 80, 'K': 82, 'P': 82
    }
    
    if position in position_thresholds and contract_status in ['Signed', 'FreeAgent'] and trait_development in ['Normal', 'Star']:
        superstar_threshold = position_thresholds[position]
        if overall_rating >= superstar_threshold:
            return 'Superstar'
        
    # Keep existing "XFactor" unless overall rating is under 90
    if trait_development == 'XFactor' and overall_rating >= 90 and contract_status in ['Signed', 'FreeAgent']:
        return trait_development        
    
    # If not in the Superstar thresholds, update to Star
    if trait_development in ['Superstar', 'XFactor'] and years_pro >= 4 and overall_rating >= 75 and contract_status in ['Signed', 'FreeAgent']:
        return 'Star'
    
    # If not in the Superstar thresholds, update to Normal
    if trait_development in ['Superstar', 'XFactor'] and years_pro >= 4 and overall_rating < 75 and contract_status in ['Signed', 'FreeAgent']:
        return 'Normal'
    
    return trait_development  # Keep the existing value if no conditions are met

df['TraitDevelopment'] = df.apply(update_trait_development, axis=1)

df['RegressionPoints'] = df.apply(calculate_freeagent_regression_points, axis=1)

df['SkillPoints'] = df.apply(calculate_age_based_skill_points, axis=1)

output_filename = 'Player_AgeBasedProgression.xlsx'
df.to_excel('Files/Madden24/IE/Test/Player_AgeBasedProgression.xlsx', index=False)