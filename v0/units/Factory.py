import battlecode as bc
import enum
import random

random.seed(6137)

directions = list(bc.Direction)

class State(enum.IntEnum):
    Initial = 0

class UnitState:
    def __init__(self, unit):
        self.state = State.Initial

def unit_turn(gc, unit, state):
    garrison = unit.structure_garrison()
    if len(garrison) > 0:
        for d in directions:
            if gc.can_unload(unit.id, d):
                gc.unload(unit.id, d)
                print('Unloaded a unit!')
    elif gc.can_produce_robot(unit.id, bc.UnitType.Ranger):
        gc.produce_robot(unit.id, bc.UnitType.Ranger)
        print('Producing a ranger...')
