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
            'spaceships': list(map(lambda x : str(x.id), location.spaceships))
        }
        formatted_locations.append(location_obj)
    return formatted_locations

def add_new_location(city_name, planet_name, spaceport_capacity):
    new_location = Location()
    new_location.planet_name = planet_name
    new_location.city_name = city_name
    new_location.spaceport_capacity = spaceport_capacity
    new_location.save()
    return new_location

def get_location_by_id(id):
    location = None
    try:
        location = Location.objects().get(id=str(id))
    except:
        return None
    return {
        'id': str(location.id),
        'city_name': location.city_name,
        'planet_name': location.planet_name,
        'spaceport_capacity': location.spaceport_capacity,
        'spaceships': list(map(lambda x : str(x.id), location.spaceships))
    }

def delete_location_by_id(id):
    Location.objects().get(id=str(id)).delete()

def get_location_ref_by_id(location_id):
    location = Location.objects().get(id=str(location_id))
    return location


def check_location_capacity_by_id(location_id):
    location = Location.objects().get(id=str(location_id))
    if len(location.spaceships) < location.spaceport_capacity:
        return True
    return False

def add_spaceship_to_location(location_id, spaceship_id):
    location = Location.objects().get(id=str(location_id))
    all_spaceships = [spaceship for spaceship in location.spaceships]
    all_spaceships.append(spaceship_id)
    location.update(spaceships=all_spaceships)

def remove_spaceship(location_id, spaceship_id):
    location = Location.objects().get(id=str(location_id))
    new_spaceships = [spaceship for spaceship in location.spaceships if str(spaceship.id) != str(spaceship_id)]
    location.update(spaceships=new_spaceships)

def location_has_spaceships(id):
    location = Location.objects().get(id=str(id))
    if len(location.spaceships) > 0:
        return True
    return False