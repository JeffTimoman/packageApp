from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_mail import Mail
from paketApp.webdata.config import Config
from paketApp.webdata.models import User, Packages
from paketApp.webdata.forms import RegistrationForm, LoginForm, UpdateAccountForm, PackageForm
from paketApp.webdata import app, db, bcrypt, mail
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return "<h1>Home Page</h1>"