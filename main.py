import pandas as pd
import xlrd

file_path = 'Files/All.xlsm'

# Tiers
tier_0 = range(95,100)
tier_1 = range(90,94)

# YOU MUST PUT sheet_name=None TO READ ALL CSV FILES IN YOUR XLSM FILE
df_players = pd.read_excel(file_path, sheet_name='124 Stuff')
# add your code for the other sheets below with df_names

# prints all sheets
print(df_players)

def proregstats():
    for row in df_players:
        if int(df_players['Rating']) in tier_0:
            df_players['Regression'] + 1 