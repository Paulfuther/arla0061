from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FormField, DateField, SelectField, IntegerField, DecimalField
from wtforms.fields.html5 import DateField, TelField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional, InputRequired, NumberRange
#from flaskblog.models import  Employee
from flask_login import current_user
import wtforms

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
    hrpicture = FileField(validators=[FileAllowed(['jpg', 'png'])])
    
    active = SelectField('Active', choices=[
                         ('Active', 'Active'), ('Y', 'Y'), ('N', 'N')])
    iprismcode = StringField('Iprism Code', validators=[
                             DataRequired(), Length(min=1, max=9)])
    submit = SubmitField('Add Employee')

   

    tobstartdate = DateField('Start Date', format='%Y-%m-%d',
                        validators=[Optional()])
    tobcompleteddate = DateField('Completed Date', format='%Y-%m-%d',
                            validators=[Optional()])
    
    tobexpirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                            validators=[Optional()])
    tobcompliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])

    whmisstartdate = DateField('Start Date', format='%Y-%m-%d',
                        validators=[Optional()])
    whmiscompleteddate = DateField('Completed Date', format='%Y-%m-%d',
                            validators=[Optional()])
    
    whmisexpirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                            validators=[Optional()])
    whmiscompliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])


    ppestartdate = DateField('Start Date', format='%Y-%m-%d',
                             validators=[Optional()])
    ppecompleteddate = DateField('Completed Date', format='%Y-%m-%d',
                                 validators=[Optional()])

    ppeexpirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                                  validators=[Optional()])
    ppecompliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])

    
            
    firestartdate = DateField('Start Date', format='%Y-%m-%d',
                            validators=[Optional()])
    firecompleteddate = DateField('Completed Date', format='%Y-%m-%d',
                                validators=[Optional()])

    fireexpirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                                validators=[Optional()])
    firecompliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])


    
        

    emerstartdate = DateField('Start Date', format='%Y-%m-%d',
                            validators=[Optional()])
    emercompleteddate = DateField('Completed Date', format='%Y-%m-%d',
                                validators=[Optional()])

    emerexpirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                                validators=[Optional()])
    emercompliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])


    


    firstaidstartdate = DateField('Start Date', format='%Y-%m-%d',
                            validators=[Optional()])
    firstaidcompleteddate = DateField('Completed Date', format='%Y-%m-%d',
                                validators=[Optional()])

    firstaidexpirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                                validators=[Optional()])
    firstaidcompliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])


    
        
    foodstartdate = DateField('Start Date', format='%Y-%m-%d',
                            validators=[Optional()])
    foodcompleteddate = DateField('Completed Date', format='%Y-%m-%d',
                                validators=[Optional()])

    foodexpirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                                validators=[Optional()])
    foodcompliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])


   


    propanestartdate = DateField('Start Date', format='%Y-%m-%d',
                            validators=[Optional()])
    propanecompleteddate = DateField('Completed Date', format='%Y-%m-%d',
                                validators=[Optional()])

    propaneexpirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                                validators=[Optional()])
    propanecompliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])


    

    hsstartdate = DateField('Start Date', format='%Y-%m-%d',
                            validators=[Optional()])
    hscompleteddate = DateField('Completed Date', format='%Y-%m-%d',
                                validators=[Optional()])

    hsexpirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                                validators=[Optional()])
    hscompliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])


    

    fuelstartdate = DateField('Start Date', format='%Y-%m-%d',
                            validators=[Optional()])
    fuelcompleteddate = DateField('Completed Date', format='%Y-%m-%d',
                                validators=[Optional()])

    fuelexpirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                                validators=[Optional()])
    fuelcompliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])


    

    alonestartdate = DateField('Start Date', format='%Y-%m-%d',
                            validators=[Optional()])
    alonecompleteddate = DateField('Completed Date', format='%Y-%m-%d',
                                validators=[Optional()])

    aloneexpirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                                validators=[Optional()])
    alonecompliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])


    
    violencestartdate = DateField('Start Date', format='%Y-%m-%d',
                        validators=[Optional()])
    violencecompleteddate = DateField('Completed Date', format='%Y-%m-%d',
                            validators=[Optional()])
    
    violenceexpirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                            validators=[Optional()])
    violencecompliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])


    

    jointstartdate = DateField('Start Date', format='%Y-%m-%d',
                            validators=[Optional()])
    jointcompleteddate = DateField('Completed Date', format='%Y-%m-%d',
                                validators=[Optional()])

    jointexpirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                                validators=[Optional()])
    jointcompliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])


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
   
    def validate_tobcompliant(self, tobcompliant):
    
        if tobcompliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')  
        
    def validate_whmiscompliant(self, whmiscompliant):
    
        if whmiscompliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')   
        
        
    def validate_ppecompliant(self, ppecompliant):
    
        if ppecompliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')

    def validate_firecompliant(self, firecompliant):
    
        if firecompliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')     

    def validate_emercompliant(self, emercompliant):
    
        if emercompliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')

    def validate_firstaidcompliant(self, firstaidcompliant):
    
        if firstaidcompliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')
        

    def validate_foodcompliant(self, foodcompliant):
    
        if foodcompliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')
        
    def validate_propanecompliant(self, propanecompliant):
    
        if propanecompliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')
        
    def validate_hscompliant(self, hscompliant):
    
        if hscompliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')
        
    def validate_fuelcompliant(self, fuelcompliant):
    
        if fuelcompliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')
    def validate_alonecompliant(self, alonecompliant):
    
        if alonecompliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')
    def validate_violencecompliant(self, violencecompliant):
    
        if violencecompliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')
        

#class giantform(FlaskForm):
#    about_you = wtforms.FormField(EmployeeForm)
#    training = wtforms.FormField(whmisForm)
#    training2 = wtforms.FormField(ppeForm)
#    training3 = wtforms.FormField(fireextinguishersForm)
#    training4 = wtforms.FormField(emergencyproceduresForm)
#    training5 = wtforms.FormField(firstaidForm)
#    training6 = wtforms.FormField(foodhandlingForm)
#    training7 = wtforms.FormField(propaneForm)
#    training8 = wtforms.FormField(healthandsafetyForm)
#    training9 = wtforms.FormField(workingaloneForm)
#    training10 = wtforms.FormField(workplaceviolenceForm)
#    training11 = wtforms.FormField(jointhealthandsafetyForm)
#    training12 = wtforms.FormField(fuelpumpshutoffForm)
  
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
    

    tobstartdate = DateField('Start Date', format='%Y-%m-%d',
                            validators=[Optional()])
    tobcompleteddate = DateField('Completed Date', format='%Y-%m-%d',
                                validators=[Optional()])

    tobexpirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                                validators=[Optional()])
    tobcompliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])

    whmisstartdate = DateField('Start Date', format='%Y-%m-%d',
                            validators=[Optional()])
    whmiscompleteddate = DateField('Completed Date', format='%Y-%m-%d',
                                validators=[Optional()])

    whmisexpirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                                    validators=[Optional()])
    whmiscompliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])

    ppestartdate = DateField('Start Date', format='%Y-%m-%d',
                            validators=[Optional()])
    ppecompleteddate = DateField('Completed Date', format='%Y-%m-%d',
                                validators=[Optional()])

    ppeexpirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                                validators=[Optional()])
    ppecompliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])

    firestartdate = DateField('Start Date', format='%Y-%m-%d',
                            validators=[Optional()])
    firecompleteddate = DateField('Completed Date', format='%Y-%m-%d',
                                validators=[Optional()])

    fireexpirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                                validators=[Optional()])
    firecompliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])

    emerstartdate = DateField('Start Date', format='%Y-%m-%d',
                            validators=[Optional()])
    emercompleteddate = DateField('Completed Date', format='%Y-%m-%d',
                                validators=[Optional()])

    emerexpirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                                validators=[Optional()])
    emercompliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])

    firstaidstartdate = DateField('Start Date', format='%Y-%m-%d',
                                validators=[Optional()])
    firstaidcompleteddate = DateField('Completed Date', format='%Y-%m-%d',
                                    validators=[Optional()])

    firstaidexpirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                                    validators=[Optional()])
    firstaidcompliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])

    foodstartdate = DateField('Start Date', format='%Y-%m-%d',
                            validators=[Optional()])
    foodcompleteddate = DateField('Completed Date', format='%Y-%m-%d',
                                validators=[Optional()])

    foodexpirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                                validators=[Optional()])
    foodcompliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])

    propanestartdate = DateField('Start Date', format='%Y-%m-%d',
                                validators=[Optional()])
    propanecompleteddate = DateField('Completed Date', format='%Y-%m-%d',
                                    validators=[Optional()])

    propaneexpirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                                    validators=[Optional()])
    propanecompliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])

    hsstartdate = DateField('Start Date', format='%Y-%m-%d',
                            validators=[Optional()])
    hscompleteddate = DateField('Completed Date', format='%Y-%m-%d',
                                validators=[Optional()])

    hsexpirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                                validators=[Optional()])
    hscompliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])

    fuelstartdate = DateField('Start Date', format='%Y-%m-%d',
                            validators=[Optional()])
    fuelcompleteddate = DateField('Completed Date', format='%Y-%m-%d',
                                validators=[Optional()])

    fuelexpirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                                validators=[Optional()])
    fuelcompliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])

    alonestartdate = DateField('Start Date', format='%Y-%m-%d',
                            validators=[Optional()])
    alonecompleteddate = DateField('Completed Date', format='%Y-%m-%d',
                                validators=[Optional()])

    aloneexpirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                                    validators=[Optional()])
    alonecompliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])

    violencestartdate = DateField('Start Date', format='%Y-%m-%d',
                                validators=[Optional()])
    violencecompleteddate = DateField('Completed Date', format='%Y-%m-%d',
                                    validators=[Optional()])

    violenceexpirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                                    validators=[Optional()])
    violencecompliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])

    jointstartdate = DateField('Start Date', format='%Y-%m-%d',
                            validators=[Optional()])
    jointcompleteddate = DateField('Completed Date', format='%Y-%m-%d',
                                    validators=[Optional()])

    jointexpirationdate = DateField('Expiration Date', format='%Y-%m-%d',
                                    validators=[Optional()])
    jointcompliant = SelectField('Compliant ?', choices=[
        ('Compliant ?', 'Compliant ?'), ('Y', 'Y'), ('N', 'N')])

    def validate_jointcompliant(self, jointcompliant):

        if jointcompliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')

    

   

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

    def validate_tobcompliant(self, tobcompliant):

        if tobcompliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')

    def validate_whmiscompliant(self, whmiscompliant):

        if whmiscompliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')

    def validate_ppecompliant(self, ppecompliant):

        if ppecompliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')

    def validate_firecompliant(self, firecompliant):

        if firecompliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')

    def validate_emercompliant(self, emercompliant):

        if emercompliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')

    def validate_firstaidcompliant(self, firstaidcompliant):

        if firstaidcompliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')

    def validate_foodcompliant(self, foodcompliant):

        if foodcompliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')

    def validate_propanecompliant(self, propanecompliant):

        if propanecompliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')

    def validate_hscompliant(self, hscompliant):

        if hscompliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')

    def validate_fuelcompliant(self, fuelcompliant):

        if fuelcompliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')

    def validate_alonecompliant(self, alonecompliant):

        if alonecompliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')

    def validate_violencecompliant(self, violencecompliant):

        if violencecompliant.data == "Compliant ?":
            raise ValidationError('Must indicate compliant or not')
