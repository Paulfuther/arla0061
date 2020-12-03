
from flask import Flask
#import flask_login
app = Flask(__name__)

from flask_ckeditor import CKEditor, CKEditorField, upload_fail, upload_success
import os
import json
from datetime import datetime
from flask import render_template_string, url_for, redirect, send_from_directory
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, current_user, UserMixin, RoleMixin, login_required, roles_required
from flask_security.utils import hash_password
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, \
    String, ForeignKey

basedir = os.path.abspath(os.path.dirname(__file__))

# Flask and Flask-SQLAlchemy initialization here
#get variables


#with open('/etc/config.json') as config_file:
#	config = json.load(config_file)

#app=app.config.from_object(config) --not needed

#app.config['SECRET_KEY'] = config.get('SECRET_KEY')
#app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI')
#app.config['SECURITY_PASSWORD_SALT'] = config.get('SECURITY_PASSWORD_SALT')


#delte next three lines on server

app.config['SECRET_KEY'] = 'c164d8ed65cf46b1df5e336bd6adc4619a31830185f62b64'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECURITY_PASSWORD_SALT'] = '6598120c4f17a416e33707393c85f809e782eb99f66a4527'

app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'
# app.config['CKEDITOR_ENABLE_CSRF'] = True  # if you want to enable CSRF protect, uncomment this line
app.config['UPLOADED_PATH'] = os.path.join(basedir, 'images')

#delte above three on server

db = SQLAlchemy(app)
#USER_APP_NAME ="app"
ckeditor = CKEditor(app)


admin = Admin(app, name='Dashboard')
    
bcrypt = Bcrypt(app)
#login_manager = flask_login.LoginManager()
#login_manager.init_app(app)

#@login_manager.user_loader
#def load_user(user_id):
#    return User.query.get(int(user_id))

class hrfiles(db.Model):
    id = db.Column(db.Integer(), primary_key= True)
    title = db.Column(db.String(120))
    effective_date = db.Column(db.DateTime(), nullable=True)
    date_of_review = db.Column(db.DateTime(), nullable=True)
    text = db.Column(db.Text)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

roles_users = db.Table(
    'roles_users',
    
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(15), unique=False)
    lastname = db.Column(db.String(15), unique=False)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    roles = db.relationship('Role',  secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def has_roles(self, *args):
        return set(args).issubset({role.name for role in self.roles})

    def __str__(self):
        return 'User %r' % (self.firstname)

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
    firstname = db.Column(db.String(20), nullable=False)
    nickname = db.Column(db.String(20), nullable=True)
    lastname = db.Column(db.String(20), nullable=False)
    store = db.Column(db.Integer)
    addressone = db.Column(db.String(20), nullable=False)
    addresstwo = db.Column(db.String(20), nullable=True)
    apt = db.Column(db.String(20), nullable=True)
    city = db.Column(db.String(20), nullable=False)
    province = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(20), nullable=False)
    mobilephone = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    SIN = db.Column(db.Integer, unique=True, nullable=False)
    sinexpire = db.Column(db.DateTime(), nullable=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    startdate = db.Column(db.DateTime(), nullable=True)
    enddate = db.Column(db.DateTime(), nullable=True)
    postal = db.Column(db.String(6), nullable=False)
    trainingid = db.Column(db.String(), nullable=False)
    trainingpassword = db.Column(db.String(), nullable=False)
    manager = db.Column(db.String)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    active = db.Column(db.String(), nullable = False)
    iprismcode = db.Column(db.String(9), nullable=False)
    
    
    #course = db.relationship('Course',  secondary=course_employee,
    #                     backref=db.backref('employees', lazy='dynamic'))
    #grade = db.relationship('Grade', secondary = course_employee,
    #                          backref = db.backref('grades', lazy = 'dynamic'))
    #course_id2 = db.Column(db.Integer(), ForeignKey('course.id'))
    #course = db.relationship('Course', secondary = course_employee, backref='gradess')
    
    def __str__(self):
        return (self.firstname)

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
 
class Empfile(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    employee2_id = db.Column(Integer(), ForeignKey('employee.id'))
    employee2 = db.relationship('Employee', backref = 'files')
    file_id = db.Column(db.Integer(), ForeignKey('hrfiles.id'))
    file = db.relationship('hrfiles', backref = 'filess') 
    sig_data = db.Column(db.Integer())
    
task_store = db.Table(
    'task_store',
    db.Column('todo_id', db.Integer(), db.ForeignKey('todo.id')),
    db.Column('store_id', db.Integer(), db.ForeignKey('store.id'))
)
       
class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    
    def __repr__(self):
        return '%r' % (self.number)
    
class Todo(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200))
    store = db.relationship('Store',  secondary=task_store,
                            backref=db.backref('users', lazy='dynamic'))
    
    def __repr__(self):
           return '%r' % (self.task)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

#create a user to test with


class MyModelView(ModelView):
    can_export = True
    can_delete = False
    #column_sortable_list = ['lastname']
    column_hide_backrefs = False
    column_list = ('firstname', 'roles')

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
    column_hide_backrefs = False
    column_list = ('firstname', 'course', 'value')
    #column_list = ('employee_id', 'course_id')

    def is_accessible(self):
        return current_user.has_roles('Admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home'))
    
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
    can_delete = True

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

class AdminViewStore(ModelView):
    
    column_sortable_list = ['number']
    
    def is_accessible(self):
            return current_user.has_roles('Admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home'))   
    
class AdminViewClass(ModelView):
    
   
    
    def is_accessible(self):
        return current_user.has_roles('Admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home'))


class AdminViewClass4(ModelView):
    can_export = True
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


#class GradeView(ModelView):
    #form_columns = ('course',)
#    inline_models = ((
#        course_employee,
#        {
#            'form_columns': ('id', 'Employee_id', 'Course_id', 'Completed'),
#        }
#    ),)


admin.add_view(MyModelView(User, db.session))

admin.add_view(MyModelView6(Role, db.session))

admin.add_view(MyModelView2(Employee, db.session))

admin.add_view(MyModelView5(Todo, db.session))

admin.add_view(AdminViewStore(Store, db.session))

#admin.add_view(AdminViewClass(Course, db.session))
admin.add_view(AdminViewClass(Course, db.session))

admin.add_view(AdminViewClass4(Grade, db.session))

admin.add_menu_item(MenuLink(name='Main Site', url='/', category = "Links"))

admin.add_view(hreditor(hrfiles, db.session))



from flaskblog import routes


