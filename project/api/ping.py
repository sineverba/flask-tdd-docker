from flask import Blueprint
from flask_restx import Api, Resource

ping_blueprint = Blueprint("ping", __name__)
api = Api(ping_blueprint)


class Ping(Resource):
    def get(self):
        return {"status": "success", "message": "pong! V 0.3.0 2020-04-20 07.56"}


api.add_resource(Ping, "/ping")
