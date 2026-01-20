"""
Docstring for Awards

A. Batting Awards:
1. Destroyer -> 40+ runs with strike rate > 275
2. Hard Hitter -> 20+ runs with strike rate > 275
3. Aspirant -> 40+ runs with strike rate between 200 and 275
4. Finisher -> 20+ runs with strike rate between 200 and 275
5. Anchor -> 30+ runs with strike rate < 200

6. Run Machine -> 50+ runs
7. Duck Shopping -> 0 runs

B. Bowling Awards:
1. Wicket Wizard -> 2+ wickets
2. Economist -> Economy rate < 12

C. Fielding Awards:
1. Safe Hands -> 2+ catches
2. Agile Feet -> 2+ run outs

D. All-Rounder Awards:
1. Nuclear Weapon -> Runs >= 60 with strike rate > 275 or Wickets >= 2 with economy rate < 12
2. Wild Card -> Runs >= 40 and Wickets >= 1 with economy rate < 15

E. Bad Awards:
1. Team Finisher -> <10 runs with strike rate < 150 and <2 wickets with economy rate > 15
2. Pakistan Express -> Economy rate > 18 with <2 wickets 
3. Cricket Murderer -> <5 runs with strike rate < 150 and 0 wickets with economy rate > 18
"""

from MVP import calculate_mvp

def determine_awards(player_stats):
    awards = []
    # Batting Awards
    strike_rate = (player_stats.runs / player_stats.balls_faced) * 100 if player_stats.balls_faced > 0 else 0
    if player_stats.runs >= 40 and (strike_rate > 275):
        awards.append("Destroyer")
    elif player_stats.runs >= 20 and (strike_rate > 275):
        awards.append("Hard Hitter")
    elif player_stats.runs >= 20 and (strike_rate >= 200 and strike_rate <= 275):
        awards.append("Finisher")
    elif player_stats.runs >= 40 and (strike_rate >= 200 and strike_rate < 275):
        awards.append("Aspirant")
    elif player_stats.runs >= 30 and (strike_rate < 200):
        awards.append("Anchor")
    if player_stats.runs >= 50:
        awards.append("Run Machine")

    # Bowling Awards
    if player_stats.wickets >= 2:
        awards.append("Wicket Wizard")
    if player_stats.overs_bowled > 0:
        economy_rate = player_stats.runs_conceded / player_stats.overs_bowled
        if economy_rate < 12:
            awards.append("Economist")

    # Fielding Awards
    if player_stats.catches >= 2:
        awards.append("Safe Hands")
    if player_stats.run_outs >= 2:
        awards.append("Agile Feet")
    
    # All-Rounder Awards

    if (player_stats.runs >= 60 and strike_rate >= 275) or (player_stats.wickets >= 3 and player_stats.overs_bowled > 0 and (player_stats.runs_conceded / player_stats.overs_bowled) < 10):
        awards.append("Nuclear Weapon")
    
    elif (player_stats.runs >= 40) and (player_stats.wickets >= 1 and player_stats.overs_bowled > 0 and (player_stats.runs_conceded / player_stats.overs_bowled) < 15):
        awards.append("Wild Card")

    # Bad Awards
    if player_stats.runs < 10 and strike_rate < 150 and player_stats.wickets <=1 and (player_stats.overs_bowled > 0 and (player_stats.runs_conceded / player_stats.overs_bowled) > 15):
        awards.append("Team Finisher")

    if player_stats.overs_bowled > 0 and (player_stats.runs_conceded / player_stats.overs_bowled) > 18 and player_stats.wickets < 2:
        awards.append("Pakistan Express")
    
    if player_stats.runs == 0 and player_stats.balls_faced > 0:
        awards.append("Duck Shopping")

    if (player_stats.runs < 5 and strike_rate < 150 and player_stats.wickets == 0 and (player_stats.overs_bowled > 0 and (player_stats.runs_conceded / player_stats.overs_bowled) > 18)):
        awards.append("Cricket Murderer")

    #Special Award
    if(player_stats.runs >= 100 and player_stats.balls_faced <= 40):
        awards.append("Annihilator")

    if (player_stats.wickets >=3 and player_stats.overs_bowled > 0 and (player_stats.runs_conceded / player_stats.overs_bowled) < 10):
        awards.append("Desert Storm")

    if (player_stats.runs >= 60 and strike_rate >= 275 and player_stats.wickets >=2 and player_stats.overs_bowled > 0 and (player_stats.runs_conceded / player_stats.overs_bowled) < 12):
        awards.append("Destruction Force")

    return awards
