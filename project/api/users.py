# project/api/users.py


from flask import request
from flask_restx import Namespace, Resource, fields

# fmt: off
from project.api.crud import (add_user, delete_user, get_all_users,
                              get_user_by_email, get_user_by_id, update_user)

# fmt: on

users_namespace = Namespace("users")

user = users_namespace.model(
    "User",
    {
        "id": fields.Integer(readOnly=True),
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "created_date": fields.DateTime,
    },
)


class UsersList(Resource):
    @users_namespace.marshal_with(user, as_list=True)
    def get(self):
        """Returns all users"""
        return get_all_users(), 200  # updated

    @users_namespace.expect(user, validate=True)
    def post(self):
        """Create new user"""
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        response_object = {}

        user = get_user_by_email(email)  # updated
        if user:
            response_object["message"] = "Sorry. That email already exists."
            return response_object, 400
        add_user(username, email)  # new
        response_object["message"] = f"{email} was added!"
        return response_object, 201


class Users(Resource):
    @users_namespace.marshal_with(user)
    def get(self, user_id):
        """Returns a single user"""
        user = get_user_by_id(user_id)  # updated
        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")
        return user, 200

    @users_namespace.expect(user, validate=True)
    def put(self, user_id):
        """Update a user"""
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        response_object = {}

        user = get_user_by_id(user_id)  # updated
        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")
        update_user(user, username, email)  # new
        response_object["message"] = f"{user.id} was updated!"
        return response_object, 200

    def delete(self, user_id):
        """Delete a single user"""
        response_object = {}
        user = get_user_by_id(user_id)  # updated
        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")
        delete_user(user)  # new
        response_object["message"] = f"{user.email} was removed!"
        return response_object, 200


users_namespace.add_resource(UsersList, "")
users_namespace.add_resource(Users, "/<int:user_id>")
