def calculate_ratings(stats):
    outs = stats.innings_batted - stats.innings_not_out
    average = round(stats.runs / outs, 2) if outs > 0 else stats. runs
    strike_rate = round((stats.runs / stats.balls_faced) * 100, 2) if stats.balls_faced > 0 else None
    economy_rate = round((stats.runs_conceded / stats.overs_bowled), 2) if stats.overs_bowled > 0 else None
    batting_score = 0

    if average:
        batting_score += min(average, 40) * 0.8      # max 32

    if strike_rate:
        batting_score += min(strike_rate, 280) * 0.05  # max 14

    batting_score = min(batting_score, 46)

    bowling_score = 0

# Calculate bowling average safely
    bowling_average = (
        stats.runs_conceded / stats.wickets
        if stats.wickets > 0 else None
    )
    bowling_score = 0

    if bowling_average is not None:
        # Reward low averages, punish high averages
        if bowling_average <= 15:
            bowling_score += 25  # elite
        elif bowling_average <= 20:
            bowling_score += 20 # very good
        elif bowling_average <= 30:
            bowling_score += 15  # average
        elif bowling_average <= 35:
            bowling_score += 5   # below average
        else:
            bowling_score += 0   # poor

    bowling_score += min(stats.wickets * 2.5, 12)

    # Cap total bowling score
    bowling_score = min(bowling_score, 36)

    fielding_score = min(
    stats.catches * 1.5 + stats.run_outs * 2.5,
    10
)

    experience_multiplier = min(1 + stats.matches / 50, 1.4)
    career_rating = round(
    min((batting_score + bowling_score + fielding_score) * experience_multiplier, 100),
    2
)   
    return career_rating


