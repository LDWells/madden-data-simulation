import dataclasses
import os
import json
import sqlite3

# Exclusively for type hints
from typing import List
from definitions import TeamStanding

# parse_season_standings
# Consumes a string, which is a path to a season's directory
# Produces a SeasonStandings object
# This is a helper 
def parse_league_standings(base_dir: str, dataset: str, league_id: str) -> List[TeamStanding]:
    league_dir = os.path.join(base_dir, dataset, league_id, "standings.json")

    with open(league_dir, 'r') as file:
        json_data = json.loads(file.read())
        
        standings = []
        for stats in json_data["teamStandingInfoList"]:

            total_losses = float(stats["totalLosses"])
            total_ties = float(stats["totalTies"])
            total_wins = float(stats["totalWins"])

            games_played = total_losses + total_ties + total_wins

            current_team = TeamStanding(
                dataset,
                league_id,
                float(stats["defPassYds"]) / games_played,
                float(stats["defRushYds"]) / games_played,
                float(stats["defTotalYds"]) / games_played,
                float(stats["netPts"]),
                float(stats["offPassYds"]) / games_played,
                float(stats["offRushYds"]) / games_played,
                float(stats["offTotalYds"]) / games_played,
                float(stats["ptsAgainst"]),
                float(stats["ptsFor"]),
                total_losses,
                total_ties,
                total_wins,
                stats["teamName"],
                float(stats["tODiff"]),
                float(stats["winPct"])
            )

            standings.append(current_team)
        
        return standings

#
# ---
#

# parse_madden_dataset
#
# Consumes a path to the data.
#   This path should contain 'datasets', which themselves contain 'leagues'
#
# Produces a List of TeamStanding objects
#
def parse_madden_data(data_dir: str) -> List[TeamStanding]:
    print(f"Parsing Madden data from {data_dir}...")

    data = []
    for curr in os.walk(data_dir):
        if 'standings.json' in curr[2]:
            (temp, league) = os.path.split(curr[0])
            (path, dataset) = os.path.split(temp)
            
            data.extend(parse_league_standings(path, dataset, league))
    
    print("Finished parsing Madden data")

    return data