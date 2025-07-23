import pandas as pd
import random

# Your File Paths
player_file_path = 'Files/Madden25/IE/Season10/Player_ExpectedSalary.xlsx' ### Replaced Player sheet, Run ContractFixer first ###
position_report_file_path = 'Files/Madden25/IE/Season10/Position_Report.xlsx'
output_file_path = 'Files/Madden25/IE/Season10/EventSystem_Results.xlsx'

# Set the season phase
season_phase = "Preseason"  ### Change this to "Preseason", "TradeDeadline", or "Offseason" ###

# Read data from the specified Excel files
player_df = pd.read_excel(player_file_path)
position_report_df = pd.read_excel(position_report_file_path, sheet_name='Team Position Depth')

# Specify relevant columns from player_df
relevant_columns_player = ['FirstName', 'LastName', 'Position', 'YearsPro', 'Age', 'ConfidenceRating', 'PLYR_DRAFTROUND','InjuryRating', 'InjuryType', 'InjuryStatus', 'TotalInjuryDuration', "ExpectedAAV"]

# Select only the relevant columns from player_df
player_subset_df = player_df[relevant_columns_player]

# Merge player_subset_df with position_report_df based on specified columns
merged_df = pd.merge(player_subset_df, position_report_df, on=['FirstName', 'LastName', 'Position', 'YearsPro'], how='inner')

def determine_contract_status(hold_out_chance, hold_in_chance, multiplier):
    chance = random.random()
    if chance <= hold_out_chance * multiplier:
        return 'Hold Out'
    elif chance <= (hold_out_chance + hold_in_chance) * multiplier:
        return 'Hold In'
    else:
        return 'No'

def young_newcontract(row):
    multiplier = 1.0
    if row['Position'] in ['WR', 'LT', 'RT', 'LE', 'RE', 'CB']:
        multiplier = 1.25
    elif row['Position'] == 'QB':
        multiplier = 1.5

    if season_phase not in ["Preseason", "Offseason"]:
        return 'No'

    rating = row['OverallRating']
    years_pro = row['YearsPro']
    years_left = row['ContractYearsLeft']

    if rating >= 90 and years_pro == 3 and years_left <= 2:
        return determine_contract_status(0.05, 0.20, multiplier)
    elif 85 <= rating <= 89 and years_pro == 3 and years_left <= 2:
        return determine_contract_status(0.01, 0.04, multiplier)
    elif 80 <= rating <= 84 and years_pro == 4 and years_left == 1:
        return determine_contract_status(0.01, 0.04, multiplier)
    elif 85 <= rating <= 89 and years_pro == 4 and years_left == 1:
        return determine_contract_status(0.03, 0.12, multiplier)
    elif rating >= 90 and years_pro == 4 and years_left == 1:
        return determine_contract_status(0.05, 0.25, multiplier)
    else:
        return 'No'

def vet_wantscontract(row):
    multiplier = 1.0
    if row['Position'] in ['WR', 'LT', 'RT', 'LE', 'RE', 'CB']:
        multiplier = 1.5
    elif row['Position'] == 'QB':
        multiplier = 2.0

    if season_phase not in ["Preseason", "Offseason"]:
        return 'No'

    rating = row['OverallRating']
    pos = row['Position']
    years_pro = row['YearsPro']
    years_left = row['ContractYearsLeft']
    current_aav = row['AAV']
    expected_aav = row['ExpectedAAV'] / 100

    if rating >= 90 and pos in ['HB', 'RB'] and years_pro >= 5 and 4 >= years_left and expected_aav >= 1.50 * current_aav:
        return determine_contract_status(0.25, 0.25, multiplier)
    elif rating >= 90 and pos in ['HB', 'RB'] and years_pro >= 5 and 4 >= years_left and expected_aav >= 1.25 * current_aav:
        return determine_contract_status(0.08, 0.25, multiplier)
    elif rating >= 90 and pos in ['HB', 'RB'] and years_pro >= 5 and 2 >= years_left and expected_aav >= current_aav:
        return determine_contract_status(0.05, 0.20, multiplier)
    
    elif rating >= 95 and pos not in ['HB', 'RB'] and years_pro >= 5 and 4 >= years_left and expected_aav >= 1.50 * current_aav:
        return determine_contract_status(0.25, 0.25, multiplier)
    elif rating >= 95 and pos not in ['HB', 'RB'] and years_pro >= 5 and 4 >= years_left and expected_aav >= 1.25 * current_aav:
        return determine_contract_status(0.08, 0.25, multiplier)
    elif rating >= 95 and pos not in ['HB', 'RB'] and years_pro >= 5 and 2 >= years_left and expected_aav >= current_aav:
        return determine_contract_status(0.05, 0.20, multiplier)
    
    elif 90 <= rating <= 94 and pos not in ['HB', 'RB'] and years_pro >= 5 and 4 >= years_left and expected_aav >= 1.50 * current_aav:
        return determine_contract_status(0.20, 0.25, multiplier)
    elif 90 <= rating <= 94 and pos not in ['HB', 'RB'] and years_pro >= 5 and 4 >= years_left and expected_aav >= 1.25 * current_aav:
        return determine_contract_status(0.08, 0.25, multiplier)
    elif 90 <= rating <= 94 and pos not in ['HB', 'RB'] and years_pro >= 5 and 2 >= years_left and expected_aav >= current_aav:
        return determine_contract_status(0.03, 0.12, multiplier)
    
    elif 85 <= rating <= 89 and pos not in ['HB', 'RB'] and years_pro >= 5 and 4 >= years_left and expected_aav >= 1.50 * current_aav:
        return determine_contract_status(0.15, 0.20, multiplier)
    elif 85 <= rating <= 89 and pos not in ['HB', 'RB'] and years_pro >= 5 and 4 >= years_left and expected_aav >= 1.25 * current_aav:
        return determine_contract_status(0.03, 0.07, multiplier)
    elif 85 <= rating <= 89 and pos not in ['HB', 'RB'] and years_pro >= 5 and 2 >= years_left and expected_aav >= current_aav:
        return determine_contract_status(0.01, 0.04, multiplier)
    
    elif 80 <= rating <= 84 and pos not in ['HB', 'RB'] and years_pro >= 5 and 4 >= years_left and expected_aav >= 1.50 * current_aav:
        return determine_contract_status(0.05, 0.15, multiplier)
    elif 80 <= rating <= 84 and pos not in ['HB', 'RB'] and years_pro >= 5 and 4 >= years_left and expected_aav >= 1.25 * current_aav:
        return determine_contract_status(0.02, 0.08, multiplier)
    elif 80 <= rating <= 84 and pos not in ['HB', 'RB'] and years_pro >= 5 and 2 >= years_left and expected_aav >= current_aav:
        return determine_contract_status(0.00, 0.01, multiplier)
    
    else:
        return 'No'

# Apply the functions
merged_df['Young_NewContract'] = merged_df.apply(young_newcontract, axis=1)
merged_df['Vet_NewContract'] = merged_df.apply(vet_wantscontract, axis=1)

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
    
    if season_phase in ["Preseason", "TradeDeadline", "Offseason"]:
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
def traderequest_wr(row):
    # Check if the position is WR
    if row['Position'] != 'WR':
        return 'No'  # Early return if the position is not WR
    
    multiplier = 1.0
    if row['ConfidenceRating'] < 20:
        multiplier = 10.0
    elif 20 <= row['ConfidenceRating'] < 30:
        multiplier = 5.0
    elif 30 <= row['ConfidenceRating'] < 40:
        multiplier = 1.5
    elif 40 <= row['ConfidenceRating'] < 50:
        multiplier = 1.0
    elif 50 <= row['ConfidenceRating'] < 60:
        multiplier = 0.5
    elif 60 <= row['ConfidenceRating'] < 70:
        multiplier = 0.1
    elif row['ConfidenceRating'] >= 70:
        multiplier = 0.05
    
    if season_phase in ["Preseason", "TradeDeadline", "Offseason"]:
        if 73 <= row['OverallRating'] <= 84 and 2 <= row['YearsPro'] <= 3 and row['PLYR_DRAFTROUND'] <= 2 and row['ContractYearsLeft'] <= 3:
            return 'Yes' if random.random() <= 0.15 * multiplier else 'No'
        elif row['OverallRating'] >= 85 and 2 <= row['YearsPro'] <= 4 and row['ContractYearsLeft'] <= 3:
            return 'Yes' if random.random() <= 0.125 * multiplier else 'No'
        elif row['OverallRating'] >= 85 and row['YearsPro'] >= 5 and row['ContractYearsLeft'] <= 5:
            return 'Yes' if random.random() <= 0.10 * multiplier else 'No'
        else:
            return 'No'
    else:
        return 'No'
    
# Apply the function to create the TradeUnhappy column
merged_df['TradeWR'] = merged_df.apply(traderequest_wr, axis=1)

# Function to determine trade request based on conditions
def traderequest_playingtime(row):
    multiplier = 0.0
    if row['Position'] in ['TE', 'LT', 'LG', 'C', 'RG', 'RT', 'LOLB', 'MLB', 'ROLB', 'FS', 'SS'] and row['Rank'] >= 2:
        multiplier = 1.0
    elif row['Position'] in ['RB', 'HB', 'DT', 'LE', 'RE'] and row['Rank'] >= 3:
        multiplier = 1.0
    elif row['Position'] in ['WR', 'CB'] and row['Rank'] >= 4:
        multiplier = 1.0

    if season_phase in ["Preseason", "TradeDeadline", "Offseason"]:
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

def tradecut_youngplayer(row):
    # Multiplier based on confidence
    confidencerating = row['ConfidenceRating']
    if confidencerating < 20:
        multiplier = 10.0
    elif confidencerating < 30:
        multiplier = 5.0
    elif confidencerating < 40:
        multiplier = 1.5
    elif confidencerating < 50:
        multiplier = 1.0
    elif confidencerating < 60:
        multiplier = 0.5
    elif confidencerating < 70:
        multiplier = 0.1
    else:
        multiplier = 0.05

    # Only consider trades during allowed phases
    if season_phase not in ["Preseason", "TradeDeadline", "Offseason"]:
        return 'No'

    # Define position groups
    position_group_one = ['TE', 'LT', 'LG', 'C', 'RG', 'RT', 'LOLB', 'MLB', 'ROLB', 'FS', 'SS']
    position_group_two = ['RB', 'HB', 'DT', 'LE', 'RE', 'QB']
    position_group_three = ['WR', 'CB']

    position = row['Position']
    rank = row['Rank']
    overall = row['OverallRating']
    years_pro = row['YearsPro']
    draft_round = row['PLYR_DRAFTROUND']

    # Only 2nd or 3rd year players
    if not (2 <= years_pro <= 3):
        return 'No'

    # 1st Round Logic
    if draft_round == 1:
        if position in position_group_one and rank >= 3:
            return 'Trade/Cut' if random.random() <= 0.75 * multiplier else 'Maybe'
        elif position in position_group_one and rank == 2:
            return 'Trade/Cut' if random.random() <= 0.5 * multiplier else 'Maybe'
        elif position in position_group_two and rank >= 4:
            return 'Trade/Cut' if random.random() <= 0.75 * multiplier else 'Maybe'
        elif position in position_group_two and rank == 3:
            return 'Trade/Cut' if random.random() <= 0.5 * multiplier else 'Maybe'
        elif position in position_group_three and rank >= 4:
            return 'Trade/Cut' if random.random() <= 0.75 * multiplier else 'Maybe'
        elif position in position_group_three and rank == 3 and overall <= 79:
            return 'Trade/Cut' if random.random() <= 0.5 * multiplier else 'Maybe'

    # Day 2 Logic
    elif 2 <= draft_round <= 3:
        if position in position_group_one and rank >= 3:
            return 'Trade/Cut' if random.random() <= 0.5 * multiplier else 'Maybe'
        elif position in position_group_one and rank == 2:
            return 'Trade/Cut' if random.random() <= 0.25 * multiplier else 'Maybe'
        elif position in position_group_two and rank >= 4:
            return 'Trade/Cut' if random.random() <= 0.5 * multiplier else 'Maybe'
        elif position in position_group_two and rank == 3:
            return 'Trade/Cut' if random.random() <= 0.25 * multiplier else 'Maybe'
        elif position in position_group_three and rank >= 4:
            return 'Trade/Cut' if random.random() <= 0.5 * multiplier else 'Maybe'
        elif position in position_group_three and rank == 3 and overall <= 74:
            return 'Trade/Cut' if random.random() <= 0.25 * multiplier else 'Maybe'

    # Day 3 Logic
    elif 4 <= draft_round <= 7:
        if position in position_group_one and rank >= 3 and overall <= 69:
            return 'Trade/Cut' if random.random() <= 0.25 * multiplier else 'Maybe'
        elif position in position_group_one and rank == 2 and overall <= 69:
            return 'Trade/Cut' if random.random() <= 0.1 * multiplier else 'Maybe'
        elif position in position_group_two and rank >= 4 and overall <= 69:
            return 'Trade/Cut' if random.random() <= 0.25 * multiplier else 'Maybe'
        elif position in position_group_two and rank == 3 and overall <= 69:
            return 'Trade/Cut' if random.random() <= 0.1 * multiplier else 'Maybe'
        elif position in position_group_three and rank >= 4 and overall <= 69:
            return 'Trade/Cut' if random.random() <= 0.25 * multiplier else 'Maybe'
        elif position in position_group_three and rank == 3 and overall <= 69:
            return 'Trade/Cut' if random.random() <= 0.1 * multiplier else 'Maybe'

    return 'No'
    
# Apply the function to create the TradeUnhappy column
merged_df['TradeCutYoungPlayer'] = merged_df.apply(tradecut_youngplayer, axis=1)

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
            return 'ACL' if random.random() <= 0.001 * multiplier else 'Achilles' if random.random() <= 0.001 * multiplier else 'PartialSeasonInjury' if random.random() <= 0.001 * multiplier else 'FullSeasonInjury' if random.random() <= 0.001 * multiplier else 'No'
        else:
            return 'No'
    if season_phase == "Offseason":
        if row['InjuryStatus'] == 'Injured' and row['TotalInjuryDuration'] >= 8 and row['Position'] in ['QB']:
            return 'ExtendedSeasonEndingInjury' if random.random() <= 0.1 * multiplier else 'ExtendedPartialSeasonInjury' if random.random() <= 0.1 * multiplier else 'No'
        if row['InjuryStatus'] == 'Injured' and row['TotalInjuryDuration'] <= 8 and row['Position'] in ['QB']:
            return 'ExtendedSeasonEndingInjury' if random.random() <= 0.05 * multiplier else 'ExtendedPartialSeasonInjury' if random.random() <= 0.05 * multiplier else 'No'
        if row['InjuryStatus'] == 'Injured' and row['TotalInjuryDuration'] >= 8 and row['Position'] not in ['QB']:
            return 'ExtendedSeasonEndingInjury' if random.random() <= 0.025 * multiplier else 'ExtendedPartialSeasonInjury' if random.random() <= 0.025 * multiplier else 'No'
        if row['InjuryStatus'] == 'Uninjured':
            return 'ACL' if random.random() <= 0.001 * multiplier else 'Achilles' if random.random() <= 0.001 * multiplier else 'PartialSeasonInjury' if random.random() <= 0.001 * multiplier else 'FullSeasonInjury' if random.random() <= 0.001 * multiplier else 'No'
        else:
            return 'No'
    else:
        return 'No'
    
# Apply the function to create the OffseasonInjury column
merged_df['OffseasonInjury'] = merged_df.apply(injury_offseason, axis=1)

# Function to determine Retirement based on conditions
def vet_earlyretirement(row):

    if season_phase == "Offseason":
        if row['Position'] in ['QB', 'K', 'P'] and row['Age'] >= 35 and row['OverallRating'] >= 70 and row['ContractYearsLeft'] <= 3:
            return 'Yes' if random.random() <= 0.01 else 'No'
        if row['Position'] in ['RB', 'HB'] and row['Age'] >= 26 and row['OverallRating'] >= 70 and row['ContractYearsLeft'] <= 3:
            return 'Yes' if random.random() <= 0.01 else 'No'
        if row['Position'] not in ['QB', 'RB', 'HB', 'K', 'P'] and row['Age'] >= 27 and row['OverallRating'] >= 70 and row['ContractYearsLeft'] <= 3:
            return 'Yes' if random.random() <= 0.005 else 'No'
        else:
            return 'No'
    elif season_phase == "Preseason":
        if row['Position'] in ['QB', 'K', 'P'] and row['Age'] >= 35 and row['OverallRating'] >= 70 and row['ContractYearsLeft'] <= 3:
            return 'Yes' if random.random() <= 0.001 else 'No'
        if row['Position'] in ['RB', 'HB'] and row['Age'] >= 26 and row['OverallRating'] >= 70 and row['ContractYearsLeft'] <= 3:
            return 'Yes' if random.random() <= 0.001 else 'No'
        if row['Position'] not in ['QB', 'RB', 'HB', 'K', 'P'] and row['Age'] >= 27 and row['OverallRating'] >= 70 and row['ContractYearsLeft'] <= 3:
            return 'Yes' if random.random() <= 0.001 else 'No'
        else:
            return 'No'
    else:
        return 'No'
    
# Apply the function to create the Retire column
merged_df['Retire'] = merged_df.apply(vet_earlyretirement, axis=1)

# Save the merged dataframe to a new Excel file
merged_df.to_excel(output_file_path, index=False)