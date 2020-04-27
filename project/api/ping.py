from flask_restx import Namespace, Resource

ping_namespace = Namespace("ping")


class Ping(Resource):
    def get(self):
        return {
            "status": "success",
            "message": "pong! V 0.6.0 - 2020-04-27 12.49 - Add Migrations",
        }


ping_namespace.add_resource(Ping, "")
