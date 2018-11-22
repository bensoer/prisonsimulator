# prisonsimulator

prisonsimulator is a simulator for solving the prisoner lightswitch problem, which is to find the fastest way
to determine if all prisoners have been inside the room.

# Prerequisites
The project is built using Python 3.6. There are no other dependencies on the project currently

# Setup
1. Clone the project
2. Execute `main.py` from terminal to execute the simulation

# Usage
There are several optional parameters that can be passed to the `main.py` to change how output is handled and
for metric collection. Metric collection will run the simulation a lot slower but will show valuable insight into
the simulations activites. The parameters are as follows:

| Parameter | Description |
| --------- | ----------- |
| --SILENT | Runs the application on silent mode, no output is printed except startup and the final results |
| --KEEPSTATS | Enables storage of metrics in an sqlite database. Required to work with `metrics.py` and if you would like to sort through results of the simulation |

Using the `--SILENT` flag will minimize output printed to console. Even if you are running with the `--KEEPSTATS`
flag it is recommended prisonsimulator be run in silent mode, as it will run a little bit faster. Silent mode is
ideal for debugging and for first time runs without the `--KEEPSTATS` flag.

By running with the `--KEEPSTATS` flag, metrics of every prisoners activity each day, along with stats about the
lightswitch will be stored in a self generated sqlite database named `simulations.db`. This file will be generated
in the project root. You can browse this data after the simulation simply by opening the db in an sqlite client of
choice. prisonsimulator though comes with a helpful parser tool called `metrics.py` which will generate some unique
metrics from the simulation.

When the simulation completes, the output will include a simulation id. Assuming you have run the simulation with
the `--KEEPSTATS` flag you can then run `metrics.py` as following:
```bash
python metrics.py -s <simulationid>
```
This will then parse through the `simulations.db` database and read out some useful metrics about the simulation. Remember
you can always do this yourself to get these same metrics or explore on your own using your own sqlite client

## Exploring simulations.db
simulations.db is a simple sqlite3 database which stores a denormalized entry of each prisoner at the end of each day.
This means for every day that is simulated, 100 entries are created! The database has onlya  single table called
`prisoner_stats` containing all data. The column headers and there meanings are as follows:

| Column Name | Description |
| ----------- | ----------- |
| id          | Unique id for the row |
| simulation_id | Unique id of the simulation that just executed. Allows for multiple simulations to occur and be stored in the same database |
| prisoner_id | Unique id of one of the prisoners |
| is_counter | Boolean of either 0 or 1 stating whether the prisoner is currently assigned the counter role |
| prisoner_visit_count | IF the prisoner has the counter role, this is the number of prisoners that have currently been counted |
| has_visited_before | Boolean of either 0 or 1 stating whether the prisoner has visited the room before. Value turns 1 on prisoners first visit and then stays that way for the rest of the simulation |
| day_count | The simulated day that this prisoner stat is for |
| max_prisoners | The maximum number of prisoners |
| declare_all_prisoners_visited | Boolean of either 0 or 1. Set to 1 if the prisoner has determined that all prisoners have visisted the room |
| total_lightswitch_flips | Count of the total number of lightswitch flips that have occured NOT SPECIFIC TO THE PRISONER |
| total_lgithtswitch_flips_on | Count of the total number of lightswitch flips on that have occured NOT SPECIFIC TO THE PRISONER |
| total_lightswitch_flips_off | Count of the total number of lightswitch flips off that have occurred NOT SPECIFIC TO THE PRISONER |
| enter_room_count | Current count of how many times the prisoner has been inside the room |

## Alter The Algorithm
You can alter the algorithm simply by adjusting the `handles_lightswitch` method within the `Prisoner` class.
This method is called everytime a prisoner enters the room, and thus has to make a specific action to the
lightswitch so as to inform or stay informed of the status of all the other prisoners.

Adjusting the `decideWhetherToAnnounce` method will change how the prisoner decides whether all other prisoners
have been in the room. This method is called everytime after `handles_lightswitch` on the same prisoner has
occurred

You can also adjust the number of prisoners by editing the `max_prisoners` variable listed in the `main.py`