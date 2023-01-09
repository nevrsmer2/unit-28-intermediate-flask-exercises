from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Pet(db.Model):

    __tablename__ = 'pets'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    species = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    photo_url = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    available = db.Column(db.Boolean, nullable=False, default=True)


def connect_db(app):
    db.app = app
    db.init_app(app)
