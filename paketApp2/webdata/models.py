from datetime import datetime
from pytz import timezone
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, Flask
from webdata import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=True)
    room = db.Column(db.String(20), default='000')
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone('Asia/Jakarta')))
    package_claimed = db.relationship('Package', backref='claimed_by', lazy=True)
    user_type = db.Column(db.Integer, nullable=False, default='1')
    #0 = superuser, 1 = admin, 2 = user, 3 = scanner.

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}', '{self.date_created}')"

class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    awb = db.Column(db.String(20), nullable=False)
    expedition = db.Column(db.String(30), nullable=False)
    owner = db.Column(db.String(100), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone('Asia/Jakarta')))

    def __repr__(self):
        return f"{{'id': {self.id}, 'awb': {self.awb}, 'expedition': {self.expedition}, 'owner': {self.owner}, 'receiver_id': {self.receiver_id}, 'date_created': {self.date_created}}}"

    @property
    def user(self):
        return User.query.filter_by(id=self.receiver_id).first()

class Api(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expedition = db.Column(db.String(30), nullable=False)
    api = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"{self.expedition}"