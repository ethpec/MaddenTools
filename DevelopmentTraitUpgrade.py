# Imports
import pandas as pd
import random

# Your File Path
file_path = 'Files/Madden24/IE/Season2/Player.xlsx'

df = pd.read_excel(file_path)

def update_trait_development(row):
    position = row['Position']
    overall_rating = row['OverallRating']
    years_pro = row['YearsPro']
    trait_development = row['TraitDevelopment']
    contract_status = row['ContractStatus']

    # Create a dictionary to specify the rating threshold for each position
    position_thresholds = {
        'QB': 88, 'HB': 88, 'WR': 88, 'TE': 88, 'LT': 88, 'LG': 88, 'C': 88, 'RG': 88, 'RT': 88, 'LE': 88, 'RE': 88, 'DT': 88, 'LOLB': 85, 'ROLB': 85, 'MLB': 88, 'CB': 88, 'FS': 88, 'SS': 88, 'FB': 80, 'K': 82, 'P': 82
    }
    
    if position in position_thresholds and contract_status in ['Signed', 'FreeAgent'] and trait_development in ['Normal', 'Star']:
        superstar_threshold = position_thresholds[position]
        if overall_rating >= superstar_threshold:
            return 'Superstar'
        
    # Keep existing "XFactor" unless overall rating is under 88
    if trait_development == 'XFactor' and overall_rating >= 88 and contract_status in ['Signed', 'FreeAgent']:
        return trait_development        
    
    # If not in the Superstar thresholds and between 75 and 87 OVR, update to Star
    if trait_development in ['Superstar', 'XFactor'] and years_pro >= 4 and overall_rating >= 75 and overall_rating <= 87 and contract_status in ['Signed', 'FreeAgent']:
        return 'Star'
    
    # If not in the Superstar thresholds, update to Normal
    if trait_development in ['Superstar', 'XFactor'] and years_pro >= 4 and overall_rating < 75 and contract_status in ['Signed', 'FreeAgent']:
        return 'Normal'
    
    return trait_development  # Keep the existing value if no conditions are met

df['TraitDevelopment'] = df.apply(update_trait_development, axis=1)

output_filename = 'DevTraitChange.xlsx'
df.to_excel('Files/Madden24/IE/Season2/DevTraitChange.xlsx', index=False)