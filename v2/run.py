import battlecode as bc
import numpy as np

import traceback
import random
import sys

import units
import strategies

from util import Tally

#==============================================================================#
#                              INITIALIZATION                                  #
#==============================================================================#
# A GameController is the main type to talk to the game.
gc = bc.GameController()
random.seed(6137)

# Get team.
my_team = gc.team()
for team in list(bc.Team):
    if team != my_team:
        enemy_team = team

# Direction list
directions = list(bc.Direction)

# Timing setup
previous_time_left = gc.get_time_left_ms()
current_time_left = gc.get_time_left_ms()

#==============================================================================#
#                                    MAP                                       #
#==============================================================================#
# Get feature map.

earth_map = gc.starting_map(bc.Planet.Earth)
mars_map = gc.starting_map(bc.Planet.Mars)

earth_grid = np.zeros((earth_map.height, earth_map.width))
mars_grid = np.zeros((earth_map.height, earth_map.width))

earth_mining_locations = list()
mars_mining_locations = list()

for y in range(earth_map.height):
    for x in range(earth_map.width):
        loc = bc.MapLocation(bc.Planet.Earth, x, y) 
        if earth_map.on_map(loc):
            if earth_map.is_passable_terrain_at(loc):
                karbonite_value = earth_map.initial_karbonite_at(loc)
                earth_grid[y][x] = karbonite_value
                if karbonite_value > 5:
                    earth_mining_locations.append(loc)
            else:
                earth_grid[y][x] = -1
        else:
            earth_grid[y][x] = -1

for y in range(mars_map.height):
    for x in range(mars_map.width):
        loc = bc.MapLocation(bc.Planet.Mars, x, y) 
        if mars_map.on_map(loc):
            if mars_map.is_passable_terrain_at(loc):
                karbonite_value = mars_map.initial_karbonite_at(loc)
                mars_grid[y][x] = karbonite_value
                if karbonite_value > 5:
                    mars_mining_locations.append(loc)
            else:
                mars_grid[y][x] = -1
        else:
            mars_grid[y][x] = -1

def print_grid(grid):
    print(np.array2string(grid, formatter={'float_kind':'{0:2.0f}'.format}))

# Map, grid, and interesting locations
map = earth_map if gc.planet() == bc.Planet.Earth else mars_map
grid = earth_grid if gc.planet() == bc.Planet.Earth else mars_grid
mining_locations = earth_mining_locations if gc.planet() == bc.Planet.Earth else mars_mining_locations
attack_locations = list()
for unit in map.initial_units:
    if unit.team != my_team:
        attack_locations.append(unit.location.map_location())

# map processing -----

# TODO: BFS
#    - Determine map connected components
#    - Locate narrow map sections, if any
#    - Determine map symmetry type (verticle, horizontal, rotational)
#    - Determine distance to enemy (symmetrical counter_part)

# TODO: Determine optimal mining spot
# TODO: Determine optimal landing locations

#==============================================================================#
#                                   SPACE                                      #
#==============================================================================#
# Get orbit pattern.
orbit = gc.orbit_pattern()

# TODO: Determine optimal rocket launching turns

#==============================================================================#
#                                  RESEARCH                                    #
#==============================================================================#
# TODO: research tree
gc.queue_research(bc.UnitType.Worker)
gc.queue_research(bc.UnitType.Ranger)
gc.queue_research(bc.UnitType.Ranger)
gc.queue_research(bc.UnitType.Ranger)


#==============================================================================#
#                                UNIT SETUP                                    #
#==============================================================================#
prev_tally = None
current_tally = None

unit_cap = {
    bc.UnitType.Factory : 10,
    bc.UnitType.Healer : 0,
    bc.UnitType.Knight : 50,
    bc.UnitType.Mage : 0,
    bc.UnitType.Ranger : 75,
    bc.UnitType.Rocket : 2,
    bc.UnitType.Worker : 15
}

unit_states = {}

for unit in map.initial_units:
    if unit.team == my_team:
        unit_states[unit.id] = units.get_unit_state(unit)

# TODO: cleanup states of units that were eliminated

#==============================================================================#
#                          EARLY_GAME_BUILD_ORDER                              #
#==============================================================================#
first_worker = None
first_worker_build_quadrant = None
first_worker_factory_dir = None

second_worker = None
second_worker_dir = None
second_worker_factory_dir = None

third_worker = None
third_worker_dir = None
third_worker_factory_dir = None

first_factory_blueprint = None

# TODO: find out better way to pick seed worker (farthest from enemy, most free)
for unit in map.initial_units:
    if unit.team == my_team:
        if gc.can_move(unit.id, bc.Direction.North) and gc.can_move(unit.id, bc.Direction.Northeast) and gc.can_move(unit.id, bc.Direction.East):
            first_worker = unit
            first_worker_build_quadrant = 1
            # Worker dir
            second_worker_dir = bc.Direction.North
            third_worker_dir = bc.Direction.East
            # Factory dir
            first_worker_factory_dir = bc.Direction.East
            second_worker_factory_dir = bc.Direction.Southwest
            third_worker_factory_dir = bc.Direction.South
            break
        elif gc.can_move(unit.id, bc.Direction.North) and gc.can_move(unit.id, bc.Direction.Northwest) and gc.can_move(unit.id, bc.Direction.West):
            first_worker = unit
            first_worker_build_quadrant = 2
            # Worker dir
            second_worker_dir = bc.Direction.North
            third_worker_dir = bc.Direction.West
            # Factory dir
            first_worker_factory_dir = bc.Direction.West
            second_worker_factory_dir = bc.Direction.Southwest
            third_worker_factory_dir = bc.Direction.South
            break
        elif gc.can_move(unit.id, bc.Direction.South) and gc.can_move(unit.id, bc.Direction.Southwest) and gc.can_move(unit.id, bc.Direction.West):
            first_worker = unit
            first_worker_build_quadrant = 3
            # Worker dir
            second_worker_dir = bc.Direction.South
            third_worker_dir = bc.Direction.West
            # Factory dir
            first_worker_factory_dir = bc.Direction.West
            second_worker_factory_dir = bc.Direction.Northwest
            third_worker_factory_dir = bc.Direction.North
            break
        elif gc.can_move(unit.id, bc.Direction.South) and gc.can_move(unit.id, bc.Direction.Southeast) and gc.can_move(unit.id, bc.Direction.East):
            first_worker = unit
            first_worker_build_quadrant = 4
            # Worker dir
            second_worker_dir = bc.Direction.South
            third_worker_dir = bc.Direction.East
            # Factory dir
            first_worker_factory_dir = bc.Direction.East
            second_worker_factory_dir = bc.Direction.Northwest
            third_worker_factory_dir = bc.Direction.North
            break

#TODO: recheck this code block to make sure nothing breaks and generalize acrosses map
EARLY_GAME_ROUND_COUNT = 5
print("STARTING EARLY GAME")
while gc.round() <= EARLY_GAME_ROUND_COUNT:
    print('EARLY ROUND:', gc.round())

    current_round = gc.round()
    my_units = gc.my_units()

    prev_tally = current_tally
    current_tally = Tally()

    try:
        if gc.planet() == bc.Planet.Earth:
            if current_round == 1:
                if first_worker is not None:
                    gc.replicate(first_worker.id, second_worker_dir)
                else:
                    gc.Error("No First Worker")
            elif current_round == 2:
                second_worker = gc.sense_unit_at_location(first_worker.location.map_location().add(second_worker_dir))
                gc.replicate(second_worker.id, third_worker_dir)
            elif current_round == 3:
                third_worker = gc.sense_unit_at_location(second_worker.location.map_location().add(third_worker_dir))
            elif current_round == 4:
                pass
            elif current_round == 5:
                gc.blueprint(first_worker.id, bc.UnitType.Factory,first_worker_factory_dir)
    except Exception as e:
        print('Error:', e)
        traceback.print_exc()

    # Send the actions we've performed, and wait for our next turn.
    gc.next_turn()
current_time_left = gc.get_time_left_ms()
print('ENDING EARLY GAME: {:d}ms elapsed, {:d}ms left'.format(current_time_left - previous_time_left, current_time_left))
print("*"*50)

#==============================================================================#
#                               CALL FOR HELP                                  #
#==============================================================================#
help_locations = list()

#==============================================================================#
#                                   MAIN LOOP                                  #
#==============================================================================#
while True:
    print('STARTING ROUND:', gc.round())

    previous_time_left = current_time_left
    current_round = gc.round()
    my_units = gc.my_units()

    # Tally
    tally = Tally()
    for unit in gc.units():
        if not unit.location.is_on_map() or not unit.location.is_on_planet(gc.planet()):
            continue
        if unit.team == gc.team():
            tally.add(unit.unit_type)
        else:
            # process enemy units we can see
            pass
            
    prev_tally = current_tally
    current_tally = Tally()

    try:
        if gc.planet() == bc.Planet.Earth:
            # determine if we want to build anything this round.
            factories_to_build = unit_cap[bc.UnitType.Factory] - tally.tally[bc.UnitType.Factory]
            workers_to_replicate = unit_cap[bc.UnitType.Worker] - tally.tally[bc.UnitType.Worker]
            rockets_to_build = unit_cap[bc.UnitType.Rocket] - tally.tally[bc.UnitType.Rocket]

            for unit in my_units:
                # Don't bother with unit not on map or in garrison
                if not unit.location.is_on_map():
                    continue

                if unit.id not in unit_states:
                    unit_states[unit.id] = units.get_unit_state(unit)
                state = unit_states[unit.id]

                # Commanding: setting unit state
                if unit.unit_type == bc.UnitType.Ranger:
                    if state.grid is None:
                        state.set_grid(grid)
                    if state.state == units.Ranger.State.Initial:
                        attack_loc = None
                        bot_loc = unit.location.map_location()
                        for loc in attack_locations:
                            if attack_loc is None or bot_loc.distance_squared_to(loc) < bot_loc.distance_squared_to(attack_loc):
                                attack_loc = loc
                        state.set_waypoint(attack_loc)
                if unit.unit_type == bc.UnitType.Worker:
                    if workers_to_replicate > 0:
                        state.replicate = True
                    if factories_to_build > 0:
                        state.blueprint_f = True
                    if rockets_to_build > 0:
                        state.blueprint_r = True

                units.run_unit_turn(gc, unit, unit_states[unit.id])

                if unit.unit_type == bc.UnitType.Worker:
                    if state.replicate:
                        state.replicate = False
                        if state.replicated:
                            workers_to_replicate -= 1
                            state.replicated = False
                    if state.blueprint_f:
                        state.blueprint_f = False
                        if state.blueprinted_f:
                            factories_to_build -= 1
                            state.blueprinted_f = False
                    if state.blueprint_r:
                        state.blueprint_r = False
                        if state.blueprinted_r:
                            rockets_to_build -= 1
                            state.blueprinted_r = False
    except Exception as e:
        print('Error:', e)
        gc.Error()
        traceback.print_exc()

    # Send the actions we've performed, and wait for our next turn.
    gc.next_turn()
    current_time_left = gc.get_time_left_ms()
    print('ENDING ROUND: {:d}ms elapsed, {:d}ms left'.format(previous_time_left - current_time_left, current_time_left))
    print("*"*50)

