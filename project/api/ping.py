from flask_restx import Namespace, Resource

ping_namespace = Namespace("ping")


class Ping(Resource):
    def get(self):
        return {
            "status": "success",
            "message": "pong! V 0.7.2 - 2020-04-27 19.33 - Update Travis",
        }


ping_namespace.add_resource(Ping, "")
