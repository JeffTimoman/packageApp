from flask_wtf import FlaskForm
# from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_login import current_user
from webdata.models import User, Package, Api
    
class AddPackageForm(FlaskForm):
    package_awb = StringField('Resi Paket', validators=[DataRequired(), Length(min=10, max=30)])
    package_expedition = QuerySelectField(query_factory=lambda: Api.query, get_label='expedition')
    submit = SubmitField('Add Package')

    def validate_package_awb(self, package_awb):
        package = Package.query.filter_by(awb=package_awb.data).first()
        if package:
            raise ValidationError('This packages already exist. Please choose a different one.')


class AddPackageManual(FlaskForm):
    package_awb = StringField('Resi Paket', validators=[DataRequired(), Length(min=10, max=30)])
    package_owner = StringField('Nama Penerima', validators=[DataRequired(), Length(min=2, max=30)])
    package_expedition = QuerySelectField(query_factory=lambda: Api.query, get_label='expedition')
    submit = SubmitField('Add Package')

    def validate_package_awb(self, package_awb):
        package = Package.query.filter_by(awb=package_awb.data).first()
        if package:
            raise ValidationError('This packages already exist. Please choose a different one.')

class AddUserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Last Name')
    room = StringField('Room')
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()]) 
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Add User')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class EditPackageForm(FlaskForm):
    package_awb = StringField('Resi Paket', validators=[DataRequired(), Length(min=10, max=30)])
    package_owner = StringField('Nama Penerima', validators=[DataRequired(), Length(min=2, max=30)])
    package_expedition = QuerySelectField(query_factory=lambda: Api.query, get_label='expedition')
    submit = SubmitField('Edit Package')

    def validate_package_awb(self, package_awb):
        package = Package.query.filter_by(awb=package_awb.data).first()
        if package:
            raise ValidationError('This packages already exist. Please choose a different one.')