from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Sting, nullable=False)
    last_name = db.Column(db.Sting, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_type = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}')"

class Packages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receipt = db.Column(db.String, nullable=False)
    expedition = db.Column(db.String, nullable=False)
    owner = db.Column(db.String, nullable=False)
    photo = db.Column(db.String, nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Package('{self.receipt}', '{self.expedition}', '{self.owner}')"
    