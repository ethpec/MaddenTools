import pandas as pd
import random

# Your File Path
file_path = 'Files/Madden26/IE/Season0/Final_AllStatBased.csv'
regression_values_file_path = 'Files/Madden26/IE/Season0/RegressionValues.xlsx'

df = pd.read_csv(file_path)

# Set the season phase
season_phase = "Offseason"  ### Change this to "Preseason" or "Offseason" ###

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

def calculate_qb_firstround_skill_points(row):
    if season_phase == "Offseason":
        if (
            row['YearsPro'] == 0
            and row['ContractStatus'] == 'Signed'
            and row['Age'] in {20, 21, 22, 23, 24, 25}
            and row['Position'] == 'QB'
            and row['PLYR_DRAFTROUND'] == 1
        ):
            dev = row['TraitDevelopment']
            if dev == 'Normal':
                chances = [0, 1, 2, 3, 4, 5, 6, 8, 10]
                probs   = [0.00, 0.30, 0.30, 0.30, 0.05, 0.025, 0.015, 0.005, 0.00]
            elif dev == 'College_Impact':
                chances = [0, 1, 2, 3, 4, 5, 6, 8, 10]
                probs   = [0.00, 0.00, 0.15, 0.25, 0.325, 0.20, 0.05, 0.025, 0.00]
            elif dev in {'College_Star', 'College_Elite'}:
                chances = [0, 1, 2, 3, 4, 5, 6, 8, 10]
                probs   = [0.00, 0.00, 0.00, 0.075, 0.15, 0.25, 0.40, 0.10, 0.025]
            else:
                return row['SkillPoints']

            # Note: weights don't need to sum to 1.0; proportions are fine.
            skill_points = random.choices(chances, probs)[0]
            return row['SkillPoints'] + skill_points

    # Not preseason or conditions not met
    return row['SkillPoints']

def calculate_freeagent_regression_points(row, season_phase):
    if season_phase == "Offseason":
        # Check the common conditions first
        if row['YearsPro'] >= 3 and row['ContractStatus'] == 'FreeAgent':
            if row['Position'] == 'QB':
                return row['RegressionPoints'] + 1
            elif 51 <= row['OverallRating'] <= 61:
                return row['RegressionPoints'] + 1
            elif 62 <= row['OverallRating'] <= 64:
                return row['RegressionPoints'] + 2  # Used to be 6, but not needed as of now
            elif row['OverallRating'] >= 65:
                return row['RegressionPoints'] + 2
    
    # Return unchanged if not offseason or no conditions met
    return row['RegressionPoints']

def calculate_vet_skill_point_addition(row):
    if season_phase == "Offseason":
        if row['ContractStatus'] in ['Signed', 'PracticeSquad', 'FreeAgent']:
            chance = random.random()
            if row['Position'] in ['HB', 'RB'] and row['YearsPro'] >= 3 and row['OverallRating'] <= 75:
                if chance < 0.03:
                    return row['SkillPoints'] + 2
                elif chance < 0.10:
                    return row['SkillPoints'] + 1
            elif row['Position'] in ['QB', 'FB', 'TE', 'LE', 'RE', 'DT', 'LOLB', 'ROLB', 'MLB', 'CB', 'FS', 'SS'] and row['YearsPro'] >= 3 and row['OverallRating'] <= 75:
                if chance < 0.01:
                    return row['SkillPoints'] + 2
                elif chance < 0.06:
                    return row['SkillPoints'] + 1
            elif row['Position'] in ['WR', 'LT', 'LG', 'C', 'RG', 'RT', 'K', 'P'] and row['YearsPro'] >= 3 and row['OverallRating'] <= 75:
                if chance < 0.02:
                    return row['SkillPoints'] + 2
                elif chance < 0.07:
                    return row['SkillPoints'] + 1
            elif row['Position'] in ['LS']:
                if chance < 0.10:
                    return row['SkillPoints'] + 2
                elif chance < 0.33:
                    return row['SkillPoints'] + 1

    return row['SkillPoints']

def calculate_random_regression(row):
    if season_phase == "Offseason":
        if row['ContractStatus'] in ['Signed', 'PracticeSquad', 'FreeAgent']:
            chance = random.random()
            if row['Position'] in ['LS']:
                if chance < 0.10:
                    return row['RegressionPoints'] + 2
                elif chance < 0.33:
                    return row['RegressionPoints'] + 1
            elif row['Position'] not in ['LS'] and row['YearsPro'] >= 3 and row['OverallRating'] <= 75:
                if chance < 0.03:
                    return row['RegressionPoints'] + 1
    return row['RegressionPoints']

def calculate_age_based_regression(row):
    if season_phase == "Offseason":
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

    # Default: no change
    return row['RegressionPoints']

# Apply the functions to the DataFrame
#df['RegressionPoints'] = df.apply(calculate_freeagent_regression_points, axis=1)
df['RegressionPoints'] = df.apply(
    calculate_freeagent_regression_points,
    axis=1,
    season_phase=season_phase
)
df['SkillPoints'] = df.apply(calculate_qb_firstround_skill_points, axis=1)
df['SkillPoints'] = df.apply(calculate_vet_skill_point_addition, axis=1)
df['RegressionPoints'] = df.apply(calculate_random_regression, axis=1)
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
df.to_csv('Files/Madden26/IE/Season0/Final.csv', index=False)
