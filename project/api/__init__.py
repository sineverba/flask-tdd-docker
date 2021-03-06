from flask_restx import Api

from project.api.ping import ping_namespace
from project.api.users import users_namespace

api = Api(version="1.0", title="Users API", doc="/doc/")
# Disable totally docs
# api = Api(doc=False)

api.add_namespace(ping_namespace, path="/ping")
# Add subdirectory
# api.add_namespace(ping_namespace, path="/api/v1/ping")
api.add_namespace(users_namespace, path="/users")
