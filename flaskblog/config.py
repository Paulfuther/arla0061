from flask_admin.contrib.sqla import ModelView
import os
from flask_admin import Admin




class Config:
    
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLAlCHEMY_DATABASE_URI')
    #SECURITY_PASSWORD_HASH = os.environ.get('SECURITY_PASSWORD_HASH')
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')



class ProductionConfig(Config):
    MYSQL_PASSWORD = 'root'
    MYSQL_USER = 'root'
    MYSQL_HOST = 'localhost'
    MYSQL_DB = 'work'
    MYSQL_PORT = 3306
