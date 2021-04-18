import flask
from flask import request
from flask_restplus import Resource, Api, reqparse, fields, Namespace
from api_location_helper import get_all_locations, add_new_location, get_location_by_id, delete_location_by_id, location_has_spaceships
from stomble_assignment.src import setup_db
from bson import json_util
import json

app = flask.Flask(__name__)
api = Api(app)
api = Namespace("Location", path="/")

def parse_json(data):
    return json.loads(json_util.dumps(data))

locations_parser = reqparse.RequestParser()
locations_parser.add_argument('cityName', type=str, help="Name of the city to be added.", required=True, location='headers')
locations_parser.add_argument('planetName', type=str, help="Name of the planet to be added.", required=True, location='headers')
locations_parser.add_argument('spaceportCapacity', type=int, help="Capacity of the spaceport to be added.", required=True, location='headers')

@api.route('/locations', methods=['GET'])
class All_Locations(Resource):
    def get(self):
        all_locations = get_all_locations()
        return {"Message": "Success", 'locations': parse_json(all_locations)}

@api.route('/location', methods=['POST'])
class Add_Location(Resource):
    @api.doc(parser = locations_parser)
    @api.expect(locations_parser)
    def post(self):
        city_name = request.headers.get('cityName')
        planet_name = request.headers.get('planetName')
        spaceport_capacity = request.headers.get('spaceportCapacity')
        location = None
        try:
            location = add_new_location(city_name, planet_name, spaceport_capacity)
        except:
            return {"Message": "Failed! Internal Server Error!"}, 500
        else:
            return {"Message": "Success", 'location': parse_json(str(location.id))}, 200

@api.route('/location/<string:id>', methods=['GET', 'DELETE'])
class Location_Id(Resource):
    def get(self, id):
        location = get_location_by_id(id)
        if location:
            return {"Message": "Success", 'location': parse_json(location)}, 200
        return {"Message": "Not Found"}, 404

    # TODO - confused about what to do if a spaceship is stationed on the location to be removed
    def delete(self, id):
        if not get_location_by_id(id):
            return {"Message": "No location by that id"}, 404
        # TODO - confused about this
        if location_has_spaceships(id):
            return {"Message": "Failed, Location has spaceships stationed"}, 400
        ############################
        try:
            delete_location_by_id(id)
        except:
            return {"Message": "Failed, Internal Server Error"}, 500
        else:
            return {"Message": "Success"}, 200

