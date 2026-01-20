 player_class.get("innings_bowled", 0) + (1 if player.overs_bowled > 0 else 0),
        "wickets": player_class.get("wickets", 0) + player.wickets,
        "overs_bowled": player_class.get("overs_bowled", 0) + player.overs_bowled,
        "maidens": player_class.get("maidens", 0) + player.maidens,
        "runs_conceded": 