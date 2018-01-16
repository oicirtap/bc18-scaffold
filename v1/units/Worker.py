import battlecode as bc
import enum
import random

random.seed(6137)

directions = list(bc.Direction)

class State(enum.IntEnum):
    Initial = 0
    Idle = 1
    MoveTo = 2
    Wander = 3
    Harvest = 4
    Build = 5
    Repair = 6

class UnitState:
    def __init__(self, unit):
        self.state = State.Idle
        self.location_target = None
        self.build_target = None
        self.harvest_direction = None
        self.next_state = None

def unit_turn(gc, unit, state, context):
    location = unit.location
    if state.state == State.Idle:
        nearby = gc.sense_nearby_units(location.map_location(), 2)
        for other in nearby:
            if gc.can_build(unit.id, other.id):
                state.location_target = other.location.map_location()
                state.build_target = other.id
                state.state = State.Build
                gc.build(unit.id, other.id)
                return
        
        # If not enough workers, build one.
        if context[0].tally[bc.UnitType.Worker] < context[1][bc.UnitType.Worker]:
            for d in directions:
                if gc.can_replicate(unit.id, d):
                    gc.replicate(unit.id, d)
                    print('Replicated!')
        # if not enough factories, make and build a blueprint.
        elif gc.karbonite() > bc.UnitType.Factory.blueprint_cost() and context[0].tally[bc.UnitType.Factory] < context[1][bc.UnitType.Factory]:
            for d in directions:
                if gc.can_blueprint(unit.id, bc.UnitType.Factory, d):
                    print('Bluprinted Factory')
                    gc.blueprint(unit.id, bc.UnitType.Factory, d)
                    state.location_target = unit.location.map_location().add(d)
                    state.state = State.Build
                    return
        # lets look for some karbonite
        else:
            for d in directions:
                if gc.can_harvest(unit.id, d):
                    gc.harvest(unit.id, d)
                    print('Harvested at location ', unit.location.map_location().add(d))
                    state.state = State.Harvest
                    state.harvest_direction = d
                    return
            closest_karbonite = find_karbonite_within(gc, unit.location.map_location(), unit.vision_range)
            if closest_karbonite is not None:
                d = unit.location.map_location().direction_to(closest_karbonite)
                if gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
                    gc.move_robot(unit.id, d)
        # Move at random
        d = random.choice(directions)
        if gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
            gc.move_robot(unit.id, d)

    elif state.state == State.Build:
        if state.build_target == None:
            state.build_target = gc.sense_unit_at_location(state.location_target).id
        if gc.can_build(unit.id, state.build_target):
            gc.build(unit.id, state.build_target)
        else:
            state.location_target = None
            state.build_target = None
            state.state = State.Idle

    elif state.state == State.Harvest:
        if state.harvest_direction is None or not gc.can_harvest(unit.id, state.harvest_direction):
            state.harvest_direction = None
            state.state = State.Idle
            return
        gc.harvest(unit.id, state.harvest_direction)
        print('Harvested at location ', unit.location.map_location().add(state.harvest_direction))

def find_karbonite_within(gc, location, radius_squared):
    locations = gc.all_locations_within(location, radius_squared)
    cosest_karbonite = None
    for l in locations:
        if gc.karbonite_at(l) > 0 and (cosest_karbonite is None or location.distance_squared_to(l) < location.distance_squared_to(cosest_karbonite)):
            cosest_karbonite = l
    return cosest_karbonite
