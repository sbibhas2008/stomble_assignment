import mongoengine
from stomble_assignment.src.db_models.spaceship_model import Spaceship
from stomble_assignment.src.db_models.location_model import Location


def get_all_locations():
    locations = Location.objects()
    formatted_locations = []
    for location in locations:
        location_obj = {
            'id': location.id,
            'city_name': location.city_name,
            'planet_name': location.planet_name,
            'spaceport_capacity': location.spaceport_capacity,
            'spaceships': list(map(lambda x : x.id, location.spaceships))
        }
        formatted_locations.append(location_obj)
    print(formatted_locations)
    return formatted_locations
