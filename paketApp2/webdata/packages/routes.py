from flask import Blueprint, render_template, request, redirect, url_for
from webdata.models import Package
# from webdata.paket.forms import PaketForm
from webdata import db
from flask_login import login_required, current_user, login_user, logout_user, login_manager

paket = Blueprint('paket', __name__)

@paket.route('/')
def index():
    return "Welcome to the Paket App"