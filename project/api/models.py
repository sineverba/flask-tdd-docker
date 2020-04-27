from sqlalchemy.sql import func

from project import db


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    remove = db.Column(db.Boolean(), default=True, nullable=True)
    remove2 = db.Column(db.Boolean(), default=True, nullable=True)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), nullable=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email
