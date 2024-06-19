import pandas as pd
import random

# Your File Paths
player_file_path = 'Files/Madden24/IE/Season4/Player.xlsx'
position_report_file_path = 'Files/Madden24/IE/Season4/Position_Report.xlsx'
output_file_path = 'Files/Madden24/IE/Season4/EventSystem_Results.xlsx'

# Set the season phase
season_phase = "Offseason"  ### Change this to "Preseason", "TradeDeadline", or "Offseason" ###

# Read data from the specified Excel files
player_df = pd.read_excel(player_file_path)
position_report_df = pd.read_excel(position_report_file_path, sheet_name='Team Position Depth')

# Specify relevant columns from player_df
relevant_columns_player = ['FirstName', 'LastName', 'Position', 'YearsPro', 'Age', 'ConfidenceRating', 'InjuryRating', 'InjuryType', 'InjuryStatus', 'TotalInjuryDuration']

# Select only the relevant columns from player_df
player_subset_df = player_df[relevant_columns_player]

# Merge player_subset_df with position_report_df based on specified columns
merged_df = pd.merge(player_subset_df, position_report_df, on=['FirstName', 'LastName', 'Position', 'YearsPro'], how='inner')

# Function to determine WantsContractNow based on conditions
def young_newcontract(row):
    multiplier = 1.0
    if row['Position'] in ['WR', 'LT', 'RT', 'LE', 'RE', 'CB']:
        multiplier = 1.25
    elif row['Position'] == 'QB':
        multiplier = 1.5
    
    if season_phase == "Preseason" or season_phase == "Offseason":
        if row['OverallRating'] >= 90 and row['YearsPro'] == 3 and row['ContractYearsLeft'] <= 2:
            return 'Yes' if random.random() <= 0.25 * multiplier else 'No'
        elif 85 <= row['OverallRating'] <= 89 and row['YearsPro'] == 3 and row['ContractYearsLeft'] <= 2:
            return 'Yes' if random.random() <= 0.05 * multiplier else 'No'
        elif 80 <= row['OverallRating'] <= 84 and row['YearsPro'] == 4 and row['ContractYearsLeft'] == 1:
            return 'Yes' if random.random() <= 0.05 * multiplier else 'No'
        elif 85 <= row['OverallRating'] <= 89 and row['YearsPro'] == 4 and row['ContractYearsLeft'] == 1:
            return 'Yes' if random.random() <= 0.15 * multiplier else 'No'
        elif row['OverallRating'] >= 90 and row['YearsPro'] == 4 and row['ContractYearsLeft'] == 1:
            return 'Yes' if random.random() <= 0.30 * multiplier else 'No'
        else:
            return 'No'
    else:
        return 'No'

# Apply the function to create the WantsContractNow column
merged_df['WantsContractNow'] = merged_df.apply(young_newcontract, axis=1)

# Function to determine Holdout based on conditions
def vet_wantscontract(row):
    multiplier = 1.0
    if row['Position'] in ['WR', 'LT', 'RT', 'LE', 'RE', 'CB']:
        multiplier = 1.5
    elif row['Position'] == 'QB':
        multiplier = 2.0

    if season_phase == "Preseason" or season_phase == "Offseason":
        if row['OverallRating'] >= 90 and row['Position'] in ['HB', 'RB'] and row['YearsPro'] >= 4 and row['ContractYearsLeft'] <= 2:
            return 'Yes' if random.random() <= 0.25 * multiplier else 'No'
        elif 85 <= row['OverallRating'] <= 89 and row['Position'] not in ['HB', 'RB'] and row['YearsPro'] >= 4 and row['ContractYearsLeft'] == 1:
            return 'Yes' if random.random() <= 0.05 * multiplier else 'No'
        elif 90 <= row['OverallRating'] <= 94 and row['Position'] not in ['HB', 'RB'] and row['YearsPro'] >= 4 and row['ContractYearsLeft'] == 1:
            return 'Yes' if random.random() <= 0.15 * multiplier else 'No'
        elif row['OverallRating'] >= 95 and row['Position'] not in ['HB', 'RB'] and row['YearsPro'] >= 4 and row['ContractYearsLeft'] == 1:
            return 'Yes' if random.random() <= 0.25 * multiplier else 'No'
        else:
            return 'No'
    else:
        return 'No'
    
# Apply the function to create the HoldoutForContract column
merged_df['HoldoutForContract'] = merged_df.apply(vet_wantscontract, axis=1)

# Function to determine trade request based on conditions
def traderequest_lowmorale(row):
    multiplier = 1.0
    if row['ConfidenceRating'] < 20:
        multiplier = 10.0
    elif 20 <= row['ConfidenceRating'] < 30:
        multiplier = 5.0
    elif 30 <= row['ConfidenceRating'] < 40:
        multiplier = 1.5
    elif 40 <= row['ConfidenceRating'] < 50:
        multiplier = 0.75
    elif 50 <= row['ConfidenceRating'] < 60:
        multiplier = 0.25
    elif 60 <= row['ConfidenceRating'] < 70:
        multiplier = 0.1
    elif row['ConfidenceRating'] >= 70:
        multiplier = 0.05
    
    if season_phase == "Preseason" or season_phase == "TradeDeadline" or season_phase == "Offseason":
        if row['OverallRating'] >= 80 and row['YearsPro'] >= 2 and row['Age'] <= 26 and row['ContractYearsLeft'] <= 3:
            return 'Yes' if random.random() <= 0.025 * multiplier else 'No'
        elif row['OverallRating'] >= 80 and row['YearsPro'] >= 2 and 27 <= row['Age'] >= 29 and row['ContractYearsLeft'] <= 3:
            return 'Yes' if random.random() <= 0.05 * multiplier else 'No'
        elif row['OverallRating'] >= 80 and row['YearsPro'] >= 2 and row['Age'] >= 30 and row['ContractYearsLeft'] <= 3:
            return 'Yes' if random.random() <= 0.10 * multiplier else 'No'
        else:
            return 'No'
    else:
        return 'No'
    
# Apply the function to create the TradeUnhappy column
merged_df['TradeUnhappy'] = merged_df.apply(traderequest_lowmorale, axis=1)

# Function to determine trade request based on conditions
def traderequest_playingtime(row):
    multiplier = 0.0
    if row['Position'] in ['TE', 'LT', 'LG', 'C', 'RG', 'RT', 'LOLB', 'MLB', 'ROLB', 'FS', 'SS'] and row['Rank'] >= 2:
        multiplier = 1.0
    elif row['Position'] in ['RB', 'HB', 'DT', 'LE', 'RE'] and row['Rank'] >= 3:
        multiplier = 1.0
    elif row['Position'] in ['WR', 'CB'] and row['Rank'] >= 4:
        multiplier = 1.0

    if season_phase == "Preseason" or season_phase == "TradeDeadline" or season_phase == "Offseason":
        if row['OverallRating'] >= 90 and row['YearsPro'] >= 2:
            return 'Yes' if random.random() <= 1.0 * multiplier else 'No'
        elif 80 <= row['OverallRating'] < 90 and row['YearsPro'] >= 2 and row['ContractYearsLeft'] <= 3 and row['ConfidenceRating'] <= 55:
            return 'Yes' if random.random() <= 0.75 * multiplier else 'No'
        elif 75 <= row['OverallRating'] < 80 and row['YearsPro'] >= 2 and row['ContractYearsLeft'] <= 3 and row['ConfidenceRating'] <= 55:
            return 'Yes' if random.random() <= 0.50 * multiplier else 'No'
        elif 70 <= row['OverallRating'] < 75 and row['YearsPro'] >= 2 and row['ContractYearsLeft'] <= 3 and row['ConfidenceRating'] <= 55:
            return 'Yes' if random.random() <= 0.025 * multiplier else 'No'
        else:
            return 'No'
    else:
        return 'No'
    
# Apply the function to create the TradePlayingTime column
merged_df['TradePlayingTime'] = merged_df.apply(traderequest_playingtime, axis=1)

# Function to determine offseason injury based on conditions
def injury_offseason(row):
    multiplier = 1.0
    if 73 <= row['InjuryRating'] <= 74 and row['Position'] not in ['HB', 'RB']:
        multiplier = 1.5
    if 75 <= row['InjuryRating'] <= 77 and row['Position'] not in ['HB', 'RB']:
        multiplier = 1.25
    if 78 <= row['InjuryRating'] <= 80 and row['Position'] not in ['HB', 'RB']:
        multiplier = 1.0
    if 81 <= row['InjuryRating'] <= 83 and row['Position'] not in ['HB', 'RB']:
        multiplier = 0.75
    if 84 <= row['InjuryRating'] <= 85 and row['Position'] not in ['HB', 'RB']:
        multiplier = 0.5
    if 78 <= row['InjuryRating'] <= 79 and row['Position'] in ['HB', 'RB']:
        multiplier = 1.5
    if 80 <= row['InjuryRating'] <= 82 and row['Position'] in ['HB', 'RB']:
        multiplier = 1.25
    if 83 <= row['InjuryRating'] <= 85 and row['Position'] in ['HB', 'RB']:
        multiplier = 1.0
    if 86 <= row['InjuryRating'] <= 88 and row['Position'] in ['HB', 'RB']:
        multiplier = 0.75
    if 89 <= row['InjuryRating'] <= 90 and row['Position'] in ['HB', 'RB']:
        multiplier = 0.5

    if season_phase == "Preseason":
        if row['InjuryStatus'] == 'Uninjured':
            return 'ACL' if random.random() <= 0.001 * multiplier else 'Achilles' if random.random() <= 0.002 * multiplier else 'PartialSeasonInjury' if random.random() <= 0.002 * multiplier else 'No'
        else:
            return 'No'
    else:
        return 'No'
    
# Apply the function to create the OffseasonInjury column
merged_df['OffseasonInjury'] = merged_df.apply(injury_offseason, axis=1)

# Function to determine Retirement based on conditions
def vet_earlyretirement(row):

    if season_phase == "Offseason":
        if row['Position'] in ['QB', 'K', 'P'] and row['Age'] >= 35 and row['OverallRating'] >= 70:
            return 'Yes' if random.random() <= 0.01 else 'No'
        if row['Position'] in ['RB', 'HB'] and row['Age'] >= 27 and row['OverallRating'] >= 70:
            return 'Yes' if random.random() <= 0.01 else 'No'
        if row['Position'] not in ['QB', 'RB', 'HB', 'K', 'P'] and row['Age'] >= 30 and row['OverallRating'] >= 70:
            return 'Yes' if random.random() <= 0.01 else 'No'
        else:
            return 'No'
    else:
        return 'No'
    
# Apply the function to create the Retire column
merged_df['Retire'] = merged_df.apply(vet_earlyretirement, axis=1)

# Save the merged dataframe to a new Excel file
merged_df.to_excel(output_file_path, index=False)