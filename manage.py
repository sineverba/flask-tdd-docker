import sys

from flask.cli import FlaskGroup

from project import create_app, db
from project.api.models import User

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command('seed_db')
def seed_db():
    db.session.add(User(username='username_1', email="info@gmail.com"))
    db.session.add(User(username='username_2', email="info@example.com"))
    db.session.commit()

@cli.command('db')
def migrate():
    migrate

def upgrade():
    upgrade

if __name__ == '__main__':
    cli()