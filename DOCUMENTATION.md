# Documentation

EA Sports has been developing and selling the Madden NFL simulation game for about 40 years, with a major stated goal of making the game as realistic as possible. Prior research has shown that league-wide simulations using the Madden Franchise mode can be used to reliably predict game outcomes, point spreads, and other team-wide metrics of play. In fact, during the 2022-2023 season, simulating actual NFL games using Madden '22 was shown to 'beat Draftkings' in certain scenarios.

Quarterback Deshuan Watson was suspended for 11 games over the 2022 NFL season for violating the NFL's personal conduct policy.
During the investigation into his behavior, the Browns announced a record-setting contract for Watson.

The goal of this project is to provide comparative tools for the analysis of simulated Madden seasons against real-world NFL data.
These tools can allow us to determine the simulation's bias and ultimately discover if the Browns' acquisition of Watson was 'worth it' from a financial perspective.

## Prerequisites

This project requires *Python 3.10* or above.

## Installation

First, clone the project repository.

```
git clone https://github.com/dussec/madden-data-analysis.git
cd ./madden-data-analysis
```

Then, install the projects dependencies from the project root:

```
python3 -m pip install -r requirements.txt
```

If the project fails to run, please re-run this command with the `--force-reinstall` flag to ensure package versions are correct.

## Note for Testers

The meat of this project is behind the scenes (scraping stats, producing a database, and calibrating it to fit the 2022 NFL season).

Pretty much all you have to play around with is the `compare` and `distribution` commands (shown below).

You CAN `rebuild` the database if you want; we don't recommend it (it takes about 5 minutes to build and calibrate. Plus, it's already included in the repo).

## Usage

The project's functionality is exposed through a command-line interface.
All commands should be placed _after_ `python3 se_p8_madden.py` (specifying `python3` is not strictly necessary, but can avoid unintended behavior when Python 2 is added to PATH).

Note, the following commands share a number of fields.
To view available options, try to run the `stats`, `leagues`, and `teams` commands.

Additionally, note that all commands can be substituted for their first letter, with a single dash preceeding.
For example, the following arguments are interchangeable:

```
--team Browns
--team=Browns
-t Browns
-tBrowns
```

### `query`

```
query [[league]] [[team]]
```

The `query` command returns the stats about a single team from a single _league_.

```
~/> python3 se_p8_madden.py query -l watson_not_suspended -t Browns
```

### `compare`

```
compare [[league]] .. [[league]] [[team]] [[stat]]
```

Displays a barchart comparing a teams performance across a number of different leagues.
Any number of league paramters can be supplied. 
For example, if we wanted to compare the Vikings' offensive rushing yards in the `watson_not_suspended` and `nfl` datasets, we would type:

```
~/> python3 se_p8_madden.py compare -l watson_not_suspended -l nfl -t Vikings -s off_rush_yds
```

See a list of all available stats with the `stats` command.

### `distribution`

```
distribution [[league]] [[against]] [[team]] [[stat]]
```

Creates a histogram that shows the distribution of a statistic across all seasons within a league, compared against another league's average.
The command takes two league names, a team, and a stat.
For example, to compare the Browns' net points in the Madden `watson_suspended_until_w13` league against the real-world NFL league, we would type:

```
~/> python3 se_p8_madden.py distribution -l watson_suspended_until_w13 -a nfl -t Browns -s net_pts
```

### `rebuild`

```
rebuild
```

Rebuilds the database from scratch. 
Madden data is parsed from the `madden_data` folder, while NFL data is scraped from the web.
I'd advise against running this, the webscraping takes a _while_ (~8 minutes).

```
~/> python3 se_p8_madden.py rebuild
```

## Calibrated Datasets

After building the database, the tool 'calibrates' the Madden datasets. 
This process finds per-team, per-stat biases between the 'watson_suspended_until_w13' and 'nfl' leagues,
then produces 4 new leagues.
These leagues are suffixed with `_calibrated` to differentiate them. 

By performing the calibration, we are slightly shifting the Madden data to reconcile it with real-world stats.
This is why we perform the calibration with the simulated league where Deshuan Watson was benched for 13 games; 
it's the same scenario that occurred in the 2022 season.