from flask import Blueprint, render_template, request, redirect, url_for, flash
from webdata.models import User, Package, Api
from datetime import datetime
from pytz import timezone
from webdata import db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
user = Blueprint('user', __name__)

@user.route('/')
@login_required
def index():
    # Get all packages for the date today
    # packages = Package.query.filter_by(date_created=datetime.now(timezone('Asia/Jakarta')).date()).all()
    
    # Get latest two packages
    packages = Package.query.order_by(Package.date_created.desc()).limit(2).all()
    print(packages)
    return render_template('user/index.html', packages=packages)

@user.route('/smp')
@login_required
def smp():
    return render_template('user/smp.html')

@user.route('/claim/<int:id>')
@login_required
def claim(id):
    package = Package.query.get_or_404(id)
    if package.receiver_id:
        flash('Packages has been claimed', 'warning')
        return redirect(url_for('user.index'))
    package.receiver_id = current_user.id
    db.session.commit()
    flash(f'Package {package.awb} been claimed!', 'info')
    return redirect(url_for('user.index'))

@user.route('/unclaim/<int:id>')
@login_required
def unclaim(id):
    package = Package.query.get(id)
    if current_user.id != package.receiver_id and current_user.user_type != 0:
        flash('You are not the owner of this package!', 'danger')
        return redirect(url_for('main.index'))
    package.receiver_id = None
    db.session.commit()
    flash(f'Package {package.awb} has been unclaimed!', 'info')
    return redirect(url_for('user.index'))
@user.route('/claim2/<int:id>')
@login_required
def claim2(id):
    package = Package.query.get_or_404(id)
    if package.receiver_id:
        flash('Packages has been claimed', 'warning')
        return redirect(url_for('user.packages'))
    package.receiver_id = current_user.id
    db.session.commit()
    flash(f'Package {package.awb} been claimed!', 'info')
    return redirect(url_for('user.packages'))

@user.route('/unclaim2/<int:id>')
@login_required
def unclaim2(id):
    package = Package.query.get(id)
    if current_user.id != package.receiver_id and current_user.user_type != 0:
        flash('You are not the owner of this package!', 'danger')
        return redirect(url_for('user.packages'))
    package.receiver_id = None
    db.session.commit()
    flash(f'Package {package.awb} has been unclaimed!', 'info')
    return redirect(url_for('user.packages'))

@user.route('/packages')
@login_required
def packages():
    tem = datetime.now(timezone('Asia/Jakarta')).date().strftime("%Y-%m-%d")
    packages = Package.query.filter(Package.date_created.like(f'%{tem}%')).all()
    # print("jalan")
    return render_template('user/packages.html', packages=packages)