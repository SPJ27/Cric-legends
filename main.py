import pdfplumber
from Read_scorecard import get_object
from MVP import calculate_mvp
from Awards import determine_awards

print(pdfplumber.__version__)

players_stats = get_object("I:\\Cric-legends\\uploads\\A_vs_B_1760858094289.pdf")
for player in players_stats:
    mvp_points = calculate_mvp(player)
    awards = determine_awards(player)

    
    print(f"Player: {player.name}")
    print(f"  MVP Points: {mvp_points}")
    print(f"  Awards: {', '.join(awards) if awards else 'None'}")
    print("--------------------------------------------------")