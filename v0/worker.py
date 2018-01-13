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
    location = unit.location
    if location.is_on_map():
        nearby = gc.sense_nearby_units(location.map_location(), 2)
        for other in nearby:
            if gc.can_build(unit.id, other.id):
                gc.build(unit.id, other.id)
                print('built a factory!')

    # okay, there weren't any dudes around
    # pick a random direction:
    d = random.choice(directions)

    # or, try to build a factory:
    if gc.karbonite() > bc.UnitType.Factory.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Factory, d):
        gc.blueprint(unit.id, bc.UnitType.Factory, d)
    # and if that fails, try to move
    elif gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
        gc.move_robot(unit.id, d)
