import pdfplumber
import re
from Player_stats import Stats

# ---------------- CONFIG ----------------
def get_object(pdf_path = r"I:\Cric-legends\A_vs_B_1760857941324 (1).pdf"):

    BATSMAN_RE = re.compile(
        r"^([A-Za-z0-9]+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\d.]+)$"
    )
    BOWLER_RE = re.compile(
        r"^([A-Za-z0-9]+)\s+([\d.]+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\d.]+)$"
    )

    players = {}


    # ---------------- HELPERS ----------------
    def get_player(name):
        if name not in players:
            players[name] = Stats(name=name)
        return players[name]


    # ---------------- PDF READ ----------------
    raw_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        print(pdf.pages[0].extract_text())
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                raw_text += text + "\n"

    lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
    match_name = lines[0] 
    # ---------------- PARSER ----------------
    def parse_scorecard(lines):
        for line in lines:

            # ---------- Batting ----------
            bat_match = BATSMAN_RE.match(line)
            if bat_match:
                name, runs, balls, fours, sixes, _ = bat_match.groups()
                p = get_player(name)
                p.runs = int(runs)
                p.balls_faced = int(balls)
                p.fours = int(fours)
                p.sixes = int(sixes)
                continue
            if line.startswith("not out"):
                p.not_out = True
            # ---------- Bowling ----------
            bowl_match = BOWLER_RE.match(line)
            if bowl_match:
                name, overs, maidens, runs_conceded, wickets, _ = bowl_match.groups()
                p = get_player(name)
                p.overs_bowled = float(overs)
                p.maidens = int(maidens)
                p.runs_conceded = int(runs_conceded)
                p.wickets = int(wickets)
                continue

            # ---------- Catches ----------
            if line.startswith("c "):
                parts = line.split()
                if len(parts) > 1:
                    catcher = parts[1]
                    get_player(catcher).catches += 1

            # ---------- Run Outs ----------
            if "Run out" in line:
                inside = re.search(r"\((.*?)\)", line)
                if inside:
                    fielder = inside.group(1)
                    get_player(fielder).run_outs += 1


    # ---------------- RUN ----------------
    parse_scorecard(lines)


    # ---------------- OUTPUT ----------------
    return [match_name, players.values()]

print(get_object())
