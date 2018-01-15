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

def unit_turn(gc, unit, state, context):
    location = unit.location
    if location.is_on_map():
        nearby = gc.sense_nearby_units(location.map_location(), 2)
        for other in nearby:
            if other.team != gc.team() and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, other.id):
                print('attacked a thing!')
                gc.attack(unit.id, other.id)

    # okay, there weren't any dudes around
    # pick a random direction:
    d = random.choice(directions)

    # and if that fails, try to move
    if gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
        gc.move_robot(unit.id, d)
