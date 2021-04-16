import flask
from flask import request
from flask_restplus import Resource, Api, reqparse, fields, Namespace
from api_location_helper import get_all_locations, add_new_location
from stomble_assignment.src import setup_db
from bson import json_util
import json

app = flask.Flask(__name__)
api = Api(app)
api = Namespace("Location")

def parse_json(data):
    return json.loads(json_util.dumps(data))

locations_parser = reqparse.RequestParser()
locations_parser.add_argument('cityName', type=str, help="Name of the city to be added.", required=True, location='headers')
locations_parser.add_argument('planetName', type=str, help="Name of the planet to be added.", required=True, location='headers')
locations_parser.add_argument('spaceportCapacity', type=int, help="Capacity of the spaceport to be added.", required=True, location='headers')

@api.route('/locations', methods=['GET'])
class All_Locations(Resource):
    def get(self):
        locations = get_all_locations()
        return {"Message": "Success"}

@api.route('/location', methods=['POST'])
class Add_Location(Resource):
    @api.doc(parser = locations_parser)
    @api.expect(locations_parser)
    def post(self):
        args = locations_parser.parse_args()
        city_name = request.headers.get('cityName')
        planet_name = request.headers.get('planetName')
        spaceport_capacity = request.headers.get('spaceportCapacity')
        if (add_new_location(city_name, planet_name, spaceport_capacity)):
            return {"Message": "Success", 'location': 'TODO'}, 200
        else:
            return {"Message": "Failed! Could not create new location!"}, 500

@api.route('/location/<string:id>', methods=['GET', 'DELETE'])
class Location_Id(Resource):
    def get(self, id):
        return {"Message": "Done"}

