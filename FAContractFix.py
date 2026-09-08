import pandas as pd
import math
import random
from config import season_path

# File Paths
fa_file_path = season_path('Player_FreeAgents.xlsx')
resign_file_path = season_path('PlayerExpiringContracts.xlsx')
player_file_path = season_path('Player.xlsx')
expected_length_file_path = season_path('ExpectedContractLength.xlsx')
player_desired_length_file_path = season_path('PlayerDesiredContractLength.xlsx')

player_df = pd.read_excel(player_file_path)
expected_length_df = pd.read_excel(expected_length_file_path)
player_desired_length_df = pd.read_excel(player_desired_length_file_path)

LENGTH_ADJUSTMENTS = {'Short': -0.25, 'Standard': 0.0, 'Long': 0.25} # Short 8%, Long 7%

AGE_THRESHOLDS = {
    'RB': 27, 'HB': 27,
    'CB': 28,
    'WR': 29, 'DT': 29, 'LOLB': 29, 'MLB': 29, 'ROLB': 29, 'FS': 29, 'SS': 29,
    'LE': 30, 'RE': 30,
    'TE': 31, 'FB': 31,
    'LT': 32, 'LG': 32, 'C': 32, 'RG': 32, 'RT': 32,
}

def get_length_adjustment(asset_name):
    match = player_desired_length_df[player_desired_length_df['PLYR_ASSETNAME'] == asset_name]
    if match.empty:
        return 0.0
    return LENGTH_ADJUSTMENTS.get(match.iloc[0]['DesiredLength'], 0.0)

def get_age_adjustment(row):
    threshold = AGE_THRESHOLDS.get(row['Position'])
    if threshold is not None and row['Age'] >= threshold:
        return random.uniform(-0.5, -0.25)
    return 0.0

def calculate_expected_contract_length(row):
    position = row['Position']
    overall_rating = row['OverallRating']
    matching_row = expected_length_df[(expected_length_df['Position'] == position) &
                                       (expected_length_df['Rating Range Start'] <= overall_rating) &
                                       (expected_length_df['Rating Range End'] >= overall_rating)]
    if not matching_row.empty:
        return matching_row.iloc[0]['Expected Contract Length']
    else:
        return None

def compute_yearly_salary(row):
    if row['StatusCheck']:
        non_zero_salaries = [row[f'ContractSalary{i}'] for i in range(8) if row[f'ContractSalary{i}'] != 0]
        non_zero_bonuses = [row[f'ContractBonus{i}'] for i in range(8) if row[f'ContractBonus{i}'] != 0]
        if non_zero_salaries and non_zero_bonuses:
            avg_salary = sum(non_zero_salaries) / len(non_zero_salaries)
            avg_bonus = sum(non_zero_bonuses) / len(non_zero_bonuses)
            return math.ceil(avg_salary), math.ceil(avg_bonus)
        elif non_zero_salaries and not non_zero_bonuses:
            avg_salary = sum(non_zero_salaries) / len(non_zero_salaries)
            avg_bonus = 0
            return math.ceil(avg_salary), None
    return None, None

def update_contractlength(row):
    initial_contract_length = row['ContractLength']

    desired_adjustment = get_length_adjustment(row['PLYR_ASSETNAME'])
    age_adjustment = get_age_adjustment(row)

    if row['StatusCheck'] and row['AddedYears'] >= 2 and row['Position'] not in ['QB'] and 2 <= initial_contract_length <= 3:
        new_contract_length = initial_contract_length
        random_number = random.random() + desired_adjustment + age_adjustment
        if random_number < -0.10:
            new_contract_length -= 1
        elif random_number >= 0.49 and random_number < 0.84:
            new_contract_length += 1
        elif random_number >= 0.84:
            new_contract_length += 2
        if not pd.isna(new_contract_length) and new_contract_length != row['ContractLength']:
            return new_contract_length, True

    elif row['StatusCheck'] and row['AddedYears'] >= 2 and row['Position'] not in ['QB'] and initial_contract_length == 1:
        new_contract_length = initial_contract_length
        random_number = random.random() + desired_adjustment + age_adjustment
        if random_number >= 0.50 and random_number < 0.83:
            new_contract_length += 1
        elif random_number >= 0.83:
            new_contract_length += 2
        if not pd.isna(new_contract_length) and new_contract_length != row['ContractLength']:
            return new_contract_length, True

    elif row['StatusCheck'] and row['AddedYears'] == 1 and row['Position'] not in ['QB'] and 2 <= initial_contract_length <= 3:
        new_contract_length = initial_contract_length
        random_number = random.random() + desired_adjustment + age_adjustment
        if random_number < -0.05:
            new_contract_length -= 1
        elif random_number >= 0.73:
            new_contract_length += 1
        if not pd.isna(new_contract_length) and new_contract_length != row['ContractLength']:
            return new_contract_length, True

    elif row['StatusCheck'] and row['AddedYears'] == 1 and row['Position'] not in ['QB'] and initial_contract_length == 1:
        new_contract_length = initial_contract_length
        random_number = random.random() + desired_adjustment + age_adjustment
        if random_number >= 0.66:
            new_contract_length += 1
        if not pd.isna(new_contract_length) and new_contract_length != row['ContractLength']:
            return new_contract_length, True

    elif row['StatusCheck'] and row['AddedYears'] == 0 and row['Position'] not in ['QB'] and 2 <= initial_contract_length <= 3:
        new_contract_length = initial_contract_length
        random_number = random.random() + desired_adjustment + age_adjustment
        if random_number < 0.15:
            new_contract_length -= 1
        elif random_number >= 0.75:
            new_contract_length += 1
        if not pd.isna(new_contract_length) and new_contract_length != row['ContractLength']:
            return new_contract_length, True

    elif row['StatusCheck'] and row['AddedYears'] == 0 and row['OverallRating'] >= 70 and row['Position'] not in ['QB'] and row['ContractSalary0'] >= 150 and initial_contract_length == 1:
        new_contract_length = initial_contract_length
        random_number = random.random() + desired_adjustment + age_adjustment
        if random_number >= 0.80:
            new_contract_length += 1
        if not pd.isna(new_contract_length) and new_contract_length != row['ContractLength']:
            return new_contract_length, True

    return row['ContractLength'], False

def edit_contract_salary(row):
    if row['ContractLengthChanged']:
        original_salaries = [row[f'ContractSalary{i}'] for i in range(8)]
        if not pd.isna(row['YearlySalary']):
            new_contract_length = int(row['ContractLength'])
            for i in range(new_contract_length, 8):
                row[f'ContractSalary{i}'] = 0

            total = new_contract_length * row['YearlySalary']
            if row['ContractLength'] == 1:
                row['ContractSalary0'] = total
            elif row['ContractLength'] == 2:
                row['ContractSalary0'] = round(0.75 * row['YearlySalary'] / 5) * 5
                row['ContractSalary1'] = total - row['ContractSalary0']
            elif row['ContractLength'] == 3:
                row['ContractSalary0'] = round(0.70 * row['YearlySalary'] / 5) * 5
                row['ContractSalary1'] = round(1.05 * row['YearlySalary'] / 5) * 5
                row['ContractSalary2'] = total - row['ContractSalary0'] - row['ContractSalary1']
            elif row['ContractLength'] == 4:
                row['ContractSalary0'] = round(0.65 * row['YearlySalary'] / 5) * 5
                row['ContractSalary1'] = round(row['YearlySalary'] / 5) * 5
                row['ContractSalary2'] = round(1.10 * row['YearlySalary'] / 5) * 5
                row['ContractSalary3'] = total - row['ContractSalary0'] - row['ContractSalary1'] - row['ContractSalary2']
            elif row['ContractLength'] == 5:
                row['ContractSalary0'] = round(0.60 * row['YearlySalary'] / 5) * 5
                row['ContractSalary1'] = round(0.95 * row['YearlySalary'] / 5) * 5
                row['ContractSalary2'] = round(1.05 * row['YearlySalary'] / 5) * 5
                row['ContractSalary3'] = round(1.15 * row['YearlySalary'] / 5) * 5
                row['ContractSalary4'] = total - row['ContractSalary0'] - row['ContractSalary1'] - row['ContractSalary2'] - row['ContractSalary3']
            elif row['ContractLength'] == 6:
                row['ContractSalary0'] = round(0.50 * row['YearlySalary'] / 5) * 5
                row['ContractSalary1'] = round(0.95 * row['YearlySalary'] / 5) * 5
                row['ContractSalary2'] = round(1.05 * row['YearlySalary'] / 5) * 5
                row['ContractSalary3'] = round(1.10 * row['YearlySalary'] / 5) * 5
                row['ContractSalary4'] = round(1.15 * row['YearlySalary'] / 5) * 5
                row['ContractSalary5'] = total - row['ContractSalary0'] - row['ContractSalary1'] - row['ContractSalary2'] - row['ContractSalary3'] - row['ContractSalary4']

        new_salaries = [row[f'ContractSalary{i}'] for i in range(8)]
        row['DidSalaryChange'] = original_salaries != new_salaries
    return row

def edit_contract_bonus(row):
    if row['ContractLengthChanged']:
        if not pd.isna(row['YearlyBonus']):
            new_contract_length = int(row['ContractLength'])
            for i in range(new_contract_length, 8):
                row[f'ContractBonus{i}'] = 0

            if new_contract_length == 1:
                row['ContractBonus0'] = row['YearlyBonus']
            elif new_contract_length == 2:
                row['ContractBonus1'] = row['YearlyBonus']
            elif new_contract_length == 3:
                row['ContractBonus2'] = row['YearlyBonus']
                row['ContractBonus1'] = row['YearlyBonus']
            elif new_contract_length == 4:
                row['ContractBonus3'] = row['YearlyBonus']
                row['ContractBonus2'] = row['YearlyBonus']
            elif 5 <= new_contract_length <= 7:
                row['ContractBonus4'] = row['YearlyBonus']
                row['ContractBonus3'] = row['YearlyBonus']
    return row

def update_cap_hit(row):
    if row['StatusCheck']:
        row['PLYR_CAPSALARY'] = row['ContractSalary0'] + row['ContractBonus0']
        row['ContractYear'] = 0
    return row

def fix_contract_salaries(row):
    if row['YearsPro'] == 1 and row['ContractYear'] == 0 and row['ContractStatus'] == 'Signed':
        row['ContractLength'] = 1
        row['ContractSalary0'] = 100
        row['ContractBonus0'] = 5
        row['ContractSalary1'] = 0
        row['ContractSalary2'] = 0
        row['ContractSalary3'] = 0
        row['ContractSalary4'] = 0
        row['ContractBonus1'] = 0
        row['ContractBonus2'] = 0
        row['ContractBonus3'] = 0
        row['ContractBonus4'] = 0
        row['PLYR_CAPSALARY'] = 105
        row['StatusCheck'] = 'Young_Adjusted'

    if row['YearsPro'] == 2 and row['ContractYear'] == 0 and row['ContractStatus'] == 'Signed':
        row['ContractLength'] = 1
        row['ContractSalary0'] = 108
        row['ContractBonus0'] = 7
        row['ContractSalary1'] = 0
        row['ContractSalary2'] = 0
        row['ContractSalary3'] = 0
        row['ContractSalary4'] = 0
        row['ContractBonus1'] = 0
        row['ContractBonus2'] = 0
        row['ContractBonus3'] = 0
        row['ContractBonus4'] = 0
        row['PLYR_CAPSALARY'] = 115
        row['StatusCheck'] = 'Young_Adjusted'

    return row

columns_to_export = [
    'Position', 'FirstName', 'LastName', 'ContractStatus', 'DidSalaryChange', 'ContractLengthChanged', 'StatusCheck', 'OriginalContractLength',
    'ContractSalary0', 'ContractSalary1', 'ContractSalary2', 'ContractSalary3', 'ContractSalary4', 'ContractSalary5', 'ContractSalary6', 'ContractSalary7',
    'ContractBonus0', 'ContractBonus1', 'ContractBonus2', 'ContractBonus3', 'ContractBonus4', 'ContractBonus5', 'ContractBonus6', 'ContractBonus7',
    'PLYR_CAPSALARY', 'ContractLength', 'ContractYear'
]

def run_contract_fix(status_check):
    df = player_df.copy()
    df['StatusCheck'] = status_check
    df['ExpectedContractLength'] = df.apply(calculate_expected_contract_length, axis=1)
    df['AddedYears'] = df['ExpectedContractLength'] - df['ContractLength']
    df['YearlySalary'], df['YearlyBonus'] = zip(*df.apply(compute_yearly_salary, axis=1))
    df['OriginalContractLength'] = df['ContractLength']
    df['ContractLength'], df['ContractLengthChanged'] = zip(*df.apply(update_contractlength, axis=1))
    df['DidSalaryChange'] = False
    df.loc[df['ContractLengthChanged'], :] = df[df['ContractLengthChanged']].apply(edit_contract_salary, axis=1)
    df.loc[df['ContractLengthChanged'], :] = df[df['ContractLengthChanged']].apply(edit_contract_bonus, axis=1)
    df = df.apply(update_cap_hit, axis=1)
    df = df.apply(fix_contract_salaries, axis=1)
    return df

# FA mode
fa_df = pd.read_excel(fa_file_path)
fa_status_check = (player_df['ContractStatus'].eq('Signed')) & (fa_df['ContractStatus'].eq('FreeAgent'))
fa_result = run_contract_fix(fa_status_check)

# Resign mode
resign_df = pd.read_excel(resign_file_path)
resign_status_check = (player_df['ContractStatus'].eq('Signed')) & (resign_df['ContractStatus'].eq('Expiring')) & (player_df['TeamIndex'].eq(resign_df['TeamIndex']))
resign_result = run_contract_fix(resign_status_check)

# Combine: prefer FA changes; fill in Resign changes where FA wasn't active
fa_active = fa_result['StatusCheck'].astype(bool)
resign_active = resign_result['StatusCheck'].astype(bool)
combined = fa_result.copy()
use_resign = resign_active & ~fa_active
combined.loc[use_resign, columns_to_export] = resign_result.loc[use_resign, columns_to_export]
combined[columns_to_export].to_excel(season_path('Player_ContractFix.xlsx'), index=False)
