from typing import Text
from flask_security.utils import get_post_login_redirect
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from sqlalchemy.sql.elements import BooleanClauseList
from sqlalchemy.sql.sqltypes import Date, String
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FormField,HiddenField, DateField, SelectField, IntegerField, DecimalField, SelectMultipleField
from wtforms.fields.html5 import DateField, TelField, TimeField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional, InputRequired, NumberRange
from flaskblog import  Employee, db, Store, User, Role, BulkEmailSendgrid, Twimlmessages
from flask_login import current_user
import wtforms
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
import phonenumbers
import re


def storelist():
    return Store.query.order_by('number')

def mgr():
    return User.query

def get_mgr_name(User):
    return f"{User.firstname} {User.lastname}"

class Confirm2faForm(FlaskForm):
    token = StringField()
    submit = SubmitField('Verify')


class LoginForm(FlaskForm):
    email = StringField('email', validators = [InputRequired(), Length(min=4, max=200), Email()])
    password = PasswordField('password', validators = [InputRequired(), Length(min=8, max=80)])
    remember_me = BooleanField('remember me')
    submit = SubmitField('Login')

class forgot_password_Form(FlaskForm):
    email = StringField('email', validators = [InputRequired(), Length(min=4, max=200), Email()])    
    submit = SubmitField('Login')

class reset_password_form(FlaskForm):
    password = PasswordField('Password', validators = [InputRequired(), Length(min=8, max=80)])
    password2 = PasswordField('Repeat Password', validators = [InputRequired(),Length(min=8, max=80), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class CommsForm(FlaskForm):
    role = (QuerySelectField(query_factory=lambda: Role.query.order_by(Role.name),
        allow_blank=False))
    message_body = TextAreaField('Message', validators=[DataRequired()])
    
class BulkEmailSendgridForm(FlaskForm):
    role = (QuerySelectField(query_factory=lambda: Role.query.order_by(Role.name),
        allow_blank=False))
    templatename = (QuerySelectField(query_factory=lambda: BulkEmailSendgrid.query.order_by(BulkEmailSendgrid.templatename),
        allow_blank=False))
   
class BulkCallForm(FlaskForm):
    role = (QuerySelectField(query_factory=lambda: Role.query.order_by(Role.name),
        allow_blank=False))
    templatename = (QuerySelectField(query_factory=lambda: Twimlmessages.query.order_by(Twimlmessages.twimlname),
        allow_blank=False))


class TelephoneForm(FlaskForm):
    area_code = IntegerField('Area Code', validators=[DataRequired()])
    number = IntegerField('Number', validators=[DataRequired(), Length(min=7, max=7)] )

class EmployeeForm(FlaskForm):
    
    email = EmailField('Email', validators=[DataRequired(), Email()])
    firstname = StringField('Firstname', validators= [DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Lastname', validators=[DataRequired(), Length(min=2, max=20)])
    store = QuerySelectField('Store',
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

    postal = StringField('Postal Code', validators=[
                         DataRequired(), Length(min=6, max=7)])
    email = StringField('Email', validators=[
                        DataRequired(), Length(min=10, max=100), Email()])
    mobilephone = StringField('mobile', validators=[
                              DataRequired()])
    token = StringField()
    sinexpire = DateField('Sin Expire', format='%Y-%m-%d', validators=[Optional()])
    
   

    trainingid = StringField('Training ID', validators=[DataRequired()])
    trainingpassword = StringField(
        'Training Password', validators=[DataRequired()])
    manager = QuerySelectField(
        query_factory=lambda: User.query.join(User.roles).filter(Role.id==2).order_by(User.user_name).filter(User.active ==1),
        allow_blank=False
    )
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
    submit2 = SubmitField('Add Employee')

   
  
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
    completed = BooleanField('Check If Completed', default=False)
    
    completeddate = DateField('Completed Date', format='%Y-%m-%d',
                          )


class SiteIncident(FlaskForm):
    injuryorillness = BooleanField()
    environmental = BooleanField()
    regulatory = BooleanField()
    economicdamage = BooleanField()
    reputation = BooleanField()
    security = BooleanField()
    fire = BooleanField()

    location = StringField('Location', validators=[DataRequired(), Length(min=1, max= 100)])

    eventdetails = TextAreaField('Details', validators=[DataRequired()])
    eventdate = DateField('EvenDate', validators=[DataRequired()])
    eventtime = TimeField('EvenTime', validators=[DataRequired()])
    reportedby = StringField('Reported by', validators=[DataRequired()])
    reportedbynumber = StringField('Phone NUmber', validators=[DataRequired()])

    suncoremployee = BooleanField()
    contractor = BooleanField()
    associate = BooleanField()
    generalpublic = BooleanField()
    other = BooleanField()
    othertext = StringField('Other')

    actionstaken = TextAreaField('Actions Taken')
    correctiveactions = TextAreaField('Corrective Actions', validators=[DataRequired()])

    sno = BooleanField()
    syes = BooleanField()
    scomment = StringField()

    rna = BooleanField()
    rno = BooleanField()
    ryes = BooleanField()
    rcomment = StringField()

    gas = BooleanField()
    diesel = BooleanField()
    sewage = BooleanField()
    chemical = BooleanField()
    chemcomment = StringField()
    deiselexhaustfluid = BooleanField()
    sother = BooleanField()
    s2comment = StringField()

    air = BooleanField()
    water = BooleanField()
    wildlife = BooleanField()
    land = BooleanField()
    volumerelease = StringField()

    pyes = BooleanField()
    pno = BooleanField()
    pna = BooleanField()
    pcase = StringField()

    stolentransactions = BooleanField()
    stoltransactions = StringField()
    stolencards = BooleanField()
    stolcards = StringField()
    stolentobacco = BooleanField()
    stoltobacco = StringField()
    stolenlottery = BooleanField()
    stollottery = StringField()
    stolenfuel = BooleanField()
    stolfuel = StringField()
    stolenother = BooleanField()
    stolother = StringField()
    stolenothervalue = StringField()
    stolenna = BooleanField()

    gender = StringField()
    height = StringField()
    weight = StringField()
    haircolor = StringField()
    haircut= StringField()
    complexion = StringField()
    beardmoustache = StringField()
    eyeeyeglasses = StringField()
    licencenumber = StringField()
    makemodel = StringField()
    color = StringField()
    scars = StringField()
    tatoos = StringField()
    hat = StringField()
    shirt = StringField()
    trousers = StringField()
    shoes = StringField()
    voice = StringField()
    bumpersticker = StringField()
    direction = StringField()
    damage = StringField()

    wgsa = BooleanField()
    wcontractor = BooleanField()
    wassociate = BooleanField()
    wpublic = BooleanField()
    wother = BooleanField()
    wothertext = StringField()
    wname = StringField()
    wnumber = StringField()
    waddress = StringField()
    wdate = DateField()
    submit = SubmitField('Submit Event Form')


    
