from typing import List
from definitions import TEAM_NAME_LOOKUP, TeamStanding

import requests
import pandas as pd

import collections
collections.Callable = collections.abc.Callable

from html_table_parser.parser import HTMLTableParser

from re import search
from bs4 import BeautifulSoup

def scrape_team_standing(team: str) -> TeamStanding:
    headers = {
        "User-Agent": "Mozilla/6.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0",
        "X-Requested-With": "XMLHttpRequest"
    }

    url = f"https://www.footballdb.com/teams/nfl/{TEAM_NAME_LOOKUP[team]}"
    
    session = requests.Session()
    response = session.get(url, headers=headers)

    html = response.content.decode()

    soup = BeautifulSoup(html, 'lxml')
    team_banner = soup.find("div", {"id": "teambanner"}).text

    games = [float(int(i)) for i in search(r"\d+-\d+(-\d+)?", team_banner).group(0).split('-')]

    total_wins = games[0]
    total_losses = games[1]
    total_ties = 0
    if len(games) > 2:
        total_ties = games[2]

    parser = HTMLTableParser()
    parser.feed(html)

    tables = [pd.DataFrame(table) for table in parser.tables]

    games_played = float(total_wins + total_losses + total_ties)

    win_pct = total_wins / games_played

    def_pass_yds = float(tables[2].iloc[3, 2].split(' ')[0])
    def_rush_yds = float(tables[2].iloc[2, 2].split(' ')[0])
    def_total_yds = float(tables[2].iloc[1, 2].split(' ')[0])

    off_pass_yds = float(tables[2].iloc[3, 1].split(' ')[0])
    off_rush_yds = float(tables[2].iloc[2, 1].split(' ')[0])
    off_total_yds = float(tables[2].iloc[1, 1].split(' ')[0])

    html = session.get(url + "/stats", headers=headers).content.decode()

    parser = HTMLTableParser()
    parser.feed(html)

    tables = [pd.DataFrame(table) for table in parser.tables]

    pts_for = float(tables[-1].iloc[-2, -1]) / games_played
    pts_against = float(tables[-1].iloc[-1, -1]) / games_played
    net_pts = float(tables[-1].iloc[-2, -1]) - float(tables[-1].iloc[-1, -1])

    team_interceptions = float(tables[-3].iloc[-2, 1])
    opp_interceptions = float(tables[-3].iloc[-1, 1])
    team_fumbles_lost = float(tables[-2].iloc[-2, 2])
    opp_fumbles_lost = float(tables[-2].iloc[-1, 2])

    turnover_diff = team_interceptions + opp_fumbles_lost - opp_interceptions - team_fumbles_lost

    return TeamStanding(
        'nfl',
        '0',
        def_pass_yds,
        def_rush_yds,
        def_total_yds,
        net_pts,
        off_pass_yds,
        off_rush_yds,
        off_total_yds,
        pts_against,
        pts_for,
        total_losses,
        total_ties,
        total_wins,
        team,
        turnover_diff,
        win_pct
    )


def parse_nfl_data() -> List[TeamStanding]:
    standings = []
    for team in TEAM_NAME_LOOKUP.keys():
        print(f"Scraping data for {team} from [https://www.footballdb.com]...")
        standings.append(scrape_team_standing(team))
        print(f"Completed processing data for {team}")

    return standings
