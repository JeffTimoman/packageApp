from flask import Flask
from webdata.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_cors import CORS, cross_origin
app = Flask(__name__)
app.config.from_object(Config)
thisConfig = Config()


app.config['SECRET_KEY'] = thisConfig.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = thisConfig.DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = 3600
app.config['MAIL_SERVER'] = thisConfig.MAIL_SERVER
app.config['MAIL_PORT'] = thisConfig.MAIL_PORT
app.config['MAIL_USERNAME'] = thisConfig.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = thisConfig.MAIL_PASSWORD
app.config['MAIL_USE_SSL'] = thisConfig.MAIL_USE_SSL
app.config['MAIL_USE_TLS'] = thisConfig.MAIL_USE_TLS

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
mail = Mail(app)
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'
db.init_app(app)

from webdata.main.routes import main
from webdata.packages.routes import paket
from webdata.user.routes import user
from webdata.admin.routes import admin
from webdata.api.routes import api
from webdata.scanner.routes import scanner
app.register_blueprint(main, url_prefix='/')
app.register_blueprint(paket, url_prefix='/packages')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(scanner, url_prefix='/scanner')