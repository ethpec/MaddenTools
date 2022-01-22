import pandas as pd
import xlrd

file_path = '/Users/ianjpeck/Documents/GitHub/madden22stats/Files/All.xlsm'

# YOU MUST PUT sheet_name=None TO READ ALL CSV FILES IN YOUR XLSM FILE
df_players = pd.read_excel(file_path, sheet_name='124 Stuff')

# prints all sheets
print(df_players)