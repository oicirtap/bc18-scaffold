import battlecode as bc
import enum
import random

import pathfinding

random.seed(6137)

directions = list(bc.Direction)

priority = dict()
priority[bc.UnitType.Ranger] = 1
priority[bc.UnitType.Mage] = 2
priority[bc.UnitType.Knight] = 3
priority[bc.UnitType.Worker] = 4
priority[bc.UnitType.Factory] = 5
priority[bc.UnitType.Rocket] = 6
priority[bc.UnitType.Healer] = 7

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

        self.stuck_counter = 0
        self.help_me = None

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
                move_randomly(gc, unit)
                state.state = State.Explore    
            else:
                if state.path is None:
                    state.calculate_path(map_location)
                if len(state.path) == 0:
                    move_randomly(gc, unit)
                    state.state = State.Explore 
                else:
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
                        move_randomly(gc, unit)
                        state.state = State.Stuck 
        else:
            attack(gc, unit, nearby_enemies)
            state.state = State.Combat

    elif state.state == State.Combat:
        if len(nearby_enemies) == 0 and state.waypoint is not None:
            state.state = State.Waypoint
        elif len(nearby_enemies) == 0 and state.waypoint is None:
            move_randomly(gc, unit)
            state.state = State.Explore
        else:
            attack(gc, unit, nearby_enemies)
            if unit.health < 81:
                run_away(gc, unit, nearby_enemies)

    elif state.state == State.Explore:
        if len(nearby_enemies) == 0:
            move_randomly(gc, unit)
        else:
            attack(gc, unit, nearby_enemies)
            state.state = State.Combat

    elif state.state == State.Stuck:
        if len(nearby_enemies) == 0:
            move_randomly(gc, unit)
            state.stuck_counter += 1
            if state.stuck_counter > 3:
                state.stuck_counter = 0
                state.state = State.Waypoint
        else:
            attack(gc, unit, nearby_enemies)
            state.state = State.Combat

def attack(gc, unit, nearby_enemies):
    if gc.is_attack_ready(unit.id):
        target_enemy = None
        for enemy in nearby_enemies:
            if target_enemy is None or priority[enemy.unit_type] < priority[target_enemy.unit_type] or enemy.health < target_enemy.health:
                target_enemy = enemy
        if gc.can_attack(unit.id, target_enemy.id):
            gc.attack(unit.id, target_enemy.id)
        return target_enemy

def move_randomly(gc, unit):
    if gc.is_move_ready(unit.id):
        random.shuffle(directions)
        for move_dir in directions:
            if gc.can_move(unit.id, move_dir):
                gc.move_robot(unit.id, move_dir)
                break

def run_away(gc, unit, nearby_enemies):
    if gc.is_move_ready(unit.id):
        target_enemy = None
        for enemy in nearby_enemies:
            if target_enemy is None or priority[enemy.unit_type] < priority[target_enemy.unit_type] or enemy.health < target_enemy.health:
                target_enemy = enemy

        run_dir = enemy.location.map_location().direction_to(unit.location.map_location())

        for d in [run_dir, pathfinding.rotate_left[run_dir], pathfinding.rotate_right[run_dir]]:
            if gc.can_move(unit.id, d):
                gc.move_robot(unit.id, d)
                break