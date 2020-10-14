
#from database import Base
#from flaskblog import db, login_manager
#from flask_login import UserMixin, LoginManager, current_user
#from flask_security import Security, SQLAlchemyUserDatastore, RoleMixin, utils
#from flask_security.utils import hash_password, encrypt_password, verify_password
#from flask_bcrypt import Bcrypt
#from sqlalchemy.ext.hybrid import hybrid_property
#from flask.ext.bcrypt import generate_password_hash
#from flask_sqlalchemy import SQLAlchemy


#@login_manager.user_loader
#def load_user(user_id):
#    return User.query.get(int(user_id))

#db = SQLAlchemy




#class Course(db.Model, RoleMixin):
#    id = db.Column(db.Integer(), primary_key = True)
#    name = db.Column(db.String(50), unique=True)
#    description = db.Column(db.String(255))
#    startdate  = db.Column(db.DateTime(), nullable=False)
    
                             
#   def __repr__(self):
#         return ' %r' % (self.name)


#class CourseDetails(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    startdate = db.Column(db.DateTime(), nullable=False)
#    course = db.Column(db.Integer, db.ForeignKey('course.id'))



    
    
    #@hybrid_property
    #def SIN(self):
    #    return self._SIN
    
    #@SIN.setter
    #def SIN(self, plaintext):
    #    self._SIN = bcrypt.generate_password_hash(plaintext).decode('utf-8')


#admin = Admin()


