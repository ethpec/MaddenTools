import pandas as pd
import numpy as np

# Your File Paths
file_path = 'Files/Madden24/IE/Season0/Player.xlsx'
all_pros_path = 'Files/Madden24/IE/Season0/AllPros.xlsx'
all_xlsm_path = 'Files/Madden24/IE/Season0/All.xlsm'

# Specify the current season year
current_season_year = 0  ####### Change this to the correct value #######

def calculate_number_value_ranking(file_path, all_pros_path, all_xlsm_path):
    """
    Calculate number value rankings for players based on conditions.

    Args:
    - file_path (str): The path to the "Player.xlsx" file.
    - all_pros_path (str): The path to the "AllPros.xlsx" file.
    - all_xlsm_path (str): The path to the "All.xlsm" file.

    Returns:
    - pd.DataFrame: The DataFrame with updated "APY," "AwardedPoints," "TotalPoints," and "DOWNSPLAYED" columns.
    """

    # Read player data from the Excel file
    df = pd.read_excel(file_path)

    # Read All Pros data from the Excel file
    all_pros_df = pd.read_excel(all_pros_path)

    # Read All.xlsm and extract the necessary information
    all_xlsm = pd.read_excel(all_xlsm_path, sheet_name=None)

    def calculate_downs_played(row):
        position = row['Position']
        first_name = row['FirstName']
        last_name = row['LastName']

        # Determine the sheet name based on the player's position
        if position in ['QB', 'RB', 'HB', 'FB', 'WR', 'TE']:
            sheet_name = 'Offensive Stats'
        elif position in ['LE', 'RE', 'DT', 'LOLB', 'ROLB', 'MLB', 'CB', 'FS', 'SS']:
            sheet_name = 'Defensive Stats'
        elif position in ['LT', 'LG', 'C', 'RG', 'RT']:
            sheet_name = 'OLine Stats'
        else:
            return None  # Return None for unsupported positions

        # Check if the SEAS_YEAR column matches the current season year
        if sheet_name in all_xlsm and 'SEAS_YEAR' in all_xlsm[sheet_name]:
            season_year = all_xlsm[sheet_name]['SEAS_YEAR'].max()
            if season_year == current_season_year:
                # Search for the player in the corresponding sheet of All.xlsm
                matching_player = all_xlsm[sheet_name][(all_xlsm[sheet_name]['FirstName'] == first_name) & (all_xlsm[sheet_name]['LastName'] == last_name) & (all_xlsm[sheet_name]['Position'] == position)]
                if not matching_player.empty:
                    return matching_player['DOWNSPLAYED'].values[0]

        return None  # Return None if player not found or SEAS_YEAR doesn't match

    def calculate_snap_points(row):
        position = row['Position']
        downs_played = row['DOWNSPLAYED']

        # Define the position-dependent snap values
        position_values = {
            'QB': 1100,
            'LE': 1100,
            'RE': 1100,
            'LOLB': 1100,
            'ROLB': 1100,
            'RB': 1100,
            'HB': 1100,
            'DT': 1100,
            'WR': 1100,
            'LT': 1100,
            'LG': 1100,
            'RG': 1100,
            'C': 1100,
            'RT': 1100,
            'MLB': 1100,
            'CB': 1100,
            'TE': 1100,
            'FS': 1100,
            'SS': 1100,
        }

        if position in position_values and pd.notna(downs_played):  # Check if downs_played is not NaN:
            position_value = position_values[position]
            snap_points = round((downs_played * 100) / position_value)
            if snap_points > 100:
                snap_points = 100
            elif snap_points < 25:
                snap_points = 0
            elif downs_played > position_value:
                snap_points = 100  # Update SnapPoints to 100 if DOWNSPLAYED > position_value
            return snap_points

        return 0  # Default to 0 SnapPoints if conditions are not met

    # Calculate DownsPlayed and add it as a new column
    df['DOWNSPLAYED'] = df.apply(calculate_downs_played, axis=1)

    # Calculate SnapPoints and add it as a new column
    df['SnapPoints'] = df.apply(calculate_snap_points, axis=1)

    # Define conditions for awarding number value rankings
    def calculate_rank(row):
        if row['ContractStatus'] in ['Signed', 'Expiring']:
            # Sum up contract salaries and bonuses and divide by contract length
            total_contract_value = (
                row['ContractSalary0'] + row['ContractBonus0'] +
                row['ContractSalary1'] + row['ContractBonus1'] +
                row['ContractSalary2'] + row['ContractBonus2'] +
                row['ContractSalary3'] + row['ContractBonus3'] +
                row['ContractSalary4'] + row['ContractBonus4'] +
                row['ContractSalary5'] + row['ContractBonus5'] +
                row['ContractSalary6'] + row['ContractBonus6'] +
                row['ContractSalary7'] + row['ContractBonus7']
            )
            contract_length = row['ContractLength']
            if contract_length > 0:
                ranking = total_contract_value / contract_length
            else:
                ranking = 0  # To avoid division by zero
        else:
            ranking = None  # Players with other contract statuses get a None value
        return ranking

    # Calculate number value rankings for each player
    df['NumberValueRanking'] = df.apply(calculate_rank, axis=1)

    # Filter out players with None values (other contract statuses)
    df = df.dropna(subset=['NumberValueRanking'])

    # Perform min-max scaling to get rankings between 1 and the number of players
    min_rank = 1
    max_rank = len(df)
    df['NumberValueRanking'] = (df['NumberValueRanking'] - df['NumberValueRanking'].min()) / (df['NumberValueRanking'].max() - df['NumberValueRanking'].min()) * (max_rank - min_rank) + min_rank

    # Rank the DataFrame based on NumberValueRanking
    df['APY'] = df['NumberValueRanking'].rank(method='first')

    # Function to update the "APY" and add "AwardedPoints" column
    def update_rank(row):
        awarded_points = 0
        matching_player = all_pros_df[(all_pros_df['FirstName'] == row['FirstName']) & (all_pros_df['LastName'] == row['LastName']) & (all_pros_df['Position'] == row['Position'])]
        if not matching_player.empty:
            if matching_player['1st Team'].values[0] == 'Y':
                awarded_points = 20
            elif matching_player['2nd Team'].values[0] == 'Y':
                awarded_points = 5
        row['AwardedPoints'] = awarded_points
        return row

    # Update the "APY" and add "AwardedPoints" column
    df = df.apply(update_rank, axis=1)

    # Calculate the "TotalPoints" as the sum of "APY" and "AwardedPoints"
    df['TotalPoints'] = df['APY'] + df['AwardedPoints'] + df['SnapPoints']

    # Calculate percentiles for "TotalPoints" to determine "CompPickValue"
    percentiles = df['TotalPoints'].rank(pct=True)
    df['CompPickValue'] = pd.cut(
        percentiles,
        bins=[0.0, 0.65, 0.75, 0.85, 0.90, 0.95, 1.0],
        labels=['None', 7, 6, 5, 4, 3]
    )

    # Sort the DataFrame based on NumberValueRanking, LastName, and FirstName
    df = df.sort_values(by=['TotalPoints'], ascending=[False])

    return df

# Calculate number value rankings for players and update columns
result_df = calculate_number_value_ranking(file_path, all_pros_path, all_xlsm_path)

# After sorting the DataFrame based on "TotalPoints," add the following code to calculate "CompRank":
# Calculate "CompRank" based on "TotalPoints" in descending order (higher TotalPoints get lower ranks)
result_df['CompRank'] = result_df['TotalPoints'].rank(method='min', ascending=False).astype(int)

# Export the resulting DataFrame to an Excel document
output_filename = 'CompPickPlayerValue.xlsx'
result_df.to_excel('Files/Madden24/IE/Season0/CompPickPlayerValue.xlsx', index=False)
