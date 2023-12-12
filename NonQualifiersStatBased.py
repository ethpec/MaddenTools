# Imports
import pandas as pd
import random

# Your File Path
file_path = 'Files/Madden24/IE/Season0/Final_PreAdjustment.csv'

df = pd.read_csv(file_path)

def add_regression_points(row):
    position = row['Position']
    years_pro = row['YearsPro']
    contract_status = row['ContractStatus']
    rating_tier = row['RatingTier']
    skill_point_off = row['SkillPointOff']
    skill_point_ol = row['SkillPointOL']
    skill_point_def = row['SkillPointDef']
    regression_points = row['RegressionPoints']

    if position in ['WR', 'TE'] and years_pro != 0 and contract_status in ['Signed', 'PracticeSquad']:
        if rating_tier in ['tier_0', 'tier_1', 'tier_2', 'tier_3'] and pd.isna(skill_point_off):
            regression_points += 3
        elif rating_tier in ['tier_4', 'tier_5', 'tier_6'] and pd.isna(skill_point_off):
            regression_points += 2

    if position == 'HB' and years_pro != 0 and contract_status in ['Signed', 'PracticeSquad']:
        if rating_tier in ['tier_0', 'tier_1', 'tier_2', 'tier_3'] and pd.isna(skill_point_off):
            regression_points += 3
        elif rating_tier in ['tier_4', 'tier_5', 'tier_6'] and pd.isna(skill_point_off):
            regression_points += 1

    if position in ['LT', 'LG', 'C', 'RG', 'RT'] and years_pro != 0 and contract_status in ['Signed', 'PracticeSquad']:
        if rating_tier in ['tier_0', 'tier_1', 'tier_2', 'tier_3'] and pd.isna(skill_point_ol):
            regression_points += 3
        elif rating_tier in ['tier_4', 'tier_5', 'tier_6'] and pd.isna(skill_point_ol):
            regression_points += 2

    if position in ['LE', 'DT', 'RE', 'LOLB', 'MLB', 'ROLB', 'CB', 'FS', 'SS'] and years_pro != 0 and contract_status in ['Signed', 'PracticeSquad']:
        if rating_tier in ['tier_0', 'tier_1', 'tier_2', 'tier_3'] and pd.isna(skill_point_def):
            regression_points += 3
        elif rating_tier in ['tier_4', 'tier_5', 'tier_6'] and pd.isna(skill_point_def):
            regression_points += 2

    row['RegressionPoints'] = regression_points
    return row

# Apply the new function to update the DataFrame
df = df.apply(add_regression_points, axis=1)

output_filename = 'Final.csv'
df.to_csv('Files/Madden24/IE/Season0/Final_AllStatBased.csv', index=False)