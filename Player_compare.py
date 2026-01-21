import json
import os
from Career_rating import calculate_ratings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "player_stats.json")

def compare(players):
    player_stats = []
    for player in players:
        # Add comparison logic here
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

        player_data = data.get(player.lower(), {})

        # Safely compute stats
        innings_batted = player_data.get("innings_batted", 0)
        not_outs = player_data.get("innings_not_out", 0)
        balls_faced = player_data.get("balls_faced", 0)
        overs_bowled = player_data.get("overs_bowled", 0)
        runs_conceded = player_data.get("runs_conceded", 0)
        wickets = player_data.get("wickets", 0)
        runs = player_data.get("runs", 0)

        # Batting average
        outs = innings_batted - not_outs
        player_data['batting_average'] = round(runs / outs, 2) if outs > 0 else None

        # Strike rate
        player_data['strike_rate'] = round((runs / balls_faced) * 100, 2) if balls_faced > 0 else None

        # Economy rate
        player_data['economy_rate'] = round(runs_conceded / overs_bowled, 2) if overs_bowled > 0 else None

        # Bowling average
        player_data['bowling_average'] = round(runs_conceded / wickets, 2) if wickets > 0 else 0

        # Career rating
        player_data['career_rating'] = calculate_ratings(type('Stats', (object,), player_data)())
        player_stats.append(player_data)
    return player_stats

players = ["saksham", "kapish", "bhavesh", "rishon", "krishna"]
stats_comparison = compare(players)

p1_stats = stats_comparison[0]

print(f"{'STAT':<20}" + "".join(f"{player:<15}" for player in players))
print("-" * len(stats_comparison) * 20)

for key in p1_stats:
    print(f"{key:<20}" + "".join(f"{(stats[key]):<15}" for stats in stats_comparison))