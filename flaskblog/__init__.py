from flask import Flask,  jsonify, request, send_file, flash
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
from flaskblog import config
#from flaskblog import MySQL
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlalchemy.sql import text, select
from sqlalchemy import *
from flask_moment import Moment




APP_ROOT = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(APP_ROOT, 'Files')

#print(UPLOAD_FOLDER)


app = Flask(__name__)


app.config['SECRET_KEY'] = '302176f4723b5282ef5fbdfd77eccc50'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
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

app.register_blueprint(errors)