import mongoengine
from stomble_assignment.src.db_models.spaceship_model import Spaceship
from stomble_assignment.src.db_models.location_model import Location

def get_all_spaceships():
    spaceships = Spaceship.objects()
    formatted_spaceships = []
    for spaceship in spaceships:
        spaceship_obj = {
            'id': str(spaceship.id),
            'name': spaceship.name,
            'model': spaceship.model,
            'status': spaceship.status,
            'location': {
                'city': spaceship.location.city_name,
                'planet': spaceship.location.planet_name
            }
        }
        formatted_spaceships.append(spaceship_obj)
    print(formatted_spaceships)
    return formatted_spaceships
