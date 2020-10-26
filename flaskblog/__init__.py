from flask import Flask
#import flask_login
app = Flask(__name__)


#from flask_user import roles_required, UserManager, SQLAlchemyAdapter
#from flaskblog import config
import os
import json
from datetime import datetime

from flask import render_template_string, url_for, redirect
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.ext.hybrid import hybrid_property
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, current_user, UserMixin, RoleMixin, login_required, roles_required
from flask_security.utils import hash_password
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
#from flaskblog.config import Config
from flask_bcrypt import Bcrypt


from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, \
    String, ForeignKey

# Flask and Flask-SQLAlchemy initialization here
#get variables


#with open('/etc/config.json') as config_file:
#	config = json.load(config_file)

#app=app.config.from_object(config) --not needed

#app.config['SECRET_KEY'] = config.get('SECRET_KEY')
#app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI')
#app.config['SECURITY_PASSWORD_SALT'] = config.get('SECURITY_PASSWORD_SALT')


#delte next three lines on server



#delte above three on server

db = SQLAlchemy(app)
#USER_APP_NAME ="app"


admin = Admin(app, name='Dashboard')
    
bcrypt = Bcrypt(app)
#login_manager = flask_login.LoginManager()
#login_manager.init_app(app)

#@login_manager.user_loader
#def load_user(user_id):
#    return User.query.get(int(user_id))

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(15), unique=True)
    lastname = db.Column(db.String(15), unique=True)
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
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    Startdate = db.Column(db.DateTime(), nullable=True)
    Enddate = db.Column(db.DateTime(), nullable=True)
    postal = db.Column(db.String(6), nullable=False)
    trainingid = db.Column(db.String(), nullable=False)
    trainingpassword = db.Column(db.String(), nullable=False)
    manager = db.Column(db.String)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    active = db.Column(db.String)
    iprismcode = db.Column(db.String(9), nullable=False)
    #course = db.relationship('Course',  secondary=course_users,
    #                       backref=db.backref('users', lazy='dynamic'))

    # tobacco training#
    tobstartdate = db.Column(db.DateTime(), nullable=True)
    tobcompleted = db.Column(db.DateTime(), nullable=True)
    tobexpireydate = db.Column(db.DateTime(), nullable=True)
    tobcompliant = db.Column(db.String(), nullable=False)
    #whmis training#
    whmisstartdate = db.Column(db.DateTime(), nullable=True)
    whmiscompleted = db.Column(db.DateTime(), nullable=True)
    whmisexpireydate = db.Column(db.DateTime(), nullable=True)
    whmiscompliant = db.Column(db.String(), nullable=False)
    #ppe training#
    ppestartdate = db.Column(db.DateTime(), nullable=True)
    ppecompleted = db.Column(db.DateTime(), nullable=True)
    ppeexpireydate = db.Column(db.DateTime(), nullable=True)
    ppecompliant = db.Column(db.String(), nullable=False)
    #fire extinguisher training#
    firestartdate = db.Column(db.DateTime(), nullable=True)
    firecompleted = db.Column(db.DateTime(), nullable=True)
    fireexpireydate = db.Column(db.DateTime(), nullable=True)
    firecompliant = db.Column(db.String(), nullable=False)
    #emergency response procedures training#
    emerstartdate = db.Column(db.DateTime(), nullable=True)
    emercompleted = db.Column(db.DateTime(), nullable=True)
    emerexpireydate = db.Column(db.DateTime(), nullable=True)
    emercompliant = db.Column(db.String(), nullable=False)
    #first aid training#
    firstaidstartdate = db.Column(db.DateTime(), nullable=True)
    firstaidcompleted = db.Column(db.DateTime(), nullable=True)
    firstaidexpireydate = db.Column(db.DateTime(), nullable=True)
    firstaidcompliant = db.Column(db.String(), nullable=False)
    #food handling traning#
    foodstartdate = db.Column(db.DateTime(), nullable=True)
    foodcompleted = db.Column(db.DateTime(), nullable=True)
    foodexpireydate = db.Column(db.DateTime(), nullable=True)
    foodcompliant = db.Column(db.String(), nullable=False)
    #propane handling training#
    propanestartdate = db.Column(db.DateTime(), nullable=True)
    propanecompleted = db.Column(db.DateTime(), nullable=True)
    propaneexpireydate = db.Column(db.DateTime(), nullable=True)
    propanecompliant = db.Column(db.String(), nullable=False)
    #health and safety training#
    hsstartdate = db.Column(db.DateTime(), nullable=True)
    hscompleted = db.Column(db.DateTime(), nullable=True)
    hsexpireydate = db.Column(db.DateTime(), nullable=True)
    hscompliant = db.Column(db.String(), nullable=False)
    #fule pump shut off training#
    fuelstartdate = db.Column(db.DateTime(), nullable=True)
    fuelcompleted = db.Column(db.DateTime(), nullable=True)
    fuelexpireydate = db.Column(db.DateTime(), nullable=True)
    fuelcompliant = db.Column(db.String(), nullable=False)
    #work alone training#
    alonestartdate = db.Column(db.DateTime(), nullable=True)
    alonecompleted = db.Column(db.DateTime(), nullable=True)
    aloneexpireydate = db.Column(db.DateTime(), nullable=True)
    alonecompliant = db.Column(db.String(), nullable=False)
    #workplace violence and harrassment traiing#
    violencestartdate = db.Column(db.DateTime(), nullable=True)
    violencecompleted = db.Column(db.DateTime(), nullable=True)
    violenceexpireydate = db.Column(db.DateTime(), nullable=True)
    violencecompliant = db.Column(db.String(), nullable=False)
    #joint health and safety training#
    jointstartdate = db.Column(db.DateTime(), nullable=True)
    jointcompleted = db.Column(db.DateTime(), nullable=True)
    jointexpireydate = db.Column(db.DateTime(), nullable=True)
    jointcompliant = db.Column(db.String(), nullable=False)
    #co2 alarm training#
    co2startdate = db.Column(db.DateTime(), nullable=True)
    co2completed = db.Column(db.DateTime(), nullable=True)
    co2expireydate = db.Column(db.DateTime(), nullable=True)
    co2compliant = db.Column(db.String(), nullable=False)
    

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

#db_adapter = SQLAlchemyAdapter(db, User)
#user_manager = UserManager(db_adapter,app)

#create a user to test with


class MyModelView(ModelView):
    can_export = True
    can_delete = False
    #column_sortable_list = ['lastname']

    def is_accessible(self):
        return current_user.has_roles('Admin' , 'Manager')
    
    

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


admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView2(Role, db.session))
admin.add_view(MyModelView2(Employee, db.session))
#admin.add_view(MyModelView3(Employee, db.session))
admin.add_menu_item(MenuLink(name='Main Site', url='/', category = "Links"))


from flaskblog import routes


