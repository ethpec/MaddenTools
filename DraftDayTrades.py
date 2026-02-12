import pandas as pd
import numpy as np
import random
import string

USER_PICK = 4
USER_TEAM_INDEX = 26

team_dict = {
    0: 'CHI', 1: 'CIN', 2: 'BUF', 3: 'DEN', 4: 'CLE', 5: 'TB', 6: 'ARI',
    7: 'LAC', 8: 'KC', 9: 'IND', 10: 'DAL', 11: 'MIA', 12: 'PHI',
    13: 'ATL', 14: 'SF', 15: 'NYG', 16: 'JAX', 17: 'NYJ', 18: 'DET',
    19: 'GB', 20: 'CAR', 21: 'NE', 22: 'LV', 23: 'LAR', 24: 'BAL',
    25: 'WAS', 26: 'NO', 27: 'SEA', 28: 'PIT', 29: 'TEN',
    30: 'MIN', 31: 'HOU', 32: 'FA'
}

def get_trade_probability(pick):
    if 1 <= pick <= 32:
        return 0.10
    elif 33 <= pick <= 96:
        return 0.05
    elif 97 <= pick <= 255:
        return 0.03
    return 0


def get_value_distribution(pick):
    if 1 <= pick <= 32:
        return {
            "UNDER": 0.20,
            "FAIR": 0.40,
            "SLIGHT_OVER": 0.25,
            "BIG_OVER": 0.15
        }
    elif 33 <= pick <= 96:
        return {
            "UNDER": 0.30,
            "FAIR": 0.45,
            "SLIGHT_OVER": 0.20,
            "BIG_OVER": 0.05
        }
    elif 97 <= pick <= 255:
        return {
            "UNDER": 0.45,
            "FAIR": 0.40,
            "SLIGHT_OVER": 0.12,
            "BIG_OVER": 0.03
        }
    return None


def roll_value_tier(distribution):
    roll = random.random()
    cumulative = 0

    for tier, probability in distribution.items():
        cumulative += probability
        if roll < cumulative:
            return tier

    return "FAIR"  # fallback safety

def get_trade_interest():
    interested_teams = []

    trade_probability = get_trade_probability(USER_PICK)
    value_distribution = get_value_distribution(USER_PICK)

    for team_index, team_abbr in team_dict.items():

        if team_index == USER_TEAM_INDEX:
            continue
        if team_abbr == 'FA':
            continue

        # Roll for interest
        if random.random() < trade_probability:

            # Roll for value tier
            value_tier = roll_value_tier(value_distribution)

            interested_teams.append({
                "team": team_index,
                "tier": value_tier
            })

    return interested_teams

trade_teams = get_trade_interest()

print("Pick:", USER_PICK)

for offer in trade_teams:
    print(team_dict[offer["team"]], "offers:", offer["tier"])