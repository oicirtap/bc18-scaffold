import battlecode as bc

class Tally:
    def __init__(self):
        self.tally = dict()

        self.tally[bc.UnitType.Factory] = 0
        self.tally[bc.UnitType.Rocket] = 0

        self.tally[bc.UnitType.Healer] = 0
        self.tally[bc.UnitType.Knight] = 0
        self.tally[bc.UnitType.Mage] = 0
        self.tally[bc.UnitType.Ranger] = 0
        self.tally[bc.UnitType.Worker] = 0

    def add(self, unit_type):
        self.tally[unit_type] += 1