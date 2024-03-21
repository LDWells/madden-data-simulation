import dataclasses
import os

import sqlite3 as sql

from definitions import TeamStanding
from typing import List

import dataclasses
import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def query_available_datasets(db_dir: str) -> List[str]:
    con = sql.connect(db_dir)
    cur = con.cursor()

    cur.execute('''
        SELECT *
        FROM sqlite_master
        WHERE type = 'table';
    ''')

    return [a[1] for a in cur.fetchall()][1:]

# query_team_standing
# Finds the associated data for a team in the given dataset
# If there are multiple entries (for example, in the Madden datasets), all relevant stats are averaged
def query_team_standing(db_dir: str, dataset: str, team_name: str) -> TeamStanding:
    connection = sql.connect(db_dir)

    cursor = connection.cursor()

    standings = [list(ts) for ts in cursor.execute(f"SELECT * FROM {dataset} WHERE team_name LIKE '{team_name}'").fetchall()]

    connection.close()

    fields = [f.type for f in dataclasses.fields(TeamStanding)][1:]

    for ts in standings[1:]:
        for i, field in enumerate(fields):
            if field == float:
                standings[0][i] += ts[i]

    for i, field in enumerate(fields):
        if field == float:
            standings[0][i] /= float(len(standings))

    standings[0].insert(0, dataset)
            
    return TeamStanding(*tuple(standings[0]))

def query_leagues(db_dir: str, dataset: str, team_name: str, column_name: str) -> List[TeamStanding]:
    connection = sql.connect(db_dir)

    cursor = connection.cursor()

    standings = [list(ts) for ts in cursor.execute(f"SELECT * FROM {dataset} WHERE team_name LIKE '{team_name}'").fetchall()]

    connection.close()

    for ts in standings:
        ts.insert(0, dataset)

    standings = [TeamStanding(*tuple(st)) for st in standings]

    return standings

def compare_stat_between_datasets(db_dir: str, datasets: List[str], team: str, stat: str):
    standings = []
    for dataset in datasets:
        standings.append(query_team_standing(db_dir, dataset, team))

    #df = pd.DataFrame(standings, columns=[stat]);

    stats = {}
    for st in standings:
        temp = dataclasses.asdict(st)
        stats[st.dataset] = temp[stat]

    plt.bar(range(len(stats)), list(stats.values()), align='center')
    plt.xticks(range(len(stats)), list(stats.keys()))
    plt.ylabel(stat, style='italic')
    plt.suptitle(f"Comparison of {stat} of the {team} in ")
    plt.title(f"{', '.join(datasets)}")

    plt.show()

def compare_distribution(db_dir: str, dataset: str, base: str, team: str, stat: str):
    dist_leagues = query_leagues(db_dir, dataset, team, stat)

    dist_seasons = []
    for league in dist_leagues:
        dist_seasons.append(league)

    base_league = dataclasses.asdict(query_team_standing(db_dir, base, team))[stat]

    dist_df = pd.DataFrame(dist_seasons, columns=[stat])
    base_df = pd.DataFrame([base_league], columns=[stat])

    dist_df["Dataset"] = dataset
    base_df["Dataset"] = base

    sns.histplot(data=dist_df, kde=True, label=dataset)
    plt.axvline(x=base_df[stat].mean(), color='r', label=base)

    plt.title("Comparison of '" + stat + "' Distribution in '" + dataset + "' Against '" + base + "' for " + team)
    plt.xlabel(stat)
    plt.ylabel("# of Leagues")
    
    handles, labels = plt.gca().get_legend_handles_labels()  # Get the handles and labels from the plot
    handles.append(plt.axvline(x=base_df[stat].mean(), color='r'))  # Add the red line to the handles

    plt.legend(handles, labels)  # Display the legend with updated handles and labels
    
    plt.show()
