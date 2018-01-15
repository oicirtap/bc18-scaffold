import battlecode as bc
import enum

""" Template for functions and classes necessary for each unit type
"""


class State(enum.IntEnum):
    Initial = 0


class UnitState:
    def __init__(self, unit):
        self.state = State.Initial

"""
Logic for unit to perform a single game turn based on its current state and context

gc: the GameController
unit: the unit that will perform the turn. The unit must be of the appropriate unit type
state: the current state of the unit
context: game context passed down by the main run.py method
"""
def unit_turn(gc, unit, state, context):
    return
