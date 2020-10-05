
from flask_security import utils, SQLAlchemyUserDatastore
from flask import Flask,  jsonify, request, send_file, flash, url_for, redirect
from random import sample
from flask_mysqldb import MySQL
from flask_moment import Moment
from datetime import time, datetime
import os
from werkzeug.utils import secure_filename
import pandas as pd
import numpy
import openpyxl
import xlrd
import xlwt
import xlsxwriter
from datetime import datetime
from io import BytesIO
from openpyxl.reader.excel import load_workbook
from os import environ
import re
import datetime as dt
import glob
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flaskblog.config import Config
#from flaskblog import MySQL
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlalchemy.sql import text, select
from sqlalchemy import *
from flask_moment import Moment

from flask_admin import Admin

from flask_admin.contrib.sqla import ModelView




APP_ROOT = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(APP_ROOT, 'Files')

#print(UPLOAD_FOLDER)

app = Flask(__name__)
app.config.from_object(Config)





#app.config.from_object("config.ProductionConfig")
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
moment = Moment(app)
login_manager=LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

#engine = create_engine('mysql://root:root@localhost/work')
#meta=MetaData(engine).reflect()
#metadata = MetaData(engine)
#db2 = engine
#print(engine.table_names())

     
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mysql = MySQL(app)
Bootstrap(app)
moment = Moment(app)

from flaskblog import routes
from flaskblog.errors.handlers import errors
from flaskblog.models import User, Role,  Employee, current_user, Security
from flask_security.utils import encrypt_password, hash_password
from flask_admin.menu import MenuLink

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

admin = Admin(app)#


#@app.before_first_request
#def create_user():
    
 #   user_datastore.create_user(email='admin', password='admin1234')#, firstname=" ", lastname=" ", active=" ", confirmed_at= " ")
  #  db.session.commit()


    

class MyModelView(ModelView):
    can_export = True
    can_delete = False
    column_exclude_list = ('password')
    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home'))
    def is_accessible(self):
        return current_user.has_roles('Admin')
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

class OtherView(ModelView):
    can_export = True
    can_delete = False


admin.add_view(MyModelView(User, db.session))
#class PositionView(ModelView):
 #   form_columns = ['id', 'roles']

admin.add_view(OtherView(Employee, db.session))
#admin.add_view(ModelView(User, db.session))
#admin.add_view(ModelView(Employee, db.session))
admin.add_view(MyModelView(Role, db.session))
#admin.add_view(OtherView(Course, db.session))
#admin.add_view(OtherView(CourseDetails, db.session))
#admin.add_link(MenuLink(name='Home', category='', url=url_for('/home')))
app.register_blueprint(errors)
