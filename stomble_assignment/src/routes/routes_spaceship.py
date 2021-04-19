import flask
from flask import request
from flask_restplus import Resource, Api, reqparse, fields, Namespace
from stomble_assignment.src.controllers import spaceship_controller
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
        spaceships = None
        try:
            spaceships = spaceship_controller.get_all_spaceships()
        except:
            return {"Message": "Failed, Internal Server Error"}, 500
        return {"Message": "Success", "Spaceships":parse_json(spaceships)}, 200

@api.route('/spaceship', methods=['POST'])
class Add_Spaceship(Resource):

    @api.doc(parser = parser)
    @api.expect(parser)
    def post(self):
        name = request.headers.get('name')
        model = request.headers.get('model')
        status = request.headers.get('status')
        location = request.headers.get('location')
        spaceship=None
        if not name or not model or not status or not location:
            return {"Message": "Invalid Parameters"}, 400
        if not spaceship_controller.is_valid_status(status):
            return {"Message": "Failed! Invalid Status"}, 400
        location_ref = spaceship_controller.get_location_ref(location)
        if not location_ref:
            return {"Message": "Failed! Invalid Location"}, 400
        if not spaceship_controller.location_has_capacity(location):
            return {"Message": "Failed! Location Spaceport Capacity reached"}, 400
        try :
            spaceship = spaceship_controller.add_new_spaceship(name, model, status, location_ref)
        except:    
            return {"Message": "Failed! Internal Server Error!"}, 500
        else:
            return {"Message": "Success", "Spaceship": parse_json(str(spaceship.id))}

status_parser = reqparse.RequestParser()
status_parser.add_argument('status', type=str, help="Station of the spaceship to be updated.", required=True, location='headers')

@api.route('/spaceship/<string:id>', methods=['GET', 'PUT', 'DELETE'])
class Spaceship_Id(Resource):

    @api.param('id', 'Id of the spaceship')
    def get(self, id):
        spaceship = spaceship_controller.get_spaceship_by_id(id)
        if not spaceship:
            return {"Message": "Failed! No spcaship by that id"}, 404
        return {"Message": "Success", "Spaceship": parse_json(spaceship)}, 200

    @api.doc(parser = status_parser)
    @api.expect(status_parser)
    @api.param('id', 'Id of the spaceship')
    def put(self, id):
        status = request.headers.get('status')
        if not spaceship_controller.get_spaceship_by_id(id):
            return {"Message": "Invalid spaceship"}, 404
        if not status:
            return {"Message": "Invalid Parameters"}, 400
        spaceship = None 
        if not spaceship_controller.is_valid_status(status):
            return {"Message": "Invalid status"}, 400
        try:
            spaceship = spaceship_controller.update_spaceship_status_by_id(id, status)
        except:
            return {"Message": "Internal Server Error"}, 500
        else:
            return {"Message": "Success", "Spaceship": parse_json(str(spaceship.id))}, 200

    @api.param('id', 'Id of the spaceship')
    def delete(self, id):
        if not spaceship_controller.get_spaceship_by_id(id):
            return {"Message": "Failed! No spcaship by that id"}, 404
        try:
            spaceship_controller.delete_spaceship_by_id(id)
        except:
            return {"Message": "Failed"}, 400
        else:
            return {"Message": "Success"}, 200

travel_parser = reqparse.RequestParser()
travel_parser.add_argument('spaceship_id', type=str, help="Id of the travelling spaceship", required=True, location='headers')
travel_parser.add_argument('destination_id', type=str, help="Id of the destination", required=True, location='headers')
       
@api.route('/spaceship/travel', methods=['PATCH'])
class Travel(Resource):

    @api.doc(parser = travel_parser)
    @api.expect(travel_parser)   
    def patch(self):
        spaceship_id = request.headers.get('spaceship_id')
        destination_id = request.headers.get('destination_id')
        if not spaceship_id or not destination_id:
            return {"Message": "Invalid Parameters"}, 400
        if not spaceship_controller.get_spaceship_by_id(spaceship_id):
            return {"Message": "Failed, No spaceship by that id"}, 404
        if not spaceship_controller.is_operational(spaceship_id):
            return {"Message": "Failed, Only operational spaceships can travel"}, 400
        if not spaceship_controller.get_location_ref(destination_id):
            return {"Message": "Failed, No location by that id"}, 404
        if not spaceship_controller.location_has_capacity(destination_id):
            return {"Message": "Failed, Destination spaceport capacity limit has reached"}, 400
        try:
            spaceship_controller.travel_spaceship(spaceship_id, destination_id)
        except:
            return {"Message": "Failed, Internal Server Error"}, 500
        return {"Message": "Success"}, 200

