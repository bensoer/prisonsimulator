import random
from Prisoner import Prisoner
from LightSwitch import LightSwitch
from Room import Room

# NOTES:
# DAYS START AT 1 (IM SORRY) NOT ZERO (IM SORRY)

def generate_prisoners(max_prisoners):
    prisoners = []
    for i in range(0, max_prisoners):
        prisoner = Prisoner(i, max_prisoners)
        prisoners.append(prisoner)

    return prisoners


def start_algorithm(prisoners, room):
    print("Starting Algorithm")
    all_have_visited = False
    day_count = 1

    print("Starting On Day " + str(day_count))

    while not all_have_visited:

        # choose a random prisoner
        prisoner_index = random.randint(0, 99)
        print("Random Prisoner Of Index: " + str(prisoner_index) + " Was Chosen To Enter The Room")
        prisoner = prisoners[prisoner_index]

        # send them into the room
        prisoner_returned_from_room = room.prisoner_enters_room(prisoner)

        # check if they want to declare anything
        has_accounted = prisoner_returned_from_room.decideWhetherToAnnounce()
        all_have_visited = has_accounted

        prisoners[prisoner_index] = prisoner_returned_from_room

        # increment the day for all prisoners
        day_count += 1
        for prisoner in prisoners:
            prisoner.incrementDayCount()

        print("Starting On Day " + str(day_count))

    return day_count

def is_valid_announcement(prisoners):

    for prisoner in prisoners:
        if not prisoner.has_visited_before:
            return False

    return True


if __name__ == '__main__':
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
    day_count = start_algorithm(prisoners, room)
    print("Simulation Completed. Analyzing Results")

    # check if the results are correct
    if not is_valid_announcement(prisoners):
        print("Announcement Was Wrong. Everyone Is Executed!")
    else:
        print("Accountement Was Right. Everyone Is Free!")

    # dump some stats
    print("It Took " + str(day_count) + " Days Before An Announcement Was Made")



