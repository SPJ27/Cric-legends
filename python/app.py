from flask import Flask, request, jsonify
import os
import json
from werkzeug.utils import secure_filename

from Career_rating import calculate_ratings
from Read_scorecard import get_object
from MVP import calculate_mvp
from Awards import determine_awards


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
STATS_FILE = os.path.join(BASE_DIR, "player_stats.json")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)


def update_player_stats(prev, p):
    """Update cumulative career stats for a player"""
    return {
        "matches": prev.get("matches", 0) + 1,
        "innings_batted": prev.get("innings_batted", 0) + (p.balls_faced > 0),
        "runs": prev.get("runs", 0) + p.runs,
        "balls_faced": prev.get("balls_faced", 0) + p.balls_faced,
        "fours": prev.get("fours", 0) + p.fours,
        "sixes": prev.get("sixes", 0) + p.sixes,
        "ducks": prev.get("ducks", 0) + (p.runs == 0 and p.balls_faced > 0),
        "fifties": prev.get("fifties", 0) + (50 <= p.runs < 100),
        "hundreds": prev.get("hundreds", 0) + (p.runs >= 100),
        "innings_not_out": prev.get("innings_not_out", 0) + p.not_out,
        "innings_bowled": prev.get("innings_bowled", 0) + (p.overs_bowled > 0),
        "wickets": prev.get("wickets", 0) + p.wickets,
        "overs_bowled": prev.get("overs_bowled", 0) + p.overs_bowled,
        "maidens": prev.get("maidens", 0) + p.maidens,
        "runs_conceded": prev.get("runs_conceded", 0) + p.runs_conceded,
        "catches": prev.get("catches", 0) + p.catches,
        "run_outs": prev.get("run_outs", 0) + p.run_outs,
    }


@app.route("/analyze", methods=["POST"])
def analyze_match():
    if "files" not in request.files:
        return jsonify({"error": "No files uploaded"}), 400

    files = request.files.getlist("files")
    matches_list = {}
    with open(STATS_FILE, "r") as f:
        career_data = json.load(f)

    for i, file in enumerate(files):
        if not file.filename.lower().endswith(".pdf"):
            continue

        filename = secure_filename(file.filename)
        path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(path)

        match_name, players = get_object(path)
        unique_match_name = match_name + f"_{i}" if match_name in matches_list else match_name
        matches_list[unique_match_name] = []
        for p in players:
            key = p.name.lower()
            prev_stats = career_data.get(key, {})
            career_data[key] = update_player_stats(prev_stats, p)
            matches_list[unique_match_name].append({"name": p.name, "mvp_score": calculate_mvp(p), "awards": determine_awards(p)})
        matches_list[unique_match_name].sort(
        key=lambda x: x["mvp_score"],
        reverse=True
    )
    with open(STATS_FILE, "w") as f:
        json.dump(career_data, f, indent=4)

    return jsonify(matches_list)


@app.route("/get_stats", methods=["GET"])
def get_stats():
    player_name = request.args.get("player_name", "").lower()

    with open(STATS_FILE, "r") as f:
        data = json.load(f)

    stats = data.get(player_name, {})

    innings = stats.get("innings_batted", 0)
    not_outs = stats.get("innings_not_out", 0)
    balls = stats.get("balls_faced", 0)
    runs = stats.get("runs", 0)
    overs = stats.get("overs_bowled", 0)
    conceded = stats.get("runs_conceded", 0)
    wickets = stats.get("wickets", 0)

    outs = innings - not_outs

    stats.update({
        "batting_average": round(runs / outs, 2) if outs > 0 else None,
        "strike_rate": round((runs / balls) * 100, 2) if balls > 0 else None,
        "economy_rate": round(conceded / overs, 2) if overs > 0 else None,
        "bowling_average": round(conceded / wickets, 2) if wickets > 0 else None,
        "career_rating": calculate_ratings(type("Stats", (), stats)())
    })

    return jsonify(stats)


if __name__ == "__main__":
    app.run(debug=True)
