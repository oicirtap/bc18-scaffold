import battlecode as bc
import enum
import random

import pathfinding

random.seed(6137)

directions = list(bc.Direction)

class State(enum.IntEnum):
    Initial = 0
    Waypoint = 1
    Combat = 2
    Explore = 3
    Stuck = 4

class UnitState:
    def __init__(self, unit):
        self.state = State.Initial
        self.grid = None

        self.waypoint = None
        self.path = None
        self.path_length = 0
        self.stuck_counter = 0

    def set_grid(self, grid):
        self.grid = pathfinding.Grid(grid)

    def set_waypoint(self, goal_loc):
        self.waypoint = goal_loc
        self.state = State.Waypoint

    def calculate_path(self, starting_loc):
        if self.waypoint is not None:
            self.path = pathfinding.fuzzy_a_star(self.grid, (starting_loc.x, starting_loc.y), (self.waypoint.x, self.waypoint.y))

def unit_turn(gc, unit, state):
    map_location = unit.location.map_location()

    my_team = gc.team()
    enemy_team = bc.Team.Blue if my_team == bc.Team.Red else bc.Team.Red

    nearby_friends = gc.sense_nearby_units_by_team(map_location, 50, my_team)
    nearby_enemies = gc.sense_nearby_units_by_team(map_location, 50, enemy_team)

    if state.state == State.Waypoint:
        if len(nearby_enemies) == 0:
            if state.waypoint is None or map_location.distance_squared_to(state.waypoint) < 50:
                state.path = None
                state.waypoint = None
                if gc.is_move_ready(unit.id):
                    move_randomly(gc, unit)
                state.state = State.Explore    
            else:
                if state.path is None:
                    state.calculate_path(map_location)
                if len(state.path) > 0:
                    move_loc = bc.MapLocation(map_location.planet, state.path[-1][0], state.path[-1][1])
                    move_dir = map_location.direction_to(move_loc)
                    if gc.is_move_ready(unit.id) and gc.can_move(unit.id, move_dir):
                        gc.move_robot(unit.id, move_dir)
                        state.path.pop()
                        state.stuck_counter = 0
                    else:
                        state.stuck_counter += 1

                    if state.stuck_counter > 5:
                        state.stuck_counter = 0
                        state.path = None
                        if gc.is_move_ready(unit.id):
                            move_randomly(gc, unit)
                        state.state = State.Stuck       
        else:
            if gc.is_attack_ready(unit.id):
                attack(gc, unit, nearby_enemies)
            state.state = State.Combat

    elif state.state == State.Combat:
        if len(nearby_enemies) == 0 and state.waypoint is not None:
            state.state = State.Waypoint
        elif len(nearby_enemies) == 0 and state.waypoint is None:
            if gc.is_move_ready(unit.id):
                move_randomly(gc, unit)
            state.state = State.Explore
        else:
            if gc.is_attack_ready(unit.id):
                attack(gc, unit, nearby_enemies)

    elif state.state == State.Explore:
        if len(nearby_enemies) == 0:
            if gc.is_move_ready(unit.id):
                move_randomly(gc, unit)
        else:
            if gc.is_attack_ready(unit.id):
                attack(gc, unit, nearby_enemies)
            state.state = State.Combat

    elif state.state == State.Stuck:
        if len(nearby_enemies) == 0:
            if gc.is_move_ready(unit.id):
                move_randomly(gc, unit)
            state.stuck_counter += 1
            if state.stuck_counter > 3:
                state.stuck_counter = 0
                state = State.Waypoint
        else:
            if gc.is_attack_ready(unit.id):
                attack(gc, unit, nearby_enemies)
            state.state = State.Combat

def attack_enemy(gc, unit, enemy):
    if gc.can_attack(unit.id, enemy.id):
        gc.attack(unit.id, enemy.id)

def attack(gc, unit, nearby_enemies):
    lowest_health_enemy = nearby_enemies[0]
    for enemy in nearby_enemies:
        if enemy.health < lowest_health_enemy.health:
            lowest_health_enemy = enemy
    if gc.can_attack(unit.id, lowest_health_enemy.id):
        gc.attack(unit.id, lowest_health_enemy.id)
    return lowest_health_enemy

def move_randomly(gc, unit):
    random.shuffle(directions)
    for move_dir in directions:
        if gc.can_move(unit.id, move_dir):
            gc.move_robot(unit.id, move_dir)
            break

def move_towards(gc, unit, other):
    unit_loc = unit.location.map_location()
    other_loc = other.location.map_location()
    d = unit_loc.direction_to(other_loc)
    for move_dir in [d, pathfinding.rotate_right[d], pathfinding.rotate_left[d]]:
        if gc.can_move(unit.id, move_dir):
            gc.move_robot(unit.id, move_dir)
            return
    move_randomly(gc, unit)
