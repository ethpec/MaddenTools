# Imports
import pandas as pd
import math
import numpy as np
from utils.salary_utils import parse_salary_table

# File Paths
all_contracts_file_path = 'Files/Madden26/IE/Season2/FreeAgency/Input/ContractOffer[].xlsx'
contract_offer_file_path = 'Files/Madden26/IE/Season2/FreeAgency/Input/ContractOffer.xlsx'
player_contract_file_path = 'Files/Madden26/IE/Season2/FreeAgency/Input/PlayerContract.xlsx'
contract_salary_file_path = 'Files/Madden26/IE/Season2/FreeAgency/Input/int[].xlsx'
player_file_path = 'Files/Madden26/IE/Season2/FreeAgency/Input/Player.xlsx'
team_info_file_path = 'Files/Madden26/IE/Season2/FreeAgency/Input/Team.xlsx'
salary_expectation_file_path = 'Files/Madden26/IE/Season2/ExpectedSalarySheet.xlsx'
position_needs_file_path = 'Files/Madden26/IE/Season2/FreeAgency/Input/PositionNeeds.xlsx'

# Load DataFrames
all_players_df = pd.read_excel(player_file_path)
salary_df = pd.read_excel(salary_expectation_file_path, sheet_name='Import (279) (FA Class)')
position_needs_df = pd.read_excel(position_needs_file_path)
team_df = pd.read_excel(team_info_file_path, usecols=['TeamIndex', 'NewHC', 'WinsLastSeason'])

# Filter to only Free Agents eligible for contract offers
fa_player_df = all_players_df[all_players_df['ContractStatus'] == 'FreeAgent'].copy()

# Filter to signed players for team needs determination
roster_df = all_players_df[all_players_df['ContractStatus'] == 'Signed'].copy()

salary_lookup = parse_salary_table(salary_df)

# Salary Interpolation
def salary_interpolation(position, overall, salary_lookup):
    if position not in salary_lookup:
        return None, None, None

    data = salary_lookup[position]
    x = data['Overall']

    def interpolate(y_values):
        return float(np.interp(overall, x, y_values))

    aav = round(interpolate(data['AAV']))
    bonus = round(interpolate(data['Bonus']))
    length = round(interpolate(data['Length']))

    return aav, bonus, length

# Weighted random adjustment for OverallRating
def random_overall_adjustment():
    choices = [-1, 0, 1, 2, 3]
    probabilities = [0.04, 0.7, 0.2, 0.04, 0.02]  # adjust as needed
    return np.random.choice(choices, p=probabilities)

# Apply to Each Row
def assign_salaryinfo(row):
    position = str(row['Position']).strip().upper()
    # Apply random adjustment to OverallRating
    adjusted_overall = min(row['OverallRating'] + random_overall_adjustment(), 99)

    aav, bonus, length = salary_interpolation(position, adjusted_overall, salary_lookup)

    row['ExpectedAAV'] = aav
    row['ExpectedBonus'] = bonus
    row['ExpectedContractLength'] = length
    row['AdjustedOverall'] = adjusted_overall
    row['SalaryCheck'] = 'Updated' if aav is not None else 'Position Missing'

    return row

# Apply salary info to all eligible free agents
fa_player_df = fa_player_df.apply(assign_salaryinfo, axis=1)

# Build team needs: for each team, rank signed players at each position by OVR,
# then match against PositionNeeds config to determine target OVR range per need
def build_team_needs(roster_df, position_needs_df):
    records = []

    for (team_index, position), group in roster_df.groupby(['TeamIndex', 'Position']):
        ranked = group.sort_values('OverallRating', ascending=False).reset_index(drop=True)
        ranked['PositionRank'] = ranked.index + 1

        needs_for_pos = position_needs_df[position_needs_df['Position'] == position]

        for _, need_row in needs_for_pos.iterrows():
            rank = need_row['Rank']
            roster_ovr_min = need_row['Roster OVR Min']
            roster_ovr_max = need_row['Roster OVR Max']

            # Get the player at this rank, or 0 if roster is short
            if rank <= len(ranked):
                slot_ovr = ranked.iloc[rank - 1]['OverallRating']
            else:
                slot_ovr = 0

            if roster_ovr_min <= slot_ovr <= roster_ovr_max:
                records.append({
                    'TeamIndex': team_index,
                    'Position': position,
                    'NeedLabel': need_row['Need Label'],
                    'SlotOVR': slot_ovr,
                    'TargetOVRMin': need_row['Target OVR Min'],
                    'TargetOVRMax': need_row['Target OVR Max'],
                })

    return pd.DataFrame(records)

team_needs_df = build_team_needs(roster_df, position_needs_df)

# Build per-team PrevTeamIndex modifier lookup
# Modifier applies to players whose PrevTeamIndex matches the team pursuing them
def build_prev_team_modifier(team_df):
    modifiers = {}
    for _, row in team_df.iterrows():
        team_index = row['TeamIndex']
        new_hc = str(row['NewHC']).strip().upper()
        wins = row['WinsLastSeason']
        if new_hc == 'NO' and wins > 9:
            modifiers[team_index] = 1.5
        elif new_hc == 'YES':
            modifiers[team_index] = 0.5
    return modifiers

prev_team_modifiers = build_prev_team_modifier(team_df)

# Match each team need against eligible FA players by position and target OVR range
def match_fa_to_needs(team_needs_df, fa_player_df, prev_team_modifiers):
    records = []

    for _, need in team_needs_df.iterrows():
        team_index = need['TeamIndex']
        matches = fa_player_df[
            (fa_player_df['Position'] == need['Position']) &
            (fa_player_df['OverallRating'] >= need['TargetOVRMin']) &
            (fa_player_df['OverallRating'] <= need['TargetOVRMax'])
        ]

        for _, player in matches.iterrows():
            position = str(player['Position']).strip().upper()
            adjusted_overall = min(player['OverallRating'] + random_overall_adjustment(), 99)
            aav, bonus, length = salary_interpolation(position, adjusted_overall, salary_lookup)

            # Apply prev team modifier if player's PrevTeamIndex matches this team
            weight = 1
            if player['PrevTeamIndex'] == team_index and team_index in prev_team_modifiers:
                weight *= prev_team_modifiers[team_index]

            # Apply adjusted overall modifier based on diff from base OverallRating
            ovr_diff = adjusted_overall - player['OverallRating']
            ovr_modifiers = {-1: 0.9, 1: 1.1, 2: 1.2, 3: 1.3}
            weight *= ovr_modifiers.get(ovr_diff, 1.0)

            weight = round(weight, 4)

            records.append({
                'TeamIndex': team_index,
                'NeedLabel': need['NeedLabel'],
                'SlotOVR': need['SlotOVR'],
                'TargetOVRMin': need['TargetOVRMin'],
                'TargetOVRMax': need['TargetOVRMax'],
                'Position': player['Position'],
                'FirstName': player['FirstName'],
                'LastName': player['LastName'],
                'OverallRating': player['OverallRating'],
                'AdjustedOverall': adjusted_overall,
                'ExpectedAAV': aav,
                'ExpectedBonus': bonus,
                'ExpectedContractLength': length,
                'SelectionWeight': weight,
            })

    return pd.DataFrame(records)

fa_matches_df = match_fa_to_needs(team_needs_df, fa_player_df, prev_team_modifiers)

# Select one FA per team need using weighted random selection
# Tracks already-selected players per team to prevent the same player being selected for multiple needs
# SelectionWeight defaults to 10 for all — modifiers will adjust this per team/player later
def select_fa_per_need(fa_matches_df):
    records = []

    for _, team_group in fa_matches_df.groupby('TeamIndex'):
        selected_players = set()

        for _, group in team_group.groupby('NeedLabel'):
            available = group[~group.apply(
                lambda r: (r['FirstName'], r['LastName']) in selected_players, axis=1
            )]

            if available.empty:
                continue

            weights = available.get('SelectionWeight', pd.Series([10] * len(available), index=available.index))
            total = weights.sum()
            probabilities = (weights / total).values

            selected = available.sample(n=1, weights=probabilities).iloc[0]
            selected_players.add((selected['FirstName'], selected['LastName']))
            records.append(selected.to_dict())

    return pd.DataFrame(records)

fa_selections_df = select_fa_per_need(fa_matches_df)

# Put created columns at the front
created_cols = ['ExpectedAAV', 'ExpectedBonus', 'ExpectedContractLength', 'AdjustedOverall', 'SalaryCheck']
remaining_cols = [c for c in fa_player_df.columns if c not in created_cols]
fa_player_df = fa_player_df[created_cols + remaining_cols]

# Export all outputs to a single workbook on separate sheets
output_filename = 'Files/Madden26/IE/Season2/FreeAgency/Output/FreeAgency.xlsx'
with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
    fa_player_df.to_excel(writer, sheet_name='ContractOffers', index=False)
    team_needs_df.to_excel(writer, sheet_name='TeamNeeds', index=False)
    fa_matches_df.to_excel(writer, sheet_name='FAMatches', index=False)
    fa_selections_df.to_excel(writer, sheet_name='FASelections', index=False)