import pandas as pd

# Set the multiplier for adjusting salaries and bonuses
adjustment_multiplier = 1  # You can change this value to adjust salaries and bonuses (0.918)

# Season Configuration
current_season_year = 10  # Edit this as based on season #
RFA_TENDER = 352
SECOND_RND_RFA_TENDER = 576

# Your File Paths
player_file_path = 'Files/Madden25/IE/Season10/Player.xlsx'
prog_reg_file_path = 'Files/Madden25/IE/Season10/AllProgRegInfo.xlsm'
output_filename = 'Files/Madden25/IE/Season10/Contracts_Adjusted.xlsx'

# Read player data from the Excel file
df = pd.read_excel(player_file_path)

# Load AllProgRegInfo sheets filtered to current and prior two season years
_prog_reg = pd.ExcelFile(prog_reg_file_path, engine='openpyxl')
_season_years = [current_season_year, current_season_year - 1, current_season_year - 2]

def _load_prog_reg_sheet(sheet_name):
    sheet_df = _prog_reg.parse(sheet_name)
    return sheet_df[sheet_df['SEAS_YEAR'].isin(_season_years)].reset_index(drop=True)

defensive_stats_df = _load_prog_reg_sheet('Defensive Stats')
kicking_stats_df   = _load_prog_reg_sheet('Kicking Stats')
oline_stats_df     = _load_prog_reg_sheet('OLine Stats')
offensive_stats_df = _load_prog_reg_sheet('Offensive Stats')

_offensive_positions = ['QB', 'RB', 'HB', 'FB', 'WR', 'TE']
_defensive_positions = ['LE', 'RE', 'DT', 'LOLB', 'MLB', 'ROLB', 'CB', 'FS', 'SS']
_kicking_positions   = ['K', 'P']
_oline_positions     = ['LT', 'LG', 'C', 'RG', 'RT']

offensive_stats_df = offensive_stats_df[offensive_stats_df['Position'].isin(_offensive_positions)]
defensive_stats_df = defensive_stats_df[defensive_stats_df['Position'].isin(_defensive_positions)]
kicking_stats_df   = kicking_stats_df[kicking_stats_df['Position'].isin(_kicking_positions)]
oline_stats_df     = oline_stats_df[oline_stats_df['Position'].isin(_oline_positions)]

_all_stats_df = pd.concat([offensive_stats_df, defensive_stats_df, kicking_stats_df, oline_stats_df], ignore_index=True)
_downs_pivot = _all_stats_df.pivot_table(
    index=['FirstName', 'LastName', 'Position'],
    columns='SEAS_YEAR',
    values='DOWNSPLAYED',
    aggfunc='first'
).reset_index()
_downs_pivot.columns.name = None
_downs_pivot.rename(columns={yr: f'DOWNSPLAYED_Y{yr}' for yr in _season_years if yr in _downs_pivot.columns}, inplace=True)
df = df.merge(_downs_pivot, on=['FirstName', 'LastName', 'Position'], how='left')

# Adjust salaries, bonuses, and PLYR_CAPSALARY for players with ContractStatus = 'Signed'
mask = df['ContractStatus'] == 'Signed'
columns_to_adjust = [f'ContractSalary{i}' for i in range(8)] + [f'ContractBonus{i}' for i in range(8)] + ['PLYR_CAPSALARY']

# Save original values for change detection after all adjustments
original_values = df[columns_to_adjust].copy()

# Apply salary multiplier directly on df
df.loc[mask, columns_to_adjust] = (df.loc[mask, columns_to_adjust] * adjustment_multiplier).astype(int).round()

# Rookie Contract Escalators
def apply_rookie_escalator(row):
    if not (row['ContractStatus'] == 'Signed' and
            row['YearsPro'] == 3 and
            2 <= row['PLYR_DRAFTROUND'] <= 7 and
            row['Position'] not in ('K', 'P', 'FB', 'LS')):
        return row

    cy = current_season_year

    def get_downs(yr):
        val = row.get(f'DOWNSPLAYED_Y{yr}', 0)
        return 0 if pd.isna(val) else val

    pcts = [get_downs(cy) / 1100, get_downs(cy - 1) / 1100, get_downs(cy - 2) / 1100]

    # Level 3: Pro Bowl appearance
    level3 = (row.get('ProBowlAppearences', 0) or 0) >= 1

    # Level 2: all 3 seasons >= 55%
    level2 = all(p >= 0.55 for p in pcts)

    # Level 1: 2nd round needs 60%, rounds 3-7 need 35%
    threshold = 0.60 if row['PLYR_DRAFTROUND'] == 2 else 0.35
    level1 = sum(1 for p in pcts if p >= threshold) >= 2 or (sum(pcts) / 3) >= threshold

    if level3:
        row['ContractSalary3'] = SECOND_RND_RFA_TENDER
        row['PLYR_CAPSALARY'] = SECOND_RND_RFA_TENDER
        row['EscalatorLevel'] = 'Level3'
    elif level2:
        row['ContractSalary3'] = RFA_TENDER + 25
        row['PLYR_CAPSALARY'] = RFA_TENDER + 25
        row['EscalatorLevel'] = 'Level2'
    elif level1:
        row['ContractSalary3'] = RFA_TENDER
        row['PLYR_CAPSALARY'] = RFA_TENDER
        row['EscalatorLevel'] = 'Level1'

    return row

df = df.apply(apply_rookie_escalator, axis=1)

# Export changed salary/bonus columns + EscalatorLevel if any escalators fired
changes_occurred = df[columns_to_adjust] != original_values
changed_cols = [col for col in columns_to_adjust if changes_occurred[col].any()]

if 'EscalatorLevel' in df.columns:
    export_df = df[['EscalatorLevel'] + changed_cols]
else:
    export_df = df[changed_cols]

export_df.to_excel(output_filename, index=False)
print(f"Impacted columns of adjusted DataFrame (rounded) exported to {output_filename}")
