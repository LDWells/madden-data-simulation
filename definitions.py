from dataclasses import dataclass

# TeamStanding
# Represents a team's stats
# Simulated standings can be created using 
#   `parse_madden_dataset` in `madden_data_parser.py`
# Real world NFL data can be created using
#   `nfl_data_parser.py`
#
@dataclass
class TeamStanding:
    dataset: str
    league_id: str 
    def_pass_yds: float 
    def_rush_yds: float 
    def_total_yds: float 
    net_pts: float 
    off_pass_yds: float 
    off_rush_yds: float  
    off_total_yds: float  # off_pass_yds + off_rush_yds
    pts_against: float 
    pts_for: float 
    total_losses: float 
    total_ties: float 
    total_wins: float 
    team_name: str 
    turnover_diff: float 
    win_pct: float 

    # Returns a string that can be used for readable print output
    def __str__(self):
        out = f"""
{self.team_name} from '{self.dataset}' with ID {self.league_id}:
    Win Percentage: {self.win_pct}
    Net Points: {self.net_pts}
    Points For / Against: {self.pts_for} / {self.pts_against}
    Wins / Losses / Ties: {self.total_wins} / {self.total_losses} / {self.total_ties}
    Offensive Yards: {self.off_total_yds}
        | Rushing: {self.off_rush_yds}
        | Passing: {self.off_pass_yds}
    Defensive Yards: {self.def_total_yds}
        | Rushing: {self.def_rush_yds}
        | Passing: {self.def_pass_yds}
    Turnover Differential: {self.turnover_diff}
        """

        return out

TEAM_NAME_LOOKUP = {
	"49ers": "san-francisco-49ers",
	"Bears": "chicago-bears",
	"Bengals": "cincinnati-bengals",
	"Bills": "buffalo-bills",
	"Broncos": "denver-broncos",
	"Browns": "cleveland-browns",
	"Buccaneers": "tampa-bay-buccaneers",
	"Cardinals": "arizona-cardinals",
	"Chargers": "los-angeles-chargers",
	"Chiefs": "kansas-city-chiefs",
	"Colts": "indianapolis-colts",
	"Commanders": "washington-commanders",
	"Cowboys": "dallas-cowboys",
	"Dolphins": "miami-dolphins",
	"Eagles": "philadelphia-eagles",
	"Falcons": "atlanta-falcons",
	"Giants": "new-york-giants",
	"Jaguars": "jacksonville-jaguars",
	"Jets": "new-york-jets",
	"Lions": "detroit-lions",
	"Packers": "green-bay-packers",
	"Panthers": "carolina-panthers",
	"Patriots": "new-england-patriots",
	"Raiders": "las-vegas-raiders",
	"Rams": "los-angeles-rams",
	"Ravens": "baltimore-ravens",
	"Saints": "new-orleans-saints",
	"Seahawks": "seattle-seahawks",
	"Steelers": "pittsburgh-steelers",
	"Texans": "houston-texans",
	"Titans": "tennessee-titans",
	"Vikings": "minnesota-vikings"
}