# Imports
import pandas as pd
import math
import numpy as np
import os
from utils.salary_utils import parse_salary_table

# FA Wave Configuration (1, 2, or 3)
WAVE = 1

# User-controlled team — excluded from all CPU FA logic
USER_TEAM_INDEX = 26

# Non-real teams excluded from all FA logic
EXCLUDED_TEAM_INDICES = [32]

CONTRACTOFFERTABLE = 4233 #4212
PLAYERCONTRACTTABLE = 4285 #4261
INTTABLE = 5543 #5454
TEAMTABLE = 5917 #5797
PLAYERTABLE = 4222 #4204

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
all_players_df['RowNum'] = all_players_df.index
salary_df = pd.read_excel(salary_expectation_file_path, sheet_name='Import (279) (FA Class)')
position_needs_df = pd.read_excel(position_needs_file_path)
team_df = pd.read_excel(team_info_file_path, usecols=['TeamIndex', 'TeamName', 'MFERow', 'NewHC', 'WinsLastSeason', 'CapSpace'])

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
    team_indices = roster_df['TeamIndex'].unique()

    for team_index in team_indices:
        team_roster = roster_df[roster_df['TeamIndex'] == team_index]

        for position, needs_for_pos in position_needs_df.groupby('Position'):
            pos_players = team_roster[team_roster['Position'] == position]
            ranked = pos_players.sort_values('OverallRating', ascending=False).reset_index(drop=True)

            for _, need_row in needs_for_pos.iterrows():
                rank = need_row['Rank']
                roster_ovr_min = need_row['Roster OVR Min']
                roster_ovr_max = need_row['Roster OVR Max']

                slot_ovr = ranked.iloc[rank - 1]['OverallRating'] if rank <= len(ranked) else 0

                if roster_ovr_min <= slot_ovr <= roster_ovr_max:
                    records.append({
                        'TeamIndex': team_index,
                        'Position': position,
                        'NeedLabel': need_row['Need Label'],
                        'SlotOVR': slot_ovr,
                        'TargetOVRMin': need_row['Target OVR Min'],
                        'TargetOVRMax': need_row['Target OVR Max'],
                        'DefaultWeight': need_row.get('DefaultWeight', 1) or 1,
                    })

    return pd.DataFrame(records)

team_needs_df = build_team_needs(roster_df, position_needs_df)
excluded_indices = EXCLUDED_TEAM_INDICES + [USER_TEAM_INDEX]
team_needs_df = team_needs_df[~team_needs_df['TeamIndex'].isin(excluded_indices)].reset_index(drop=True)

# Adjust TargetOVR range per team based on available CapSpace
def cap_ovr_adjustment(cap_space):
    if cap_space >= 7500:   return 3
    elif cap_space >= 5000: return 2
    elif cap_space >= 2500: return 1
    elif cap_space >= 0:    return 0
    else:                   return -1

cap_lookup = team_df.set_index('TeamIndex')['CapSpace'].to_dict()
team_needs_df['OVRAdjustment'] = team_needs_df['TeamIndex'].map(cap_lookup).apply(cap_ovr_adjustment)
team_needs_df['TargetOVRMin'] = team_needs_df['TargetOVRMin'] + team_needs_df['OVRAdjustment']
team_needs_df['TargetOVRMax'] = team_needs_df['TargetOVRMax'] + team_needs_df['OVRAdjustment']
team_needs_df.drop(columns=['OVRAdjustment'], inplace=True)

# Build per-team PrevTeamIndex modifier lookup (former players more or less likely to return)
def build_prev_team_modifier(team_df):
    modifiers = {}
    for _, row in team_df.iterrows():
        team_index = row['TeamIndex']
        new_hc = str(row['NewHC']).strip().upper()
        wins = row['WinsLastSeason']
        if new_hc == 'NO' and wins > 9:
            modifiers[team_index] = 2.0
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
            ovr_modifiers = {-1: 0.75, 0: 1.0, 1: 1.25, 2: 1.5, 3: 1.75}
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
                'DefaultWeight': float(need.get('DefaultWeight', 1) or 1),
                'RowNum': player['RowNum'],
            })

    return pd.DataFrame(records)

fa_matches_df = match_fa_to_needs(team_needs_df, fa_player_df, prev_team_modifiers)

# For Wave 2&3, restore previously rolled values (AdjustedOverall, salary, weight) for
# existing team/need/player combinations so evaluations don't change between waves.
if WAVE > 1:
    rolled_cols = ['AdjustedOverall', 'ExpectedAAV', 'ExpectedBonus', 'ExpectedContractLength', 'SelectionWeight']
    match_keys = ['TeamIndex', 'NeedLabel', 'FirstName', 'LastName']
    try:
        prev_matches_df = pd.read_excel(
            'Files/Madden26/IE/Season2/FreeAgency/Output/FreeAgency.xlsx',
            sheet_name='FAMatches',
            usecols=match_keys + rolled_cols
        )
        fa_matches_df = fa_matches_df.merge(
            prev_matches_df, on=match_keys, how='left', suffixes=('', '_prev')
        )
        for col in rolled_cols:
            prev_col = col + '_prev'
            if prev_col in fa_matches_df.columns:
                fa_matches_df[col] = fa_matches_df[prev_col].combine_first(fa_matches_df[col])
                fa_matches_df.drop(columns=[prev_col], inplace=True)
    except Exception:
        pass  # Fall back to freshly rolled values if sheet is missing

# Load previous wave selections if running Wave 2 or 3
# Keys are (TeamIndex, NeedLabel) -> (FirstName, LastName)
def load_previous_selections(output_filename):
    if not os.path.exists(output_filename):
        return {}
    try:
        prev_df = pd.read_excel(output_filename, sheet_name='FASelections')
        return {
            (row['TeamIndex'], row['NeedLabel']): (row['FirstName'], row['LastName'])
            for _, row in prev_df.iterrows()
        }
    except Exception:
        return {}

# Select one FA per team need using weighted random selection.
# For Wave 2&3, prefers previously selected players if still available as FAs,
# otherwise falls back to weighted random selection from remaining candidates.
# Tracks already-selected players per team to prevent the same player being selected for multiple needs.
# No cap/offer limits applied here — all needs are filled regardless of cap space.
def select_fa_per_need(fa_matches_df, previous_selections=None):
    records = []

    for _, team_group in fa_matches_df.groupby('TeamIndex'):
        team_index = team_group.iloc[0]['TeamIndex']
        selected_players = set()

        for need_label, group in team_group.groupby('NeedLabel'):
            available = group[~group.apply(
                lambda r: (r['FirstName'], r['LastName']) in selected_players, axis=1
            )]

            if available.empty:
                continue

            # Wave 2&3: keep previous selection if that player is still an available FA
            if previous_selections:
                prev_name = previous_selections.get((team_index, need_label))
                if prev_name:
                    prev_match = available[
                        (available['FirstName'] == prev_name[0]) &
                        (available['LastName'] == prev_name[1])
                    ]
                    if not prev_match.empty:
                        selected = prev_match.iloc[0]
                        selected_players.add((selected['FirstName'], selected['LastName']))
                        records.append(selected.to_dict())
                        continue

            # Default: weighted random selection
            weights = available['SelectionWeight'] if 'SelectionWeight' in available.columns else pd.Series([10] * len(available), index=available.index)
            probabilities = (weights / weights.sum()).values

            selected = available.sample(n=1, weights=probabilities).iloc[0]
            selected_players.add((selected['FirstName'], selected['LastName']))
            records.append(selected.to_dict())

    return pd.DataFrame(records)

# From FASelections, build FAOffers by weighted-randomly drawing needs per team
# until the cap floor is hit or 10 offers are made.
# Each need's weight is based on the selected player's OVR and wave multipliers.
def build_fa_offers(fa_selections_df, team_df, wave, cap_floor_lookup):
    records = []

    cap_lookup = team_df.set_index('TeamIndex')['CapSpace'].to_dict()

    def wave_weight(ovr, wave):
        if wave == 1:
            if ovr >= 90:   return 3.0
            elif ovr >= 85: return 2.5
            elif ovr >= 80: return 2.0
            elif ovr >= 75: return 1.5
            elif ovr >= 70: return 1.0
            else:           return 0.5
        elif wave == 2:
            if ovr >= 90:   return 3.0
            elif ovr >= 80: return 2.0
            elif ovr >= 70: return 1.5
            else:           return 1.0
        else:  # wave 3
            if ovr >= 80:   return 2.0
            else:           return 1.0

    for team_index, team_group in fa_selections_df.groupby('TeamIndex'):
        remaining_cap = cap_lookup.get(team_index, 0)
        cap_floor = cap_floor_lookup.get(team_index, 0)
        offers = 0

        pool = team_group.copy()
        pool['OfferWeight'] = pool.apply(lambda r: wave_weight(r['OverallRating'], wave) * float(r.get('DefaultWeight', 1) or 1), axis=1)

        ovr_penalty = {2: 1, 3: 2}.get(wave, 0)

        while offers < 10 and remaining_cap > cap_floor and not pool.empty:
            weights = pool['OfferWeight']
            probabilities = (weights / weights.sum()).values

            idx = np.random.choice(pool.index, p=probabilities)
            selected = pool.loc[idx].to_dict()

            if ovr_penalty > 0:
                position = str(selected['Position']).strip().upper()
                adjusted_overall = max(selected['AdjustedOverall'] - ovr_penalty, 0)
                aav, bonus, length = salary_interpolation(position, adjusted_overall, salary_lookup)
                selected['AdjustedOverall'] = adjusted_overall
                selected['ExpectedAAV'] = aav
                selected['ExpectedBonus'] = bonus
                selected['ExpectedContractLength'] = length

            records.append(selected)
            remaining_cap -= selected['ExpectedAAV']
            offers += 1
            pool = pool.drop(idx)

    return pd.DataFrame(records)

# Apply wave-specific SelectionWeight modifiers before selection
# Returns a modified copy — base weights in fa_matches_df remain unchanged
def apply_wave_modifiers(fa_matches_df, wave):
    df = fa_matches_df.copy()

    if wave == 1:
        def ovr_multiplier(ovr):
            if ovr >= 90:   return 3.0
            elif ovr >= 85: return 2.5
            elif ovr >= 80: return 2.0
            elif ovr >= 75: return 1.5
            elif ovr >= 70: return 1.0
            else:           return 0.5

        df['SelectionWeight'] = df.apply(
            lambda r: round(r['SelectionWeight'] * ovr_multiplier(r['OverallRating']), 4), axis=1
        )

    elif wave == 3:
        def ovr_multiplier(ovr):
            if ovr >= 90: return 2.0
            else:         return 1.0

        df['SelectionWeight'] = df.apply(
            lambda r: round(r['SelectionWeight'] * ovr_multiplier(r['OverallRating']), 4), axis=1
        )

    elif wave == 2:
        def ovr_multiplier(ovr):
            if ovr >= 90:   return 3.0
            elif ovr >= 80: return 2.0
            elif ovr >= 70: return 1.5
            else:           return 1.0

        df['SelectionWeight'] = df.apply(
            lambda r: round(r['SelectionWeight'] * ovr_multiplier(r['OverallRating']), 4), axis=1
        )

    return df

# Build TeamPhilosophy: roll cap floors once on Wave 1, persist for Wave 2+
output_filename = 'Files/Madden26/IE/Season2/FreeAgency/Output/FreeAgency.xlsx'

if WAVE > 1 and os.path.exists(output_filename):
    try:
        team_philosophy_df = pd.read_excel(output_filename, sheet_name='TeamPhilosophy')
    except Exception:
        team_philosophy_df = None
else:
    team_philosophy_df = None

if team_philosophy_df is None:
    team_philosophy_df = team_df[['TeamIndex', 'TeamName', 'CapSpace']].copy()
    team_philosophy_df['CapFloor'] = [
        np.random.choice(range(-100, -2100, -100)) for _ in range(len(team_philosophy_df))
    ]

cap_floor_lookup = team_philosophy_df.set_index('TeamIndex')['CapFloor'].to_dict()

previous_selections = load_previous_selections(output_filename) if WAVE > 1 else {}

fa_selections_df = select_fa_per_need(apply_wave_modifiers(fa_matches_df, WAVE), previous_selections or None)

fa_offers_df = build_fa_offers(fa_selections_df, team_df, WAVE, cap_floor_lookup)
fa_offers_df['ReferenceRow'] = range(len(fa_offers_df))

# Put created columns at the front
created_cols = ['ExpectedAAV', 'ExpectedBonus', 'ExpectedContractLength', 'AdjustedOverall', 'SalaryCheck']
remaining_cols = [c for c in fa_player_df.columns if c not in created_cols]
fa_player_df = fa_player_df[created_cols + remaining_cols]

# Build ContractOffer[] output
contract_offer_table_binary = format(2 * CONTRACTOFFERTABLE, '016b')
contract_offer_array_df = pd.read_excel(all_contracts_file_path, dtype=str)

# Find the first slot that is all zeros (32 zeros or just '0')
first_empty_slot = None
for col in contract_offer_array_df.columns:
    val = str(contract_offer_array_df.at[0, col]).strip().replace('nan', '0')
    if val == '0' or val == '0' * 32:
        first_empty_slot = int(col.replace('ContractOffer', ''))
        break

if first_empty_slot is not None:
    for _, row in fa_offers_df.iterrows():
        ref = int(row['ReferenceRow'])
        slot = first_empty_slot + ref
        col = f'ContractOffer{slot}'
        if col in contract_offer_array_df.columns:
            contract_offer_array_df.at[0, col] = contract_offer_table_binary + format(slot, '016b')

contract_offer_output_path = 'Files/Madden26/IE/Season2/FreeAgency/Output/ContractOffer[].xlsx'
with pd.ExcelWriter(contract_offer_output_path, engine='openpyxl') as writer:
    contract_offer_array_df.to_excel(writer, index=False)

# Build ContractOffer output
contract_offer_df = pd.read_excel(contract_offer_file_path, dtype=str)

# Step 1: set IsSigned to FALSE where Contract has no reference
contract_offer_df['IsSigned'] = contract_offer_df.apply(
    lambda r: 'FALSE' if (str(r['Contract']).strip() == '0' or str(r['Contract']).strip() == '0' * 32) else r['IsSigned'],
    axis=1
)

# Step 2: find first empty Contract row, then write player contract references from FAOffers
player_contract_table_binary = format(2 * PLAYERCONTRACTTABLE, '016b')
first_empty_contract_row = None
for idx in contract_offer_df.index:
    val = str(contract_offer_df.at[idx, 'Contract']).strip()
    if val == '0' or val == '0' * 32:
        first_empty_contract_row = idx
        break

player_table_binary = format(2 * PLAYERTABLE, '016b')
team_table_binary = format(2 * TEAMTABLE, '016b')
mfe_row_lookup = team_df.set_index('TeamIndex')['MFERow'].to_dict()

int_table_binary = format(2 * INTTABLE, '016b')
player_contract_df = pd.read_excel(player_contract_file_path, dtype=str)
int_df = pd.read_excel(contract_salary_file_path, dtype=str)

if first_empty_contract_row is not None:
    for _, row in fa_offers_df.iterrows():
        ref = int(row['ReferenceRow'])
        slot = first_empty_contract_row + ref
        length = int(row['ExpectedContractLength'])
        aav = str(int(row['ExpectedAAV']) - int(row['ExpectedBonus']))
        bonus = str(int(row['ExpectedBonus']))
        salary_row = slot * 2
        bonus_row = (slot * 2) + 1

        if slot in contract_offer_df.index:
            contract_offer_df.at[slot, 'Contract'] = player_contract_table_binary + format(slot, '016b')
            contract_offer_df.at[slot, 'Player'] = player_table_binary + format(int(row['RowNum']), '016b')
            mfe_row = int(mfe_row_lookup.get(row['TeamIndex'], 0))
            contract_offer_df.at[slot, 'Team'] = team_table_binary + format(mfe_row, '016b')

        if slot in player_contract_df.index:
            player_contract_df.at[slot, 'SalaryTable'] = int_table_binary + format(salary_row, '016b')
            player_contract_df.at[slot, 'BonusTable'] = int_table_binary + format(bonus_row, '016b')
            player_contract_df.at[slot, 'Length'] = str(length)

        for yr in range(7):
            col = f'int{yr}'
            value = aav if yr < length else '0'
            bonus_value = bonus if yr < length else '0'
            if salary_row in int_df.index and col in int_df.columns:
                int_df.at[salary_row, col] = value
            if bonus_row in int_df.index and col in int_df.columns:
                int_df.at[bonus_row, col] = bonus_value

contract_offer_detail_output_path = 'Files/Madden26/IE/Season2/FreeAgency/Output/ContractOffer.xlsx'
player_contract_output_path = 'Files/Madden26/IE/Season2/FreeAgency/Output/PlayerContract.xlsx'
int_output_path = 'Files/Madden26/IE/Season2/FreeAgency/Output/int[].xlsx'
with pd.ExcelWriter(contract_offer_detail_output_path, engine='openpyxl') as writer:
    contract_offer_df[['Team', 'Player', 'Contract', 'IsSigned']].to_excel(writer, index=False)
with pd.ExcelWriter(player_contract_output_path, engine='openpyxl') as writer:
    player_contract_df[['SalaryTable', 'BonusTable', 'Length']].to_excel(writer, index=False)
with pd.ExcelWriter(int_output_path, engine='openpyxl') as writer:
    int_df.to_excel(writer, index=False)

# Export all outputs to a single workbook on separate sheets
with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
    fa_player_df.to_excel(writer, sheet_name='FreeAgents', index=False)
    team_needs_df.to_excel(writer, sheet_name='TeamNeeds', index=False)
    team_philosophy_df.to_excel(writer, sheet_name='TeamPhilosophy', index=False)
    fa_matches_df.to_excel(writer, sheet_name='FAMatches', index=False)
    fa_selections_df.to_excel(writer, sheet_name='FASelections', index=False)
    fa_offers_df.to_excel(writer, sheet_name='FAOffers', index=False)