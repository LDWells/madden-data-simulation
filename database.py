import dataclasses
import os

import sqlite3 as sql

from typing import List
from definitions import TEAM_NAME_LOOKUP, TeamStanding

from madden_data_parser import parse_madden_data
from nfl_data_parser import parse_nfl_data


def calibrate_madden_datasets(db_dir: str, datasets: List[str], base: str):
    connection = sql.connect(db_dir)
    cursor = connection.cursor()

    madden_results = {}  # stores all columns for a given team and database
    original_madden_results = {}
    nfl_results = {}
    differences = {}  # produces {team_name: {column: {dataset: value}}} pairs

    columns = [field.name for field in dataclasses.fields(TeamStanding)][1:]

    column_types = [f.type for f in dataclasses.fields(TeamStanding)][1:]

    teams = list(TEAM_NAME_LOOKUP.keys())

    for y in range(len(datasets)):
        madden_results[datasets[y]] = []  # stores all columns for a given team and database
        for x in range(len(teams)):
            madden_team_results = {}

            # Query to get the average stats from the madden dataset
            for column in columns:
                cursor.execute("SELECT AVG({}) FROM {} WHERE team_name = ?".format(column, datasets[y]), (teams[x],))
                madden_team_results[column] = cursor.fetchone()[0]

            madden_results[datasets[y]].append(madden_team_results)

    for x in range(len(teams)):
        nfl_results[teams[x]] = {}

        # Query to get the stats from the nfl dataset
        for column in columns:
            cursor.execute("SELECT {} FROM nfl WHERE team_name = ?".format(column), (teams[x],))
            nfl_results[teams[x]][column] = cursor.fetchone()[0]

    # Calculate the differences between madden and nfl results
    for team in teams:
        differences[team] = {}
        for column, column_type in zip(columns, column_types):
            if column_type != float: continue
            
            madden_value = madden_results[base][teams.index(team)][column]
            
            differences[team][column] = madden_value - float(nfl_results[team][column])
        '''
        for column in columns:
            if column != "team_name":
                differences[team][column] = {}
                for dataset in datasets:
                    madden_value = madden_results[dataset][teams.index(team)][column]
                    nfl_value = float(nfl_results[team][column])
                    differences[team][column][dataset] = madden_value - nfl_value
        '''


    # Retrieve all the entities per team from original_madden_results
    for y in range(len(datasets)):
        original_madden_results[datasets[y]] = []  # stores all columns for a given team and database
        for x in range(len(teams)):
            original_madden_team_results = {}

            for column in columns:
                cursor.execute("SELECT {} FROM {} WHERE team_name = ?".format(column, datasets[y]), (teams[x],))
                rows = cursor.fetchall()
                column_values = [row[0] for row in rows]
                original_madden_team_results[column] = column_values

            original_madden_results[datasets[y]].append(original_madden_team_results)

    #deletes tables
    for dataset in datasets:
        table_name = f"{dataset}_calibrated"
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    # Create a new table for each dataset and insert the calibrated results
    for dataset in datasets:
        table_name = f"{dataset}_calibrated"
        cursor.execute(f"CREATE TABLE {table_name}({', '.join(columns)})")

        for i in range(len(original_madden_results[dataset][0]['team_name'])):
            for x in range(len(teams)):
                team = teams[x]
                madden_team_results = original_madden_results[dataset][x]  # Get all entities per team
                insert_values = []

                for column in columns:
                    if column == "league_id":
                        insert_values.append("0") 
                    elif column == "team_name":
                        insert_values.append(f"'{team}'")
                    else:
                        madden_value = madden_team_results[column][i]  # Select the i-th value
                        calibrated_value = madden_value - differences[team][column]
                        insert_values.append(str(calibrated_value))

                cursor.execute(f"INSERT INTO {table_name} VALUES({', '.join(insert_values)})")

    connection.commit()

    connection.close()

def calibrate_madden_datasets_preset():
    path = os.path.dirname(os.path.realpath(__file__))
    db_dir = os.path.join(path, "db", "data.db")

    madden_dir = os.listdir(os.path.join(path, "madden_data"))
    madden_datasets = [f for f in madden_dir]

    calibrate_madden_datasets(db_dir, madden_datasets, "watson_suspended_until_w13")

# rebuild_database
# Deletes the old database and rebuilds it from a list of TeamStanding objects
# The db_dir should be the full path to the database, including its name
def rebuild_database(db_dir: str, standings: List[TeamStanding]):
    if os.path.isfile(db_dir):
        os.remove(db_dir)

    connection = sql.connect(db_dir)

    cursor = connection.cursor()

    fields = [f.name for f in dataclasses.fields(TeamStanding)]

    cursor.execute(f"CREATE TABLE data({', '.join(fields)})")

    for team_standing in [dataclasses.astuple(ts) for ts in standings]:
        cursor.execute(f"INSERT INTO data VALUES({('?, ' * len(fields)).removesuffix(', ')})", team_standing)
        
        try:
            cursor.execute(f"SELECT * FROM {team_standing[0]}").fetchone() is None
        except sql.OperationalError:
            cursor.execute(f"CREATE TABLE {team_standing[0]}({', '.join(fields[1:])})")
        
        cursor.execute(f"INSERT INTO {team_standing[0]} VALUES({('?, ' * (len(fields) - 1)).removesuffix(', ')})", team_standing[1:])

    connection.commit()
    connection.close()

def rebuild_database_preset():
    path = os.path.dirname(os.path.realpath(__file__))

    madden_data_dir = os.path.join(path, "madden_data")
    nfl_data_dir = os.path.join(path, "nfl_data")

    standings = parse_madden_data(madden_data_dir) + parse_nfl_data()

    db_dir = os.path.join(path, "db", "data.db")

    rebuild_database(db_dir, standings)

    calibrate_madden_datasets_preset()

calibrate_madden_datasets_preset()