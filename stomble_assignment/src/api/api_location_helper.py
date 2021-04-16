import mongoengine
from stomble_assignment.src.db_models.spaceship_model import Spaceship
from stomble_assignment.src.db_models.location_model import Location


def get_all_locations():
    locations = Location.objects()
    formatted_locations = []
    for location in locations:
        location_obj = {
            'id': str(location.id),
            'city_name': location.city_name,
            'planet_name': location.planet_name,
            'spaceport_capacity': location.spaceport_capacity,
            'spaceships': list(map(lambda x : x.id, location.spaceships))
        }
        formatted_locations.append(location_obj)
    return formatted_locations

def add_new_location(city_name, planet_name, spaceport_capacity):
    new_location = Location()
    new_location.planet_name = planet_name
    new_location.city_name = city_name
    new_location.spaceport_capacity = spaceport_capacity
    new_location.save()
    return True

def get_location_by_id(oid):
    for location in Location.objects:
        if str(location.id) == str(oid):
            return {
                'id': str(location.id),
                'city_name': location.city_name,
                'planet_name': location.planet_name,
                'spaceport_capacity': location.spaceport_capacity,
                'spaceships': list(map(lambda x : x.id, location.spaceships))
            }
    return None

def delete_location_by_id(oid):
    loc_obj = None
    for location in Location.objects:
        if str(location.id) == str(oid):
            loc_obj = location
            break
    if loc_obj:
        loc_obj.delete()
        return True
    return False

