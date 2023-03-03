import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash
from webdata.models import User, Package, Api
from webdata.admin.forms import AddUserForm, AddPackageForm, AddPackageManual, EditPackageForm
from webdata import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from pytz import timezone
admin = Blueprint('admin', __name__)

@admin.route('/')
@login_required
def index():
    # Get all packages for the date today yyyy-mm-dd
    # tem = datetime.now(timezone('Asia/Jakarta')).date().strftime("%Y-%m-%d")
    # packages = Package.query.filter(Package.date_created.like(f'%{tem}%')).all()
    # packages = Package.query.order_by(Package.date_created.desc()).limit(2).all()
    # print(packages)
    today_packages = Package.query.filter(Package.date_created.like(f'%{datetime.now(timezone("Asia/Jakarta")).date().strftime("%Y-%m-%d")}%')).all()
    # packages this day claimed
    claimed_today = Package.query.filter(Package.date_created.like(f'%{datetime.now(timezone("Asia/Jakarta")).date().strftime("%Y-%m-%d")}%')).filter(Package.receiver_id != None).all()
    month_packages = Package.query.filter(Package.date_created.like(f'%{datetime.now(timezone("Asia/Jakarta")).date().strftime("%Y-%m")}%')).all()
    claimed_month = Package.query.filter(Package.date_created.like(f'%{datetime.now(timezone("Asia/Jakarta")).date().strftime("%Y-%m")}%')).filter(Package.receiver_id != None).all()
    if current_user.user_type != 0:
        flash('You are not allowed to access this page!', 'danger')
        return redirect(url_for('main.index'))
    flash(f'Welcome {current_user.first_name} {current_user.last_name}!', 'success')
    return render_template('admin/index.html', entered_today=len(today_packages), claimed_today=len(claimed_today), entered_month=len(month_packages), claimed_month=len(claimed_month))

@admin.route('/adduser', methods=['GET', 'POST'])
@login_required
def adduser():
    if current_user.user_type != 0:
        flash('You are not allowed to access this page!', 'danger')
        return redirect(url_for('main.index'))
    form = AddUserForm()
    if form.validate_on_submit():
        form.password.data = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        print("jalan")
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=form.password.data, room=form.room.data, user_type=1)
        db.session.add(user)
        db.session.commit()
        flash('User has been created!', 'success')
        return redirect(url_for('admin.adduser'))
    if (not(form.validate_on_submit)):
        flash('User has not been created!', 'danger')
    return render_template('admin/add_user.html', form=form)

@admin.route('/addpackage', methods=['GET', 'POST'])
@login_required
def addpackage():
    if current_user.user_type != 0:
        flash('You are not allowed to access this page!', 'danger')
        return redirect(url_for('main.index'))
    nana = Api.query.all()
    form = AddPackageForm()
    # flash("Welcome Paket", 'success')
    if form.validate_on_submit():
        awb = form.package_awb.data
        exp = form.package_expedition.data
        
        data = get_data(awb, exp.id)
        if data == "Error":
            flash('Package is not valid!', 'danger')
        else :
            package = Package(awb=data[0], owner=data[1], expedition=data[2])
            db.session.add(package)
            db.session.commit()
            flash(f'Package for {data[1]} has been added!', 'success')
    if (not(form.validate_on_submit)):
        flash('Package has not been created!', 'danger')
    return render_template('admin/add_package.html', form=form)

@admin.route('/addpackagemanual', methods=['GET', 'POST'])
@login_required
def addpackagemanual():
    if current_user.user_type != 0:
        flash('You are not allowed to access this page!', 'danger')
        return redirect(url_for('main.index'))
    form = AddPackageManual()
    flash("Welcome Paket", 'success')
    if form.validate_on_submit():
        awb = form.package_awb.data
        exp = form.package_expedition.data
        owner = form.package_owner.data
        package = Package(awb=awb, owner=owner, expedition=exp)
        db.session.add(package)
        db.session.commit()
        flash(f'Package for {package.owner} has been added!', 'success')
    if (not(form.validate_on_submit)):
        flash('Package has not been created!', 'danger')
    return render_template('admin/add_manual.html', form=form)

@admin.route('/listuser')
@login_required
def listuser():
    if current_user.user_type != 0:
        flash('You are not allowed to access this page!', 'danger')
        return redirect(url_for('main.index'))
    #sort user by first_name and last_name where user_type = 1
    users = User.query.filter_by(user_type=1).order_by(User.first_name, User.last_name).all()
    return render_template('admin/list_user.html', users=users)

@admin.route('/listpackage')
@login_required
def listpackage():
    if current_user.user_type != 0:
        flash('You are not allowed to access this page!', 'danger')
        return redirect(url_for('main.index'))
    packages = Package.query.all()
    # Get user data from package foreign key backref
    users = User.query.all()
    return render_template('admin/list_package.html', packages=packages, users=users)

def get_data(awb, exp_id):
    api = Api.query.get(exp_id)
    # print(api.api, api.expedition, awb)
    r = requests.get(f'https://api.binderbyte.com/v1/track?api_key={api.api}&courier={api.expedition}&awb={awb}')
    r_dict = r.json()
    # print(r_dict)
    if int(r.status_code) == 200:
        return r_dict['data']['summary']['awb'], r_dict['data']['detail']['receiver'], r_dict['data']['summary']['courier']
    else :
        return "Error"

@admin.route('/removeuser/<int:user_id>')
@login_required
def removeuser(user_id):
    if current_user.user_type != 0:
        flash('You are not allowed to access this page!', 'danger')
        return redirect(url_for('main.index'))
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.first_name} {user.last_name} has been removed!', 'success')
    return redirect(url_for('admin.listuser'))

@admin.route('/removepackage/<int:package_id>')
@login_required
def removepackage(package_id):
    if current_user.user_type != 0:
        flash('You are not allowed to access this page!', 'danger')
        return redirect(url_for('main.index'))
    package = Package.query.get(package_id)
    db.session.delete(package)
    db.session.commit()
    flash(f'Package {package.awb} has been removed!', 'success')
    return redirect(url_for('admin.listpackage'))

@admin.route('/logout')
@login_required
def logout():
    return redirect(url_for('main.logout'))

@admin.route('addmanual/<expedition>/<awb>/<owner>', methods=['GET', 'POST'])
def addmanual(expedition, awb, owner):
    package = Package(awb=awb, owner=owner, expedition=expedition)
    db.session.add(package)
    db.session.commit()
    return redirect(url_for('admin.listpackage'))
 

@admin.route('/claim/<int:package_id>')
@login_required
def claim(package_id):
    if current_user.user_type != 0:
        flash('You are not allowed to access this page!', 'danger')
        return redirect(url_for('main.index'))
    package = Package.query.get(package_id)
    package.receiver_id = current_user.id
    db.session.commit()
    flash(f'Package {package.awb} has been claimed!', 'success')
    return redirect(url_for('admin.listpackage'))

@admin.route('unclaim/<int:package_id>')
@login_required
def unclaim(package_id):
    if current_user.user_type != 0:
        flash('You are not allowed to access this page!', 'danger')
        return redirect(url_for('main.index'))
    package = Package.query.get(package_id)
    package.receiver_id = None
    db.session.commit()
    flash(f'Package {package.awb} has been unclaimed!', 'success')
    return redirect(url_for('admin.listpackage'))
