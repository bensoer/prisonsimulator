

class Room:

    light_switch = None

    def __init__(self, light_switch):
        self.light_switch = light_switch

    def prisoner_enters_room(self, prisoner):

        prisoner.handles_lightswitch(self.light_switch)
        return prisoner
