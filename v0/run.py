import battlecode as bc
import random
import sys
import traceback

import os

import unit_util

print(os.getcwd())

print("pystarting")

# A GameController is the main type that you talk to the game with.
# Its constructor will connect to a running game.
gc = bc.GameController()
directions = list(bc.Direction)

print("pystarted")

# It's a good idea to try to keep your bots deterministic, to make debugging easier.
# determinism isn't required, but it means that the same things will happen in every thing you run,
# aside from turns taking slightly different amounts of time due to noise.
random.seed(6137)

# Initialization -----------------------------------------------------------------------------------
# Everything we want to do before the main game loop

my_team = gc.team()

# get map features -----

earth_map = gc.starting_map(bc.Planet.Earth)
mars_map = gc.starting_map(bc.Planet.Mars)

# map contains the map of the current planet
map = earth_map
if gc.planet() == bc.Planet.Mars:
    map = mars_map

orbit = gc.orbit_pattern()

# map processing -----

# TODO: BFS
#    - Determine map connected components
#    - Locate narrow map sections, if any
#    - Determine distance to enemy

# TODO: Determine optimal landing locations

# TODO: Determine optimal rocket launching turns

# TODO: research tree
gc.queue_research(bc.UnitType.Worker)
gc.queue_research(bc.UnitType.Rocket)
gc.queue_research(bc.UnitType.Knight)

# Unit Setup -----

unit_states = {}

for unit in map.initial_units:
    if unit.unit_type == bc.UnitType.Worker:
        unit_states[unit.id] = unit_util.get_unit_init_state(unit)

# Main Loop ----------------------------------------------------------------------------------------

while True:
    # We only support Python 3, which means brackets around print()
    print('pyround:', gc.round())

    # frequent try/catches are a good idea
    try:
        # walk through our units:
        for unit in gc.my_units():
            if unit.id not in unit_states:
                unit_states[unit.id] = unit_util.get_unit_init_state(unit)
            unit_util.unit_turn(gc, unit, unit_states[unit.id])
        # TODO: cleanup states of units that were eliminated
    except Exception as e:
        print('Error:', e)
        # use this to show where the error was
        traceback.print_exc()

    # send the actions we've performed, and wait for our next turn.
    gc.next_turn()

    # these lines are not strictly necessary, but it helps make the logs make more sense.
    # it forces everything we've written this turn to be written to the manager.
    sys.stdout.flush()
    sys.stderr.flush()
