from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from webdata.models import Package, Api, User
from webdata import db, bcrypt, mail, app
from flask_login import login_required, current_user, login_user, logout_user
import requests
from flask_cors import CORS, cross_origin
from datetime import datetime
from pytz import timezone
api = Blueprint('api', __name__)


CORS = CORS(app, supports_credentials=True)
#POST METHOD
@api.route('/add/<awb>/<expedition>/<owner>')
@login_required
def add(awb, expedition, owner):
    newPaket = Packages(awb=awb, expedition=expedition, owner=owner)
    db.session.add(newPaket)
    db.session.commit()
    return "Paket added"

@api.route('/addreceiver/<int:id>/<int:user_id>')
@login_required
def addreceiver(id, user_id):
    paket = Packages.query.get(id)
    paket.receiver_id = user_id
    db.session.commit()
    return "Receiver added"

@api.route('/packagedata/<int:id>/awb')
def getdata(id, awb):
    api = Packages.query.get(id)
    r = requests.get(f'https://api.binderbyte.com/v1/track?api_key={api.api}&courier={api.expedition}&awb={awb}')
    r_dict = r.json()
    if r.status_code == 200:
        return r_dict['data']['summary']['awb'], r_dict['data']['detail']['receiver'], r_dict['data']['summary']['courier']
    else :
        return "Error"

@api.route('/get_package_json/')
@api.route('/get_package_json/<pin>')
@cross_origin(supports_credentials=True)
def get_package_json_pin(pin =''):
    tem = datetime.now(timezone('Asia/Jakarta')).date().strftime('%Y-%m-%d')
    if pin != None and pin != '' and pin != 'undefined' and pin != 'null': 
        # Format time to Asia/Jakarta now, yyyy-mm-dd
        # packages = Package.query.filter(Package.owner.like(f'%{pin}%')).all()
        packages = Package.query.filter(Package.owner.like(f'%{pin}%')).filter(Package.date_created.like(f'%{tem}%')).all()
        # Get packages data where date is today
        # packages_today = Package.query.filter(Package.owner.like(f'%{pin}%')).filter(Package.date.like(f'%{datetime.now().strftime("%Y-%m-%d")}%')).all()
        if packages :
            the_json = []
            for package in packages:
                the_json.append({
                    'id': package.id,
                    'awb': package.awb,
                    'expedition' : package.expedition,
                    'owner': package.owner,
                    'receiver_id': package.receiver_id,
                })
            the_json = sorted(the_json, key=lambda k: k['owner'], reverse=False)
            return jsonify(the_json)
        
        packages = Package.query.filter(Package.awb.like(f'%{pin}%')).filter(Package.date_created.like(f'%{tem}%')).all()
        if packages :
            the_json = []
            for package in packages:
                the_json.append({
                    'id': package.id,
                    'awb': package.awb,
                    'expedition' : package.expedition,
                    'owner': package.owner,
                    'receiver_id': package.receiver_id,
                })
            # Sort by owner 
            the_json = sorted(the_json, key=lambda k: k['owner'], reverse=False)
            return jsonify(the_json)
        
        packages = Package.query.filter(Package.expedition.like(f'%{pin}%')).filter(Package.date_created.like(f'%{tem}%')).all()
        if packages:
            the_json = []
            for package in packages:
                temp = package.user.first_name
                the_json.append({
                    'id': package.id,
                    'awb': package.awb,
                    'expedition' : package.expedition,
                    'owner': package.owner,
                    'receiver_id': package.receiver_id,
                })
            the_json = sorted(the_json, key=lambda k: k['owner'], reverse=False)
            return jsonify(the_json)
    else :
        packages = Package.query.filter(Package.date_created.like(f'%{tem}%')).all()
        the_json = []
        for package in packages:
            the_json.append({
                'id': package.id,
                'awb': package.awb,
                'expedition' : package.expedition,
                'owner': package.owner,
                'receiver_id': package.receiver_id,
            })
        the_json = sorted(the_json, key=lambda k: k['owner'], reverse=False)
        return jsonify(the_json)