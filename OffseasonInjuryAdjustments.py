# Imports
import pandas as pd
import random
from config import season_path

# Your File Path
player_file_path = season_path('Player.xlsx')

df = pd.read_excel(player_file_path)

def get_duration_tier(max_injury_duration):
    if max_injury_duration >= 30:
        return '30+'
    elif max_injury_duration >= 20:
        return '20-29'
    elif max_injury_duration >= 10:
        return '10-19'
    elif max_injury_duration >= 5:
        return '5-9'
    else:
        return '1-4'

def get_injury_rating_tier(injury_rating):
    if injury_rating >= 85:
        return '85+'
    elif injury_rating >= 80:
        return '80-84'
    elif injury_rating >= 75:
        return '75-79'
    else:
        return '74-'

# Durations never go past this
DURATION_CAP = 62

# The duration each outcome rolls the player's injury to
DURATION_RANGES = {
    'SeasonEnding': (55, 62),
    'PartialSeason': (32, 45),
    'OffseasonTrainingImpact': (27, 31),
}

# The order the odds are listed in below
OUTCOME_ORDER = ('SeasonEnding', 'PartialSeason', 'OffseasonTrainingImpact')

# (MaxInjuryDuration tier, InjuryRating tier) -> percent odds of each outcome, in OUTCOME_ORDER.
# Whatever is left over out of 100 is the chance the player's injury is left alone.
INJURY_OUTCOMES = {
    ('30+',   '85+'):   (2, 4, 0),
    ('30+',   '80-84'): (4, 6, 0),
    ('30+',   '75-79'): (6, 8, 0),
    ('30+',   '74-'):   (8, 10, 0),

    ('20-29', '85+'):   (1, 3, 5),
    ('20-29', '80-84'): (2, 5, 7),
    ('20-29', '75-79'): (3, 7, 9),
    ('20-29', '74-'):   (4, 9, 11),

    ('10-19', '85+'):   (1, 2, 4),
    ('10-19', '80-84'): (1, 3, 6),
    ('10-19', '75-79'): (2, 4, 8),
    ('10-19', '74-'):   (2, 5, 10),

    ('5-9',   '85+'):   (0, 1, 3),
    ('5-9',   '80-84'): (0, 1, 4),
    ('5-9',   '75-79'): (0, 1, 5),
    ('5-9',   '74-'):   (0, 1, 6),

    ('1-4',   '85+'):   (0, 0, 1),
    ('1-4',   '80-84'): (0, 0, 1),
    ('1-4',   '75-79'): (0, 0, 1),
    ('1-4',   '74-'):   (0, 0, 1),
}

def roll_outcome(odds):
    roll = random.randint(1, 100)
    cumulative = 0
    for outcome, chance in zip(OUTCOME_ORDER, odds):
        cumulative += chance
        if roll <= cumulative:
            return outcome
    return None

# Function to update injuries
def update_offseason_injuries(row):

    # Check if the player meets the criteria to reset injury duration
    if row['ContractStatus'] in ['Signed', 'FreeAgent', 'PracticeSquad'] and row['InjuryStatus'] == 'Uninjured':
        #row['IsInjuredReserve'] == True and 
        #row['MinInjuryDuration'] >= 55 and 
        #row['MaxInjuryDuration'] >= 55):
        row['MinInjuryDuration'] = 0
        row['MaxInjuryDuration'] = 0
        row['TotalInjuryDuration'] = 0
        row['InjuryType'] = 'Invalid_'
        row['InjurySeverity'] = 'Invalid_'

    # Suspensions are stored as injuries with InjuryType 'DoNotUse' — leave their durations alone
    if (row['ContractStatus'] in ['Signed', 'FreeAgent', 'PracticeSquad'] and row['InjuryStatus'] == 'Injured'
            and row['InjuryType'] != 'DoNotUse'):

        duration_tier = get_duration_tier(row['MaxInjuryDuration'])
        rating_tier = get_injury_rating_tier(row['InjuryRating'])
        outcome = roll_outcome(INJURY_OUTCOMES[(duration_tier, rating_tier)])

        if outcome is not None:
            low, high = DURATION_RANGES[outcome]
            duration = min(random.randint(low, high), DURATION_CAP)

            # Injuries only ever get longer, and all three durations land on the same value
            if duration > int(row['MaxInjuryDuration']):
                row['MinInjuryDuration'] = duration
                row['MaxInjuryDuration'] = duration
                row['TotalInjuryDuration'] = duration

    if row['ContractStatus'] in ['Signed', 'FreeAgent', 'PracticeSquad'] and row['InjuryStatus'] == 'Uninjured':
            
        for col in row.index:
            if 'WearAndTear' in col:
                row[col] = 10

    return row

# Track the original DataFrame before applying updates
original_df = df.copy()

# Apply the new function to update the DataFrame
df = df.apply(update_offseason_injuries, axis=1)

# Identify columns with no changes
columns_to_remove = [
    column for column in df.columns if df[column].equals(original_df[column])
]

# Drop columns with no edits
df.drop(columns=columns_to_remove, inplace=True)

# Save the updated DataFrame to Excel
output_filename = season_path('Player_OffseasonInjuryChanges.xlsx')
df.to_excel(output_filename, index=False)

print(df.dtypes)