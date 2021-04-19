import flask
from flask import request
from flask_restplus import Resource, Api, reqparse, fields, Namespace
from stomble_assignment.src.controllers import location_controller
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
        locations = location_controller.get_all_locations()
        if not locations:
            return {"Message": "Failed"}, 404
        return {"Message": "Success", 'Locations': parse_json(locations)}

@api.route('/location', methods=['POST'])
class Add_Location(Resource):
    @api.doc(parser = locations_parser)
    @api.expect(locations_parser)
    def post(self):
        city_name = request.headers.get('cityName')
        planet_name = request.headers.get('planetName')
        spaceport_capacity = request.headers.get('spaceportCapacity')
        if not city_name or not planet_name or not spaceport_capacity:
            return {"Message": "Invalid Parameters"}, 400
        location = None
        try:
            location = location_controller.add_new_location(city_name, planet_name, spaceport_capacity)
        except:
            return {"Message": "Failed! Internal Server Error!"}, 500
        else:
            return {"Message": "Success", 'Location': parse_json(str(location.id))}, 200

@api.route('/location/<string:id>', methods=['GET', 'DELETE'])
class Location_Id(Resource):
    def get(self, id):
        location = location_controller.get_location_by_id(id)
        if location:
            return {"Message": "Success", 'Location': parse_json(location)}, 200
        return {"Message": "No location by that id"}, 404

    # TODO - confused about what to do if a spaceship is stationed on the location to be removed
    def delete(self, id):
        if not location_controller.get_location_by_id(id):
            return {"Message": "No location by that id"}, 404
        # TODO - confused about this
        if location_controller.location_has_spaceships(id):
            return {"Message": "Failed, Location has spaceships stationed"}, 400
        ############################
        try:
            location_controller.delete_location_by_id(id)
        except:
            return {"Message": "Failed, Internal Server Error"}, 500
        else:
            return {"Message": "Success"}, 200

