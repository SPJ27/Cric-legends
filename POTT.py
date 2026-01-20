def calculate_series_rating(mvp_points):
    # 1. Calc avg.
    avg_mvp = sum(mvp_points) / len(mvp_points) if mvp_points else 0

    # 2. Std Dev.
    variance = sum((x - avg_mvp) ** 2 for x in mvp_points) / len(mvp_points) if mvp_points else 0
    std_dev = variance ** 0.5

    # 3. Best Score
    best_score = max(mvp_points) if mvp_points else 0

    total_rating = 0.6 * avg_mvp - 0.2 * std_dev + 0.2 * best_score
    return total_rating

player_1 = [10, 12, 400, 45]
player_2 = [110, 115, 120, 198]

print("Player 1 Series Rating:", calculate_series_rating(player_1))
print("Player 2 Series Rating:", calculate_series_rating(player_2))