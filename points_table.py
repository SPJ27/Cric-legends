matches = {
    "team_a":
    {
        "points": 4,
        "matches_played": 2,
        "wins": 2,
        "loss": 0,
        "runs_scored": 74,
        "overs_faced": 4.0,
        "runs_conceded": 71,
        "overs_bowled": 3.5,
    },
    "team_b":
    {
        "points": 0,
        "matches_played": 2,
        "wins": 0,
        "loss": 2,
        "runs_scored": 82,
        "overs_faced": 3.5,
        "runs_conceded": 83,
        "overs_bowled": 3.83333,
    },
    "team_c":
    {
        "points": 2,
        "matches_played": 2,
        "wins": 1,
        "loss": 1,
        "runs_scored": 79,
        "overs_faced": 3.5,
        "runs_conceded": 78,
        "overs_bowled": 3.3333,
    },
}

def calculate_nrr(matches):
    run_rates = {}
    for team, stats in matches.items():
        print(team)
        print(stats)
        runs_scored = stats["runs_scored"]
        overs_faced = stats["overs_faced"]
        runs_conceded = stats["runs_conceded"]
        overs_bowled = stats["overs_bowled"]
        if overs_faced == 0 or overs_bowled == 0:
            return 0.0
        nrr = (runs_scored / overs_faced) - (runs_conceded / overs_bowled)
        run_rates[team] = round(nrr, 3)
    return run_rates

print(calculate_nrr(matches))