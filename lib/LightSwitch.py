

class LightSwitch:

    # true/false reflects the switch being on or off. TRUE = ON, FALSE = OFF
    switch = False

    total_lightswitch_flips = 0
    total_lightswitch_flips_on = 0
    total_lightswitch_flips_off = 0

    def __index__(self, is_on):
        self.switch = is_on

    def isSwitchOn(self):
        return self.switch

    def isSwitchOff(self):
        return not self.switch

    def turnSwitchOn(self):
        self.total_lightswitch_flips += 1
        self.total_lightswitch_flips_on += 1
        self.switch = True

    def turnSwitchOff(self):
        self.total_lightswitch_flips += 1
        self.total_lightswitch_flips_off += 1
        self.switch = False