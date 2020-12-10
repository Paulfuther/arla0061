from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FormField, DateField, SelectField, IntegerField, DecimalField
from wtforms.fields.html5 import DateField, TelField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional, InputRequired, NumberRange
from flaskblog import  Employee, db, Store
from flask_login import current_user
import wtforms
from wtforms.ext.sqlalchemy.fields import QuerySelectField
import phonenumbers
import re


def storelist():
    return Store.query.order_by('number')

class LoginForm(FlaskForm):
    email = StringField('email', validators = [InputRequired(), Length(min=4, max=200)])
    password = PasswordField('password', validators = [InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')
    submit = SubmitField('Login')

    
class TelephoneForm(FlaskForm):
    area_code = IntegerField('Area Code', validators=[DataRequired()])
    number = IntegerField('Number', validators=[DataRequired(), Length(min=7, max=7)] )

class EmployeeForm(FlaskForm):
    firstname = StringField('Firstname', validators= [DataRequired(), Length(min=2, max=20)])
    nickname = StringField('Nickname', validators=[Optional()])
    lastname = StringField('Lastname', validators=[DataRequired(), Length(min=2, max=20)])
    store = QuerySelectField(query_factory = storelist, allow_blank = False)
                        
    addressone = StringField('Address Line 1', validators=[
                             DataRequired(), Length(min=2, max=100)])
    addresstwo = StringField('Address Line 2', validators=[
                             Optional(), Length(min=2, max=100)])
    apt = StringField('Unit/Apt', validators=[Optional()])
    city = StringField('City', validators=[
                       DataRequired(), Length(min=2, max=20)])
    province = StringField('Province', validators=[
                           DataRequired(), Length(min=2, max=20)])
    country = StringField('Country', validators=[
                          DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[
                        DataRequired(), Length(min=10, max=100), Email()])
    #mobilephone = TelField(validators=[DataRequired(), Length(min=10, max=10)])
    mobilephone = StringField('mobile', validators=[
                              DataRequired(), Length(min=9, max=12)])
    SIN = StringField('sin', validators=[DataRequired(), Length(min=9, max=9)])
    Startdate = DateField('Start Date', format='%Y-%m-%d',
                          validators=[DataRequired()])
    Enddate = DateField('End Date', format='%m/%d/%Y', validators=[Optional()])

    postal = StringField('Postal Code', validators=[
                         DataRequired(), Length(min=6, max=6)])
    trainingid = StringField('Training ID', validators=[DataRequired()])
    trainingpassword = StringField(
        'Training Password', validators=[DataRequired()])
    manager = SelectField('manager', choices=[(
                          'Manager Name', 'Manager Name'), ('Terry', "Terry"),
        ('Steph', 'Steph'), ('Wanda', 'Wanda'), ('Sahib', 'Sahib'),
        ('Paul', 'Paul')])
    hrpicture = FileField(validators=[FileAllowed(['jpg', 'png'])])
    
    active = SelectField('Active', choices=[
                         ('Active', 'Active'), ('Y', 'Y'), ('N', 'N')])
    iprismcode = StringField('Iprism Code', validators=[
                             DataRequired(), Length(min=1, max=9)])
    submit = SubmitField('Add Employee')

   

    
    def validate_jointcompliant(self, jointcompliant):

        if jointcompliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')
        
    def validate_mobilephone(self, mobilephone):
        user = Employee.query.filter_by(mobilephone=mobilephone.data).first()
        if user:
            raise ValidationError( 'That mobile is Taken')

    def validate_email(self, email):
        emp = Employee.query.filter_by(email=email.data).first()
        if emp:
            raise ValidationError('That email is Taken')

    def validate_SIN(self, SIN):
        user = Employee.query.filter_by(SIN=SIN.data).first()
        if user:
            raise ValidationError('That SIN is Taken')

    def validate_iprismcode(self, iprismcode):
        user = Employee.query.filter_by(iprismcode=iprismcode.data).first()
        if user:
            raise ValidationError('That code is Taken')

    def validate_store(self, store):
        if store.data == "Home Store":
            raise ValidationError('Please Enter a Store')

    def validate_active(self, active):

        if active.data == "Active":
            print("homestore")
            raise ValidationError('Must indicate active or not')

    def validate_manager(self, active):

        if active.data == "Manager Name":
            print("Manager Name")
            raise ValidationError('Must Select a Manager')
   
    
  
class EmployeeUpdateForm(FlaskForm):

    firstname = StringField('Firstname', validators=[
                            DataRequired(), Length(min=2, max=20)])
    nickname = StringField('Nickname', validators=[Optional()])
    lastname = StringField('Lastname', validators=[
                           DataRequired(), Length(min=2, max=20)])
    dob = DateField('DOB', format='%Y-%m-%d',
                    validators=[DataRequired()])
    store = StringField()
    addressone = StringField('Address Line 1', validators=[
                             DataRequired(), Length(min=2, max=100)])
    addresstwo = StringField('Address Line 2', validators=[
                             Optional(), Length(min=2, max=100)])
    apt = StringField('Unit/Apt', validators=[Optional()])
    city = StringField('City', validators=[
                       DataRequired(), Length(min=2, max=20)])
    province = StringField('Province', validators=[
                           DataRequired(), Length(min=2, max=20)])
    country = StringField('Country', validators=[
                          DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[
                        DataRequired(), Length(min=10, max=100), Email()])
    mobilephone = StringField('mobile', validators=[
                              DataRequired(), Length(min=9, max=12) ])
    SIN = StringField('sin', validators=[DataRequired(), Length(min=9, max=9)])
    startdate = DateField('Start Date', format='%Y-%m-%d',
                          validators=[DataRequired()])
    enddate = DateField('End Date', format='%m/%d/%Y', validators=[Optional()])
    postal = StringField('Postal Code', validators=[
                         DataRequired(), Length(min=6, max=6)])
    manager = SelectField('manager', choices=[(
                          'Manager Name', 'Manager Name'), ('Terry', "Terry"),
        ('Steph', 'Steph'), ('Wanda', 'Wanda'), ('Sahib', 'Sahib'),
        ('Paul', 'Paul')])

    delete = SubmitField('Delete Employee')
    submit = SubmitField('Edit Employee')
    trainingid = StringField('Training ID', validators=[DataRequired()])
    trainingpassword = StringField(
        'Training Password', validators=[DataRequired()])
    hrpicture = FileField(validators=[
        FileAllowed(['jpg', 'png'])])
    active = SelectField('Active', choices=[
                         ('Active', 'Active'), ('Y', 'Y'), ('N', 'N')])
    iprismcode = StringField('Iprism Code', validators=[
                             DataRequired(), Length(min=1, max=9)])
    
    
class grade_form(FlaskForm):
    
    coursename = StringField()
    coursegrade = StringField()
    

    
    


    def validate_store(self, store):
        if store.data == "Home Store":
            raise ValidationError('Please Enter a Store')

    def validate_active(self, active):

        if active.data == "Active":
            print("homestore")
            raise ValidationError('Must indicate active or not')

    def validate_manager(self, active):

        if active.data == "Manager Name":
            print("Manager Name")
            raise ValidationError('Must Select a Manager')

    
      
       

 
 
