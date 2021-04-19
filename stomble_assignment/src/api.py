import flask
from flask_restplus import Api
from stomble_assignment.src.routes.routes_location import api as namespace_location
from stomble_assignment.src.routes.routes_spaceship import api as namespace_spaceship
from stomble_assignment.src import setup_db

setup_db.global_init()

app = flask.Flask(__name__)
api = Api(app)
api.add_namespace(namespace_location)
api.add_namespace(namespace_spaceship)

if __name__ == '__main__':
    app.run(debug=True)

