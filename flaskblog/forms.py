from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FormField, DateField, SelectField, IntegerField, DecimalField
from wtforms.fields.html5 import DateField, TelField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional, InputRequired, NumberRange
from flaskblog.models import User, Employee
from flask_login import current_user
import wtforms

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign-Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That Username is Taken. Please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That Email is Taken. Please choose a different one')      

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                'That Username is Taken. Please choose a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                'That Email is Taken. Please choose a different one')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
    
class TelephoneForm(FlaskForm):
    area_code = IntegerField('Area Code', validators=[DataRequired()])
    number = IntegerField('Number', validators=[DataRequired(), Length(min=7, max=7)] )

class EmployeeForm(FlaskForm):
    firstname = StringField('Firstname', validators= [DataRequired(), Length(min=2, max=20)])
    nickname = StringField('Nickname', validators=[Optional()])
    lastname = StringField('Lastname', validators=[DataRequired(), Length(min=2, max=20)])
    store = SelectField('Store', choices=[('Home Store', 'HomeStore'), ("396", "396"), ('398', '398'),
                                          ('402', '402'), ('414', '414'), ('1616','1616'), ('8156', '8156'),
                                          ('8435', '8435'), ('33410', '33410'),
                                          ('33485', '33485'), ('48314', '48314'),
                                          ('65077', '65077'), ('65231', '65231')])
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
    hrpicture = FileField(validators=[
        FileAllowed(['jpg', 'png'])])
    active = SelectField('Active', choices=[
                         ('Active', 'Active'), ('Y', 'Y'), ('N', 'N')])
    iprismcode = StringField('Iprism Code', validators=[
                             DataRequired(), Length(min=1, max=9)])
    submit = SubmitField('Add Employee')

    def validate_mobilephone(self, mobilephone):
        user = Employee.query.filter_by(mobilephone=mobilephone.data).first()
        if user:
            raise ValidationError(
                'That mobile is Taken')

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

    
    

class whmisForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d', 
                          validators=[Optional()])
    completeddate = DateField('Completed Date', format='%Y-%m-%d',
                          validators=[Optional()])
    datequalified = DateField('Date Qualified', format='%Y-%m-%d',
                          validators=[Optional()])
    expirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                          validators=[Optional()])
    compliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])

    def validate_compliant(self, compliant):

        if compliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')
class ppeForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d',
                          validators=[Optional()])
    completeddate = DateField('Completed Date', format='%Y-%m-%d',
                              validators=[Optional()])
    datequalified = DateField('Date Qualified', format='%Y-%m-%d',
                              validators=[Optional()])
    expirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                               validators=[Optional()])
    compliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])

    def validate_compliant(self, compliant):

        if compliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')
class fireextinguishersForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d',
                          validators=[Optional()])
    completeddate = DateField('Completed Date', format='%Y-%m-%d',
                              validators=[Optional()])
    datequalified = DateField('Date Qualified', format='%Y-%m-%d',
                              validators=[Optional()])
    expirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                               validators=[Optional()])
    compliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])

    def validate_compliant(self, compliant):

        if compliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not') 
class emergencyproceduresForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d',
                          validators=[Optional()])
    completeddate = DateField('Completed Date', format='%Y-%m-%d',
                              validators=[Optional()])
    datequalified = DateField('Date Qualified', format='%Y-%m-%d',
                              validators=[Optional()])
    expirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                               validators=[Optional()])
    compliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])

    def validate_compliant(self, compliant):

        if compliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')
class firstaidForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d',
                          validators=[Optional()])
    completeddate = DateField('Completed Date', format='%Y-%m-%d',
                              validators=[Optional()])
    datequalified = DateField('Date Qualified', format='%Y-%m-%d',
                              validators=[Optional()])
    expirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                               validators=[Optional()])
    compliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])

    def validate_compliant(self, compliant):

        if compliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')
class foodhandlingForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d',
                          validators=[Optional()])
    completeddate = DateField('Completed Date', format='%Y-%m-%d',
                              validators=[Optional()])
    datequalified = DateField('Date Qualified', format='%Y-%m-%d',
                              validators=[Optional()])
    expirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                               validators=[Optional()])
    compliant = SelectField('Compliant ?', choices=[
        ('Compliant ?e', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])

    def validate_compliant(self, compliant):

        if compliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')
class propaneForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d',
                          validators=[Optional()])
    completeddate = DateField('Completed Date', format='%Y-%m-%d',
                              validators=[Optional()])
    datequalified = DateField('Date Qualified', format='%Y-%m-%d',
                              validators=[Optional()])
    expirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                               validators=[Optional()])
    compliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])

    def validate_compliant(self, compliant):

        if compliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')
class healthandsafetyForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d',
                          validators=[Optional()])
    completeddate = DateField('Completed Date', format='%Y-%m-%d',
                              validators=[Optional()])
    datequalified = DateField('Date Qualified', format='%Y-%m-%d',
                              validators=[Optional()])
    expirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                               validators=[Optional()])
    compliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])

    def validate_compliant(self, compliant):

        if compliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')
class fuelpumpshutoffForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d',
                          validators=[Optional()])
    completeddate = DateField('Completed Date', format='%Y-%m-%d',
                              validators=[Optional()])
    datequalified = DateField('Date Qualified', format='%Y-%m-%d',
                              validators=[Optional()])
    expirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                               validators=[Optional()])
    compliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])

    def validate_compliant(self, compliant):

        if compliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')
class workingaloneForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d',
                          validators=[Optional()])
    completeddate = DateField('Completed Date', format='%Y-%m-%d',
                              validators=[Optional()])
    datequalified = DateField('Date Qualified', format='%Y-%m-%d',
                              validators=[Optional()])
    expirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                               validators=[Optional()])
    compliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])

    def validate_compliant(self, compliant):

        if compliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')
class workplaceviolenceForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d',
                          validators=[Optional()])
    completeddate = DateField('Completed Date', format='%Y-%m-%d',
                              validators=[Optional()])
    datequalified = DateField('Date Qualified', format='%Y-%m-%d',
                              validators=[Optional()])
    expirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                               validators=[Optional()])
    compliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])

    def validate_compliant(self, compliant):

        if compliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')
class jointhealthandsafetyForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d',
                          validators=[Optional()])
    completeddate = DateField('Completed Date', format='%Y-%m-%d',
                              validators=[Optional()])
    datequalified = DateField('Date Qualified', format='%Y-%m-%d',
                              validators=[Optional()])
    expirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                               validators=[Optional()])
    compliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])

    def validate_compliant(self, compliant):

        if compliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')

class giantform(FlaskForm):
    about_you = wtforms.FormField(EmployeeForm)
    training = wtforms.FormField(whmisForm)
    training2 = wtforms.FormField(ppeForm)
    training3 = wtforms.FormField(fireextinguishersForm)
    training4 = wtforms.FormField(emergencyproceduresForm)
    training5 = wtforms.FormField(firstaidForm)
    training6 = wtforms.FormField(foodhandlingForm)
    training7 = wtforms.FormField(propaneForm)
    training8 = wtforms.FormField(healthandsafetyForm)
    training9 = wtforms.FormField(workingaloneForm)
    training10 = wtforms.FormField(workplaceviolenceForm)
    training11 = wtforms.FormField(jointhealthandsafetyForm)
    training12 = wtforms.FormField(fuelpumpshutoffForm)
    



class EmployeeUpdateForm(FlaskForm):

    firstname = StringField('Firstname', validators=[
                            DataRequired(), Length(min=2, max=20)])
    nickname = StringField('Nickname', validators=[Optional()])
    lastname = StringField('Lastname', validators=[
                           DataRequired(), Length(min=2, max=20)])
    store = SelectField('Store', choices=[('Home Store', 'HomeStore'), ("396", "396"), ('398', '398'),
                                          ('402', '402'), ('414', '414'), ('1616',
                                                                           '1616'), ('8156', '8156'),
                                          ('8435', '8435'), ('33410', '33410'),
                                          ('33485', '33485'), ('48314', '48314'),
                                          ('65077', '65077'), ('65231', '65231')])
    addressone = StringField('Address Line 1', validators=[
                             DataRequired(), Length(min=2, max=100)])
    addresstwo = StringField('Address Line 2', validators=[
                             DataRequired(), Length(min=2, max=100)])
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
                              DataRequired(), Length(min=9, max=12)])
    SIN = StringField('sin', validators=[DataRequired(), Length(min=9, max=9)])
    Startdate = DateField('Start Date', format='%Y-%m-%d',
                          validators=[DataRequired()])
    Enddate = DateField('End Date', format='%m/%d/%Y', validators=[Optional()])
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
    
