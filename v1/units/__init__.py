import battlecode as bc

import units.Factory as F
import units.Knight as K
import units.Worker as W
import units.Ranger as R


def get_unit_state(unit):
    # Structure state.
    if unit.unit_type == bc.UnitType.Factory:
        return F.UnitState(unit)
    if unit.unit_type == bc.UnitType.Rocket:
        pass

    # Robot state.
    if unit.unit_type == bc.UnitType.Worker:
        return W.UnitState(unit)
    if unit.unit_type == bc.UnitType.Knight:
        return K.UnitState(unit)
    if unit.unit_type == bc.UnitType.Ranger:
        return R.UnitState(unit)
    if unit.unit_type == bc.UnitType.Mage:
        pass
    if unit.unit_type == bc.UnitType.Healer:
        pass

    return None


def run_unit_turn(gc, unit, state, context):
    begin_turn(gc, unit)

    # Structure turn.
    if unit.unit_type == bc.UnitType.Factory:
        F.unit_turn(gc, unit, state, context)
    if unit.unit_type == bc.UnitType.Rocket:
        pass

    # Unit turn.
    if unit.unit_type == bc.UnitType.Worker:
        W.unit_turn(gc, unit, state, context)
    if unit.unit_type == bc.UnitType.Knight:
        K.unit_turn(gc, unit, state, context)
    if unit.unit_type == bc.UnitType.Ranger:
        R.unit_turn(gc, unit, state)
    if unit.unit_type == bc.UnitType.Mage:
        pass
    if unit.unit_type == bc.UnitType.Healer:
        pass

    end_turn(gc, unit)


def begin_turn(gc, unit):
    # Perform any actions that we want all units to perform at the begining.
    return


def end_turn(gc, unit):
    # Perform any actions that we want all units to perform at the end.
    return


