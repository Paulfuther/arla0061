from typing import Text
from flask_security.utils import get_post_login_redirect
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from sqlalchemy.sql.elements import BooleanClauseList
from sqlalchemy.sql.sqltypes import Date, String
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, \
        RadioField, FormField,HiddenField, DateField, SelectField, IntegerField, DecimalField, SelectMultipleField, TextField
from wtforms.fields.html5 import DateField, TelField, TimeField, EmailField, DateTimeLocalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional, \
            InputRequired, NumberRange
from flaskblog import  Employee, db, Store, User, Role, BulkEmailSendgrid, Twimlmessages, Company
from flask_login import current_user
import wtforms
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
import phonenumbers
import re
from flask_ckeditor import CKEditorField

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
    two_fa = RadioField('Label', choices=[('sms', 'SMS'), ('whatsapp', 'WhatsApp')])
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
   
class BulkCreatedEmailSendgridForm(FlaskForm):
    role = (QuerySelectField(query_factory=lambda: Role.query.order_by(Role.name),
        allow_blank=True, blank_text="Select a Role",validators=[DataRequired()]))
    subject = StringField('Subject',validators=[DataRequired()])
    body = CKEditorField('Message', validators=[DataRequired()])

class BulkCallForm(FlaskForm):
    role = (QuerySelectField(query_factory=lambda: Role.query.order_by(Role.name),
        allow_blank=False))
    templatename = (QuerySelectField(query_factory=lambda: Twimlmessages.query.order_by(Twimlmessages.twimlname),
        allow_blank=False))


class TelephoneForm(FlaskForm):
    area_code = IntegerField('Area Code', validators=[DataRequired()])
    number = IntegerField('Number', validators=[DataRequired(), Length(min=7, max=7)] )

class checkinoutForm(FlaskForm):
    start_date = DateField('EvenDate', validators=[DataRequired()])
    start_time = TimeField('EvenTime', validators=[DataRequired()])
    end_date = DateField('EvenDate', validators=[DataRequired()])
    end_time = TimeField('EvenTime', validators=[DataRequired()])
    store = QuerySelectField(
        query_factory=lambda: Store.query.order_by(Store.number),
        allow_blank=False
    )

class UserForm(FlaskForm):
    company_id = QuerySelectField(
        query_factory = lambda: Company.query.order_by(Company.name),
        allow_blank=False
    )

                                  

class NewRegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    firstname = StringField('Firstname', validators= [DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    mobilephone = StringField('mobile', validators=[
                              DataRequired()])
    submit2 = SubmitField('Create Account')
    password = StringField('Password', validators= [DataRequired()])
    passwordconfirm = StringField('Password Confirm', validators= [DataRequired()])
    monavail = StringField('Monday Availability', validators= [DataRequired()])
    tueavail = StringField('Tuesday Availability', validators=[DataRequired()])
    wedavail = StringField('Wednesday Availability', validators=[DataRequired()])
    thuavail = StringField('Thursday Availability', validators=[DataRequired()])
    friavail = StringField('Friday Availability', validators=[DataRequired()])
    satavail = StringField('Saturday Availability', validators=[DataRequired()])
    sunavail = StringField('Sunday Availability', validators=[DataRequired()])


class EmployeeForm(FlaskForm):
    
    email = EmailField('Email', validators=[DataRequired(), Email()])
    firstname = StringField('Firstname', validators= [DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    store = QuerySelectField('Store',
        query_factory=lambda: Store.query.order_by(Store.number),
        allow_blank=False
    )
    
    addressone = StringField('Address Line 1', validators=[
                              Length(min=2, max=100)])
    addresstwo = StringField('Address Line 2', validators=[
                             Optional(), Length(min=2, max=100)])
    apt = StringField('Unit/Apt', validators=[Optional()])
    city = StringField('City', validators=[
                       Length(min=2, max=20)])
    province = StringField('Province', validators=[
                           Length(min=2, max=20)])
    country = StringField('Country', validators=[Optional()])

    postal = StringField('Postal Code', validators=[
                          Length(min=6, max=7)])
    email = StringField('Email', validators=[
                        DataRequired(), Length(min=10, max=100), Email()])
    mobilephone = StringField('mobile', validators=[
                              DataRequired()])
    token = StringField()
    sinexpire = DateField('Sin Expire', format='%Y-%m-%d', validators=[Optional()])
    
   

    trainingid = StringField('Training ID')
    trainingpassword = StringField(
        'Training Password')
    manager = QuerySelectField(
        query_factory=lambda: User.query.join(User.roles).filter(Role.id==2).order_by(User.user_name).filter(User.active ==1),
        allow_blank=False
    )
    hrpicture = FileField(validators=[FileAllowed(['jpg', 'jpeg','png', 'HEIC'])])
    iprismcode = StringField('Iprism Code', validators=[
                              Length(min=1, max=9)])
    monavail = StringField('Monday Availability', validators= [Optional()])
    tueavail = StringField('Tuesday Availability', validators=[Optional()])
    wedavail = StringField('Wednesday Availability', validators=[Optional()])
    thuavail = StringField('Thursday Availability', validators=[Optional()])
    friavail = StringField('Friday Availability', validators=[Optional()])
    satavail = StringField('Saturday Availability', validators=[Optional()])
    sunavail = StringField('Sunday Availability', validators=[Optional()])
    submit2 = SubmitField('Add Employee')

   
  
class EmployeeUpdateForm(FlaskForm):
   
    #username = StringField('Username', validators=[
    #    DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[
                        DataRequired(), Length(min=10, max=100), Email()])
    password = StringField('Password', validators=[
        DataRequired(), Length(min=2, max=100)])
    
    firstname = StringField('Firstname', validators=[
                            DataRequired()])
    nickname = StringField('Nickname', validators=[Optional()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    dob = DateField('DOB', format='%Y-%m-%d')
    store = QuerySelectField(
        query_factory=lambda: Store.query.order_by(Store.number),
        allow_blank=False
    )
    addressone = StringField('Address Line 1', validators=[
                             Length(min=2, max=100)])
    addresstwo = StringField('Address Line 2', validators=[
                             Optional(), Length(min=2, max=100)])
    apt = StringField('Unit/Apt', validators=[Optional()])
    city = StringField('City', validators=[
                       Length(min=2, max=20)])
    province = StringField('Province', validators=[
                           DataRequired(), Length(min=2, max=20)])
    country = StringField('Country', validators=[
                          Optional()])
    
    mobilephone = StringField('mobile', validators=[
                              Length(min=9, max=12) ])
    
    startdate = DateField('Start Date', format='%Y-%m-%d',
                         )
    enddate = DateField('End Date', format='%Y-%m-%d', validators=[Optional()])
    postal = StringField('Postal Code', validators=[
                         Length(min=6, max=7)])
    manager = QuerySelectField(
        query_factory=lambda: User.query.join(User.roles).filter(
            Role.id == 2).order_by(User.user_name),
        allow_blank=False
    )

    trainingid = StringField('Training ID')
    trainingpassword = StringField(
        'Training Password')
    hrpicture = FileField(validators=[
        FileAllowed(['jpg', 'jpeg','png', 'HEIC'])])
    
    iprismcode = StringField('Iprism Code', validators=[
                             DataRequired(), Length(min=1, max=9)])
    mon_avail = StringField('Monday Availability', validators= [Optional()])
    tue_avail = StringField('Tuesday Availability', validators=[Optional()])
    wed_avail = StringField('Wednesday Availability', validators=[Optional()])
    thu_avail = StringField('Thursday Availability', validators=[Optional()])
    fri_avail = StringField('Friday Availability', validators=[Optional()])
    sat_avail = StringField('Saturday Availability', validators=[Optional()])
    sun_avail = StringField('Sunday Availability', validators=[Optional()])
    submit = SubmitField('Update Employee')

    def validate_mon_avail(self, mon_avail):
        if mon_avail.Length < 3:
            raise ValidationError('Must be 3 characters or more')

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

    store =QuerySelectField('Store',
        query_factory=lambda: Store.query.order_by(Store.number),
        allow_blank=False
    )

    eventdetails = TextAreaField('Details')#
    eventdate = DateField('EvenDate', validators=[DataRequired()])#
    eventtime = TimeField('EvenTime', validators=[DataRequired()])#
    reportedby = StringField('Reported by', validators=[DataRequired()])#
    reportedbynumber = StringField('Phone NUmber', validators=[DataRequired()])#

    suncoremployee = BooleanField()
    contractor = BooleanField()
    associate = BooleanField()
    generalpublic = BooleanField()
    other = BooleanField()
    othertext = StringField('Other')

    actionstaken = TextAreaField('Actions Taken')
    correctiveactions = TextAreaField('Corrective Actions', validators=[Optional()])#

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


class SiteIncidentUpdate(FlaskForm):
    injuryorillness = BooleanField()
    environmental = BooleanField()
    regulatory = BooleanField()
    economicdamage = BooleanField()
    reputation = BooleanField()
    security = BooleanField()
    fire = BooleanField()

    store =QuerySelectField(
        query_factory=lambda: Store.query.order_by(Store.number),
        allow_blank=False
    )

    eventdetails = TextAreaField('Details')#
    eventdate = DateField('EvenDate', validators=[DataRequired()])#
    eventtime = TimeField('EvenTime', validators=[DataRequired()])#
    reportedby = StringField('Reported by', validators=[DataRequired()])#
    reportedbynumber = StringField('Phone NUmber', validators=[DataRequired()])#

    suncoremployee = BooleanField()
    contractor = BooleanField()
    associate = BooleanField()
    generalpublic = BooleanField()
    other = BooleanField()
    othertext = StringField('Other')

    actionstaken = TextAreaField('Actions Taken')
    correctiveactions = TextAreaField('Corrective Actions', validators=[Optional()])#

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

   

  
