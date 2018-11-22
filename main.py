import random
from lib.Prisoner import Prisoner
from lib.LightSwitch import LightSwitch
from lib.Room import Room
from sql.SQLiteManager import SQLiteManager
import argparse
import logging

# NOTES:
# DAYS START AT 1 (IM SORRY) NOT ZERO (IM SORRY)

logger = logging.getLogger("prisonsimulator")
logger.setLevel(logging.DEBUG)


def generate_prisoners(max_prisoners):
    prisoners = []
    for i in range(0, max_prisoners):
        prisoner = Prisoner(i, max_prisoners)
        prisoners.append(prisoner)

    return prisoners


def start_algorithm(prisoners, room, keep_stats):
    logger.info("Starting Algorithm")
    all_have_visited = False
    day_count = 1
    simulation_id = random.randint(0, (2**60))

    sqlite_manager = None
    if keep_stats:
        sqlite_manager = SQLiteManager()

    logger.info("Starting On Day " + str(day_count))

    while not all_have_visited:

        # choose a random prisoner
        prisoner_index = random.randint(0, 99)
        logger.info("Random Prisoner Of Index: " + str(prisoner_index) + " Was Chosen To Enter The Room")
        prisoner = prisoners[prisoner_index]

        # send them into the room
        prisoner_returned_from_room = room.prisoner_enters_room(prisoner)

        # check if they want to declare anything
        has_accounted = prisoner_returned_from_room.decideWhetherToAnnounce()
        all_have_visited = has_accounted

        prisoners[prisoner_index] = prisoner_returned_from_room

        # increment the day for all prisoners and take a record if enabled

        if keep_stats:
            sqlite_manager.addRecordsForPrisoners(prisoners, simulation_id)

        day_count += 1
        for prisoner in prisoners:
            prisoner.incrementDayCount()

        logger.info("Starting On Day " + str(day_count))

    if keep_stats:
        sqlite_manager.closeEverything()
    return day_count

def is_valid_announcement(prisoners):

    for prisoner in prisoners:
        if not prisoner.has_visited_before:
            return False

    return True


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Prison Simulator')
    parser.add_argument("--KEEPSTATS",
                        help="Include flag to have stats exported to sqlite database. Warning this slows down the simulation alot", action='store_true')
    parser.add_argument("--SILENT",
                       help="Run the simulation in silent mode. Makes it a bit faster. Now output is printed except loading and post simulation", action='store_true')

    args = parser.parse_args()
    keep_stats = args.KEEPSTATS
    silent_mode = args.SILENT

    if not silent_mode:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        logger.addHandler(ch)

    print("Starting Simulator")

    # build all of our structures and data
    max_prisoners = 100

    print("Prisoner Count Set To: " + str(max_prisoners))
    print("Now Genrating Prisoner Objects")
    prisoners = generate_prisoners(max_prisoners)
    print("Prisoners Generated. Building LightSwitch And Room Components")
    # create a lightswitch
    light_switch = LightSwitch()
    # create a room
    room = Room(light_switch)

    print("Now Executing Simulation")
    # start the simulation
    day_count = start_algorithm(prisoners, room, keep_stats)
    print("Simulation Completed. Analyzing Results")

    # check if the results are correct
    if not is_valid_announcement(prisoners):
        print("Announcement Was Wrong. Everyone Is Executed!")
    else:
        print("Accountement Was Right. Everyone Is Free!")

    # dump some stats
    print("It Took " + str(day_count) + " Days Before An Announcement Was Made")



