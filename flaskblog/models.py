from flaskblog import db, app
from datetime import datetime
from flask_user import  UserMixin
import jwt, pytz
from time import time
from . import ma
from sqlalchemy import  Integer, ForeignKey


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
    db.Column('store_id', db.Integer(), db.ForeignKey('store.id')))

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

    #def __str__(self):
    #    return (self.firstname)

class Company(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    address = db.Column(db.String(200))
    address_two = db.Column(db.String(200))
    city = db.Column(db.String(200))
    state_province = db.Column(db.String(200))
    country = db.Column(db.String(200))
    phone_number = db.Column(db.String(100))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 
   # users = db.relationship('User', backref='company', lazy=True)

    def _str__(self):
        return (self.name)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean, default = True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    confirmed_at = db.Column(db.DateTime)
    user_name = db.Column(db.String(100))
    phone = db.Column(db.String(100), unique=True)
    # new additions 
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 
    email_confirmed = db.Column(db.Boolean, default=False)
    email_confirmed_date = db.Column(db.DateTime)
    #employee = db.relationship('Customer', backref= 'user', uselist = False)
    roles = db.relationship('Role',  secondary=roles_users,
                           backref=db.backref('users', lazy='dynamic'))

    check_in_out = db.relationship('checkinout', backref='user', lazy=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    company = db.relationship('Company', backref = 'company')

    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.roles is  None:
            self.roles = Role.query.filter_by(name="GSA").first()

    def has_roles(self, *args):
        return set(args).issubset({role.name for role in self.roles})

    def is_active(self):
        return self.active

    def __str__(self):
        return str(self.firstname) 

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time()+ expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')
    
    def get_mail_confirm_token(self, expires_in=600):
        return jwt.encode(
            {'confirm_email': self.id, 'exp': time()+ expires_in},
            app.config['SECRET_KEY'], algorithm="HS256")

    def __repr__(self):
        return self.firstname

    @staticmethod
    def verify_email_confirm_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],algorithms=['HS256'])['confirm_email']
        except:
            return
        return User.query.get(id)

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = ('id', 'email', 'roles')
user_schema = UserSchema(many=True)


class BulkEmailSendgrid(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    templatename = db.Column(db.String, unique=True)
    templateid = db.Column(db.String(200), unique=True)
    
    def __repr__(self):
        return '%r' % (self.templatename)

    #def __str__(self):
    #    return (self.templatename)
        
 
class Twimlmessages(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    twimlname = db.Column(db.String, unique=True)
    twimlid = db.Column(db.String(200), unique=True)
    
    def __repr__(self):
        return '%r' % (self.twimlname)

    #def __str__(self):
    #    return (self.twimlname)

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    

    def __str__(self):
        return (self.name)

    #def __repr__(self):
    #    return (self.name)

    #def __hash__(self):
    #    return hash(self.name)

   

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    firstname = db.Column(db.String(), nullable=False)
    lastname = db.Column(db.String(), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    store = db.relationship('Store', backref = 'store')
    addressone = db.Column(db.String(20), nullable=True)
    addresstwo = db.Column(db.String(20), nullable=True)
    apt = db.Column(db.String(20), nullable=True)
    city = db.Column(db.String(), nullable=True)
    province = db.Column(db.String(), nullable=True)
    country = db.Column(db.String(), nullable=True)
    mobilephone = db.Column(db.String(), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    dob = db.Column(db.DateTime(),nullable=True)
    startdate = db.Column(db.DateTime(),nullable=True)
    sin_number = db.Column(db.String())
    sinexpire = db.Column(db.DateTime(), nullable=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    
   
    postal = db.Column(db.String(6), nullable=True)
    trainingid = db.Column(db.String(),unique=True, nullable=True)
    trainingpassword = db.Column(db.String(), nullable=True)
    manager = db.Column(db.Integer)
    image_file = db.Column(db.String(50), nullable=True,
                           default='default.jpg')
    
    iprismcode = db.Column(db.String(9), nullable=False)
    
    mon_avail = db.Column(db.String(100), nullable=False)
    tue_avail = db.Column(db.String(100), nullable=False)
    wed_avail = db.Column(db.String(100), nullable=False)
    thu_avail = db.Column(db.String(100), nullable=False)
    fri_avail = db.Column(db.String(100), nullable=False)
    sat_avail = db.Column(db.String(100), nullable=False)
    sun_avail = db.Column(db.String(100), nullable=False)
    employee_doc = db.relationship('Empdocs', backref='employee', lazy=True)
   
    
    #def __str__(self):
    #    return (self.firstname) 

class EmployeeSchema(ma.Schema):
    class Meta:
        model = Employee
        store = ma.Nested("StoreSchema", exclude=("store",))
        fields = ('id', 'firstname', 'lastname', 'mobilephone','email', 'store_id', 'image_file', 'number')
employee_schema = EmployeeSchema(many=True)

class EmployeeSMSSchema(ma.Schema):
    class Meta:
        model = Employee
        fields = ('id','mobilephone')
employeeSMS_schema = EmployeeSMSSchema(many=True)



class Course(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)  
    
    
    #def __str__(self):
    #    return '%r' % (self.name)
   
class Grade(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    
    employee_id = db.Column(Integer(), ForeignKey('employee.id'))
    employee = db.relationship('Employee', backref = 'grades')
    course_id = db.Column(db.Integer(), ForeignKey('course.id'))
    course = db.relationship('Course', backref='grade')
    completed = db.Column(db.Boolean, default = False)
    completeddate = db.Column(db.String(), nullable=True)
      
    #def __str__(self):
    #    return (self.course_id)

class staffschedule(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    employee_id = db.Column(Integer(), ForeignKey('employee.id'))
    employee = db.relationship('Employee', backref = 'schedule')
    storeworked = db.Column(db.String())
    shift_description = db.Column(db.String())
    shift_hours = db.Column(db.Integer())
    shift_date = db.Column(db.Date)
 
    #def __str__(self):
    #    return (self.id)

class staffscheduleschema(ma.Schema):
    class Meta:
        model = staffschedule
        
        employee=ma.Nested("employee_schema")
        fields = ('id', 'firstname', 'shift_description','shift_hours', 'shift_date')

staffschedule_schema = staffscheduleschema(many=True)

class Empfile(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    employee2_id = db.Column(Integer(), ForeignKey('employee.id'))
    employee2 = db.relationship('Employee', backref = 'files')
    file_id = db.Column(db.Integer(), ForeignKey('hrfiles.id'))
    file = db.relationship('hrfiles', backref = 'filess') 
    sig_data = db.Column(db.Integer())
    
    #def __str__(self):
    #    return (self.id)

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    carwash =  db.Column(db.Boolean, default = False)
    phone = db.Column(db.String(), nullable=False)
    check_in_out = db.relationship('checkinout', backref='store', lazy=True)
    address = db.Column(db.String())
    city = db.Column(db.String())
    province = db.Column(db.String())
    
    def __repr__(self):
        return f"{self.number}  {self.address}  {self.city}  {self.province}"

    #def __str__(self):
    #    return (self.number)
   
class StoreSchema(ma.Schema):
    class Meta:
        model = Store
        fields = ('number','phone')
store_schema = StoreSchema(many=True)
        
    
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


     

class Incident(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     injuryorillness = db.Column(db.Boolean, default = False)
     environmental = db.Column(db.Boolean, default = False)
     regulatory = db.Column(db.Boolean, default = False)
     economicdamage = db.Column(db.Boolean, default = False)
     reputation = db.Column(db.Boolean, default = False)
     security = db.Column(db.Boolean, default = False)
     fire = db.Column(db.Boolean, default = False)

     store_id =db.Column(db.Integer, db.ForeignKey('store.id'))
     store = db.relationship('Store', backref = 'stores')
     eventdetails = db.Column(db.String())
     eventdate = db.Column(db.DateTime(), nullable = True)
     eventtime = db.Column(db.Time())
     reportedby = db.Column(db.String())
     reportedbynumber = db.Column(db.String())

     suncoremployee = db.Column(db.Boolean, default = False)
     contractor = db.Column(db.Boolean, default = False)
     associate = db.Column(db.Boolean, default = False)
     generalpublic = db.Column(db.Boolean, default = False)
     other = db.Column(db.Boolean, default = False)
     othertext = db.Column(db.String())

     actionstaken = db.Column(db.String())
     correctiveactions = db.Column(db.String())

     sno = db.Column(db.Boolean, default = False)
     syes = db.Column(db.Boolean, default = False)
     scomment = db.Column(db.String())

     rna = db.Column(db.Boolean, default = False)
     rno = db.Column(db.Boolean, default = False)
     ryes = db.Column(db.Boolean, default = False)
     rcomment = db.Column(db.String())

     gas = db.Column(db.Boolean, default = False)
     diesel = db.Column(db.Boolean, default = False)
     sewage = db.Column(db.Boolean, default = False)
     chemical = db.Column(db.Boolean, default = False)
     chemcomment = db.Column(db.String())
     deiselexhaustfluid = db.Column(db.Boolean, default = False)
     sother = db.Column(db.Boolean, default = False)
     s2comment = db.Column(db.String())

     air = db.Column(db.Boolean, default = False)
     water = db.Column(db.Boolean, default = False)
     wildlife = db.Column(db.Boolean, default = False)
     land = db.Column(db.Boolean, default = False)
     volumerelease = db.Column(db.String())

     pyes = db.Column(db.Boolean, default = False)
     pno = db.Column(db.Boolean, default = False)
     pna = db.Column(db.Boolean, default = False)
     pcase = db.Column(db.String())

     stolentransactions = db.Column(db.Boolean, default = False)
     stoltransactions = db.Column(db.String())
     stolencards = db.Column(db.Boolean, default = False)
     stolcards = db.Column(db.String())
     stolentobacco = db.Column(db.Boolean, default = False)
     stoltobacco = db.Column(db.String())
     stolenlottery = db.Column(db.Boolean, default = False)
     stollottery = db.Column(db.String())
     stolenfuel = db.Column(db.Boolean, default = False)
     stolfuel = db.Column(db.String())
     stolenother = db.Column(db.Boolean, default = False)
     stolother = db.Column(db.String())
     stolenothervalue = db.Column(db.String())
     stolenna = db.Column(db.Boolean, default = False)

     gender = db.Column(db.String())
     height = db.Column(db.String())
     weight = db.Column(db.String())
     haircolor = db.Column(db.String())
     haircut= db.Column(db.String())
     complexion = db.Column(db.String())
     beardmoustache = db.Column(db.String())
     eyeeyeglasses = db.Column(db.String())
     licencenumber = db.Column(db.String())
     makemodel = db.Column(db.String())
     color = db.Column(db.String())
     scars = db.Column(db.String())
     tatoos = db.Column(db.String())
     hat = db.Column(db.String())
     shirt = db.Column(db.String())
     trousers = db.Column(db.String())
     shoes = db.Column(db.String())
     voice = db.Column(db.String())
     bumpersticker = db.Column(db.String())
     direction = db.Column(db.String())
     damage = db.Column(db.String())
     incident_images = db.relationship('incident_files', backref='incident_images', lazy=True)
     image_folder = db.Column(db.String())

     
    

class incident_files(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    image = db.Column(db.String(100), nullable=False)
    incident_id = db.Column(db.Integer, db.ForeignKey('incident.id'))

    

class Empdocs(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    file_document = db.Column(db.String(100), nullable=False)
    file_employee = db.Column(db.Integer, db.ForeignKey('employee.id'))

    

class checkinout(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    startdate = db.Column(db.DateTime(), nullable = True)
    starttime = db.Column(db.Time())
    enddate = db.Column(db.DateTime(), nullable = True)
    endtime = db.Column(db.Time())
    check_store = db.Column(db.Integer, db.ForeignKey('store.id'))
    check_user = db.Column(db.Integer, db.ForeignKey('user.id'))

class completedfile(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    userid = db.Column(db.Integer())
    completed =db.Column(db.Boolean, default=False)
    date_completed = db.Column(db.DateTime(timezone=True), default=pytz.utc.localize(datetime.utcnow()).astimezone(pytz.timezone("America/New_York")))

class Error(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    traceback = db.Column(db.String())
    time = db.Column(db.DateTime(timezone=True), default=pytz.utc.localize(datetime.utcnow()).astimezone(pytz.timezone("America/New_York")))


class UserActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    activity_type = db.Column(db.String(), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    firstname = db.Column(db.String())
    lastname = db.Column(db.String())
    endpoint = db.Column(db.String(200), nullable=False)
    method = db.Column(db.String(50), nullable=False)



