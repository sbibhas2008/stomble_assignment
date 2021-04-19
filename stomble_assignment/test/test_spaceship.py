import pytest
import requests
import json
from stomble_assignment.src import setup_db
from stomble_assignment.src.models import location_model, spaceship_model

setup_db.global_init()

def clear_db():
    location_model.Location.objects.delete()
    spaceship_model.Spaceship.objects.delete()

@pytest.fixture
def supply_url():
	return "http://localhost:5000"

'''
    Tests
'''

# if all parameters not supplied, request should fail
def test_add_shapceship_invalid_params(supply_url):
    clear_db()
    url = supply_url + "/spaceship"
    req = requests.post(url=url, headers={"name": "test"})
    assert req.status_code == 400

# if status is not valid, req should fail
def test_add_spaceship_invalid_status(supply_url):
    clear_db()
    url = supply_url + "/location"
    req = requests.post(url=url, headers={"cityName": "test", "planetName": "test-planet", "spaceportCapacity": "3"})
    assert req.status_code == 200
    # get the new location id
    loc = req.json()
    loc_id = loc['Location']
    url = supply_url + "/spaceship"
    req = requests.post(url=url, headers={"name": "test", "model": "test-model", "status": "invalid-status", "location": loc_id})
    assert req.status_code == 400

# if invalid location is supplied, req should fail
def test_add_spaceship_invalid_loc(supply_url):
    clear_db()
    url = supply_url + "/spaceship"
    req = requests.post(url=url, headers={"name": "test", "model": "test-model", "status": "operational", "location": "fake_loc"})
    assert req.status_code == 400

# if location's spaceport capacity has reached its limit, req should fail
def test_add_spaceship_location_full(supply_url):
    clear_db()
    url = supply_url + "/location"
    req = requests.post(url=url, headers={"cityName": "test", "planetName": "test-planet", "spaceportCapacity": "1"})
    assert req.status_code == 200
    # get the new location id
    loc = req.json()
    loc_id = loc['Location']
    #add 1 spaceship
    url = supply_url + "/spaceship"
    req = requests.post(url=url, headers={"name": "test", "model": "test-model", "status": "operational", "location": loc_id})
    assert req.status_code == 200
    # adding another spaceship should fail since the location can only station 1 spaceship
    req = requests.post(url=url, headers={"name": "test-1", "model": "test-model-1", "status": "operational", "location": loc_id})
    assert req.status_code == 400

def test_add_get_spaceship_success(supply_url):
    clear_db()
    url = supply_url + "/location"
    req = requests.post(url=url, headers={"cityName": "test", "planetName": "test-planet", "spaceportCapacity": "1"})
    assert req.status_code == 200
    # get the new location id
    loc = req.json()
    loc_id = loc['Location']
    #add 1 spaceship
    url = supply_url + "/spaceship"
    req = requests.post(url=url, headers={"name": "test", "model": "test-model", "status": "operational", "location": loc_id})
    assert req.status_code == 200
    '''
        Test get spaceship by id success
    '''
    spaceship_id = req.json()['Spaceship']
    url = supply_url + "/spaceship/" + spaceship_id
    req = requests.get(url=url)
    assert req.status_code == 200
    assert req.json()['Spaceship']['location'] == loc_id

    # The location should also have spaceship id stored
    url = supply_url + "/location/" + loc_id
    req = requests.get(url=url)
    assert req.status_code == 200
    assert spaceship_id in req.json()['Location']['spaceships']

# if id is not valid, request should fail
def test_get_spaceship_by_id_fail(supply_url):
    clear_db()
    url = supply_url + "/spaceship/invalid-id"
    req = requests.get(url=url)
    assert req.status_code == 404

# if id is not valid, req should fail
def test_delete_spaceship_fail(supply_url):
    clear_db()
    url = supply_url + "/spaceship/invalid-id"
    req = requests.delete(url=url)
    assert req.status_code == 404

def test_delete_spaceship_success(supply_url):
    clear_db()
    # add a location
    url = supply_url + "/location"
    req = requests.post(url=url, headers={"cityName": "test", "planetName": "test-planet", "spaceportCapacity": "1"})
    assert req.status_code == 200
    # get the new location id
    loc = req.json()
    loc_id = loc['Location']
    # add spaceship to that location
    url = supply_url + "/spaceship"
    req = requests.post(url=url, headers={"name": "test", "model": "test-model", "status": "operational", "location": loc_id})
    assert req.status_code == 200
    spaceship_id = req.json()['Spaceship']
    # delete the spaceship
    url = supply_url + "/spaceship/" + spaceship_id
    req = requests.delete(url=url)
    assert req.status_code == 200
    # deleted spaceship should not longer be stationed in the location
    url = supply_url + "/location/" + loc_id
    req = requests.get(url=url)
    assert req.status_code == 200
    assert spaceship_id not in req.json()['Location']['spaceships']

# if id is not valid, req should fail
def test_update_status_invalid_id_fail(supply_url):
    clear_db()
    url = supply_url + "/spaceship/invalid-id"
    req = requests.put(url=url)
    assert req.status_code == 404

# if invalid status is supplied, request should fail
def test_update_status_invalid_status_fail(supply_url):
    clear_db()
    # add a location
    url = supply_url + "/location"
    req = requests.post(url=url, headers={"cityName": "test", "planetName": "test-planet", "spaceportCapacity": "1"})
    assert req.status_code == 200
    # get the new location id
    loc = req.json()
    loc_id = loc['Location']
    # add spaceship to that location
    url = supply_url + "/spaceship"
    req = requests.post(url=url, headers={"name": "test", "model": "test-model", "status": "operational", "location": loc_id})
    assert req.status_code == 200
    spaceship_id = req.json()['Spaceship']
    # update status
    url = supply_url + "/spaceship/" + spaceship_id
    req = requests.put(url=url, headers={"status": "invalid-status"})
    assert req.status_code == 400

def update_status_success(supply_url):
    clear_db()
    # add a location
    url = supply_url + "/location"
    req = requests.post(url=url, headers={"cityName": "test", "planetName": "test-planet", "spaceportCapacity": "1"})
    assert req.status_code == 200
    # get the new location id
    loc = req.json()
    loc_id = loc['Location']
    # add spaceship to that location
    url = supply_url + "/spaceship"
    req = requests.post(url=url, headers={"name": "test", "model": "test-model", "status": "operational", "location": loc_id})
    assert req.status_code == 200
    spaceship_id = req.json()['Spaceship']
    # update status
    url = supply_url + "/spaceship/" + spaceship_id
    req = requests.put(url=url, headers={"status": "maintenance"})
    assert req.status_code == 200

# if invalid params are supplied, req should fail
def test_travel_invalid_params_fail(supply_url):
    clear_db()
    url = supply_url + "/spaceship/travel"
    req = requests.patch(url=url, headers={"spaceship_id": "invalid_spaceship", "destination_id": "invalid"})
    assert req.status_code == 404

# if destination spaceport capacity has reached the limit, req should fail   
def test_travel_dest_capacity_reached_fail(supply_url):
    clear_db()
    url = supply_url + "/location"
    req = requests.post(url=url, headers={"cityName": "test", "planetName": "test-planet", "spaceportCapacity": "3"})
    assert req.status_code == 200
    # get the new location id
    loc = req.json()
    loc_id_1 = loc['Location']
    # create a new spaceship stationed on the new location 
    url = supply_url + "/spaceship"
    req = requests.post(url=url, headers={"name": "test", "model": "test-model", "status": "operational", "location": loc_id_1})
    assert req.status_code == 200
    spaceship_id_1 = req.json()['Spaceship']
    # create another location
    url = supply_url + "/location"
    req = requests.post(url=url, headers={"cityName": "test-1", "planetName": "test-planet-1", "spaceportCapacity": "1"})
    assert req.status_code == 200
    # get the new location id
    loc = req.json()
    loc_id_2 = loc['Location']
    # create a new spaceship stationed on the new location 
    url = supply_url + "/spaceship"
    req = requests.post(url=url, headers={"name": "test-1", "model": "test-model-1", "status": "operational", "location": loc_id_2})
    assert req.status_code == 200
    spaceship_id_2 = req.json()['Spaceship']
    # now travel the first spaceship to second destination
    url = supply_url + "/spaceship/travel"
    req = requests.patch(url=url, headers={"spaceship_id": spaceship_id_1, "destination_id": loc_id_2})
    assert req.status_code == 400

# if spaceship status is not operational, req should fail
def test_travel_only_operational_can_travel(supply_url):
    clear_db()
    url = supply_url + "/location"
    req = requests.post(url=url, headers={"cityName": "test", "planetName": "test-planet", "spaceportCapacity": "3"})
    assert req.status_code == 200
    # get the new location id
    loc = req.json()
    loc_id_1 = loc['Location']
    # create a new spaceship stationed on the new location 
    url = supply_url + "/spaceship"
    req = requests.post(url=url, headers={"name": "test", "model": "test-model", "status": "maintenance", "location": loc_id_1})
    assert req.status_code == 200
    spaceship_id_1 = req.json()['Spaceship']
    # create another location
    url = supply_url + "/location"
    req = requests.post(url=url, headers={"cityName": "test-1", "planetName": "test-planet-1", "spaceportCapacity": "1"})
    assert req.status_code == 200
    # get the new location id
    loc = req.json()
    loc_id_2 = loc['Location']
    # now travel the first spaceship to second destination
    url = supply_url + "/spaceship/travel"
    req = requests.patch(url=url, headers={"spaceship_id": spaceship_id_1, "destination_id": loc_id_2})
    assert req.status_code == 400

def test_travel_success(supply_url):
    clear_db()
    url = supply_url + "/location"
    req = requests.post(url=url, headers={"cityName": "test", "planetName": "test-planet", "spaceportCapacity": "3"})
    assert req.status_code == 200
    # get the new location id
    loc = req.json()
    loc_id_1 = loc['Location']
    # create a new spaceship stationed on the new location 
    url = supply_url + "/spaceship"
    req = requests.post(url=url, headers={"name": "test", "model": "test-model", "status": "operational", "location": loc_id_1})
    assert req.status_code == 200
    spaceship_id_1 = req.json()['Spaceship']
    # create another location
    url = supply_url + "/location"
    req = requests.post(url=url, headers={"cityName": "test-1", "planetName": "test-planet-1", "spaceportCapacity": "1"})
    assert req.status_code == 200
    # get the new location id
    loc = req.json()
    loc_id_2 = loc['Location']
    # now travel the first spaceship to second destination
    url = supply_url + "/spaceship/travel"
    req = requests.patch(url=url, headers={"spaceship_id": spaceship_id_1, "destination_id": loc_id_2})
    assert req.status_code == 200
    # spaceship 1 should no longer be stationed in location 1
    url = supply_url + "/location/" + loc_id_1
    req = requests.get(url=url)
    assert req.status_code == 200
    assert spaceship_id_1 not in req.json()['Location']['spaceships']
    # spaceship's location should be changed to destination after travelling
    url = supply_url + "/spaceship/" + spaceship_id_1
    req = requests.get(url=url)
    assert req.status_code == 200
    assert req.json()['Spaceship']['location'] != loc_id_1
    assert req.json()['Spaceship']['location'] == loc_id_2
    # destination location should have the spaceship stationed after travelling
    url = supply_url + "/location/" + loc_id_2
    req = requests.get(url=url)
    assert req.status_code == 200
    assert spaceship_id_1 in req.json()['Location']['spaceships']


   