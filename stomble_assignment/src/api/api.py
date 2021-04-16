import flask
from flask import request
from flask_restplus import Resource, Api, reqparse, fields
from api_location import api as namespace_location
from api_spaceship import api as namespace_spaceship
from api_spaceship_helper import get_all_spaceships
from api_location_helper import get_all_locations, add_new_location
from stomble_assignment.src import setup_db
from bson import json_util
import json

setup_db.global_init()

app = flask.Flask(__name__)
api = Api(app)
api.add_namespace(namespace_location)
api.add_namespace(namespace_spaceship)

if __name__ == '__main__':
    app.run(debug=True)

