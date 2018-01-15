import battlecode as bc
import enum
import random

import pathfinding

random.seed(6137)

directions = list(bc.Direction)

class State(enum.IntEnum):
    Initial = 0

class UnitState:
    def __init__(self, unit):
        self.state = State.Initial
        self.loc = None
        self.grid = None

        self.waypoint = None
        self.path = None

    def set_grid(self, grid):
        self.grid = pathfinding.Grid(grid)

    def set_waypoint(self, goal):
        self.waypoint = goal
        self.path = pathfinding.a_star(self.grid, (self.loc.x, self.loc.y), (self.waypoint.x, self.waypoint.y))

def unit_turn(gc, unit, state):
    location = unit.location
    if location.is_on_map():
        map_location = location.map_location()
        nearby = gc.sense_nearby_units(map_location, 70)
        for other in nearby:
            if other.team != gc.team() and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, other.id):
                print('attacked a thing!')
                gc.attack(unit.id, other.id)

            if state.waypoint is None or map_location.distance_squared_to(state.waypoint) < 50:
                random.shuffle(directions)
                for d in directions:
                    if gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
                        gc.move_robot(unit.id, d)
                        state.loc = map_location.add(d)
            elif state.path is not None and len(state.path) > 0:
                new_loc = bc.MapLocation(map_location.planet, state.path[0][0], state.path[0][1])
                d = map_location.direction_to(new_loc)
                if gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
                    gc.move_robot(unit.id, d)
                    state.loc = new_loc
                    state.path = state.path[1:]