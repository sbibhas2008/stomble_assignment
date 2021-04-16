import flask
from flask import request
from flask_restplus import Resource, Api, reqparse, fields, Namespace
from api_spaceship_helper import get_all_spaceships
from stomble_assignment.src import setup_db
from bson import json_util
import json

app = flask.Flask(__name__)
api = Api(app)
api = Namespace("Spaceship")

def parse_json(data):
    return json.loads(json_util.dumps(data))

@api.route('/spaceships', methods=['GET'])
class Spaceships(Resource):
    def get(self):
        spaceships = get_all_spaceships()
        return {"spaceships":parse_json(spaceships)}, 200