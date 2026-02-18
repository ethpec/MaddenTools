import pandas as pd
import numpy as np
import random

# =========================
# USER INPUT
# =========================

TRADE_DIRECTION = "UP"  # "DOWN" or "UP"
USER_PICK = 122 # 1 less than pick number
USER_TEAM_NAME = 'NO'

# =========================
# FILE PATHS
# =========================

pick_file_path = 'Files/Madden26/IE/Season1/DraftPicks.xlsx'
index_file_path = 'Files/Madden26/IE/Season1/DraftTeamIndex.xlsx'
value_file_path = 'Files/Madden26/IE/Season1/DraftPickValue.xlsx'

# =========================
# LOAD DATA
# =========================

team_index_df = pd.read_excel(index_file_path)
team_picks_df = team_index_df[['Team Name', 'Team Index', 'Binary']].copy()
team_picks_df['Binary'] = team_picks_df['Binary'].astype(str).str.zfill(16)

draft_picks_df = pd.read_excel(pick_file_path)
draft_picks_df = draft_picks_df[draft_picks_df['YearOffset'] == 0].copy()
draft_picks_df['CurrentTeam'] = draft_picks_df['CurrentTeam'].astype(str).str[-16:]

pick_value_df = pd.read_excel(value_file_path)

# Merge pick values
draft_picks_df = pd.merge(
    draft_picks_df,
    pick_value_df[['Pick', 'Value']],
    how='left',
    left_on='PickNumber',
    right_on='Pick'
)

# =========================
# CALCULATE TEAM PICK COUNTS
# =========================

num_draft_picks = draft_picks_df.groupby('CurrentTeam').size().reset_index(name='PicksThisYear')

team_picks_df = pd.merge(
    team_picks_df,
    num_draft_picks,
    how='left',
    left_on='Binary',
    right_on='CurrentTeam'
)

team_picks_df['PicksThisYear'].fillna(0, inplace=True)
team_picks_df.drop(columns='CurrentTeam', inplace=True)

# =========================
# CALCULATE TEAM TOTAL DRAFT CAPITAL
# =========================

team_pick_values = draft_picks_df.groupby('CurrentTeam')['Value'].sum().reset_index()

team_picks_df = pd.merge(
    team_picks_df,
    team_pick_values,
    how='left',
    left_on='Binary',
    right_on='CurrentTeam'
)

team_picks_df['Value'].fillna(0, inplace=True)
team_picks_df.drop(columns='CurrentTeam', inplace=True)

# Remove teams with zero capital
team_picks_df = team_picks_df[team_picks_df['Value'] > 0]

# =========================
# BUILD DRAFT ORDER LOOKUP
# =========================

draft_order_df = draft_picks_df[['CurrentTeam', 'PickNumber']].copy()
draft_order_df.columns = ['Binary', 'PickNumber']

# Merge team names into draft order
draft_order_df = pd.merge(
    draft_order_df,
    team_picks_df[['Binary', 'Team Name']],
    on='Binary',
    how='left'
)

# =========================
# HELPER FUNCTIONS
# =========================

def get_base_probability(pick):
    if TRADE_DIRECTION == "DOWN":
        if 1 <= pick <= 32:
            return 0.0625
        elif 33 <= pick <= 64:
            return 0.0725
        elif 65 <= pick <= 96:
            return 0.0625
        elif 97 <= pick <= 255:
            return 0.0525
        return 0
    else: # USER trading up
        if 1 <= pick <= 32:
            return 0.125
        elif 33 <= pick <= 64:
            return 0.15
        elif 65 <= pick <= 96:
            return 0.125
        elif 97 <= pick <= 255:
            return 0.1
        return 0

def get_pick_multiplier(num_picks):
    if TRADE_DIRECTION == "DOWN": # (USER trading down)
        if num_picks >= 10:
            return 1.5
        elif num_picks == 9:
            return 1.375
        elif num_picks == 8:
            return 1.25
        elif num_picks == 7:
            return 1.125
        elif num_picks == 6:
            return 1
        elif num_picks == 5:
            return 0.875
        elif num_picks <= 4:
            return 0.75
        return 1

    else:  # TRADE UP (USER trading up)
        if num_picks >= 10:
            return 0.75
        elif num_picks == 9:
            return 0.875
        elif num_picks == 8:
            return 1
        elif num_picks == 7:
            return 1.125
        elif num_picks == 6:
            return 1.25
        elif num_picks == 5:
            return 1.375
        elif num_picks <= 4:
            return 1.5
        return 1
    
def get_capital_multiplier(total_pick_value):
    if TRADE_DIRECTION == "DOWN": # (USER trading down)
        if total_pick_value >= 4000:
            return 1.3
        elif 4000 > total_pick_value >= 3000:
            return 1.2
        elif 3000 > total_pick_value >= 2000:
            return 1.1
        elif 2000 > total_pick_value >= 1500:
            return 1
        elif 1500 > total_pick_value >= 1000:
            return 0.9
        elif 1000 > total_pick_value >= 750:
            return 0.8
        elif total_pick_value < 750:
            return 0.7
        return 1
    
    else:  # TRADE UP (USER trading up)
        if total_pick_value >= 4000:
            return 0.7
        elif 4000 > total_pick_value >= 3000:
            return 0.8
        elif 3000 > total_pick_value >= 2000:
            return 0.9
        elif 2000 > total_pick_value >= 1500:
            return 1
        elif 1500 > total_pick_value >= 1000:
            return 1.1
        elif 1000 > total_pick_value >= 750:
            return 1.2
        elif total_pick_value < 750:
            return 1.3
        return 1
    
def get_distance_multiplier(team_pick_position):
    if TRADE_DIRECTION == "DOWN": # (USER trading down)
        distance = abs(team_pick_position - USER_PICK)

        if distance <= 5:
            return 1.0
        elif distance <= 10:
            return 0.875
        elif distance <= 15:
            return 0.75
        else:
            return 0.25
        
    else:  # TRADE UP (USER trading up)
        distance = abs(team_pick_position - USER_PICK)

        if distance <= 5:
            return 1.125
        elif distance <= 10:
            return 1.0
        elif distance <= 15:
            return 0.875
        else:
            return 0.75

def get_distance_limit(pick):
    if TRADE_DIRECTION == "DOWN":
        if 1 <= pick <= 5:
            return 10
        elif 6 <= pick <= 10:
            return 15
        elif 11 <= pick <= 32:
            return 20
        elif 33 <= pick <= 96:
            return 25
        else:
            return 32
    else: # USER trading up
        if 1 <= pick <= 32:
            return 20
        elif 33 <= pick <= 64:
            return 25
        elif 65 <= pick <= 96:
            return 30
        else:
            return 32       


def get_value_distribution(pick):
    if TRADE_DIRECTION == "DOWN":
        if 1 <= pick <= 32:
            return {
                "UNDER (~95%)": 0.15,
                "FAIR": 0.40,
                "SLIGHT_OVER (~105%)": 0.30,
                "BIG_OVER (~110%+)": 0.15
            }
        elif 33 <= pick <= 96:
            return {
                "UNDER (~95%)": 0.15,
                "FAIR": 0.50,
                "SLIGHT_OVER (~105%)": 0.25,
                "BIG_OVER (~110%+)": 0.10
            }
        else:
            return {
                "UNDER (~95%)": 0.15,
                "FAIR": 0.60,
                "SLIGHT_OVER (~105%)": 0.20,
                "BIG_OVER (~110%+)": 0.05
            }
    else: # USER trading up
        if 1 <= pick <= 32:
            return {
                "UNDER (~95%)": 0.15,
                "FAIR": 0.40,
                "SLIGHT_OVER (~105%)": 0.30,
                "BIG_OVER (~110%+)": 0.15
            }
        elif 33 <= pick <= 96:
            return {
                "UNDER (~95%)": 0.15,
                "FAIR": 0.50,
                "SLIGHT_OVER (~105%)": 0.25,
                "BIG_OVER (~110%+)": 0.10
            }
        else:
            return {
                "UNDER (~95%)": 0.15,
                "FAIR": 0.60,
                "SLIGHT_OVER (~105%)": 0.20,
                "BIG_OVER (~110%+)": 0.05
            }

def roll_value_tier(distribution):
    roll = random.random()
    cumulative = 0

    for tier, probability in distribution.items():
        cumulative += probability
        if roll < cumulative:
            return tier

    return "FAIR"

# =========================
# GET USER PICK VALUE
# =========================

user_pick_value = pick_value_df.loc[
    pick_value_df['Pick'] == USER_PICK, 'Value'
].values[0]

distance_limit = get_distance_limit(USER_PICK)

# =========================
# TRADE INTEREST ENGINE
# =========================

def get_trade_interest():
    interested_teams = []

    base_probability = get_base_probability(USER_PICK)
    value_distribution = get_value_distribution(USER_PICK)

    for _, team_row in team_picks_df.iterrows():

        team_name = team_row['Team Name']
        team_total_value = team_row['Value']
        picks_this_year = team_row['PicksThisYear']

        if TRADE_DIRECTION in ("DOWN") and team_name == USER_TEAM_NAME:
            continue

        if TRADE_DIRECTION == "DOWN":
            # All picks after user pick (same as before)
            team_picks_after = draft_order_df[
                (draft_order_df['Team Name'] == team_name) &
                (draft_order_df['PickNumber'] > USER_PICK)
            ]

            if team_picks_after.empty:
                continue

            # Use the earliest pick after user
            team_pick_position = team_picks_after['PickNumber'].min()

            # Distance filter
            if team_pick_position > USER_PICK + distance_limit:
                continue

        else:  # TRADE UP
            # All picks before user pick
            team_picks_before = draft_order_df[
                (draft_order_df['Team Name'] == team_name) &
                (draft_order_df['PickNumber'] < USER_PICK)
            ]

            # Only consider picks within the distance window
            eligible_picks = team_picks_before[
                team_picks_before['PickNumber'] >= USER_PICK - distance_limit
            ]

            if eligible_picks.empty:
                continue  # no eligible pick in range

            # Use the pick closest to the user pick (latest pick in range)
            team_pick_position = eligible_picks['PickNumber'].max()

        if TRADE_DIRECTION == "DOWN":
            if team_pick_position > USER_PICK + distance_limit:
                continue
        else:  # TRADE UP
            if team_pick_position < USER_PICK - distance_limit:
                continue

        # Must have enough capital
        if team_total_value < user_pick_value * 0.5:
            continue

        pickcount_aggression_multiplier = get_pick_multiplier(picks_this_year)
        pickvalue_aggression_multiplier = get_capital_multiplier(team_total_value)
        distance_multiplier = get_distance_multiplier(team_pick_position)
        trade_probability = base_probability * pickcount_aggression_multiplier * pickvalue_aggression_multiplier * distance_multiplier

        # Hot-zone boosts
        if 0 <= USER_PICK <= 9:
            trade_probability *= 1.125
        elif 10 <= USER_PICK <= 19:
            trade_probability *= 1.025
        elif 20 <= USER_PICK <= 29:
            trade_probability *= 1.1
        elif 30 <= USER_PICK <= 34:
            trade_probability *= 1.25
        elif 35 <= USER_PICK <= 39:
            trade_probability *= 1.125
        elif 40 <= USER_PICK <= 44:
            trade_probability *= 1.075
        elif 45 <= USER_PICK <= 49:
            trade_probability *= 1.05
        elif 50 <= USER_PICK <= 99:
            trade_probability *= 1.025
        elif 100 <= USER_PICK <= 255:
            trade_probability *= 1.0

        trade_probability = min(trade_probability, 0.25)

        if np.random.rand() < trade_probability:
            tier = roll_value_tier(value_distribution)

            interested_teams.append({
                "team": team_name,
                "pick_position": team_pick_position,
                "picks": picks_this_year,
                "capital": int(team_total_value),
                "tier": tier
            })

    return interested_teams


# =========================
# RUN
# =========================

offers = get_trade_interest()

# Sort offers from smallest pick number to largest
offers = sorted(offers, key=lambda x: x['pick_position'])

print(f"\n========== TRADE OFFERS FOR PICK {USER_PICK} ==========\n")

if not offers:
    print("No teams interested.\n")
else:
    for offer in offers:
        print(
            f"{offer['team']} (Pick {offer['pick_position']}) | "
            f"Picks: {offer['picks']} | "
            f"Capital: {offer['capital']} | "
            f"Offer Tier: {offer['tier']}"
        )

print("\n=======================================================\n")