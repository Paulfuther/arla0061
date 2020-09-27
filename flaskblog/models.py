from flaskblog import db, login_manager
from flaskblog import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

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

    
    #traiing#
    
    whmis = db.relationship(
        'whmis', backref='employee', uselist=False)  
    ppe = db.relationship(
        'ppe', backref='employee', uselist=False)
    fireextinguishers = db.relationship(
        'fireextinguishers', backref='employee', uselist=False)
    emergencyresponseprocedures = db.relationship(
        'emergencyresponseprocedures', backref='employee', uselist=False)
    firstaid = db.relationship(
        'firstaid', backref='employee', uselist=False)
    foodhandling = db.relationship(
        'foodhandling', backref='employee', uselist=False)
    propane = db.relationship(
        'propane', backref='employee', uselist=False)
    healthandsafety = db.relationship(
        'healthandsafety', backref='employee', uselist=False)
    fuelpumpshutoff = db.relationship(
        'fuelpumpshutoff', backref='employee', uselist=False)
    workingalone = db.relationship(
        'workingalone', backref='employee', uselist=False)
    workplaceviolence = db.relationship(
        'workplaceviolence', backref='employee', uselist=False)
    jointhealthandsafety = db.relationship(
        'jointhealthandsafety', backref='employee', uselist=False)
    
    #def __repr__(self):
     #   return f"Employee('{self.firstname}', '{self.SIN}')"

class whmis(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    startdate = db.Column(db.DateTime(), nullable=True)
    completed = db.Column(db.String)
    datequalified = db.Column(db.DateTime(), nullable=True)
    expireydate = db.Column(db.DateTime(), nullable=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    compliant = db.Column(db.String)
    
class ppe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    startdate = db.Column(db.DateTime(), nullable=True)
    completed = db.Column(db.String)
    datequalified = db.Column(db.DateTime(), nullable=True)
    expireydate = db.Column(db.DateTime(), nullable=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    compliant = db.Column(db.String)

class fireextinguishers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    startdate = db.Column(db.DateTime(), nullable=True)
    completed = db.Column(db.String)
    datequalified = db.Column(db.DateTime(), nullable=True)
    expireydate = db.Column(db.DateTime(), nullable=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    compliant = db.Column(db.String)

class emergencyresponseprocedures(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    startdate = db.Column(db.DateTime(), nullable=True)
    completed = db.Column(db.String)
    datequalified = db.Column(db.DateTime(), nullable=True)
    expireydate = db.Column(db.DateTime(), nullable=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    compliant = db.Column(db.String)

class firstaid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    startdate = db.Column(db.DateTime(), nullable=True)
    completed = db.Column(db.String)
    datequalified = db.Column(db.DateTime(), nullable=True)
    expireydate = db.Column(db.DateTime(), nullable=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    compliant = db.Column(db.String)

class foodhandling(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    startdate = db.Column(db.DateTime(), nullable=True)
    completed = db.Column(db.String)
    datequalified = db.Column(db.DateTime(), nullable=True)
    expireydate = db.Column(db.DateTime(), nullable=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    compliant = db.Column(db.String)

class propane(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    startdate = db.Column(db.DateTime(), nullable=True)
    completed = db.Column(db.String)
    datequalified = db.Column(db.DateTime(), nullable=True)
    expireydate = db.Column(db.DateTime(), nullable=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    compliant = db.Column(db.String)

class healthandsafety(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    startdate = db.Column(db.DateTime(), nullable=True)
    completed = db.Column(db.String)
    datequalified = db.Column(db.DateTime(), nullable=True)
    expireydate = db.Column(db.DateTime(), nullable=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    compliant = db.Column(db.String)

class fuelpumpshutoff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    startdate = db.Column(db.DateTime(), nullable=True)
    completed = db.Column(db.String)
    datequalified = db.Column(db.DateTime(), nullable=True)
    expireydate = db.Column(db.DateTime(), nullable=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    compliant = db.Column(db.String)

class workingalone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    startdate = db.Column(db.DateTime(), nullable=True)
    completed = db.Column(db.String)
    datequalified = db.Column(db.DateTime(), nullable=True)
    expireydate = db.Column(db.DateTime(), nullable=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    compliant = db.Column(db.String)

class workplaceviolence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    startdate = db.Column(db.DateTime(), nullable=True)
    completed = db.Column(db.String)
    datequalified = db.Column(db.DateTime(), nullable=True)
    expireydate = db.Column(db.DateTime(), nullable=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    compliant = db.Column(db.String)

class jointhealthandsafety(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    startdate = db.Column(db.DateTime(), nullable=True)
    completed = db.Column(db.String)
    datequalified = db.Column(db.DateTime(), nullable=True)
    expireydate = db.Column(db.DateTime(), nullable=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    compliant = db.Column(db.String)
    
   
