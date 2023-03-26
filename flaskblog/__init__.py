
from pyexpat.errors import messages
from flask import Flask, session

app = Flask(__name__)

from dotenv import load_dotenv
from time import time
import jwt, uuid, traceback, pytz
from flask_ckeditor import CKEditor, CKEditorField, upload_fail, upload_success
import os, base64
import json
from functools import wraps
from datetime import datetime, timedelta
from flask import render_template_string, make_response, url_for, redirect, send_from_directory, \
     request, render_template, send_file, abort, g, message_flashed, flash
from flask_admin import Admin, expose, BaseView
from flask_admin.form import rules
from flask_admin.actions import action
from flask_admin.contrib.fileadmin import FileAdmin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy.ext.hybrid import hybrid_property
from flask_admin.contrib.sqla import ModelView
from flask_marshmallow import Marshmallow
from marshmallow import Schema
from flask_admin.menu import MenuLink
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash 
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, \
    String, ForeignKey, or_
from flask_email_verifier import EmailVerifier
from flask_login import  user_logged_out, user_logged_in, login_required,\
        current_user, LoginManager, fresh_login_required
from flask_user import roles_required, roles_accepted, UserMixin
from celery import Celery
from celery.schedules import crontab
from flaskblog.tasks import *
import dropbox
from dropbox import DropboxOAuth2Flow
from dropbox.files import WriteMode
import pdfkit,boto
import boto.s3.connection
from io import BytesIO
from twilio.rest import Client
from functools import wraps
from twilio.request_validator import RequestValidator
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import  Mail, Attachment, FileContent, FileName, FileType, Disposition
from PIL import Image

bcrypt = Bcrypt(app)
basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()

# use evnironment variables while building
app.config['SECRET_KEY'] =os.environ.get('SECRET_KEY') 
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get('SECURITY_PASSWORD_SALT')
app.config['SECURITY_RECOVERABLE'] = True
app.config['SECURITY_CHANGEABLE'] = False
app.config['SECURITY_EMAIL_SENDER'] = ('valid_email@my_domain.com')
app.config['MAIL_SERVER']= os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['EMAIL_VERIFIER_KEY']= os.environ.get('EMAIL_VERIFIER_KEY')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'
#app.config['CKEDITOR_ENABLE_CSRF'] = True  # if you want to enable CSRF protect, uncomment this line
app.config['UPLOADED_PATH'] = os.path.join(basedir, 'images')
EMPLOYEE_FILE_UPLOAD_PATH = os.path.join(basedir, 'static/employee_docs')
INCIDENT_UPLOAD_PATH=os.path.join(basedir, 'static/incidentpictures')
INCIDENT_HIRES_UPLOAD_PATH=os.path.join(basedir, 'static/incidentpictures_hires')
BULK_EMAIL_PATH=os.path.join(basedir, 'static/emailfiles')
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg',  '.png', '.gif']
app.config['INCIDENT_UPLOAD_PATH'] = INCIDENT_UPLOAD_PATH
app.config['INCIDENT_HIRES_UPLOAD_PATH'] = INCIDENT_HIRES_UPLOAD_PATH
app.config['BULK_EMAIL_PATH']= BULK_EMAIL_PATH
app.config['EMPLOYEE_FILE_UPLOAD_PATH']= EMPLOYEE_FILE_UPLOAD_PATH
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=5)
LINODE_ACCESS_KEY = os.environ.get('LINODE_BUCKET_ACCESS_KEY')
LINODE_SECRET_KEY = os.environ.get('LINODE_BUCKET_SECRET_KEY')
LINODE_BUCKET_URL = os.environ.get('LINODE_BUCKET_URL') 
LINODE_BUCKET_NAME = os.environ.get('LINODE_BUCKET_NAME')
LINODE_REGION = os.environ.get('LINODE_REGION')

conn = boto.connect_s3(
        aws_access_key_id = LINODE_ACCESS_KEY,
        aws_secret_access_key = LINODE_SECRET_KEY,
        host = LINODE_REGION,
        #is_secure=False,               # uncomment if you are not using ssl
        calling_format = boto.s3.connection.OrdinaryCallingFormat(),
        )

#app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
#CELERY_ENABLE_UTC = False
#USE_TZ=True
#CELERY_TIMEZONE = 'Canada/Eastern'
app.config['CELERYBEAT_SCHEDULE']= {
    'call_stores_monthly': {
        'task':'call_stores_monthly',
        'schedule': crontab(day_of_month="1-7",hour="12,20"),
        },
    }


account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
twilio_from = os.environ['TWILIO_FROM']


celery.conf.update(app.config)
#global COOKIE_TIME_OUT
#COOKIE_TIME_OUT = 60*60*24*7 #5 days

SENDGRID_NEWHIRE_ID = os.environ.get('SENDGRID_NEWHIRE_ID')
SENDGRID_NEW_HIRE_FILE_ID=os.environ.get('SENDGRID_NEW_HIRE_FILE_ID')
NOTIFY_SERVICE_SID = os.environ.get('TWILIO_NOTIFY_SERVICE_SID')
DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
TWILIO_VERIFY_SID = os.environ.get('TWILIO_VERIFY_SID')
sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
client = Client(account_sid, auth_token)
verify = client.verify.services(TWILIO_VERIFY_SID)


SESSION_COOKIE_SECURE = True
REMEMBER_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
REMEMBER_COOKIE_HTTPONLY = True

def validate_twilio_request(f):
    """Validates that incoming requests genuinely originated from Twilio"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Create an instance of the RequestValidator class
        validator = RequestValidator(os.environ.get('TWILIO_AUTH_TOKEN'))

        # Validate the request using its URL, POST data,
        # and X-TWILIO-SIGNATURE header
        request_valid = validator.validate(
            request.url,
            request.form,
            request.headers.get('X-TWILIO-SIGNATURE', ''))

        # Continue processing the request if it's valid, return a 403 error if
        # it's not
        if request_valid:
            return f(*args, **kwargs)
        else:
            return abort(403)
    return decorated_function


DROP_BOX_KEY = os.environ.get('DROP_BOX_KEY')
DROP_BOX_SECRET = os.environ.get('DROP_BOX_SECRET')
DROP_BOX_SHORT_TOKEN=os.environ.get('DROP_BOX_SHORT_TOKEN')

verifier = EmailVerifier(app)
db = SQLAlchemy(app)
#dbx = dropbox.Dropbox(DROP_BOX_KEY)

ma = Marshmallow(app)
ckeditor = CKEditor(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'
login_manager.session_protection="basic"
login_manager.login_message = 'You need to login first'
login_manager.refresh_view = 'logout'
login_manager.needs_refresh_message = 'This is a sensitive area. You need to login aagin to continue'
login_manager.needs_refresh_message_category = 'info'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#@app.context_processor
#def context_processor():
#    return dict(session=session)


#@celery.task(context=True)




@celery.task
def save_images(upload_directory):
    print(upload_directory)
    for f in os.listdir(upload_directory):

        print(f)

    
            #file = request.files.get(f)
        i=Image.open(os.path.join(upload_directory,f))
        i.thumbnail((2000,2000), Image.LANCZOS)  
        print(i.size)  
            #securefilename = secure_filename(file.filename)
            #upload_directory = os.path.join(INCIDENT_UPLOAD_PATH,unique_num)
            #os.mkdir(upload_directory)
        i.save(os.path.join(upload_directory,f),optimize=True)
        print (f)
            #print(upload_directory)
        return "uploading..."



@celery.task
def make_incident_pdf(file_id, random_number):
    with app.test_request_context():
        rol =  User.query.filter(User.roles.any(Role.id == 9)).all()
        print(file_id)
        img = '/Users/paulfuther/arla0061/flaskblog/static/images/SECURITYPERSON.jpg'
        css = "flaskblog/static/main.css"
        file = Incident.query.get(file_id)
        fdate1 = file.eventdate
        #print(fdate1)
        fdate= datetime.strftime(fdate1,'%Y-%m-%d')
        #print(fdate)
        fstore = file.location
        id = file_id
        #print(fdate)
        gsa = Incident.query.get(file_id)
        ident = gsa.id
        print(ident)

        picture = incident_files.query.filter_by(incident_id=file_id)
       
        rendered = render_template('eventreportpdf.html',gsa=gsa, css=css, picture=picture, random_number=random_number)
        options = {'enable-local-file-access': None,
            '--keep-relative-links': '',
            '--cache-dir':'/Users/paulfuther/arla0061/flaskblog',
            'encoding' : "UTF-8"
        }
        css = "flaskblog/static/main.css"
        
        pdf = pdfkit.from_string(rendered, False, options=options, css=css)

        file = BytesIO(pdf)
            #print(type(file))
        created_on = datetime.now().strftime('%Y-%m-%d')
        filename = f" {fstore} {fdate}  ID  {id} {created_on}.pdf"

        # need to create a bytes file to use as an attachment for sendgrid

        encoded_file = base64.b64encode(pdf).decode()
        attachedFile = Attachment(
                FileContent(encoded_file),
                FileName(filename),
                FileType('application/pdf'),
                Disposition('attachment')) 


        bucket_name = 'paulfuther'
        #file_path = file
        folder_name = f"EMPLOYEES/{staff_id}_{gsa.lastname}_{gsa.firstname}/DOCUMENTS"
        object_key = '{}/{}'.format(folder_name, filename)
        bucket = conn.lookup(bucket_name)
        key = bucket.new_key('{}/{}'.format(folder_name, filename))
        key.set_contents_from_file(file)

        #for x in rol:
                
         #   email = x.email
         #   message = Mail(
         #   from_email = DEFAULT_SENDER,
         #   to_emails=email,
         #   subject ='A new incident report has been filed',
         #   html_content='<strong>An incident report has been filed. {}<strong>'.format(filename))
         #   message.attachment = attachedFile
         #   response = sg.send(message)
         #   print(response.status_code, response.body, response.headers)

            # upload to drop box

        #with file as f:    
        #    dbx.files_upload(f.read(), path=f"/SITEINCIDENTS/{filename}", mode=WriteMode('overwrite'))
    

@celery.task
def make_pdf(staff_id, signatures):
    with app.test_request_context():
        #signatures = sigs#Empfile.query.filter_by(employee2_id = staff_id)
        ## this is incorrect. Employeeid is not user id. correct before pbulishing.
        rol =  User.query.filter(or_(User.roles.any(Role.id == 9), User.id==staff_id)).all()
        img = '/files/image-20201205212708-1.png'

       
        print(len(signatures))

        #print(signatures)
        for x in rol:
            print(x.email)
        print(staff_id)
        #return "done"
        
        image1 = '/Users/paulfuther/arla0061/flaskblog/images/image-20201205212708-1.png'
        image2 = '/Users/paulfuther/arla0061/flaskblog/images/image-20201205213750-1.png'
        image3 = '/Users/paulfuther/arla0061/flaskblog/images/image-20201205213046-1.png '
        image4 = '/Users/paulfuther/arla0061/flaskblog/images/image-20201205213057-2.png'
        image5 = '/Users/paulfuther/arla0061/flaskblog/images/uniformfour.png'
        image6 = '/Users/paulfuther/arla0061/flaskblog/images/uniformthree.png' 

        x=signatures
        hrpage = hrfiles.query.all()
        for y in hrpage:
            print(y.id)
        gsa = Employee.query.filter_by(user_id = staff_id).first()
        print(gsa)
        fname = gsa.firstname
        lname = gsa.lastname
        id = gsa.id
        print(fname)
        date_today = datetime.now()
        rendered = render_template('employeefilepdf2.html',
                                   image1=image1, image2=image2, image3 = image3, image4 = image4, 
                                   image5=image5, image6=image6,hrpage = hrpage, signatures=signatures,
                                    date_today=date_today, gsa=gsa)
    
        options = {'enable-local-file-access': None,
            '--keep-relative-links': '',
            '--cache-dir':'/Users/paulfuther/arla0061/flaskblog',
            'encoding' : "UTF-8"
        }
        css = "flaskblog/static/jquery.signaturepad.css"
        css2 = ".."
        pdf = pdfkit.from_string(rendered, False, options=options, css=css)

        file = BytesIO(pdf)
        created_on = datetime.now().strftime('%Y-%m-%d')
        filename = f" {lname} {fname}  NEWHIREFILE ID  {id} {created_on}.pdf"

        encoded_file = base64.b64encode(pdf).decode()
        attachedFile = Attachment(
                FileContent(encoded_file),
                FileName(filename),
                FileType('application/pdf'),
                Disposition('attachment')) 
#            for x in rol:
            #email = x.email
            #message = Mail(
            #from_email=DEFAULT_SENDER,
            #to_emails= email,
            #subject = 'A New Hire File has been created',
            #html_content='<strong>A new hire file has been created and uploaded to dropbox. {}<strong>'.format(filename)
            #)
            
            #message.dynamic_template_data = {
                
            #    'name':gsa.firstname,
            #    'userid':gsa.trainingid,
            #    'password':gsa.trainingpassword

            #}
        
            #message.template_id = SENDGRID_NEW_HIRE_FILE_ID
            #message.attachment=attachedFile
            #response = sg.send(message)
         ##///

        # upload newhire file to linode.
        # new hire files are in the folder EMPLOYEES then their user id and lastname then first name.

        bucket_name = 'paulfuther'
        #file_path = file
        folder_name = f"EMPLOYEES/{staff_id}_{gsa.lastname}_{gsa.firstname}/DOCUMENTS"
        object_key = '{}/{}'.format(folder_name, filename)
        bucket = conn.lookup(bucket_name)
        key = bucket.new_key('{}/{}'.format(folder_name, filename))
        key.set_contents_from_file(file)



        #with file as f:    
        #    dbx.files_upload(f.read(), path=f"/NEWHRFILES/{filename}", mode=WriteMode('overwrite'))
    




admin = Admin(app, name='Dashboard')
    
bcrypt = Bcrypt(app)

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

task_store = db.Table(
    'task_store',
    db.Column('todo_id', db.Integer(), db.ForeignKey('todo.id')),
    db.Column('store_id', db.Integer(), db.ForeignKey('store.id'))
)

incident_store = db.Table(
    'incident_store',
    db.Column('incidentnumbers_id', db.Integer(),
              db.ForeignKey('incidentnumbers.id')),
    db.Column('store_id', db.Integer(), db.ForeignKey('store.id')))

salt_store = db.Table(
    'salt_store',
    db.Column('saltlog_id', db.Integer(), db.ForeignKey('saltlog.id')),
    db.Column('store_id', db.Integer(), db.ForeignKey('store.id'))
)

reclaim_store = db.Table(
    'reclaim_store',
    db.Column('reclaim_id', db.Integer(), db.ForeignKey('reclaimtank.id')),
    db.Column('store_id', db.Integer(), db.ForeignKey('store.id'))
)

maintain_store = db.Table(
    'maintain_store',
    db.Column('maintain_id', db.Integer(), db.ForeignKey('cwmaintenance.id')),
    db.Column('store_id', db.Integer(), db.ForeignKey('store.id'))
)

class hrfiles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(120))
    effective_date = db.Column(db.DateTime(), nullable=True)
    date_of_review = db.Column(db.DateTime(), nullable=True)
    text = db.Column(db.Text)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    #def __str__(self):
    #    return (self.firstname)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean, default = True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    confirmed_at = db.Column(db.DateTime)
    user_name = db.Column(db.String(100))
    phone = db.Column(db.String(100), unique=True)
    # new additions 
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 
    email_confirmed = db.Column(db.Boolean, default=False)
    email_confirmed_date = db.Column(db.DateTime)
    #employee = db.relationship('Customer', backref= 'user', uselist = False)
    roles = db.relationship('Role',  secondary=roles_users,
                           backref=db.backref('users', lazy='dynamic'))

    check_in_out = db.relationship('checkinout', backref='user', lazy=True)
    
 

    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.roles is  None:
            self.roles = Role.query.filter_by(name="GSA").first()

    def has_roles(self, *args):
        return set(args).issubset({role.name for role in self.roles})

    def is_active(self):
        return self.active

    def __str__(self):
        return str(self.firstname) 

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time()+ expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')
    
    def get_mail_confirm_token(self, expires_in=600):
        return jwt.encode(
            {'confirm_email': self.id, 'exp': time()+ expires_in},
            app.config['SECRET_KEY'], algorithm="HS256")

    def __repr__(self):
        return self.firstname

    @staticmethod
    def verify_email_confirm_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],algorithms=['HS256'])['confirm_email']
        except:
            return
        return User.query.get(id)

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = ('id', 'email', 'roles')
user_schema = UserSchema(many=True)


class BulkEmailSendgrid(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    templatename = db.Column(db.String, unique=True)
    templateid = db.Column(db.String(200), unique=True)
    
    def __repr__(self):
        return '%r' % (self.templatename)

    #def __str__(self):
    #    return (self.templatename)
        
 
class Twimlmessages(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    twimlname = db.Column(db.String, unique=True)
    twimlid = db.Column(db.String(200), unique=True)
    
    def __repr__(self):
        return '%r' % (self.twimlname)

    #def __str__(self):
    #    return (self.twimlname)

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    

    def __str__(self):
        return (self.name)

    #def __repr__(self):
    #    return (self.name)

    #def __hash__(self):
    #    return hash(self.name)

   

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    firstname = db.Column(db.String(), nullable=False)
    lastname = db.Column(db.String(), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    store = db.relationship('Store', backref = 'store')
    addressone = db.Column(db.String(20), nullable=True)
    addresstwo = db.Column(db.String(20), nullable=True)
    apt = db.Column(db.String(20), nullable=True)
    city = db.Column(db.String(), nullable=True)
    province = db.Column(db.String(), nullable=True)
    country = db.Column(db.String(), nullable=True)
    mobilephone = db.Column(db.String(), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    dob = db.Column(db.DateTime(),nullable=True)
    startdate = db.Column(db.DateTime(),nullable=True)
    sinexpire = db.Column(db.DateTime(), nullable=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    
   
    postal = db.Column(db.String(6), nullable=True)
    trainingid = db.Column(db.String(),unique=True, nullable=True)
    trainingpassword = db.Column(db.String(), nullable=True)
    manager = db.Column(db.Integer)
    image_file = db.Column(db.String(50), nullable=True,
                           default='default.jpg')
    
    iprismcode = db.Column(db.String(9), nullable=False)
    
    mon_avail = db.Column(db.String(100), nullable=False)
    tue_avail = db.Column(db.String(100), nullable=False)
    wed_avail = db.Column(db.String(100), nullable=False)
    thu_avail = db.Column(db.String(100), nullable=False)
    fri_avail = db.Column(db.String(100), nullable=False)
    sat_avail = db.Column(db.String(100), nullable=False)
    sun_avail = db.Column(db.String(100), nullable=False)
    employee_doc = db.relationship('Empdocs', backref='employee', lazy=True)
   
    
    #def __str__(self):
    #    return (self.firstname) 

class EmployeeSchema(ma.Schema):
    class Meta:
        model = Employee
        store = ma.Nested("StoreSchema", exclude=("store",))
        fields = ('id', 'firstname', 'lastname', 'mobilephone','email', 'store_id', 'image_file', 'number')
employee_schema = EmployeeSchema(many=True)

class EmployeeSMSSchema(ma.Schema):
    class Meta:
        model = Employee
        fields = ('id','mobilephone')
employeeSMS_schema = EmployeeSMSSchema(many=True)



class Course(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)  
    
    
    #def __str__(self):
    #    return '%r' % (self.name)
   
class Grade(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    
    employee_id = db.Column(Integer(), ForeignKey('employee.id'))
    employee = db.relationship('Employee', backref = 'grades')
    course_id = db.Column(db.Integer(), ForeignKey('course.id'))
    course = db.relationship('Course', backref='grade')
    completed = db.Column(db.Boolean, default = False)
    completeddate = db.Column(db.String(), nullable=True)
      
    #def __str__(self):
    #    return (self.course_id)

class staffschedule(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    employee_id = db.Column(Integer(), ForeignKey('employee.id'))
    employee = db.relationship('Employee', backref = 'schedule')
    storeworked = db.Column(db.String())
    shift_description = db.Column(db.String())
    shift_hours = db.Column(db.Integer())
    shift_date = db.Column(db.Date)
 
    #def __str__(self):
    #    return (self.id)

class staffscheduleschema(ma.Schema):
    class Meta:
        model = staffschedule
        
        employee=ma.Nested("employee_schema")
        fields = ('id', 'firstname', 'shift_description','shift_hours', 'shift_date')

staffschedule_schema = staffscheduleschema(many=True)

class Empfile(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    employee2_id = db.Column(Integer(), ForeignKey('employee.id'))
    employee2 = db.relationship('Employee', backref = 'files')
    file_id = db.Column(db.Integer(), ForeignKey('hrfiles.id'))
    file = db.relationship('hrfiles', backref = 'filess') 
    sig_data = db.Column(db.Integer())
    
    #def __str__(self):
    #    return (self.id)

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    carwash =  db.Column(db.Boolean, default = False)
    phone = db.Column(db.String(), nullable=False)
    check_in_out = db.relationship('checkinout', backref='store', lazy=True)
    address = db.Column(db.String())
    city = db.Column(db.String())
    province = db.Column(db.String())
    
    def __repr__(self):
        return f"{self.number}  {self.address}  {self.city}  {self.province}"

   # def __str__(self):
   #     return (self.number)
   
class StoreSchema(ma.Schema):
    class Meta:
        model = Store
        fields = ('number','phone')
store_schema = StoreSchema(many=True)
        
    
class reclaimtank(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    reclaimdate = db.Column(db.DateTime(), nullable=True)
    reclaimstore = db.relationship('Store', secondary = reclaim_store,
                                   backref = db.backref('recstore', lazy = 'dynamic'))
    tankonewater = db.Column(db.String(100))
    tankonesand = db.Column(db.String(100))
    tanktwowater = db.Column(db.String(100))
    tanktwosand = db.Column(db.String(100))
    tanklids = db.Column(db.String(100))
    changepillows = db.Column(db.String(100))

class cwmaintenance(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    maintaindate = db.Column(db.DateTime(), nullable = True)
    maintainstore = db.relationship('Store', secondary = maintain_store,
                                   backref = db.backref('maintstore', lazy = 'dynamic'))
    workdone = db.Column(db.String(500))
    partsused = db.Column(db.String(500))

    

# To do list 
class Todo(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200))
    store = db.relationship('Store',  secondary=task_store,
                            backref=db.backref('users', lazy='dynamic'))
    
    def __repr__(self):
        return '%r' % (self.task)

   

 # ticket numbers
 
class Incidentnumbers(db.Model):
     id = db.Column(db.Integer, primary_key = True)
     incstore = db.relationship('Store', secondary = incident_store,
                             backref=db.backref('incusers', lazy='dynamic'))
     incident = db.Column(db.String(100))
     details = db.Column(db.String(500))
     
     def __repr__(self):
         return '%r' % (self.details)

    

# salt log
       
class Saltlog(db.Model):
     id = db.Column(db.Integer, primary_key = True)
     saltdate = db.Column(db.DateTime(), nullable=True)
     saltstore = db.relationship('Store', secondary = salt_store,
                             backref=db.backref('saltusers', lazy='dynamic'))
     
     area = db.Column(db.String(100))
     gsa = db.Column(db.String(500))
     
     def __repr__(self):
         return '%r' % (self.area)      


     

class Incident(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     injuryorillness = db.Column(db.Boolean, default = False)
     environmental = db.Column(db.Boolean, default = False)
     regulatory = db.Column(db.Boolean, default = False)
     economicdamage = db.Column(db.Boolean, default = False)
     reputation = db.Column(db.Boolean, default = False)
     security = db.Column(db.Boolean, default = False)
     fire = db.Column(db.Boolean, default = False)

     store_id =db.Column(db.Integer, db.ForeignKey('store.id'))
     store = db.relationship('Store', backref = 'stores')
     eventdetails = db.Column(db.String())
     eventdate = db.Column(db.DateTime(), nullable = True)
     eventtime = db.Column(db.Time())
     reportedby = db.Column(db.String())
     reportedbynumber = db.Column(db.String())

     suncoremployee = db.Column(db.Boolean, default = False)
     contractor = db.Column(db.Boolean, default = False)
     associate = db.Column(db.Boolean, default = False)
     generalpublic = db.Column(db.Boolean, default = False)
     other = db.Column(db.Boolean, default = False)
     othertext = db.Column(db.String())

     actionstaken = db.Column(db.String())
     correctiveactions = db.Column(db.String())

     sno = db.Column(db.Boolean, default = False)
     syes = db.Column(db.Boolean, default = False)
     scomment = db.Column(db.String())

     rna = db.Column(db.Boolean, default = False)
     rno = db.Column(db.Boolean, default = False)
     ryes = db.Column(db.Boolean, default = False)
     rcomment = db.Column(db.String())

     gas = db.Column(db.Boolean, default = False)
     diesel = db.Column(db.Boolean, default = False)
     sewage = db.Column(db.Boolean, default = False)
     chemical = db.Column(db.Boolean, default = False)
     chemcomment = db.Column(db.String())
     deiselexhaustfluid = db.Column(db.Boolean, default = False)
     sother = db.Column(db.Boolean, default = False)
     s2comment = db.Column(db.String())

     air = db.Column(db.Boolean, default = False)
     water = db.Column(db.Boolean, default = False)
     wildlife = db.Column(db.Boolean, default = False)
     land = db.Column(db.Boolean, default = False)
     volumerelease = db.Column(db.String())

     pyes = db.Column(db.Boolean, default = False)
     pno = db.Column(db.Boolean, default = False)
     pna = db.Column(db.Boolean, default = False)
     pcase = db.Column(db.String())

     stolentransactions = db.Column(db.Boolean, default = False)
     stoltransactions = db.Column(db.String())
     stolencards = db.Column(db.Boolean, default = False)
     stolcards = db.Column(db.String())
     stolentobacco = db.Column(db.Boolean, default = False)
     stoltobacco = db.Column(db.String())
     stolenlottery = db.Column(db.Boolean, default = False)
     stollottery = db.Column(db.String())
     stolenfuel = db.Column(db.Boolean, default = False)
     stolfuel = db.Column(db.String())
     stolenother = db.Column(db.Boolean, default = False)
     stolother = db.Column(db.String())
     stolenothervalue = db.Column(db.String())
     stolenna = db.Column(db.Boolean, default = False)

     gender = db.Column(db.String())
     height = db.Column(db.String())
     weight = db.Column(db.String())
     haircolor = db.Column(db.String())
     haircut= db.Column(db.String())
     complexion = db.Column(db.String())
     beardmoustache = db.Column(db.String())
     eyeeyeglasses = db.Column(db.String())
     licencenumber = db.Column(db.String())
     makemodel = db.Column(db.String())
     color = db.Column(db.String())
     scars = db.Column(db.String())
     tatoos = db.Column(db.String())
     hat = db.Column(db.String())
     shirt = db.Column(db.String())
     trousers = db.Column(db.String())
     shoes = db.Column(db.String())
     voice = db.Column(db.String())
     bumpersticker = db.Column(db.String())
     direction = db.Column(db.String())
     damage = db.Column(db.String())
     incident_images = db.relationship('incident_files', backref='incident_images', lazy=True)
     image_folder = db.Column(db.String())

     
    

class incident_files(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    image = db.Column(db.String(100), nullable=False)
    incident_id = db.Column(db.Integer, db.ForeignKey('incident.id'))

    

class Empdocs(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    file_document = db.Column(db.String(100), nullable=False)
    file_employee = db.Column(db.Integer, db.ForeignKey('employee.id'))

    

class checkinout(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    startdate = db.Column(db.DateTime(), nullable = True)
    starttime = db.Column(db.Time())
    enddate = db.Column(db.DateTime(), nullable = True)
    endtime = db.Column(db.Time())
    check_store = db.Column(db.Integer, db.ForeignKey('store.id'))
    check_user = db.Column(db.Integer, db.ForeignKey('user.id'))

class completedfile(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    userid = db.Column(db.Integer())
    completed =db.Column(db.Boolean, default=False)
    date_completed = db.Column(db.DateTime(timezone=True), default=pytz.utc.localize(datetime.utcnow()).astimezone(pytz.timezone("America/New_York")))

class Error(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    traceback = db.Column(db.String())
    time = db.Column(db.DateTime(timezone=True), default=pytz.utc.localize(datetime.utcnow()).astimezone(pytz.timezone("America/New_York")))


class UserActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    activity_type = db.Column(db.String(), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    firstname = db.Column(db.String())
    lastname = db.Column(db.String())
    endpoint = db.Column(db.String(200), nullable=False)
    method = db.Column(db.String(50), nullable=False)

#@app.before_request
#def track_activity():
#    activity = UserActivity(user_id=current_user.id, endpoint=request.endpoint, method=request.method)
#    db.session.add(activity)
#    db.session.commit()

@app.errorhandler(500)
def internal_server_error(error):
    trace = traceback.format_exc()
    error = Error(message=str(error), time=datetime.utcnow(),traceback=trace )
    db.session.add(error)
    db.session.commit()

    message = client.messages \
    .create(
         body='An Internal Server Error Has Occured',
         from_=twilio_from,
         to='+15196707469'
     )

    flash("An internal error has occurred. The administrator has been notified.")
    return redirect(url_for('login'))
    
@app.errorhandler(AttributeError)
def handle_attribute_error(error):
    trace = traceback.format_exc()
    db.session.add(Error(message=str(error), traceback=trace, time=datetime.utcnow()))
    db.session.commit()

    #message = client.messages \
    #.create(
    #     body='An Attribute Error Has Occured',
    #     from_=twilio_from,
    #     to='+15196707469'
     #)

    flash("An Attribute Error has occurred. The administrator has been notified.")
    return redirect(url_for('login'))


@app.errorhandler(ValueError)
def handle_value_error(error):
    db.session.add(Error(message=str(error), time=datetime.utcnow()))
    db.session.commit()
    #message = client.messages \
    #.create(
    #     body='A Value Error Has Occured',
    #     from_=twilio_from,
    #     to='+15196707469'
    # )

    flash("A Value Error has occurred. The administrator has been notified.")
    return redirect(url_for('login'))
    


# here we initiate the datastore which is used in the Admin model


# feb 27 2021



class MyModelView(ModelView):
    can_export = True
    can_delete = False
    form_excluded_columns = ('password',)
    form_edit_rules = ('firstname','lastname', 'phone' ,'email', 'roles', 'active')
    column_sortable_list = ['lastname']
    column_list = ( 'firstname','lastname','user_name', 'active','created_on', 'updated_on', 'email','email_confirmed', 'email_confirmed_date','roles', 'phone')
    column_searchable_list = ['lastname', 'firstname']
    
    def is_accessible(self):
        return current_user.has_roles('Admin')
    

class MyModelView3(ModelView):
    can_export = True
    can_delete = False
    

class MyModelView2(ModelView):
    #create_modal = True
    #edit_modal = True
    can_export = True
    can_delete = False
    column_hide_backrefs = True
    #column_list = ('firstname', 'course', 'value')
    #column_list = ('employee_id', 'course_id')
    #column_editable_list = ['firstname', 'lastname']
    column_searchable_list = ['firstname', 'lastname']
    #list_columns = ['firstname','store']
    def is_accessible(self):
        return current_user.has_roles('Admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home'))
    
    def on_model_change(self, form, model, is_created):
         
        super().on_model_change(form, model, is_created)
    
class MyModelView6(ModelView):
    can_export = True
    can_delete = False

    def is_accessible(self):
        return current_user.has_roles('Admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home'))
    
class MyModelView3(ModelView):
    can_export = True
    can_delete = False

    def is_accessible(self):
        return current_user.has_roles('Manager')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home'))
    
class MyModelView4(ModelView):
    can_export = True
    can_delete = False

    def is_accessible(self):
        return current_user.has_roles('Admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home'))

class MyModelView5(ModelView):
    can_export = True
    can_delete = True
    column_hide_backrefs = False
    column_list = ('store', 'task')
    
    
    
    #column_select_related_list = (Todo.store, Todo.task)
    def is_accessible(self):
        return current_user.has_roles('Admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home'))

class MyModelView8(ModelView):
    can_export = True
    can_delete = True
    column_hide_backrefs = False
    form_args = {
        'incstore': {
            'query_factory': lambda: Store.query.order_by(Store.number)
                
        }
    }
    column_list = ('incstore', 'incident', 'details')
    #column_select_related_list = (Todo.store, Todo.task)
    

    def is_accessible(self):
        return current_user.has_roles('Admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home'))

class MyModelView9(ModelView):
    can_export = True
    can_delete = False
    column_hide_backrefs = False
    column_default_sort = ('saltdate', True)
    form_args = {
            'saltstore': {
                'query_factory': lambda: Store.query.order_by(Store.number)
                    
            }
        }
    column_list = ('saltstore','saltdate', 'area', 'gsa')
    #column_select_related_list = (Todo.store, Todo.task)

    def is_accessible(self):
        return current_user.has_roles('Admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home'))

class MyModelViewReclaim(ModelView):
    can_export = True
    can_delete = False
    column_hide_backrefs = False
    column_default_sort = ('reclaimdate', True)
    form_args = {
        'reclaimstore': {
            'query_factory': lambda: Store.query.filter_by(
                carwash = True
                ).order_by(Store.number)
        }
    }
    
    
    column_list = ('reclaimdate', 'reclaimstore', 'tankonewater','tankonesand', 'tanktwowater', 'tanktwosand', 'changepillows')
    #column_select_related_list = (Todo.store, Todo.task)

    def is_accessible(self):
        return current_user.has_roles('Admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home'))

class AdminViewStore(ModelView):
    
    column_sortable_list = ['number']
    
    def is_accessible(self):
            return current_user.has_roles('Admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home'))   
    
class AdminViewClass(ModelView):
    
    can_delete = True
    
    @action('publish to all staff', 'Approve', 'Are you sure you want to add this course toa ll')
    def action_approve(self, ids):
        id3 = request.form.get('rowid')
        id4 = int(id3) 
        print(id4)
        
        emps = Grade.query.all()
        gsa = Employee.query.all()
        for gsas in gsa:
            check = Grade.query.filter_by(employee_id=gsas.id, course_id = id4, ).first()
            if not check:
                print("emp" ,gsas.firstname, "nope")
                newcourse = Grade(completed=0, employee_id = gsas.id, course_id = id4)
                db.session.add(newcourse)
                
            else:
                print("emp", check.employee_id, "success")
        db.session.commit()    
        
        
    
    def is_accessible(self):
        return current_user.has_roles('Admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home'))

class AdminViewClass4(ModelView):
    can_export = True
    can_delete = False
    
    #column_sortable_list = ['Grade.employee']

    def is_accessible(self):
        return current_user.has_roles('Admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home'))

class hreditor(ModelView):
    form_overrides = dict(text=CKEditorField)
    
    column_exclude_list = ('text')
    create_template = 'create.html'
    edit_template = 'edit.html'

    can_delete = False
    def is_accessible(self):
        return current_user.has_roles('Admin')

class MyModelView10(ModelView):
    can_export = True
    can_delete = False
    column_hide_backrefs = False
    column_default_sort = ('maintaindate', True)
    form_args = {
        'maintainstore': {
            'query_factory': lambda: Store.query.order_by(Store.number)

        }
    }
    column_list = ('maintainstore', 'maintaindate', 'workdone', 'partsused')
    #column_select_related_list = (Todo.store, Todo.task)

    def is_accessible(self):
        return current_user.has_roles('Admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home'))

class MyModelView11(ModelView):
    can_export = True
    can_delete = False
    
   # emp = query.filter(Employee.id.notin_(Empfile.query.all()))
   # file = Empfile.query.with_entities(Empfile.employee2_id).distinct()

    #nofile = Employee.query.filter(
     #   Employee.id.notin_(file)).order_by(Employee.store)

    #def nofile_function(self):
     #   return Employee.query.filter(Employee.id.notin_(Empfile.query.with_entities(Empfile.employee2_id).distinct()))

    #form_args = {
     #   'firstname': {
      #      'query_factory': lambda: nofile_function

       # }
    #}
    #column_list = ('firstname')


    def is_accessible(self):
        return current_user.has_roles('Admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home'))

class EmailView(BaseView):
    @expose('/')
    def index(self):
        return self.render('send_email.html')
    
    can_delete = False

    def is_accessible(self):
        return current_user.has_roles('Admin')
    
class MyModelView12(ModelView):
    can_export = True
    can_delete = False

    def is_accessible(self):
        return current_user.has_roles('Admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home'))

class MyModelView14(ModelView):
    can_export = True
    can_delete = False

    def is_accessible(self):
        return current_user.has_roles('Admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home'))

class MyModelView15(ModelView):
    can_export = True
    can_delete = False
    #column_sortable_list = ['lastname']
    column_hide_backrefs = False
    #column_list = ( 'firstname','lastname','store','user_name', 'active','created_on', 'updated_on', 'email','email_confirmed', 'email_confirmed_date','roles', 'phone')
    #column_searchable_list = ['store']
    
    def is_accessible(self):
        return current_user.has_roles('Admin' )

class MyModelView16(ModelView):
    can_export = True
    can_delete = True

class RoleModelView(ModelView):
        pass
    
#class S3BucketView(BaseView):
#    @expose('/')
#    def index(self):
#        column_list = ('name', 'size', 'last_modified')
#        # Connect to Linode Object Storage
#        conn = boto.connect_s3(
#        aws_access_key_id = LINODE_ACCESS_KEY,
#        aws_secret_access_key = LINODE_SECRET_KEY,
#      host = LINODE_REGION,
        #is_secure=False,               # uncomment if you are not using ssl
#        calling_format = boto.s3.connection.OrdinaryCallingFormat(),
#        )

        # Retrieve a reference to your bucket
 #       bucket_name = 'paulfuther'
 #       bucket = conn.get_bucket(bucket_name)

 #       for key in bucket.list():
 #           print("{name}\t{size}\t{modified}".format(
 #               name = key.name,
 #               size = key.size,
  #              modified = key.last_modified,
  #          ))

        # Get the contents of the bucket
   #     contents = []
   #     for key in bucket.list():
   #         contents.append({
   #             'name': key.name,
   #             'size': key.size,
   #             'last_modified': key.last_modified,
   #         })
   #     print(contents)
#
     #   return self.render('s3_bucket_view.html', contents=contents)

     


# these are the views needed to display tables in the Admin section

admin.add_view(MyModelView(User, db.session))
admin.add_view(RoleModelView(Role, db.session))
admin.add_view(RoleModelView(Error, db.session))
admin.add_view(MyModelView2(Employee, db.session))
admin.add_view(MyModelView5(Todo, db.session))
admin.add_view(AdminViewStore(Store, db.session))
admin.add_view(AdminViewClass(Course, db.session))
admin.add_view(AdminViewClass4(Grade, db.session))
admin.add_menu_item(MenuLink(name='Main Site', url='/', category = "Links"))
admin.add_view(hreditor(hrfiles, db.session))
#admin.add_view(MyModelView8(Incidentnumbers, db.session, category = "Paul"))
admin.add_view(MyModelView9(Saltlog, db.session))
admin.add_view(MyModelViewReclaim(reclaimtank, db.session, category = "Paul"))
admin.add_view(MyModelView12(BulkEmailSendgrid, db.session, category="Paul"))
admin.add_view(MyModelView14(Twimlmessages, db.session, category="Paul"))
admin.add_view(MyModelView10(cwmaintenance, db.session, category = "Paul"))
admin.add_view(MyModelView15(checkinout, db.session, category = "Paul"))
admin.add_view(EmailView(name = 'Email', endpoint='email'))
#admin.add_view(MyModelView11(Employee, db.session))
#admin.add_view(EmailView(name = 'Email', endpoint='email'))
#admin.add_view(S3BucketView(name='Linode Object Storage'))
admin.add_view(MyModelView16(completedfile, db.session))

from flaskblog import routes


