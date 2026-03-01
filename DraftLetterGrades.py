# Imports
import pandas as pd
import random

# ==============================
# File Paths
# ==============================

file_path = 'Files/Madden26/IE/Season2/Player.xlsx'
scouting_file_path = 'Files/Madden26/IE/Season2/AllScoutInfo.xlsx'

# ==============================
# Load Player DataFrame
# ==============================

df = pd.read_excel(file_path)

# ==============================
# Convert numeric columns to object
# ==============================

# This makes it safe to assign letter grades
numeric_columns = df.select_dtypes(include='number').columns
df[numeric_columns] = df[numeric_columns].astype(object)

# ==============================
# Load other sheets
# ==============================

positions_df = pd.read_excel(scouting_file_path, sheet_name="Positions")
spline_df = pd.read_excel(scouting_file_path, sheet_name="spline")
sheet_1680_df = pd.read_excel(scouting_file_path, sheet_name="1680")

# Track original BEFORE edits
original_df = df.copy()

# Set Positions index (this one we know)
positions_df.set_index("Position", inplace=True)

# ==============================
# Process Draft Players
# ==============================

for index, player in df[df["ContractStatus"] == "Draft"].iterrows():

    position = player["Position"]

    if position not in positions_df.index:
        continue

    pos_row = positions_df.loc[position]

    for attribute, spline_key in pos_row.items():

        if spline_key == 0:
            continue

        if attribute not in df.columns:
            continue

        # spline_key is the row index
        if spline_key >= len(spline_df):
            print(f"spline_key {spline_key} out of spline_df range")
            continue

        spline_row = spline_df.iloc[int(spline_key) - 2]
        x_row_value = spline_row["x row"]

        # Use x_row_value as row index
        if x_row_value >= len(sheet_1680_df):
            continue

        int_row = sheet_1680_df.iloc[int(x_row_value) - 2]

        int1 = int_row["int1"]
        int2 = int_row["int2"]
        int3 = int_row["int3"]
        int4 = int_row["int4"]
        int5 = int_row["int5"]
        int6 = int_row["int6"]

        player_value = player[attribute]

        # ==============================
        # Letter Grade Logic
        # ==============================
        if int5 == 0:
            if player_value <= int1:
                df.at[index, attribute] = "F"

            elif player_value <= int2:
                df.at[index, attribute] = "D"

            elif player_value <= int3:
                df.at[index, attribute] = "C"

            elif player_value <= int4:
                df.at[index, attribute] = "B"

            elif player_value >= int4:
                df.at[index, attribute] = "A"


        else:
            if player_value <= int1:
                df.at[index, attribute] = "F"

            elif player_value <= int2:
                df.at[index, attribute] = "D"

            elif player_value <= int3:
                df.at[index, attribute] = "C"

            elif player_value <= int4:
                df.at[index, attribute] = "B"

            elif player_value <= int5:
                df.at[index, attribute] = "A"

            elif player_value <= int6:
                df.at[index, attribute] = "S"

            else:
                df.at[index, attribute] = "SS"

# ==============================
# Keep only changed columns
# ==============================

columns_to_keep = [
    column for column in df.columns
    if not df[column].equals(original_df[column])
]

# Ensure essential columns are at front
front_columns = ["ContractStatus", "FirstName", "LastName", "Position"]

# Only add front_columns if they exist in the DataFrame
front_columns = [col for col in front_columns if col in df.columns]

# Combine front columns with changed columns, avoiding duplicates
columns_to_keep = front_columns + [col for col in columns_to_keep if col not in front_columns]

# Reorder the DataFrame
df = df[columns_to_keep]

# ==============================
# Save Output
# ==============================

output_filename = 'Files/Madden26/IE/Season2/Draft_LetterGrades.xlsx'
df.to_excel(output_filename, index=False)

print("Draft letter grades generated successfully.")