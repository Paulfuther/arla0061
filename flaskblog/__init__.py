
from flask import Flask

#import flask_login
app = Flask(__name__)

from dotenv import load_dotenv
from flask_ckeditor import CKEditor, CKEditorField, upload_fail, upload_success
import os
import json
#import pdfkit
from datetime import datetime
from flask import render_template_string, url_for, redirect, send_from_directory, request
from flask_admin import Admin, expose, BaseView
from flask_admin.actions import action
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, current_user, UserMixin, RoleMixin, login_required, roles_required
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



basedir = os.path.abspath(os.path.dirname(__file__))

# Flask and Flask-SQLAlchemy initialization here
#get variables

#!!!!!!!!!!!!!!!!!! you need the next three lines of code on the server#
# environment variables are hidden.....#

#with open('/etc/config.json') as config_file:
#	config = json.load(config_file)

#app=app.config.from_object(config) --not needed

load_dotenv()

# use evnironment variables while building
app.config['SECRET_KEY'] =os.environ.get('SECRET_KEY') 
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get('SECURITY_PASSWORD_SALT')
app.config['SECURITY_RECOVERABLE'] = False
app.config['SECURITY_CHANGEABLE'] = False
app.config['SECURITY_EMAIL_SENDER'] = ('NO-REPLY@LOCALHOST.COM')
app.config['MAIL_SERVER']= os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['EMAIL_VERIFIER_KEY']= os.environ.get('MAIL_VERIFIER_KEY')

app.config['MAIL_DEFAULT_SENDER'] = 'paul.futher@gmail.com'
app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'
# app.config['CKEDITOR_ENABLE_CSRF'] = True  # if you want to enable CSRF protect, uncomment this line
app.config['UPLOADED_PATH'] = os.path.join(basedir, 'images')


#app.config['CELERY_BROKER_URL'] = 'amqp://guest:guest@localhost'
#app.config['CELERY_BACKEND_URL'] = 'db+sqlite:///test.db'

verifier = EmailVerifier(app)

# initialize celery

#celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
#celery.conf.update(app.config)

@celery.task
def print_names(person):
    print(person)


    
@celery.task
def trythis():
    return "5"



db = SQLAlchemy(app)

# configure celery

#celery = Celery('tasks', broker='amqp://guest:guest@localhost')
#celery = celery

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
def add_this(x,y):
    return (x+y)

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


