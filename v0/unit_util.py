import battlecode as bc

import factory as f
import knight as k
import worker as w

def get_unit_init_state(unit):
    if unit.unit_type == bc.UnitType.Factory:
        return f.UnitState(unit)
    if unit.unit_type == bc.UnitType.Healer:
        pass
    if unit.unit_type == bc.UnitType.Knight:
        return k.UnitState(unit)
    if unit.unit_type == bc.UnitType.Mage:
        pass
    if unit.unit_type == bc.UnitType.Ranger:
        pass
    if unit.unit_type == bc.UnitType.Rocket:
        pass
    if unit.unit_type == bc.UnitType.Worker:
        return w.UnitState(unit)
    return None

def unit_turn(gc, unit, state):
    begin_turn(gc, unit)
    if unit.unit_type == bc.UnitType.Factory:
        f.unit_turn(gc, unit, state)
    if unit.unit_type == bc.UnitType.Healer:
        pass
    if unit.unit_type == bc.UnitType.Knight:
        k.unit_turn(gc, unit, state)
    if unit.unit_type == bc.UnitType.Mage:
        pass
    if unit.unit_type == bc.UnitType.Ranger:
        pass
    if unit.unit_type == bc.UnitType.Rocket:
        pass
    if unit.unit_type == bc.UnitType.Worker:
        w.unit_turn(gc, unit, state)
    end_turn(gc, unit)

def begin_turn(gc, unit):
    # perform any actions that we want all units to perform at the begining
    return

def end_turn(gc, unit):
    #perform any actions that we want all units to perform at the end
    return
