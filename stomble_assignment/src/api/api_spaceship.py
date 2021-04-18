import flask
from flask import request
from flask_restplus import Resource, Api, reqparse, fields, Namespace
from api_spaceship_helper import get_all_spaceships, is_valid_status, get_location_ref, add_new_spaceship, location_has_capacity, get_spaceship_by_id, delete_spaceship_by_id, update_spaceship_status_by_id
from stomble_assignment.src import setup_db
from bson import json_util
import json

app = flask.Flask(__name__)
api = Api(app)
api = Namespace("Spaceship", path="/")

def parse_json(data):
    return json.loads(json_util.dumps(data))

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, help="Name of the spaceship to be added.", required=True, location='headers')
parser.add_argument('model', type=str, help="Model of the spaceship to be added.", required=True, location='headers')
parser.add_argument('status', type=str, help="Station of the spaceship to be added.", required=True, location='headers')
parser.add_argument('location', type=str, help="Hanger locationId where the spaceship will be stationed", required=True, location='headers')


@api.route('/spaceships', methods=['GET'])
class All_Spaceships(Resource):
    def get(self):
        spaceships = get_all_spaceships()
        return {"spaceships":parse_json(spaceships)}, 200

@api.route('/spaceship', methods=['POST'])
class Add_Spaceship(Resource):
    @api.doc(parser = parser)
    @api.expect(parser)
    def post(self):
        name = request.headers.get('name')
        model = request.headers.get('model')
        status = request.headers.get('status')
        location = request.headers.get('location')
        if not is_valid_status(status):
            return {"Message": "Failed! Invalid Status"}, 400
        location_ref = get_location_ref(location)
        if not location_ref:
            return {"Message": "Failed! Invalid Location"}, 400
        if not location_has_capacity(location):
            return {"Message": "Failed! Location Spaceport Capacity reached"}, 400
        if add_new_spaceship(name, model, status, location_ref):
            return {"Message": "Success", "spaceship": "TODO"}
        return {"Message": "Failed! Internal Server Error!"}, 500

status_parser = reqparse.RequestParser()
status_parser.add_argument('status', type=str, help="Station of the spaceship to be updated.", required=True, location='headers')

@api.route('/spaceship/<string:id>', methods=['GET', 'PUT', 'DELETE'])
class Spaceship_Id(Resource):
    def get(self, id):
        spaceship = get_spaceship_by_id(id)
        if not spaceship:
            return {"Message": "Failed! No spcaship by that id"}, 404
        return {"Message": "Success", "spaceship": parse_json(spaceship)}, 200
    @api.doc(parser = status_parser)
    @api.expect(status_parser)
    def put(self, id):
        status = request.headers.get('status')
        if not is_valid_status(status):
            return {"Message": "Invalid status"}, 400
        if not get_spaceship_by_id(id):
            return {"Message": "Invalid spaceship"}, 400
        if not update_spaceship_status_by_id(id, status):
            return {"Message": "Internal Server Error"}, 500
        return {"Message": "Success"}, 200
    def delete(self, id):
        if delete_spaceship_by_id(id):
            return {"Message": "Success"}, 200
        return {"Message": "Failed"}, 400
