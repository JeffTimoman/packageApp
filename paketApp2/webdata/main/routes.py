from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, current_user, logout_user, login_required, current_user
from webdata.models import User, Package, Api
from webdata.main.forms import LoginForm, RequestResetForm, ResetPasswordForm
from webdata import db, bcrypt, mail, app
from flask_mail import Message
main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    if current_user.user_type == 0:
        return redirect(url_for('admin.index'))
    if current_user.user_type == 1:
        return redirect(url_for('user.index'))
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            return redirect(url_for('main.login'))
    return render_template('login.html', form=form)
    
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))

@main.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('main.login'))
    return render_template('reset_password.html', form=form)   


@main.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('main.reset_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            flash('Passwords do not match', 'danger')
            print(jalan)
            return redirect(url_for('main.reset_token', token=token))
        else : 
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated! You are now able to log in', 'success')
            return redirect(url_for('main.login'))
    return render_template('reset_token.html', form=form)

@main.route('/get_package_json')
def get_package_json():
    packages = Package.query.all()
    the_json = []
    for package in packages:
        the_json.append({
            'id': package.id,
            'awb': package.awb,
            'expedition' : package.expedition,
            'owner': package.owner,
            'receiver_id': package.receiver_id,
        })
    return jsonify(the_json)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender=f"{app.config['MAIL_USERNAME']}",
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('main.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)