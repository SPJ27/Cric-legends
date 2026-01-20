def calculate_mvp(stats):
    score = stats.runs
    balls = stats.balls_faced
    fours = stats.fours
    sixes = stats.sixes
    not_out = stats.not_out

    strike_rate = (score / balls) * 100 if balls > 0 else 0

    wickets = stats.wickets
    overs = stats.overs_bowled
    maidens = stats.maidens
    runs_conceded = stats.runs_conceded

    economy_rate = (runs_conceded / overs) if overs > 0 else None

    catches = stats.catches
    run_outs = stats.run_outs

    batting_points = score + fours + (sixes * 2)

    if balls >= 4:
        if strike_rate > 130:
            batting_points += strike_rate / 10
        elif strike_rate < 100:
            batting_points -= 5

    if score >= 30:
        batting_points += score / 5
    elif score == 0 and balls > 0:
        batting_points -= 10

    if not_out:
        batting_points += 5

    bowling_points = 0

    bowling_points += wickets * 25
    bowling_points += maidens * 10

    if overs > 0:
        if economy_rate < 6:
            bowling_points += 15
        elif economy_rate <= 9:
            bowling_points += 5
        elif economy_rate <= 12 and economy_rate > 9:
            bowling_points += 5
        elif economy_rate > 12:
            bowling_points -= 15
        elif economy_rate > 10:
            bowling_points -= 10

    if wickets >= 3:
        bowling_points += 5
    if wickets >= 5:
        bowling_points += 10

    fielding_points = (catches * 5) + (run_outs * 5)

    all_rounder_bonus = 0
    if score >= 20 and wickets >= 1:
        all_rounder_bonus = 10

    total_points = batting_points + bowling_points + fielding_points + all_rounder_bonus
    return round(total_points, 2)

