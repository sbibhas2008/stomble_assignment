import mongoengine
from bson.objectid import ObjectId

class Spaceship(mongoengine.Document):
    id = ObjectId
    name = mongoengine.StringField(require=True)
    model = mongoengine.StringField(required=True)
    status= mongoengine.StringField(required=True, default="operational", choices=['operational', 'decommissioned', 'maintenance'])
    location = mongoengine.ReferenceField("Location", required=True)

    meta = {
        'db_alias': 'core',
        'collection': 'spaceships'
    }

