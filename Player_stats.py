class Stats:
    def __init__(
        self,
        name,
        runs=0,
        balls_faced=0,
        fours=0,
        sixes=0,
        wickets=0,
        overs_bowled=0,
        maidens=0,
        hat_tricks=0,
        runs_conceded=0,
        catches=0,
        run_outs=0
    ):
        self.name = name
        self.runs = runs
        self.balls_faced = balls_faced
        self.fours = fours
        self.sixes = sixes
        self.not_out = False
        self.wickets = wickets
        self.overs_bowled = overs_bowled
        self.maidens = maidens
        self.hat_tricks = hat_tricks
        self.runs_conceded = runs_conceded
        self.catches = catches
        self.run_outs = run_outs


