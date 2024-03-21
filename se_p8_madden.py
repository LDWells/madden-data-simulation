import dataclasses
import sys
import os
from argparse import ArgumentParser
from analysis import query_available_datasets, query_team_standing, compare_stat_between_datasets, compare_distribution
from database import rebuild_database_preset
from definitions import TEAM_NAME_LOOKUP, TeamStanding
path = os.path.dirname(os.path.realpath(__file__))
db_dir = os.path.join(path, "db", "data.db")
available_datasets = query_available_datasets(db_dir)
def parse_query(args):
    parser = ArgumentParser()
    parser.add_argument("-l", "--league", dest="league", required=True, 
        choices=available_datasets)
    parser.add_argument("-t", "--team", dest="team", required=True, 
        choices=list(TEAM_NAME_LOOKUP.keys()))
    result = vars(parser.parse_args(args))
    print(query_team_standing(db_dir, result["league"], result["team"]))
def parse_compare(args):
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-ls", "--leagues", dest="leagues", nargs="*", 
        choices=available_datasets)
    group.add_argument("-l", "--league", dest="leagues", action="append", 
        choices=available_datasets)

    parser.add_argument("-t", "--team", dest="team", required=True, 
        choices=list(TEAM_NAME_LOOKUP.keys()))
    parser.add_argument("-s", "--stat", dest="stat", required=True, 
        choices=[field.name for field in dataclasses.fields(TeamStanding)])

    result = vars(parser.parse_args(args))
    compare_stat_between_datasets(db_dir, result["leagues"], result["team"], result["stat"])
def parse_distribution(args):
    parser = ArgumentParser()
    parser.add_argument("-l", "--league", dest="league", 
        choices=available_datasets, required=True)
    parser.add_argument("-a", "--against", dest="against", 
        choices=available_datasets, required=True)
    parser.add_argument("-t", "--team", dest="team", required=True, 
        choices=list(TEAM_NAME_LOOKUP.keys()))
    parser.add_argument("-s", "--stat", dest="stat", required=True, 
        choices=[field.name for field in dataclasses.fields(TeamStanding)])

    result = vars(parser.parse_args(args))
    
    compare_distribution(db_dir, result["league"], result["against"], result["team"], result["stat"])
def parse_rebuild(args):
    rebuild_database_preset()
def parse_stats(args):
    print("Available Statistics:\n  | " + '\n  | '.join([field.name for field in dataclasses.fields(TeamStanding)]))
def parse_teams(args):
    print("Available Teams:\n  | " + '\n  | '.join(list(TEAM_NAME_LOOKUP.keys())))
def parse_leagues(args):
    print("Available Leagues:\n  | " + '\n  | '.join(available_datasets))
if __name__ == '__main__':
    args = sys.argv[1:]
    
    if(len(args) == 0):
        print("error: must specify command and requisite arguments")
        sys.exit()
    command, *args = args
    match command:
        case "query": parse_query(args)
        case "compare": parse_compare(args)
        case "distribution": parse_distribution(args)
        case "rebuild": parse_rebuild(args)
        case "stats": parse_stats(args)
        case "teams": parse_teams(args)
        case "leagues": parse_leagues(args)