def parse_salary_table(salary_df):
    salary_data = {}

    # Group rows by Position (last column)
    for pos, group in salary_df.groupby('Position'):
        pos = str(pos).strip().upper()

        # Extract numeric values for each Type ignoring first column (Type) and last (Position)
        overall = group[group['Type'] == 'OverallRating'].iloc[0, 1:-1].astype(float).tolist()
        aav = group[group['Type'] == 'AAV'].iloc[0, 1:-1].astype(float).tolist()
        bonus = group[group['Type'] == 'Bonus'].iloc[0, 1:-1].astype(float).tolist()
        length = group[group['Type'] == 'Length'].iloc[0, 1:-1].astype(float).tolist()

        salary_data[pos] = {
            'Overall': overall,
            'AAV': aav,
            'Bonus': bonus,
            'Length': length
        }

    return salary_data
