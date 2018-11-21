

class LightSwitch:

    # true/false reflects the switch being on or off. TRUE = ON, FALSE = OFF
    switch = False

    def __index__(self, is_on):
        self.switch = is_on

    def isSwitchOn(self):
        return self.switch

    def isSwitchOff(self):
        return not self.switch

    def turnSwitchOn(self):
        self.switch = True

    def turnSwitchOff(self):
        self.switch = False