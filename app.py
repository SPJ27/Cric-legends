from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename

from Read_scorecard import get_object
from MVP import calculate_mvp
from Awards import determine_awards
import json

file_path = 'i:/Cric-legends/player_stats.json'

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/analyze", methods=["POST"])
def analyze_match():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if not file.filename.endswith(".pdf"):
        return jsonify({"error": "Only PDF files allowed"}), 400

    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)
    # Save player stats to JSON
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    players = get_object(path)

    response = []
    for p in players:
        player_class = data.get(p.name.lower(), {})
        data[p.name.lower()] = {
            "matches": player_class.get("matches", 0) + 1,
            "innings_batted": player_class.get("innings_batted", 0) + (1 if p.balls_faced > 0 else 0),
            "runs": player_class.get("runs", 0) + p.runs,
            "balls_faced": player_class.get("balls_faced", 0) + p.balls_faced,
            "fours": player_class.get("fours", 0) + p.fours,
            "sixes": player_class.get("sixes", 0) + p.sixes,
            "ducks": player_class.get("ducks", 0) + (1 if p.runs == 0 and p.balls_faced > 0 else 0),
            "fifties": player_class.get("fifties", 0) + (1 if 50 <= p.runs < 100 else 0),
            "hundreds": player_class.get("hundreds", 0) + (1 if p.runs >= 100 else 0),
            "innings_not_out": player_class.get("not_out", 0) + (1 if p.not_out else 0),
            "innings_bowled": player_class.get("innings_bowled", 0) + (1 if p.overs_bowled > 0 else 0),
            "wickets": player_class.get("wickets", 0) + p.wickets,
            "overs_bowled": player_class.get("overs_bowled", 0) + p.overs_bowled,
            "maidens": player_class.get("maidens", 0) + p.maidens,
            "runs_conceded": player_class.get("runs_conceded", 0) + p.runs_conceded,
            "catches": player_class.get("catches", 0) + p.catches,
            "run_outs": player_class.get("run_outs", 0) + p.run_outs,
        }
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        response.append({
            "name": p.name,
            "mvp_score": calculate_mvp(p),
            "awards": determine_awards(p),
            "stats": {
                "runs": p.runs,
                "balls": p.balls_faced,
                "fours": p.fours,
                "sixes": p.sixes,
                "not_out": p.not_out,
                "wickets": p.wickets,
                "overs": p.overs_bowled,
                "runs_conceded": p.runs_conceded,
                "catches": p.catches,
                "run_outs": p.run_outs
            }
        })
    


    
    # Sort MVP leaderboard
    response.sort(key=lambda x: x["mvp_score"], reverse=True)

    return jsonify({
        "mvp": response[0] if response else None,
        "leaderboard": response
    })


@app.route("/get_stats", methods=["GET"])
def get_stats():
    player_name = request.args.get("player_name", "").lower()
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    player_data = data.get(player_name, {})
    player_data['strike_rate'] = round((player_data.get("runs", 0) / player_data.get("balls_faced", 1)) * 100, 2)
    return jsonify(player_data)

if __name__ == "__main__":
    app.run(debug=True)
