from random import random


class Game:
    teams = {}

    def __init__(self, home_team_id, away_team_id, score=(0, 0)):
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.winner_id = None
        self.score = score

    def predict_winner(self):
        home_team = self.teams[self.home_team_id]
        away_team = self.teams[self.away_team_id]
        def bonus(difference, upper_bound, lower_bound=0.0):
            base_value = pow(difference/upper_bound, 3)
            if difference >= 0:
                value = min(1, base_value)
            else:
                value = max(-1, base_value)
            return value if abs(difference) > lower_bound else 0
        win_advantage = home_team.win_percentage() - away_team.win_percentage()
        win_bonus = bonus(win_advantage, 0.3, 0.05) * 0.3
        offrtg_advantage = self.offensive_rating(home_team, away_team) - self.offensive_rating(away_team, home_team)
        offrtg_bonus = bonus(offrtg_advantage, 12) * 0.15
        scoring_advantage = home_team.game_stats['PPG'] - away_team.game_stats['PPG']
        scoring_bonus = bonus(scoring_advantage, 10) * 0.05
        shooting_advantage = home_team.game_stats['FG%'] - away_team.game_stats['FG%']
        shooting_bonus = bonus(shooting_advantage, 0.25) * 0.1
        three_point_advantage = home_team.game_stats['3P%'] - away_team.game_stats['3P%']
        three_point_bonus = bonus(three_point_advantage, 0.2) * 0.05
        rebound_advantage = home_team.game_stats['RPG'] - away_team.game_stats['RPG']
        rebound_bonus = bonus(rebound_advantage, 10) * 0.05
        net_advantage = 0.5 + win_bonus + offrtg_bonus + scoring_bonus + shooting_bonus + three_point_bonus + rebound_bonus
        chance = random() * 0.75
        print(net_advantage, chance)
        return self.home_team_id if net_advantage > chance else self.away_team_id

    def offensive_rating(self, team, opponent_team):
        PTS = team.season_stats["PTS"]
        FGA = team.season_stats["FGA"]
        FGM = team.season_stats["FGM"]
        FTA = team.season_stats["FTA"]
        TOV = team.season_stats["TO"]
        ORB = team.season_stats["OFFR"]
        DRB = team.season_stats["DEFR"]
        opp_FGA = opponent_team.season_stats["FGA"]
        opp_FGM = opponent_team.season_stats["FGM"]
        opp_FTA = opponent_team.season_stats["FTA"]
        opp_TOV = opponent_team.season_stats["TO"]
        opp_ORB = opponent_team.season_stats["OFFR"]
        opp_DRB = opponent_team.season_stats["DEFR"]
        def partial_possession(fga, fgm, fta, tov, orb, opp_drb):
            return fga + 0.4 * fta - 1.07 * (orb / (orb + opp_drb)) * (fga - fgm) + tov
        tm_part = partial_possession(FGA, FGM, FTA, TOV, ORB, opp_DRB)
        opp_part = partial_possession( opp_FGA, opp_FGM, opp_FTA, opp_TOV, opp_ORB, DRB)
        possessions = (tm_part + opp_part) / 2
        return 100 * PTS / possessions
