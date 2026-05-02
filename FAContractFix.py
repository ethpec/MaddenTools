import pandas as pd
import math
import random

# File Paths
fa_file_path = 'Files/Madden25/IE/Season11/Player_FreeAgents.xlsx'
resign_file_path = 'Files/Madden25/IE/Season11/PlayerExpiringContracts.xlsx'
player_file_path = 'Files/Madden25/IE/Season11/Player.xlsx'
expected_length_file_path = 'Files/Madden25/IE/Season11/ExpectedContractLength.xlsx'
player_desired_length_file_path = 'Files/Madden25/IE/Season11/PlayerDesiredContractLength.xlsx'

player_df = pd.read_excel(player_file_path)
expected_length_df = pd.read_excel(expected_length_file_path)
player_desired_length_df = pd.read_excel(player_desired_length_file_path)

LENGTH_ADJUSTMENTS = {'Short': -0.25, 'Standard': 0.0, 'Long': 0.25} # Short 8%, Long 7%

def get_length_adjustment(asset_name):
    match = player_desired_length_df[player_desired_length_df['PLYR_ASSETNAME'] == asset_name]
    if match.empty:
        return 0.0
    return LENGTH_ADJUSTMENTS.get(match.iloc[0]['DesiredLength'], 0.0)

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
    if row['StatusCheck'] and row['AddedYears'] >= -1:
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

    if row['StatusCheck'] and row['AddedYears'] >= 2 and row['Position'] not in ['QB'] and 2 <= initial_contract_length <= 3:
        new_contract_length = row['ContractLength']
        random_number = random.random() + desired_adjustment
        if random_number < 0.01:
            new_contract_length -= 1
        elif random_number >= 0.49 and random_number < 0.84:
            new_contract_length += 1
        elif random_number >= 0.84:
            new_contract_length += 2
        if not pd.isna(new_contract_length) and new_contract_length != row['ContractLength']:
            return new_contract_length, True

    elif row['StatusCheck'] and row['AddedYears'] >= 2 and row['Position'] not in ['QB'] and initial_contract_length == 1:
        new_contract_length = row['ContractLength']
        random_number = random.random() + desired_adjustment
        if random_number >= 0.50 and random_number < 0.83:
            new_contract_length += 1
        elif random_number >= 0.83:
            new_contract_length += 2
        if not pd.isna(new_contract_length) and new_contract_length != row['ContractLength']:
            return new_contract_length, True

    elif row['StatusCheck'] and row['AddedYears'] == 1 and row['Position'] not in ['QB'] and 2 <= initial_contract_length <= 4:
        new_contract_length = row['ContractLength']
        random_number = random.random() + desired_adjustment
        if random_number < 0.02:
            new_contract_length -= 1
        elif random_number >= 0.73:
            new_contract_length += 1
        if not pd.isna(new_contract_length) and new_contract_length != row['ContractLength']:
            return new_contract_length, True

    elif row['StatusCheck'] and row['AddedYears'] == 1 and row['Position'] not in ['QB'] and initial_contract_length == 1:
        new_contract_length = row['ContractLength']
        random_number = random.random() + desired_adjustment
        if random_number >= 0.75:
            new_contract_length += 1
        if not pd.isna(new_contract_length) and new_contract_length != row['ContractLength']:
            return new_contract_length, True

    elif row['StatusCheck'] and row['AddedYears'] == 0 and row['Position'] not in ['QB'] and 2 <= initial_contract_length <= 4:
        new_contract_length = row['ContractLength']
        random_number = random.random() + desired_adjustment
        if random_number < 0.15:
            new_contract_length -= 1
        elif random_number >= 0.85:
            new_contract_length += 1
        if not pd.isna(new_contract_length) and new_contract_length != row['ContractLength']:
            return new_contract_length, True

    elif row['StatusCheck'] and row['AddedYears'] == 0 and row['OverallRating'] >= 70 and row['Position'] not in ['QB'] and row['ContractSalary0'] >= 150 and initial_contract_length == 1:
        new_contract_length = row['ContractLength']
        random_number = random.random() + desired_adjustment
        if random_number >= 0.85:
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

            if row['ContractLength'] == 1:
                row['ContractSalary0'] = int(row['YearlySalary'])
            elif row['ContractLength'] == 2:
                row['ContractSalary0'] = int(0.80 * row['YearlySalary'])
                row['ContractSalary1'] = int(1.20 * row['YearlySalary'])
            elif row['ContractLength'] == 3:
                row['ContractSalary0'] = int(0.75 * row['YearlySalary'])
                row['ContractSalary1'] = int(1.05 * row['YearlySalary'])
                row['ContractSalary2'] = int(1.20 * row['YearlySalary'])
            elif row['ContractLength'] == 4:
                row['ContractSalary0'] = int(0.70 * row['YearlySalary'])
                row['ContractSalary1'] = row['YearlySalary']
                row['ContractSalary2'] = int(1.10 * row['YearlySalary'])
                row['ContractSalary3'] = int(1.20 * row['YearlySalary'])
            elif row['ContractLength'] == 5:
                row['ContractSalary0'] = int(0.60 * row['YearlySalary'])
                row['ContractSalary1'] = int(0.95 * row['YearlySalary'])
                row['ContractSalary2'] = int(1.05 * row['YearlySalary'])
                row['ContractSalary3'] = int(1.15 * row['YearlySalary'])
                row['ContractSalary4'] = int(1.25 * row['YearlySalary'])
            elif row['ContractLength'] == 6:
                row['ContractSalary0'] = int(0.50 * row['YearlySalary'])
                row['ContractSalary1'] = int(0.95 * row['YearlySalary'])
                row['ContractSalary2'] = int(1.05 * row['YearlySalary'])
                row['ContractSalary3'] = int(1.10 * row['YearlySalary'])
                row['ContractSalary4'] = int(1.15 * row['YearlySalary'])
                row['ContractSalary5'] = int(1.25 * row['YearlySalary'])

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

columns_to_export = [
    'Position', 'FirstName', 'LastName', 'ContractStatus', 'DidSalaryChange', 'ContractLengthChanged', 'StatusCheck', 'OriginalContractLength',
    'ContractSalary0', 'ContractSalary1', 'ContractSalary2', 'ContractSalary3', 'ContractSalary4', 'ContractSalary5', 'ContractSalary6', 'ContractSalary7',
    'ContractBonus0', 'ContractBonus1', 'ContractBonus2', 'ContractBonus3', 'ContractBonus4', 'ContractBonus5', 'ContractBonus6', 'ContractBonus7',
    'ContractLength', 'ContractYear'
]

def run_contract_fix(status_check, output_path):
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
    df[columns_to_export].to_excel(output_path, index=False)

# FA mode
fa_df = pd.read_excel(fa_file_path)
fa_status_check = (player_df['ContractStatus'].eq('Signed')) & (fa_df['ContractStatus'].eq('FreeAgent'))
run_contract_fix(fa_status_check, 'Files/Madden25/IE/Season11/Player_FAContractFix.xlsx')

# Resign mode
resign_df = pd.read_excel(resign_file_path)
resign_status_check = (player_df['ContractStatus'].eq('Signed')) & (resign_df['ContractStatus'].eq('Expiring')) & (player_df['TeamIndex'].eq(resign_df['TeamIndex']))
run_contract_fix(resign_status_check, 'Files/Madden25/IE/Season11/Player_ResignContractFix.xlsx')
