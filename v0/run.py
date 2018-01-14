import battlecode as bc
import random, time, sys, traceback

from util import Tally
from units.util import get_unit_state, run_unit_turn


# A GameController is the main type to talk to the game.
gc = bc.GameController()
random.seed(6137)

#==============================================================================#
#                              INITIALIZATION                                  #
#               Everything we want to do before the main game loop             #
#==============================================================================#

# Get team.
my_team = gc.team()

# Get feature map.
earth_map = gc.starting_map(bc.Planet.Earth)
mars_map = gc.starting_map(bc.Planet.Mars)

# Set "map" to be the map of the current planet.
map = earth_map
if gc.planet() == bc.Planet.Mars:
    map = mars_map

# Get orbit pattern.
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
current_tally = Tally()
tally = Tally()

unit_states = {}

for unit in map.initial_units:
    if unit.unit_type == bc.UnitType.Worker:
        unit_states[unit.id] = get_unit_state(unit)

#==============================================================================#
#                                   MAIN LOOP                                  #
#==============================================================================#
while True:
    print('ROUND:', gc.round())
    start_time = time.clock()

    tally = current_tally
    current_tally = Tally()
    try:
        if gc.round() < 20:
            pass
        else:
            for unit in gc.my_units():
                # update tally
                current_tally.add(unit.unit_type)
                if unit.id not in unit_states:
                    unit_states[unit.id] = get_unit_state(unit)
                run_unit_turn(gc, unit, unit_states[unit.id])
        # TODO: cleanup states of units that were eliminated




    except Exception as e:
        print('Error:', e)
        traceback.print_exc()

    # Send the actions we've performed, and wait for our next turn.
    gc.next_turn()
    print('======== {:.3f}ms ========'.format((time.clock() - start_time)*1000.0))

