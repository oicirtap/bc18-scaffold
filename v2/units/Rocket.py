import battlecode as bc
import enum

""" Template for functions and classes necessary for each unit type
"""


class State(enum.IntEnum):
    Initial = 0


class UnitState:
    def __init__(self, unit):
        self.state = State.Initial
        self.destination = None
        self.force_launch = False
"""
Logic for unit to perform a single game turn based on its current state and context

gc: the GameController
unit: the unit that will perform the turn. The unit must be of the appropriate unit type
state: the current state of the unit
context: game context passed down by the main run.py method
"""
def unit_turn(gc, unit, state):
    if state.force_launch:
        if state.destination is None:
            # TODO: quickly pick a destination in mars given some heuristic
            state.destination = None
        if gc.can_launch_rocket(unit.id, state.destination):
            gc.launch_rocket(unit.id, state.destination)
    if state.destination is None:
        return
    if len(unit.structure_garrison()) != unit.structure_max_capacity():
        return
    other_units = gc.sense_nearby_units_by_team(unit.location.map_location(), 2, gc.team())
    if len(other_units) > 0:
        return
    if gc.can_launch_rocket(unit.id, state.destination):
        gc.launch_rocket(unit.id, state.destination)
