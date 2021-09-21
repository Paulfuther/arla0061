
from flask import Flask

app = Flask(__name__)

from dotenv import load_dotenv
from flask_ckeditor import CKEditor, CKEditorField, upload_fail, upload_success
import os
import json
from datetime import datetime
from flask import render_template_string, make_response, url_for, redirect, send_from_directory, \
     request, render_template, send_file
from flask_admin import Admin, expose, BaseView
from flask_admin.actions import action
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, current_user, \
     UserMixin, RoleMixin, login_required, roles_required
from flask_security.utils import hash_password
from flask_admin.contrib.sqla import ModelView
from flask_marshmallow import Marshmallow
from marshmallow import Schema
from flask_admin.menu import MenuLink
from flask_bcrypt import Bcrypt, generate_password_hash
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, \
    String, ForeignKey
from flask_mail import Mail, Message
from flask_email_verifier import EmailVerifier
from flask_login import  user_logged_out, user_logged_in
from celery import Celery
from flaskblog.tasks import celery
import dropbox
from dropbox.files import WriteMode
import pdfkit
from io import BytesIO

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()

# use evnironment variables while building
app.config['SECRET_KEY'] =os.environ.get('SECRET_KEY') 
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get('SECURITY_PASSWORD_SALT')
app.config['SECURITY_RECOVERABLE'] = False
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

DROP_BOX_KEY = os.environ.get('DROP_BOX_KEY')

verifier = EmailVerifier(app)
db = SQLAlchemy(app)
dbx = dropbox.Dropbox(DROP_BOX_KEY)
ma = Marshmallow(app)
ckeditor = CKEditor(app)
mail = Mail(app)

@celery.task
def send_async_email(email_data):
    """Background task to send an email with Flask-Mail."""
    msg = Message(email_data['subject'],
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email_data['to']])
    msg.body = email_data['body']
    with app.app_context():
        mail.send(msg)


@celery.task
def send_async_email2(email_data):
    """Background task to send an email with Flask-Mail."""
    msg = Message(email_data['subject'],
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email_data['to']])
    msg.body = email_data['body']
    with app.app_context():
        mail.send(msg)

@celery.task
def make_pdf(staff_id):
    with app.test_request_context():
        signatures = Empfile.query.filter_by(employee2_id = staff_id)
        rol =  User.query.filter(User.roles.any(Role.id == 3)).all()
    
         


        img = '/files/image-20201205212708-1.png'

        image1 = '/Users/paulfuther/arla0061/flaskblog/images/image-20201205212708-1.png'
        image2 = '/Users/paulfuther/arla0061/flaskblog/images/image-20201205213750-1.png'
        image3 = '/Users/paulfuther/arla0061/flaskblog/images/image-20201205213046-1.png '
        image4 = '/Users/paulfuther/arla0061/flaskblog/images/image-20201205213057-2.png'
        image5 = '/Users/paulfuther/arla0061/flaskblog/images/uniformfour.png'
        image6 = '/Users/paulfuther/arla0061/flaskblog/images/uniformthree.png' 


        x=signatures
        hrpage = hrfiles.query.all()
        gsa = Employee.query.get(staff_id)
        fname = gsa.firstname
        lname = gsa.lastname
        id = gsa.id
        print(fname)
    
        rendered = render_template('employeefilepdf.html',image1=image1, image2=image2, image3 = image3, image4 = image4, image5=image5, image6=image6,hrpage = hrpage, signatures=signatures, gsa=gsa)
    
        

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
        filename = f" {lname} {fname}  ID  {id} {created_on}.pdf"

        #response = make_response(pdf)
        #response.headers['Content-Type']='application/pdf'
        #response.headers['Content-Disposition']='inline'

        for x in rol:
            email = x.email
            email_data = {
                'subject': 'A new hire file has been created',
                'to': email,
                'body': 'A new hire file has been created and uploaded to dropbox. {}'.format(filename),
               
            }

            msg = Message(email_data['subject'],
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email_data['to']])
            msg.body = email_data['body']
            msg.attach("pdf","application/pdf", pdf)
            mail.send(msg)
        
        with file as f:    
            dbx.files_upload(f.read(), path=f"/NEWHRFILES/{filename}", mode=WriteMode('overwrite'))
    
        
        #file = BytesIO(pdf)
        #return (file),{
        #    'Content-Type': 'application/pdf',
        #    'Content-Disposition': 'inline'
        #   }
        
        
        #return send_file(file,
        #         attachment_filename=filename,
        #         mimetype='application/pdf',
        #         as_attachment=True,
        #         cache_timeout=1
        #          )      

       

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
    db.Column('store_id', db.Integer(), db.ForeignKey('store.id'))
)

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

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean, default = True)
    confirmed_at = db.Column(db.DateTime)
    user_name = db.Column(db.String(100), nullable=False)
    
    # new additions 
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 
       
    #employee = db.relationship('Customer', backref= 'user', uselist = False)
    roles = db.relationship('Role',  secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.roles is  None:
            self.roles = Role.query.filter_by(name="GSA").first()
    
    def has_roles(self, *args):
        return set(args).issubset({role.name for role in self.roles})

    def __str__(self):
        return (self.user_name) 
    
    
        
 

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '%r' % (self.name)

    def __hash__(self):
        return hash(self.name)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    firstname = db.Column(db.String(20), nullable=False)
    nickname = db.Column(db.String(20), nullable=True)
    lastname = db.Column(db.String(20), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    store = db.relationship('Store', backref = 'store')
    addressone = db.Column(db.String(20), nullable=False)
    addresstwo = db.Column(db.String(20), nullable=True)
    apt = db.Column(db.String(20), nullable=True)
    city = db.Column(db.String(20), nullable=False)
    province = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(20), nullable=False)
    mobilephone = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), nullable=False)
   
    sinexpire = db.Column(db.DateTime(), nullable=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    startdate = db.Column(db.DateTime(), nullable=True)
    enddate = db.Column(db.DateTime(), nullable=True)
    postal = db.Column(db.String(6), nullable=False)
    trainingid = db.Column(db.String(),unique=True, nullable=False)
    trainingpassword = db.Column(db.String(), nullable=False)
    manager = db.Column(db.Integer)
    image_file = db.Column(db.String(50), nullable=False,
                           default='default.jpg')
    
    iprismcode = db.Column(db.String(9), nullable=False)
    dob = db.Column(db.DateTime(), nullable=True)
   
    mon_avail = db.Column(db.String(100), nullable=False)
    tue_avail = db.Column(db.String(100), nullable=False)
    wed_avail = db.Column(db.String(100), nullable=False)
    thu_avail = db.Column(db.String(100), nullable=False)
    fri_avail = db.Column(db.String(100), nullable=False)
    sat_avail = db.Column(db.String(100), nullable=False)
    sun_avail = db.Column(db.String(100), nullable=False)
    
   
    
    def __str__(self):
        return (self.firstname) 

class EmployeeSchema(ma.Schema):
    class Meta:
        model = Employee
        store = ma.Nested("StoreSchema", exclude=("store",))
        fields = ('id', 'firstname', 'lastname', 'email', 'store_id', 'image_file', 'number')
        
        
employee_schema = EmployeeSchema(many=True)

class Course(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)  
    
    
    def __str__(self):
        return '%r' % (self.name)
   
class Grade(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    value = db.Column(db.String(), default="n")
    employee_id = db.Column(Integer(), ForeignKey('employee.id'))
    employee = db.relationship('Employee', backref = 'grades')
    course_id = db.Column(db.Integer(), ForeignKey('course.id'))
    course = db.relationship('Course', backref='grade')
    completeddate = db.Column(db.String(),  nullable=True)
      
class staffschedule(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    employee_id = db.Column(Integer(), ForeignKey('employee.id'))
    employee = db.relationship('Employee', backref = 'schedule')
    storeworked = db.Column(db.String())
    shift_description = db.Column(db.String())
    shift_hours = db.Column(db.Integer())
    shift_date = db.Column(db.Date)
 
class Empfile(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    employee2_id = db.Column(Integer(), ForeignKey('employee.id'))
    employee2 = db.relationship('Employee', backref = 'files')
    file_id = db.Column(db.Integer(), ForeignKey('hrfiles.id'))
    file = db.relationship('hrfiles', backref = 'filess') 
    sig_data = db.Column(db.Integer())
    
class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    carwash =  db.Column(db.Boolean, default = False)
    
    def __repr__(self):
        return str(self.number)
   
class StoreSchema(ma.Schema):
    class Meta:
        model = Store
        
    
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


class siteincident(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     injuryorillness = db.Column(db.Boolean, default = False)
     environmental = db.Column(db.Boolean, default = False)
     regulatory = db.Column(db.Boolean, default = False)
     economicDamage = db.Column(db.Boolean, default = False)
     reputation = db.Column(db.Boolean, default = False)
     security = db.Column(db.Boolean, default = False)
     fire = db.Column(db.Boolean, default = False)

     location = db.Column(db.String())

     eventdetails = db.Column(db.String())
     eventdate = db.Column(db.DateTime(), nullable = True)
     eventtime = db.Column(db.String())
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




# here we initiate the datastore which is used in the Admin model

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

#create a user to test with





#@user_registered.connect_via(app)
#def user_registered_sighandler(app, user, confirm_token):
#    default_role = user_datastore.find_role('GSA')
#    user_datastore.add_role_to_user(user, default_role)
#    db.session.commit()



class MyModelView(ModelView):
    can_export = True
    can_delete = False
    #column_sortable_list = ['lastname']
    column_hide_backrefs = False
    column_list = ( 'user_name', 'active','created_on', 'updated_on', 'roles')
    column_searchable_list = ['user_name']
    def is_accessible(self):
        return current_user.has_roles('Admin' )
    
    

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home'))

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.password = hash_password(form.password.data)
        else:
            old_password = form.password.object_data
            # If password has been changed, hash password
            if not old_password == model.password:
                model.password = hash_password(form.password.data)

class MyModelView2(ModelView):
    can_export = True
    can_delete = False
    #column_hide_backrefs = False
    #column_list = ('firstname', 'course', 'value')
    #column_list = ('employee_id', 'course_id')
    column_searchable_list = ['firstname']
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
    
    can_delete = False
    
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
                newcourse = Grade(value="n", employee_id = gsas.id, course_id = id4)
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
    

    
# these are the views needed to display tables in the Admin section

admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView6(Role, db.session))
admin.add_view(MyModelView2(Employee, db.session))
admin.add_view(MyModelView5(Todo, db.session))
admin.add_view(AdminViewStore(Store, db.session))
admin.add_view(AdminViewClass(Course, db.session))
admin.add_view(AdminViewClass4(Grade, db.session))
admin.add_menu_item(MenuLink(name='Main Site', url='/', category = "Links"))
admin.add_view(hreditor(hrfiles, db.session))
admin.add_view(MyModelView8(Incidentnumbers, db.session, category = "Paul"))
admin.add_view(MyModelView9(Saltlog, db.session))
admin.add_view(MyModelViewReclaim(reclaimtank, db.session, category = "Paul"))
admin.add_view(MyModelView10(cwmaintenance, db.session, category = "Paul"))
#admin.add_view(MyModelView11(Employee, db.session))
admin.add_view(EmailView(name = 'Email', endpoint='email'))
#admin.add_sub_category(name = "Links", parent_name="Team")

from flaskblog import routes


