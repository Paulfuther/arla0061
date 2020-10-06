from flaskblog import db, login_manager
from flaskblog import datetime
from flask_login import UserMixin, LoginManager, current_user
from flask_security import Security, SQLAlchemyUserDatastore, RoleMixin, utils
from flask_security.utils import hash_password, encrypt_password, verify_password
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
#from flask.ext.bcrypt import generate_password_hash



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

#course_users = db.Table(
 #   'course_users',
 #   db.Column('employee_id', db.Integer(), db.ForeignKey('employee.id')),
 #   db.Column('course_id', db.Integer(), db.ForeignKey('course.id')))
    


#course_data = db.Table(
#    'course_data',
#    db.Column('coursedetails_id', db.Integer(), db.ForeignKey('coursedetails.id')),
#    db.Column('course_id', db.Integer(), db.ForeignKey('course.id'))
#)



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(15), unique=True)
    lastname = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    roles = db.relationship('Role',  secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
       
    def has_roles(self, *args):
        return set(args).issubset({role.name for role in self.roles})
    
    def __str__(self):
        return 'User %r' % (self.firstname)
    
    
    
    
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))
    
    def __repr__(self):
        return '%r' % (self.name)
    
    def __hash__(self):
        return hash(self.name)

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


class Employee(db.Model):
    id=db.Column(db.Integer, primary_key=True)
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
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    Startdate = db.Column(db.DateTime(), nullable=True)
    Enddate = db.Column(db.DateTime(), nullable=True)
    postal = db.Column(db.String(6), nullable=False)
    trainingid = db.Column(db.String(), nullable=False)
    trainingpassword = db.Column(db.String(), nullable=False)
    manager = db.Column(db.String)
    image_file = db.Column(db.String(20), nullable=False,default='default.jpg')
    active = db.Column(db.String)
    iprismcode = db.Column(db.String(9), nullable=False)
    #course = db.relationship('Course',  secondary=course_users,
     #                       backref=db.backref('users', lazy='dynamic'))
    
    # tobacco training#
    tobstartdate = db.Column(db.DateTime(), nullable=True)
    tobcompleted = db.Column(db.String)
    tobexpireydate = db.Column(db.DateTime(), nullable=True)
    tobcompliant = db.Column(db.String(), nullable=False)
    #whmis training#
    whmisstartdate = db.Column(db.DateTime(), nullable=True)
    whmiscompleted = db.Column(db.String)
    whmisexpireydate = db.Column(db.DateTime(), nullable=True)
    whmiscompliant = db.Column(db.String(), nullable=False)
    #ppe training#
    ppestartdate = db.Column(db.DateTime(), nullable=True)
    ppecompleted = db.Column(db.String)
    ppeexpireydate = db.Column(db.DateTime(), nullable=True)
    ppecompliant = db.Column(db.String(), nullable=False)
    #fire extinguisher training#
    firestartdate = db.Column(db.DateTime(), nullable=True)
    firecompleted = db.Column(db.String)
    fireexpireydate = db.Column(db.DateTime(), nullable=True)
    firecompliant = db.Column(db.String(), nullable=False)
    #emergency response procedures training#
    emerstartdate = db.Column(db.DateTime(), nullable=True)
    emercompleted = db.Column(db.String)
    emerexpireydate = db.Column(db.DateTime(), nullable=True)
    emercompliant = db.Column(db.String(), nullable=False)
    #first aid training#
    firstaidstartdate = db.Column(db.DateTime(), nullable=True)
    firstaidcompleted = db.Column(db.String)
    firstaidexpireydate = db.Column(db.DateTime(), nullable=True)
    firstaidcompliant = db.Column(db.String(), nullable=False)
    #food handling traning#
    foodstartdate = db.Column(db.DateTime(), nullable=True)
    foodcompleted = db.Column(db.String)
    foodexpireydate = db.Column(db.DateTime(), nullable=True)
    foodcompliant = db.Column(db.String(), nullable=False)
    #propane handling training#
    propanestartdate = db.Column(db.DateTime(), nullable=True)
    propanecompleted = db.Column(db.String)
    propaneexpireydate = db.Column(db.DateTime(), nullable=True)
    propanecompliant = db.Column(db.String(), nullable=False)
    #health and safety training#
    hsstartdate = db.Column(db.DateTime(), nullable=True)
    hscompleted = db.Column(db.String)
    hsexpireydate = db.Column(db.DateTime(), nullable=True)
    hscompliant = db.Column(db.String(), nullable=False)
    #fule pump shut off training#
    fuelstartdate = db.Column(db.DateTime(), nullable=True)
    fuelcompleted = db.Column(db.String)
    fuelexpireydate = db.Column(db.DateTime(), nullable=True)
    fuelcompliant = db.Column(db.String(), nullable=False)
    #work alone training#
    alonestartdate = db.Column(db.DateTime(), nullable=True)
    alonecompleted = db.Column(db.String)
    aloneexpireydate = db.Column(db.DateTime(), nullable=True)
    alonecompliant = db.Column(db.String(), nullable=False)
    #workplace violence and harrassment traiing#
    violencestartdate = db.Column(db.DateTime(), nullable=True)
    violencecompleted = db.Column(db.String)
    violenceexpireydate = db.Column(db.DateTime(), nullable=True)
    violencecompliant = db.Column(db.String(), nullable=False)
    #joint health and safety training#
    jointstartdate = db.Column(db.DateTime(), nullable=True)
    jointcompleted = db.Column(db.String)
    jointexpireydate = db.Column(db.DateTime(), nullable=True)
    jointcompliant = db.Column(db.String(), nullable=False)
    
    
    #@hybrid_property
    #def SIN(self):
    #    return self._SIN
    
    #@SIN.setter
    #def SIN(self, plaintext):
    #    self._SIN = bcrypt.generate_password_hash(plaintext).decode('utf-8')
