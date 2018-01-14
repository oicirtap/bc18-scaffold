import battlecode as bc
import enum

""" Template for functions and classes necessary for each unit type
"""


class State(enum.IntEnum):
    Initial = 0


class UnitState:
    def __init__(self, unit):
        self.state = State.Initial


def unit_turn(gc, unit, state):
    return
