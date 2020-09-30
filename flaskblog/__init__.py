
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
from flaskblog.models import User, Role,  Employee, current_user

admin = Admin(app)


class MyModelView(ModelView):
    can_export = True
    can_delete = False
    def is_accessible(self):
        
        return current_user.is_authenticated
        
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home'))

admin.add_view(MyModelView(User, db.session))
#class PositionView(ModelView):
 #   form_columns = ['id', 'roles']

admin.add_view(MyModelView(Employee, db.session))
#admin.add_view(ModelView(User, db.session))
#admin.add_view(ModelView(Employee, db.session))
admin.add_view(MyModelView(Role, db.session))
app.register_blueprint(errors)
