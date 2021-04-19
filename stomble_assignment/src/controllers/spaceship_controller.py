import mongoengine
from stomble_assignment.src.models.spaceship_model import Spaceship
from stomble_assignment.src.models.location_model import Location
from stomble_assignment.src.controllers import location_controller

# returns all spaceships from db
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

# before this function is invoked, all the params have been validated
def add_new_spaceship(name, model, status, location):
    new_spaceship = Spaceship()
    new_spaceship.name = name
    new_spaceship.model = model
    new_spaceship.status = status
    new_spaceship.location = location
    new_spaceship.save()

    # now add the spaceship to the location
    location_controller.add_spaceship_to_location(str(location.id), new_spaceship.id)
    return new_spaceship

def is_valid_status(status):
    if status in ['operational', 'decommissioned', 'maintenance']:
        return True
    return False

'''
    Functions requiring id
'''

# get spaceship id provided its id
def get_spaceship_by_id(id):
    spaceship = None
    try:
        spaceship = Spaceship.objects.get(id=str(id))
    except:
        return None
    return {
        'id': str(spaceship.id),
        'name': spaceship.name,
        'model': spaceship.model,
        'status': spaceship.status,
        'location': str(spaceship.location.id)
    }

def delete_spaceship_by_id(id):
    spaceship = Spaceship.objects.get(id=str(id))
    location_controller.remove_spaceship(spaceship.location.id, id)
    spaceship.delete()

def update_spaceship_status_by_id(id, status):
    spaceship = Spaceship.objects.get(id=str(id))
    spaceship.update(status=status)
    return spaceship

def is_operational(id):
    res = None
    try:
        res = Spaceship.objects.get(id=str(id)).status == "operational"
    except:
        return False
    return res

def travel_spaceship(spaceship_id, destination_id):
    spaceship = Spaceship.objects.get(id=str(spaceship_id))
    destination = get_location_ref(destination_id)
    current_location = spaceship.location.id
    location_controller.remove_spaceship(current_location, spaceship_id)
    location_controller.add_spaceship_to_location(destination_id, spaceship.id)
    spaceship.update(location=destination)

'''
    Functions accessing location controller
'''

# returns location object provided its id
def get_location_ref(location):
    loc = None 
    try:
        loc = location_controller.get_location_ref_by_id(location)
    except:
        return False
    else:
        return loc

# checks if a location can station more spaceships
def location_has_capacity(location_id):
    return location_controller.check_location_capacity_by_id(location_id)