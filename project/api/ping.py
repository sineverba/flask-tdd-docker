from flask import Blueprint
from flask_restx import Api, Resource

ping_blueprint = Blueprint("ping", __name__)
api = Api(ping_blueprint)


class Ping(Resource):
    def get(self):
        return {
            "status": "success",
            "message": "pong! V 0.5.0 - 2020-04-26 11.18 - Add CORS",
        }


api.add_resource(Ping, "/ping")
