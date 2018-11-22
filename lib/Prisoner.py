

class Prisoner:

    is_counter = False # whether this person is a designated counter
    prisoner_visit_count = 0  # assuming this person is the counter - this is the counters running total of people who have visited

    has_visited_before = False  # represents andrews logic of being "counted"
    day_count = 1  # local variable of the current day it is
    prisoner_number = -1  # the id number for this particular prisoner - mostly for logging and debugging
    max_prisoners = 0  # parameter specifying how many prisoners total there are

    declare_all_prisoners_visited = False  # override variable for cases where the counter can immediatly determine who visited

    enter_room_count = 0 # how many times this prisoner has entered the room - controlled by room object!

    def __init__(self, prisoner_number, max_prisoners):
        self.prisoner_number = prisoner_number
        self.max_prisoners = max_prisoners

    def setPrisonerIsCounter(self, is_counter):
        self.is_counter = is_counter

    def prisonerIsCounter(self):
        return self.is_counter

    def incrementCount(self):
        self.prisoner_visit_count += 1

    def incrementDayCount(self):
        self.day_count += 1

    def handles_lightswitch(self, light_switch):
        # this is essentially the decision algorithm

        if self.day_count < 100:
            # for day 1 - 99

            if light_switch.isSwitchOn():
                # there are no conditions for this
                pass
            if light_switch.isSwitchOff():
                # switch stays off and you are the counter

                if not self.has_visited_before:
                    # you have not visited before and the light is off
                    self.has_visited_before = True
                else:
                    # you have visited before and the light is off
                    self.is_counter = True
                    light_switch.turnSwitchOn()

                    # set prisoner count to number of days minus 1
                    self.prisoner_visit_count = self.day_count - 1

        elif self.day_count == 100:
            # for day 100

            # if you see the lightswitch off. declare that everyone has been in
            if light_switch.isSwitchOff():
                # on day 100 if the switch is off then everyone has been in
                self.declare_all_prisoners_visited = True

            # if you see the lightswithc on. turn it off
            if light_switch.isSwitchOn():
                light_switch.turnSwitchOff()

        else:
            # for day 101 and beyond
            if light_switch.isSwitchOn():

                # if the lightswitch is on and you are the counter. turn it off and add one to the count
                # of prisoners visited
                if self.is_counter:
                    light_switch.turnSwitchOff()
                    self.prisoner_visit_count += 1

            if light_switch.isSwitchOff():

                if self.has_visited_before:
                    # no handling for this condition
                    pass
                else:
                    # if you are uncounted and you see the lightswitch off. turn the lightswitch on and be counted
                    self.has_visited_before = True
                    light_switch.turnSwitchOn()

    def decideWhetherToAnnounce(self):

        # if this is the counting prisoner and he has reached the max prisoner count - he should say so
        if (self.is_counter and self.prisoner_visit_count >= self.max_prisoners) or self.declare_all_prisoners_visited:
            return True

        return False

