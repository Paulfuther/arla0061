from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FormField, DateField, SelectField, IntegerField, DecimalField
from wtforms.fields.html5 import DateField, TelField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional, InputRequired, NumberRange
from flaskblog import  Employee, db, Store, User, Role
from flask_login import current_user
import wtforms
from wtforms.ext.sqlalchemy.fields import QuerySelectField
import phonenumbers
import re


def storelist():
    return Store.query.order_by('number')

def mgr():
    return User.query

def get_mgr_name(User):
    return f"{User.firstname} {User.lastname}"

class LoginForm(FlaskForm):
    email = StringField('email', validators = [InputRequired(), Length(min=4, max=200)])
    password = PasswordField('password', validators = [InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')
    submit = SubmitField('Login')

    
class TelephoneForm(FlaskForm):
    area_code = IntegerField('Area Code', validators=[DataRequired()])
    number = IntegerField('Number', validators=[DataRequired(), Length(min=7, max=7)] )

class EmployeeForm(FlaskForm):
    username = StringField('Username', validators=[
                            DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[
                         Length(min=10, max=100), Email()])
    password = StringField('Password', validators=[
        DataRequired(), Length(min=2, max=100)])
    active = BooleanField(default="checked")
    firstname = StringField('Firstname', validators= [DataRequired(), Length(min=2, max=20)])
    nickname = StringField('Nickname', validators=[Optional()])
    lastname = StringField('Lastname', validators=[DataRequired(), Length(min=2, max=20)])
    store = QuerySelectField(
        query_factory=lambda: Store.query.order_by(Store.number),
        allow_blank=False
    )
   
    dob = DateField('Date of Birth', format='%Y-%m-%d',
                    validators=[DataRequired()])
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

    postal = StringField('Postal Code', validators=[
                         DataRequired(), Length(min=6, max=7)])
    email = StringField('Email', validators=[
                        DataRequired(), Length(min=10, max=100), Email()])
    mobilephone = StringField('mobile', validators=[
                              DataRequired(), Length(min=9, max=12)])
    
    sinexpire = DateField('Sin Expire', format='%Y-%m-%d', validators=[Optional()])
    Startdate = DateField('Start Date', format='%Y-%m-%d',
                          validators=[DataRequired()])
    Enddate = DateField('End Date', format='%m/%d/%Y', validators=[Optional()])

    trainingid = StringField('Training ID', validators=[DataRequired()])
    trainingpassword = StringField(
        'Training Password', validators=[DataRequired()])
    manager = QuerySelectField(
        query_factory=lambda: User.query.join(User.roles).filter(Role.id==2).order_by(User.user_name),
        allow_blank=False
    )
    
   # gradelist = Grade.query\
    #    .filter_by(employee_id=staff_id)\
     #   .join(Employee, Employee.id == Grade.employee_id)\
     #   .join(Course, Course.id == Grade.course_id)\
     #   .add_columns(Course.name, Grade.value, Grade.completeddate)\
     #   .order_by(Grade.course_id)
    
    
    #manager = SelectField('manager', choices=[(
    #                      'Manager Name', 'Manager Name'), ('Terry', "Terry"),
    #    ('Steph', 'Steph'), ('Wanda', 'Wanda'), ('Sahib', 'Sahib'),
    #    ('Paul', 'Paul')])
    hrpicture = FileField(validators=[FileAllowed(['jpg', 'jpeg','png', 'HEIC'])])
    
   
    iprismcode = StringField('Iprism Code', validators=[
                             DataRequired(), Length(min=1, max=9)])
    monavail = StringField('Monday Availability', validators=[
                           DataRequired(), Length(min=2, max=100)])
    tueavail = StringField('Tuesday Availability', validators=[
                           DataRequired(), Length(min=2, max=100)])
    wedavail = StringField('Wednesday Availability', validators=[
                           DataRequired(), Length(min=2, max=100)])
    thuavail = StringField('Thursday Availability', validators=[
                           DataRequired(), Length(min=2, max=100)])
    friavail = StringField('Friday Availability', validators=[
                           DataRequired(), Length(min=2, max=100)])
    satavail = StringField('Saturday Availability', validators=[
                           DataRequired(), Length(min=2, max=100)])
    sunavail = StringField('Sunday Availability', validators=[
                           DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Add Employee')

   

        
    def validate_mobilephone(self, mobilephone):
        user = Employee.query.filter_by(mobilephone=mobilephone.data).first()
        if user:
            raise ValidationError( 'That mobile is Taken')

    def validate_email(self, email):
        emp = Employee.query.filter_by(email=email.data).first()
        if emp:
            raise ValidationError('That email is Taken')

    

    
        
    def validate_trainingid(self, trainingid):
        user = Employee.query.filter_by(trainingid=trainingid.data).first()
        if user:
            raise ValidationError('That id is Taken')

    def validate_store(self, store):
        if store.data == "Home Store":
            raise ValidationError('Please Enter a Store')

    def validate_active(self, active):

        if active.data == "Active":
            print("homestore")
            raise ValidationError('Must indicate active or not')

    def validate_manager(self, manager):

        if manager.data == "Manager Name":
            print("Manager Name")
            raise ValidationError('Must Select a Manager')
   
    
  
class EmployeeUpdateForm(FlaskForm):
   
    username = StringField('Username', validators=[
        DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[
                        DataRequired(), Length(min=10, max=100), Email()])
    password = StringField('Password', validators=[
        DataRequired(), Length(min=2, max=100)])
    
    firstname = StringField('Firstname', validators=[
                            DataRequired(), Length(min=2, max=20)])
    nickname = StringField('Nickname', validators=[Optional()])
    lastname = StringField('Lastname', validators=[
                           DataRequired(), Length(min=2, max=20)])
    dob = DateField('DOB', format='%Y-%m-%d',
                    validators=[DataRequired()])
    store = QuerySelectField(
        query_factory=lambda: Store.query.order_by(Store.number),
        allow_blank=False
    )
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
    
    mobilephone = StringField('mobile', validators=[
                              DataRequired(), Length(min=9, max=12) ])
    
    startdate = DateField('Start Date', format='%Y-%m-%d',
                          validators=[DataRequired()])
    enddate = DateField('End Date', format='%Y-%m-%d', validators=[Optional()])
    postal = StringField('Postal Code', validators=[
                         DataRequired(), Length(min=6, max=7)])
    manager = QuerySelectField(
        query_factory=lambda: User.query.join(User.roles).filter(
            Role.id == 2).order_by(User.user_name),
        allow_blank=False
    )

    trainingid = StringField('Training ID', validators=[DataRequired()])
    trainingpassword = StringField(
        'Training Password', validators=[DataRequired()])
    hrpicture = FileField(validators=[
        FileAllowed(['jpg', 'jpeg','png', 'HEIC'])])
    
    iprismcode = StringField('Iprism Code', validators=[
                             DataRequired(), Length(min=1, max=9)])
    mon_avail = StringField('Monday Availability', validators=[
                           DataRequired(), Length(min=2, max=100)])
    tue_avail = StringField('Tuesday Availability', validators=[
                           DataRequired(), Length(min=2, max=100)])
    wed_avail = StringField('Wednesday Availability', validators=[
                           DataRequired(), Length(min=2, max=100)])
    thu_avail = StringField('Thursday Availability', validators=[
                           DataRequired(), Length(min=2, max=100)])
    fri_avail = StringField('Friday Availability', validators=[
                           DataRequired(), Length(min=2, max=100)])
    sat_avail = StringField('Saturday Availability', validators=[
                           DataRequired(), Length(min=2, max=100)])
    sun_avail = StringField('Sunday Availability', validators=[
                           DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Update Employee')

class Schedule(FlaskForm):
    store = SelectField('Store', choices=[('Home Store', 'Home Store'), ("396", "396"), ('398', '398'),
                                          ('402', '402'), ('414', '414'), ('1616',
                                                                           '1616'), ('8156', '8156'),
                                          ('8435', '8435'), ('33410',
                                                             '33410'),
                                          ('33485', '33485'), ('48314',
                                                               '48314'),
                                          ('65077', '65077'), ('65231', '65231')])
   
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

    
class schedule_start(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])   
    store = SelectField('Store', choices=[('Home Store', 'Home Store'), ("396", "396"), ('398', '398'),
                                          ('402', '402'), ('414', '414'), ('1616',
                                                                           '1616'), ('8156', '8156'),
                                          ('8435', '8435'), ('33410',
                                                             '33410'),
                                          ('33485', '33485'), ('48314',
                                                               '48314'),
                                          ('65077', '65077'), ('65231', '65231')])
 
class GradeForm(FlaskForm):
    completed = SelectField('Completed', choices=[
                         ('Completed Y or N?', 'Completed Y or N?'), ('Y', 'Y'), ('N', 'N')], default="N")
    
    completeddate = DateField('Completed Date', format='%Y-%m-%d',
                          )
