import flask
from flask_restplus import Resource, Api, reqparse, fields
from api_spaceship_helper import get_all_spaceships
from api_location_helper import get_all_locations
from stomble_assignment.src import setup_db
from bson import json_util
import json

setup_db.global_init()

app = flask.Flask(__name__)
api = Api(app)

def parse_json(data):
    return json.loads(json_util.dumps(data))

@api.route('/locations', methods=['GET'])
class Locations(Resource):
    def get(self):
        locations = get_all_locations()
        return {"Message": "Success"}

@api.route('/spaceships', methods=['GET'])
class Spaceships(Resource):
    def get(self):
        spaceships = get_all_spaceships()
        return {"spaceships":parse_json(spaceships)}, 200

if __name__ == '__main__':
    app.run(debug=True)

