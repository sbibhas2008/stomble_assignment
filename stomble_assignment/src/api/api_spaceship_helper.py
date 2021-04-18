import mongoengine
from stomble_assignment.src.db_models.spaceship_model import Spaceship
from stomble_assignment.src.db_models.location_model import Location
from api_location_helper import get_location_ref_by_id, add_spaceship_to_location, check_location_capacity_by_id, remove_spaceship

def get_all_spaceships():
    spaceships = Spaceship.objects()
    formatted_spaceships = []
    for spaceship in spaceships:
        spaceship_obj = {
            'id': str(spaceship.id),
            'name': spaceship.name,
            'model': spaceship.model,
            'status': spaceship.status,
            'location': str(spaceship.location.id)
        }
        formatted_spaceships.append(spaceship_obj)
    return formatted_spaceships

def is_valid_status(status):
    if status in ['operational', 'decommissioned', 'maintenance']:
        return True
    return False

def get_location_ref(location):
    return get_location_ref_by_id(location)

# before this function is invoked, all the params have been validated
def add_new_spaceship(name, model, status, location):
    new_spaceship = Spaceship()
    new_spaceship.name = name
    new_spaceship.model = model
    new_spaceship.status = status
    new_spaceship.location = location
    new_spaceship.save()

    # now add the spaceship to the location
    add_spaceship_to_location(str(location), new_spaceship.id)
    return True

def location_has_capacity(location_id):
    return check_location_capacity_by_id(location_id)

def get_spaceship_by_id(id):
    for spaceship in Spaceship.objects:
        if str(spaceship.id) == str(id):
            return {
                'id': str(spaceship.id),
                'name': spaceship.name,
                'model': spaceship.model,
                'status': spaceship.status,
                'location': str(spaceship.location.id)
            }
    return None

def delete_spaceship_by_id(id):
    spaceship_obj = None
    for spaceship in Spaceship.objects:
        if str(spaceship.id) == str(id):
            spaceship_obj = spaceship
            break
    if not spaceship_obj:
        return False 
    remove_spaceship(spaceship_obj.location.id, id)
    spaceship_obj.delete()
    return True

def update_spaceship_status_by_id(id, status):
    for spaceship in Spaceship.objects:
        if str(spaceship.id) == str(id): 
            spaceship.update(status=status)
            return True
    return False


