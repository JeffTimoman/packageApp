from flask import Blueprint, render_template, url_for, flash, redirect, request
from webdata.models import User, Package, Api

scanner = Blueprint('scanner', __name__)

@scanner.route('/')
def index():
    return render_template('scanner/index.html')