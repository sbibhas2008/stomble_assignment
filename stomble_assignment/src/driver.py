from stomble_assignment.src.db_models import location_model, spaceship_model
from stomble_assignment.src import setup_db

setup_db.global_init()

location = location_model.Location()
location.planet_name = "Mars"
location.city_name = "Mars-123"
location.spaceport_capacity = 3
location.save()
print(location.id)
print("Success!")

spaceship = spaceship_model.Spaceship()
spaceship.name = "Apollo-11"
spaceship.model = "11"
spaceship.status = "operational"
spaceship.location = location
spaceship.save()
print(spaceship.id)
print("success!")