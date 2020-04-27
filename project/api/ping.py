from flask_restx import Namespace, Resource

ping_namespace = Namespace("ping")


class Ping(Resource):
    def get(self):
        return {
            "status": "success",
            "message": "pong! V 0.9.0 - 2020-04-27 20.28 - Update Migrations and user",
        }


ping_namespace.add_resource(Ping, "")
