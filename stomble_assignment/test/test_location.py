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
def test_add_location_invalid_params(supply_url):
    clear_db()
    url = supply_url + "/location"
    req = requests.post(url=url, headers={"cityName": "test"})
    assert req.status_code == 400

# if spaceport capacity is not numeric, request should fail
def test_add_location_invalid_spaceport_capacity(supply_url):
    clear_db()
    url = supply_url + "/location"
    req = requests.post(url=url, headers={"cityName": "test", "planetName": "test-planet", "spaceportCapacity": "abc"})
    assert req.status_code == 400

# if all params are valid, request should succeed  
def test_add_location_success(supply_url):
    clear_db()
    url = supply_url + "/location"
    req = requests.post(url=url, headers={"cityName": "test", "planetName": "test-planet", "spaceportCapacity": "3"})
    assert req.status_code == 200

# if spaceships are stationed on a location, delete should fail
def test_delete_location_not_empty_fail(supply_url):
    clear_db()
    url = supply_url + "/location"
    req = requests.post(url=url, headers={"cityName": "test", "planetName": "test-planet", "spaceportCapacity": "3"})
    assert req.status_code == 200
    # get the new location id
    loc = req.json()
    loc_id = loc['Location']
    # create a new spaceship stationed on the new location 
    url = supply_url + "/spaceship"
    req = requests.post(url=url, headers={"name": "test", "model": "test-model", "status": "operational", "location": loc_id})
    assert req.status_code == 200
    # deleting this location should fail because a spaceship is stationed there
    url = supply_url + "/location/" + loc_id
    req = requests.delete(url=url)
    assert req.status_code == 400
 
def test_delete_invalid_id_fail(supply_url):
    clear_db()
    url = supply_url + "/location/fake_id"
    req = requests.delete(url=url)
    assert req.status_code == 404

def test_delete_location_success(supply_url):
    clear_db()
    # first add a location
    url = supply_url + "/location"
    req = requests.post(url=url, headers={"cityName": "test", "planetName": "test-planet", "spaceportCapacity": "3"})
    assert req.status_code == 200
    # get the new location id
    loc = req.json()
    loc_id = loc['Location']
    #now delete the new location
    url = supply_url + "/location/" + loc_id
    req = requests.delete(url=url)
    assert req.status_code == 200

def test_get_loc_by_id_success(supply_url):
    clear_db()
    # first add a location
    url = supply_url + "/location"
    req = requests.post(url=url, headers={"cityName": "test", "planetName": "test-planet", "spaceportCapacity": "3"})
    assert req.status_code == 200
    # get the new location by id
    loc = req.json()
    loc_id = loc['Location']
    url = supply_url + "/location/" + loc_id
    req = requests.get(url=url)
    assert req.status_code == 200

# if invalid id is supplied, req should fail
def test_get_loc_by_id_fail(supply_url):
    clear_db()
    url = supply_url + "/location/fake_id"
    req = requests.get(url=url)
    assert req.status_code == 404
    


