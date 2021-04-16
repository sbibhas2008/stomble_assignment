import mongoengine
from bson.objectid import ObjectId


class Location(mongoengine.Document):
    id = ObjectId
    city_name = mongoengine.StringField(require=True)
    planet_name = mongoengine.StringField(require=True)
    spaceport_capacity = mongoengine.IntField(required=True)
    spaceships = mongoengine.ListField(mongoengine.ReferenceField('Spaceship'))

    meta = {
        'db_alias': 'core',
        'collection': 'locations'
    }

