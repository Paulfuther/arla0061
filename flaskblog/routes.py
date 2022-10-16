from mmap import PAGESIZE
from dropbox.files import WriteMode
from emailverifier.models import response
from flask import Flask, render_template, jsonify, request, send_file, url_for, redirect,\
    flash, abort, send_from_directory, make_response, session, current_app, app
from requests.api import options
from sqlalchemy.sql.functions import current_time
from flaskblog.forms import LoginForm, EmployeeForm, EmployeeUpdateForm, SiteIncident, \
    grade_form, schedule_start, Schedule, GradeForm, CommsForm, BulkEmailSendgridForm, \
        forgot_password_Form, BulkCallForm, reset_password_form, Confirm2faForm, checkinoutForm,\
            NewRegisterForm
from flaskblog import app, Employee, User, Role, roles_users, bcrypt, \
    db, dbx, Course, Grade, Store, hrfiles, upload_fail, upload_success, Empfile, \
        staffschedule, Incident, User, Customer, employee_schema, staffschedule_schema, make_pdf,\
            make_incident_pdf,send_bulk_email, celery, client, Client, twilio_from, validate_twilio_request, Mail, \
                 employeeSMS_schema, NOTIFY_SERVICE_SID, BulkEmailSendgrid,\
                     DEFAULT_SENDER, Store,Twimlmessages, store_schema, SENDGRID_NEWHIRE_ID, \
                         login_required, roles_required, roles_accepted, check_password_hash, sg, SendGridAPIClient,\
                             basedir,INCIDENT_UPLOAD_PATH, incident_files, checkinout, user_schema

from flask_email_verifier import EmailVerifier
from io import BytesIO
import os, string, secrets
import json
import pdfkit
from werkzeug.utils import secure_filename
import pandas as pd
import numpy
import openpyxl
import xlrd
import xlwt
import xlsxwriter
from flaskblog import datetime, verifier
from flask_moment import Moment
import secrets
from PIL import Image
import re, base64
from sqlalchemy.sql import text, select, exists
from sqlalchemy import *
from sqlalchemy import extract
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_mail import Message
from json import dumps, loads
from twilio.twiml.messaging_response import MessagingResponse
import time
from flask_cors import CORS
from flaskblog.utils.request import validate_body
from flaskblog.utils.response import response, error_response
from flaskblog.utils.sms import send_bulk_sms
from flaskblog.utils.twofa import _get_twilio_verify_client, request_verification_token, \
                    check_verification_token, request_verification_token_whatsapp
from flask_login import current_user, login_user, logout_user, fresh_login_required
moment = Moment(app)
CORS(app)


@app.route('/clock_in_out', methods=['GET','POST'])
@login_required
def clock_in_out():
    form = checkinoutForm()
    store = Store.query.all()
    if request.method == 'GET':
        cleaning = checkinout.query.filter(checkinout.id)\
        .join( User, checkinout.check_user == User.id)\
            .join(Store, checkinout.check_store==Store.id)\
        .add_columns(User.firstname, Store.number, checkinout.startdate,checkinout.starttime, checkinout.enddate,
         checkinout.endtime).order_by(checkinout.startdate.desc())
        return render_template('clickinout.html', form=form, store=store, cleaning=cleaning)
    if request.method =='POST':
        form_data = request.form
        start_date = form.start_date.data
        end_date = form.end_date.data
        store = form.store.data
        newstarttime=str(form.start_time.data)
        newstarttime =datetime.strptime(newstarttime, '%H:%M:%S').time()
        newendtime=str(form.end_time.data)
        newendtime=datetime.strptime(newendtime, '%H:%M:%S').time()
        newstartdate1=str(form.start_date.data)
        newstartdate=datetime.strptime(newstartdate1, '%Y-%m-%d').date()
        #newstartdate = start_date.date()
        print(form.start_date.data, form.start_time.data, form.store.data.id, current_user, newstartdate)

        clockin = checkinout(check_user = current_user.id, 
                            check_store = form.store.data.id,
                            startdate = newstartdate,
                            starttime = newstarttime,
                            enddate= end_date,
                            endtime=newendtime)
        db.session.add(clockin)
        db.session.commit()
        #cleaning = checkinout.query.all()
        
        cleaning = checkinout.query.filter(checkinout.id)\
        .join( User, checkinout.check_user == User.id)\
            .join(Store, checkinout.check_store==Store.id)\
        .add_columns(User.firstname, Store.number, checkinout.startdate,checkinout.starttime, checkinout.enddate,
         checkinout.endtime).order_by(checkinout.startdate.desc())
        flash("Time Submitted. Thank")
        return redirect(url_for('clock_in_out'))

@app.route('/updatefirstname')
def update_phone():

    #this route copied all 

    newuser =  Employee.query.filter(Employee.id)
    
    for x in newuser:
        print(x.firstname, x.mobilephone, x.user_id)
        user=User.query.get(x.user_id)
        print (user)
        user.firstname = x.firstname
        user.lastname = x.lastname
        db.session.commit()
        print(user.firstname, user.lastname)
    
    return "done"

@app.route("/")
def home(): 
    return render_template("home.html")


@app.route("/login", methods = ['GET', 'POST'])
def login():
    form=LoginForm()
    if current_user.is_authenticated:
        return render_template("layout.html")
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('That email does not exits')
        elif user.active == False:
            flash('You are not an active user')
            return render_template("login.html", form=form)
        elif user is None or not bcrypt.check_password_hash(user.password, form.password.data):
            flash('invalid username or password')
            return redirect(url_for('login', form=form)  )
        elif user.email_confirmed == 0:      
            send_email_confirmation(user)
            flash('please confirm email')
            return redirect(url_for('login'))
        elif user and bcrypt.check_password_hash(user.password, form.password.data):
            user_phone =db.session.query(Employee.mobilephone, User)\
            .filter(Employee.user_id == user.id).first()
            print(user.phone)
            print(user.active)
            print(form.two_fa.data)
            # testing
            login_user(user, remember=form.remember_me.data)
            return render_template("layout.html", title="home")

            # end here
            if form.two_fa.data=="sms":
                request_verification_token(user.phone)
                session['phone']=user.phone
                return redirect(url_for('verify_2fa'))
            elif form.two_fa.data=="whatsapp":
                request_verification_token_whatsapp(user.phone)
                session['phone']=user.phone
                return redirect(url_for('verify_2fa'))
            else:
                flash('you need to select a 2fa channel')
                #return redirect(url_for('lodin'))
            #session['phone']=user_phone
            return redirect(url_for('login', form=form))
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if current_user.has_roles('GSA'):
                gsaid = int(current_user.id)
                staff = Employee.query.filter_by(user_id=gsaid).first()
                exists = Empfile.query.filter_by(employee2_id=staff.id).first()
                return render_template("gsadashboard.html", staff=staff, exists=exists)
            print(current_user)
            return render_template("layout.html", title="home")
    #print("nope")    
    return render_template("login.html", form=form)

@app.route("/home22", methods = ['GET', 'POST'])
@login_required
def home22():
    print(current_user.id)
    gsaid = int(current_user.id)
    staff = Employee.query.filter_by(user_id=gsaid).first()
    if current_user.has_roles('GSA'):
        print(staff.id)
        exists = Empfile.query.filter_by(employee2_id=staff.id).first()
        if exists:    
            return render_template('gsadashboard.html', staff=staff, exists=exists)
        else:
            print("no")
            flash("no file exists") 
            #print('user is gsa')
            return render_template('gsadashboard.html', staff=staff, exists=exists)
    
    #return render_template('testsig.html')
    
    return render_template('layout.html')
    #return render_template('home.html')

#@app.route('/new_hire_hr_list', methods = ['GET','POST'])
#def new_hire_hr_list():
    #emp = Employee.query.get(3)
    #print(emp.firstname)
    #return render_template('newhirehomehr.html', emp=emp)

def send_email_confirmation(user):
    token = user.get_mail_confirm_token()
    email = user.email
    message=Mail(
        from_email = DEFAULT_SENDER,
        to_emails=email,
        subject = 'Please Verify Email for Petro Canada',
        html_content=render_template('email/confirm_email.html', user=user, token=token)
            )
    response = sg.send(message)
    
@app.route('/newhire_verify2fa', methods=['GET', 'POST'])
def newhire_verify_2fa():
    phone=request.form['phone']    
    print(phone)
    print("yes")
    request_verification_token(phone)
    print("requesting code")
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route('/newhire_verify2fa_check', methods=['GET','POST'])
def newhire_verify2f1_check():
    token=request.form['token']
    phone=request.form['phone']
    if check_verification_token(phone,token):
            response = 1
            return (jsonify(response))
    print("huh")
    response = 0
    return (jsonify(response))
    
@app.route('/verify2fa', methods=['GET', 'POST'])
def verify_2fa():
    form = Confirm2faForm()
    if form.validate_on_submit():
        print(form.token.data)
        print("yes")
        phone=session['phone']
        if check_verification_token(phone, form.token.data):
            user = User.query.filter_by(phone = phone).first()
            login_user(user, remember=True)
            print(current_user)
            return render_template("layout.html", title="home")
        flash ('invalid code please login again')
    print("huh")
    return render_template('verify.html', form=form)

@app.route("/forgot_password", methods = ['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = forgot_password_Form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
            flash('Check your email for the instrucitons to reset your password')
        else:
            flash('Invalide Credentials')
        return redirect(url_for('login'))
    return render_template("forgot_password.html", title="Reset Password", form=form)

def send_password_reset_email(user):
    token=user.get_reset_password_token()
    email = user.email
    message = Mail(
            from_email=DEFAULT_SENDER,
            to_emails= email,
            subject = 'Welcome to Petro Canada',
            html_content=render_template('email/reset_password.html', user=user, token=token)
            )
    response = sg.send(message)

@app.route('/reset_password/<token>', methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('login'))
    form = reset_password_form()
    if form.validate_on_submit():
        user.password = bcrypt.generate_password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your password has been reset')
        return redirect(url_for('login'))

    return render_template('reset_password.html', form=form, user=user)

@app.route('/confirm_email/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.verify_email_confirm_token(token)
    if not user:
        return redirect(url_for('login'))
    
    user.email_confirmed = True
    user.email_confirmed_date = datetime.utcnow()
    db.session.add(user)
    db.session.commit()
    flash('Your email has been verified')
    return redirect(url_for("login"))
    
def fetch_sms():
    return client.messages.stream()

@app.route('/fetch_twilio')
def fetch_twilio():
    sms = fetch_sms()
    return render_template("fetch_twilio.html", sms=sms)

@app.route('/fetch_calls')
def fecth_calls():
    calls = client.calls.list(limit=20)
    for record in calls:
        print(record.sid)   
    return "done"

@app.route('/fetch_call_events')
def fetch_call_events():
    events = client.calls('CA7d4e808eed188f5c1754342cd9cdc1bb') \
               .events \
               .list(limit=20)

    #for record in events:
    #    print(record.request)
    #    request_items = record.request.items()
    #    print(type(record.request))
    #    for item in request_items:
    #        print(item)
    for record in events:
        #print(record.request)
        print("------------")
        json_string = json.dumps(record.request) 
        stringone=json.loads(json_string)   
        print(stringone['parameters'])
        key =(stringone['parameters'])
        print(key)
        for x in key:
            print(x[0])
        #print(type(stringone))
      
  
    #for key in events:
     #  print(key)
    return "done"

@app.route("/home2<int:user_id>")
@login_required
def home2():
    print(current_user.id)
    gsaid = int(current_user.id)
    staff = Employee.query.filter_by(user_id=gsaid).first()
    if current_user.has_roles('GSA'):
        
        print(staff.id)
        
        exists = Empfile.query.filter_by(employee2_id=staff.id).first()
        
        if exists:
            flash("you have a file")
            return render_template('gsadashboard.html', staff=staff, exists=exists)
        else:
            print("no")
            flash("no file exists")
      
        
            #print('user is gsa')
            return render_template('gsadashboard.html', staff=staff, exists=exists)
    
    #return render_template('testsig.html')
    
    return render_template('layout.html')
    #return render_template('home.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/commsmenu', methods = ['GET', 'POST'])
@login_required
@roles_required('Admin')
#@fresh_login_required
def comms_menu():
    #if not fresh_login_required:
    return render_template('commsmenu.html')
    #else:
    #return redirect(url_for('logout'))

@app.route('/twiliocall', methods = ['GET', 'POST'])
@login_required
@roles_required('Admin')
def twilio_call():

    # form for bulk calls
    form=BulkCallForm()

    if request.method == "GET":
        return render_template("twiliocalls.html", form=form)
    else:
        
        twimlname = request.form['templatename']
        bulk_call = Twimlmessages.query.get(twimlname)
        twil_id = bulk_call.twimlid
        #print(twil_id)
        # this is using twilml machine learning text to speach.
        # this only goes out to stores.
        site = db.session.query(Store.number,Store.phone).all()
        for x in site:
            print(x.number, x.phone)
        for x in site:
            call = client.calls.create(
                            url=twil_id,
                            to=x.phone,
                            from_=twilio_from
        )              
        print(call.sid)
        
        return render_template("layout.html")
   
@app.route('/bulkemail', methods = ['GET', 'POST'])
@login_required
@roles_required('Admin')
def bulk_email():
    form=BulkEmailSendgridForm()
    
    if request.method == "GET":
        return render_template("commsemail.html", form=form)
    else:
        
        role_id = request.form['role']
        templatename = request.form['templatename']
        send_bulk_email.apply_async(args=[role_id,templatename], countdown=10) 
        
        return render_template("layout.html")

@app.route('/bulkms', methods = ['GET', 'POST'])
@login_required
@roles_required('Admin')
def bulk_sms():
    form=CommsForm()
    if request.method == "GET":
        return render_template("comms.html", form=form)
    else:
        
        role_id = request.form['role']
        message_to_send = request.form['message_body']
        print(message_to_send)
        print(role_id)
        
    # this is bulk sms using the notify api from twilio.
    # first we grab all employees who are active users.
    # we need to search specifically for mobile phone

        gsa = db.session.query(Employee.mobilephone, Employee.firstname,User,Role)\
        .filter((roles_users.c.user_id == User.id) & (roles_users.c.role_id == Role.id))\
            .join(User, Employee.user_id == User.id).order_by(Employee.firstname)\
        .filter(User.active == 1)\
            .filter(Role.id==role_id)\
        .all()
    # gsa returns an object. Although we can serialise the object, we still
    # have issues generating the proper format for twilio rest api.
    # so we do it old school.

        gsat = []
        for id in gsa:
            gsatt = id.mobilephone
            print(gsatt, id.firstname)
            gsat.append(gsatt)

    # we need a message to send. This will be a variable.

        message = message_to_send
        print(message)
                    
    
    # call the function send_bulk_sms.
    # it is a file in the utils section.
    # this will create the list needed by twilio.
    # we are sending a payload called a binding.
        #for x in gsa:
            #print (x.mobilephone, x.firstname)

        send_bulk_sms(gsat, message)

    # once completed. Do something.

        return render_template("layout.html")

@app.route("/sms", methods=['GET', 'POST'])
@validate_twilio_request
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    resp = MessagingResponse()

    # Add a message
    resp.message("Thank you for the call")

    return str(resp)

@app.route('/testincident', methods = ['GET', 'POST'])
@login_required
def print_incident():
    form=SiteIncident()
    x=int(85)
    gsa = Incident.query.get(x)
    ident = gsa.id
    print(ident)
    picture = incident_files.query.filter_by(incident_id=ident)
    for x in picture:
        print( x.image)
    print (basedir)
    return render_template('eventreportpdf.html' , form=form, gsa=gsa, picture=picture)

@app.route('/email/<email>')
@login_required
@roles_accepted('Admin', 'Manager')
def email(email):
    # Retrieve an info for the given email address
    email_address_info = verifier.verify(email)
    if email_address_info is not None:
        data = dumps(loads(email_address_info.json_string), indent=4)
        resp = make_response(data, 200)
        resp.headers['Content-Type'] = 'application/json'
 
        value1 = json.loads(data)
        print (value1['formatCheck'],value1['smtpCheck'])
    else:
        
        resp = make_response('None', 404)
    return resp


@app.route("/process_images", methods = ['GET', 'POST'])
@login_required
def process_images():
    form = SiteIncident()
    pics= request.files.getlist('photos[]')
    print (pics)
            #filename = secure_filename(pics.filename)
            #print(INCIDENT_UPLOAD_PATH)
            #target = os.path.join(app.config['INCIDENT_UPLOAD_PATH'], 'static/incidentpictures')
           
    for pic in pics:
        if not pic:
            pass
        else:
            i=Image.open(pic)
            i.thumbnail((300,300), Image.LANCZOS)  
            print(i.size)    
            i.save(os.path.join(INCIDENT_UPLOAD_PATH,secure_filename(pic.filename)))
    return render_template('eventreport.html', form=form)




@app.route("/event", methods = ['GET', 'POST'])
@login_required
@roles_accepted('Admin', 'Manager')
def eventreport():
    form = SiteIncident()
    
    # get all of the information from the form

    if form.validate_on_submit():
            pics= request.files.getlist('photos[]')
            print (pics)
            print(form.location.data)
            #filename = secure_filename(pics.filename)
            #print(INCIDENT_UPLOAD_PATH)
            #target = os.path.join(app.config['INCIDENT_UPLOAD_PATH'], 'static/incidentpictures')
           
            #for pic in pics:
            #    if not pic:
            #        pass
            #    else:
            #        i=Image.open(pic)#

                    #= Image.open(pic)
            #        i.thumbnail((300,300), Image.LANCZOS)
                    #i.save(picture_paththumb)
            #        print(i.size)
                    #new_pic = image.resize(300,300)
             #       i.save(os.path.join(INCIDENT_UPLOAD_PATH,secure_filename(pic.filename)))
        
            #return render_template('layout.html')
            newtime=str(form.eventtime.data)
            time2 =datetime.strptime(newtime, '%H:%M:%S').time()
            inc=Incident(injuryorillness=form.injuryorillness.data,
                            environmental =form.environmental.data,
                            regulatory =form.regulatory.data,
                            economicdamage = form.economicdamage.data,
                            reputation = form.reputation.data,
                            security = form.security.data,
                            fire = form.fire.data,
                            location = str(form.location.data),
                            eventdetails = form.eventdetails.data,
                            eventdate = form.eventdate.data,
                            eventtime = time2,
                            reportedby = form.reportedby.data,
                            reportedbynumber = form.reportedbynumber.data,
                            suncoremployee = form.suncoremployee.data,
                            contractor = form.contractor.data,
                            associate = form.associate.data,
                            generalpublic = form.generalpublic.data,
                            other = form.other.data,
                            othertext = form.othertext.data,
                            actionstaken = form.actionstaken.data,
                            correctiveactions = form.correctiveactions.data,
                            sno = form.sno.data,
                            syes = form.syes.data,
                            scomment = form.scomment.data,
                            rna = form.rna.data,
                            rno = form.rno.data,
                            ryes = form.ryes.data,
                            rcomment = form.rcomment.data,
                            gas = form.gas.data,
                            diesel = form.diesel.data,
                            sewage = form.sewage.data,
                            chemical = form.chemical.data,
                            chemcomment = form.chemcomment.data,
                            deiselexhaustfluid = form.deiselexhaustfluid.data,
                            sother = form.sother.data,
                            s2comment = form.scomment.data,
                            air = form.air.data,
                            water = form.water.data,
                            wildlife = form.wildlife.data,
                            land = form.land.data,
                            volumerelease = form.volumerelease.data,
                            pyes = form.pyes.data,
                            pno = form.pno.data,
                            pna = form.pna.data,
                            pcase = form.pcase.data,
                            stolentransactions = form.stolentransactions.data,
                            stoltransactions = form.stoltransactions.data,
                            stolencards = form.stolencards.data,
                            stolcards = form.stolcards.data,
                            stolentobacco = form.stolentobacco.data,
                            stoltobacco = form.stoltobacco.data,
                            stolenlottery = form.stolenlottery.data,
                            stollottery = form.stollottery.data,
                            stolenfuel = form.stolenfuel.data,
                            stolfuel = form.stolfuel.data,
                            stolenother = form.stolenother.data,
                            stolother = form.stolother.data,
                            stolenothervalue = form.stolenothervalue.data,
                            stolenna = form.stolenna.data,
                            gender = form.gender.data,
                            height = form.height.data,
                            weight = form.weight.data,
                            haircolor = form.haircolor.data,
                            haircut= form.haircut.data,
                            complexion = form.complexion.data,
                            beardmoustache = form.beardmoustache.data,
                            eyeeyeglasses = form.eyeeyeglasses.data,
                            licencenumber = form.licencenumber.data,
                            makemodel = form.makemodel.data,
                            color = form.color.data,
                            scars = form.scars.data,
                            tatoos = form.tatoos.data,
                            hat = form.hat.data,
                            shirt = form.shirt.data,
                            trousers = form.trousers.data,
                            shoes = form.shoes.data,
                            voice = form.voice.data,
                            bumpersticker = form.bumpersticker.data,
                            direction = form.direction.data,
                            damage = form.damage.data)
                            
            db.session.add(inc)
            db.session.flush()
            #db.session.commit()

            for pic in  pics:
                if not pic:
                    pass
                else:

                    incimage = incident_files(image=secure_filename(pic.filename),
                                    incident_id = inc.id)
                    db.session.add(incimage)
            db.session.commit()

            print(inc.id)
            file_id = int(inc.id)
            flash('Your form has been submitted, uploaded to dropbox and sent to the ARL. Thank you', 'success')
            
            # once the data has been written to the database, we create a pdf.
            # we call a task mamanger to do this. That is the apply_async 
           # make_incident_pdf.apply_async(args=[file_id], countdown=10)

            return("good")
            return render_template('layout.html')
           
    return render_template('eventreport.html', form=form)

@app.route("/nofile")
@login_required
@roles_accepted('Admin', 'Manager')
def nofile():
    
    
    file = Empfile.query.with_entities(Empfile.employee2_id).distinct()
    
    nofile = Employee.query.filter(Employee.id.notin_(file))\
        .join(Store, Store.id == Employee.store_id)\
            .join(User, Employee.user_id == User.id)\
        .filter(User.active == 1)\
        .add_columns(Store.number, Employee.firstname, Employee.lastname)\
        .order_by(Store.number)
        

    return render_template('nofile.html', nofile=nofile)

@app.route("/activebystore")
@login_required
@roles_accepted('Admin', 'Manager')
def activebystore():
    
    
    activebystore = Employee.query.filter(Employee.id)\
        .join(Store, Store.id == Employee.store_id)\
            .join(User, Employee.user_id == User.id)\
        .filter(User.active == 1)\
        .add_columns(Store.number, Employee.firstname, Employee.lastname, User.active)\
        .order_by(Store.number)
        
    for x in activebystore:
        print(x.firstname, x.lastname, x.number, x.active)

    return render_template('activebystore.html', activebystore=activebystore)

@app.route("/activebystoreexcel")
@login_required
@roles_accepted('Admin', 'Manager')
def activebystoreexcel():
    activebystore = Employee.query.filter(Employee.id)\
        .join(Store, Store.id == Employee.store_id)\
            .join(User, Employee.user_id == User.id)\
        .filter(User.active == 1)\
        .add_columns(Store.number, Employee.firstname, Employee.lastname, User.active)\
        .order_by(Store.number)
    
    
    out = BytesIO()
    writer = pd.ExcelWriter(out, engine = 'xlsxwriter')
    df = pd.read_sql(activebystore.statement, activebystore.session.bind)
    df = df[['number','firstname','lastname']]
    df.to_excel(writer, index=False)
    writer.save()
    out.seek(0)
    
    

    return send_file(out, attachment_filename="activebystore.xlsx", as_attachment=True)


@app.route("/nofileexcel")
@login_required
@roles_accepted('Admin', 'Manager')
def nofileexcel():
    emp = Employee.query.filter(Employee.id)
    file = Empfile.query.with_entities(Empfile.employee2_id).distinct()
    
    nofile = Employee.query.filter(Employee.id.notin_(file))\
        .join(Store, Store.id==Employee.store_id)\
        .add_columns(Store.number, Employee.firstname)\
        .order_by(Store.number)
    
    #for x in nofile:
     #   print(x.Store)
    
    out = BytesIO()
    writer = pd.ExcelWriter(out, engine = 'xlsxwriter')
    df = pd.read_sql(nofile.statement, nofile.session.bind)
    df = df[['number','firstname','lastname']]
    df.to_excel(writer, index=False)
    writer.save()
    out.seek(0)
    
    

    return send_file(out, attachment_filename="nofile.xlsx", as_attachment=True)

@app.route("/verifyphonetoday", methods = ['GET','POST'])
def verifyphone():
    form = EmployeeForm()

    # get mobile numbers passed from the form
    # the h264 version is in hidden number
    # send back json response for front end to use as a key to 
    # assign the proper alert message
    # proper emails and phone numbers are then locked in the form

    mobile = request.form['mobilephone']
    hiddenmobile = request.form['mobilephone2']
    #print(mobile,hiddenmobile)
    if mobile == "":
        response = (7)
    else:    
        user = User.query.filter(or_(User.phone==mobile, User.phone==hiddenmobile)).first()
        #print(user)
        if user:
            response = (5)
        else:
            response = (6)
    
    #rint(response)
    return jsonify(response)

@app.route("/verifyemailtoday", methods = ['GET','POST'])
@login_required
@roles_accepted('Admin', 'Manager')
def verify():
    form = EmployeeForm()
    email = request.form['email']
    emailcheck = User.query.filter_by(email=form.email.data).first()
    email_address_info = verifier.verify(email)
    print(email)
    #print(emailcheck)
        
    #check to see if email is blank

    if email == "":
        response = (0)
        print("no email")
    # check to see if email is already in use in the database.    
    elif emailcheck:
        response = (1)
    # check to see if email is valid using service 

    else:
         response = (3)
    
    print(response)#, response2)
    return jsonify(response)#, response2)

@app.route("/schedule", methods = ['GET', 'POST'])
@login_required
@roles_accepted('Admin', 'Manager')
def schedule():
    
    form = Schedule()
   
    
    return render_template('schedule.html', form=form)

@app.route("/searchschedule", methods=['GET', 'POST'])
@login_required
@roles_accepted('Admin', 'Manager')
def searchschedule():
    
    
    #form = request.form
    search_value= request.form.get("text")
    
    print(search_value)
    hsdate1 = request.form.getlist('hidden-sdate')
    shifts = request.form.getlist('writtenhours')
    hoursworked = request.form.getlist('hours')
    #search_value = form.store.data
    
    hsdate1 = request.form.getlist('hidden-sdate')
    store_id = Store.query.filter_by(number=search_value).first()
    storeid = store_id.id
    
    gsa1 = Employee.query.filter_by(store_id=storeid)\
        .join(User, User.id==Employee.user_id)\
            .filter(User.active==1)\
            
    gsa = gsa1.order_by(Employee.store_id).all()
    
    
    s_v = int(search_value)
    
    '''s_s = Employee.query.filter(Employee.store_id==storeid)\
        .join(User, User.id==Employee.user_id)\
            .filter(User.active==1)\
            .outerjoin(staffschedule, Employee.id==staffschedule.employee_id)\
                    .add_columns(Employee.firstname,Employee.id,\
                         staffschedule.shift_description, staffschedule.shift_hours,\
                              staffschedule.shift_date, staffschedule.employee_id).all()
    '''

    s_s =db.session.query(staffschedule)

    #for r in s_s:
     #   print(r.shift_date, type(r.shift_date), r.id, r.firstname, r.shift_description, r.shift_hours)


    df=pd.read_sql(s_s.statement,s_s.session.bind)
    #idx= pd.date_range('2021-12-21', '2021-12-29')
    #df.index = pd.DatetimeIndex(df.index)
    #df = df.reindex(idx, fill_value=0)
    #f.loc[idx]
    #df = df.set_index('shift_date')
   
    print(df)

    results = staffschedule_schema.dump(s_s)
    result = jsonify(results)
    print(result)
    return result



    return render_template('schedule.html', gsa=gsa, search_string=search_value,\
         form=form, s_s=s_s)


    for rr in s_s:
        print(rr.firstname)

    for r in s_s:
        print(r.shift_date, r.id, r.firstname, r.shift_description, r.shift_hours)
              

    df=pd.read_sql(s_s.statement,s_s.session.bind)
    df=df.drop(df.columns[[1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,36]], axis=1)
    print(df)
    df3=df.values.tolist()
    print(df3)

  

    df=df.pivot_table(index=['id','firstname'] ,columns='shift_date', \
        values=['shift_description', 'shift_hours'], aggfunc='first')\
        .reset_index()
    print(df)  
    newdf = df.values.tolist()  
    ldf=len(df.columns)     
    #print(newdf)      
    
    print(len(df.columns)) 


    df2 = pd.read_sql(gsa1.statement,gsa1.session.bind)
    df2=df2.pivot_table(index=['id','firstname'])
    print(df2)
    return render_template('schedule.html', ldf=ldf,gsa=gsa, search_string=search_value,\
         form=form, s_s=s_s,  newdf=newdf)
   
        
    '''
    elif 'submithours' in request.form['action']:
          
        store_id = Store.query.filter_by(number=search_value).first()
        storeid = store_id.id
            
        if search_value == "Home Store":
                            gsa = Employee.query\
                                .order_by(Employee.store_id).all()

                            #for staff in gsa:
                            #   print(staff.id)
                            #return render_template('schedule.html', gsa=gsa)

        gsa1 = Employee.query.filter_by(store_id=storeid)
        gsa = gsa1.order_by(Employee.store_id).all()
        storenumber = search_value
        sdescription = request.form.getlist('writtenhours')
        shours = request.form.getlist('hours')
        sdate1 = request.form.getlist('sdate')
        hsdate1 = request.form.getlist('hidden-sdate')
        gsalength = len(gsa)
       
      
        
        y=0        
        for g in gsa:
            for obj in hsdate1:
                newdate = datetime.strptime(obj, '%b-%d-%Y')
                print(g,g.id, storenumber, newdate, sdescription[y], shours[y])
                empsched = staffschedule( employee_id = g.id,
                                         storeworked = storeid,
                                    shift_description = sdescription[y],
                                    shift_hours = shours[y],
                                    shift_date = newdate)
                db.session.add(empsched)
                y=y+1
        db.session.commit()
            
        return render_template('schedule.html', form=form, gsa=gsa)
    '''
    return render_template('schedule.html')

@app.route("/addtoschedule", methods = ['GET', 'POST'])
@login_required
@roles_accepted('Admin', 'Manager')
def addtoschedule():
    form=request.form
    search_value = form['search_string']
    shifts = request.form.getlist('writtenhours')
    print(search_value)
    for x in shifts:
        if x != '':
            print(shifts)
        
    return render_template('schedule.html', form=form)
        
#@app.route("/employeedashboard", methods = ['GET', 'POST'])
#@login_required
#@roles_required('GSA')
#def employeedashboard():

def storelist():
    return db.session.query(Store).all.order_by('number')

@app.route("/sendfile<int:staff_id>", methods =['GET', 'POST'])
@login_required
def sendfile(staff_id):
    gsa = Employee.query.get(staff_id)
    #hrpage = hrfiles.query.limit(3).all()
    hrpage = hrfiles.query.all()
    #print(gsa.firstname)

    make_pdf.apply_async(args=[staff_id], countdown=10)
    return render_template('layout.html')

@app.route("/hrfile<int:staff_id>", methods=['GET', 'POST'])
@login_required
def hrfile(staff_id):
    gsa = Employee.query.get(staff_id)
    hrpage = hrfiles.query.all()
    
    #print(gsa.firstname)
    for x in hrpage:
        print(x.id)
    exists = Empfile.query.filter_by(employee2_id = staff_id).first()
    if exists:
        print("yes")
        flash("This employee has a file. Thank you.")
        return redirect(url_for("hrlist"))

    if request.method == "POST":
        #sigs = request.form.getlist('output')
        signature = request.form.getlist('output')
        #signatures = json.dumps(signature)
        hrpage = hrfiles.query.limit(3).all()
        #sigs2 = json.dumps(sigs)
        #print(sigs)
        
        #for x in sigs:
        #   print(x)
        f = (staff_id)
        y = 1
        z = 0
        for x in hrpage:
                empfile = Empfile(employee2_id= f,
                                file_id= y,
                                sig_data = signature[z])
          
                data = request.form['output']
                #print(data)
                #print("hello")               
                db.session.add(empfile)
                y += 1
                z += 1
                
        db.session.commit()
        signatures = Empfile.query.filter_by(employee2_id = staff_id)
        for x in signatures:
            print (x)
        flash("file completed. Thank you")
        #make_pdf.apply_async(args=[staff_id, sigs], countdown=10)
        return render_template('employeefilepdf2.html', hrpage=hrpage ,signatures=signatures, staff_id = staff_id, gsa=gsa)
        return ('success')
  
    #print("success")
  
    return render_template('ckfile.html', hrpage=hrpage, gsa=gsa)

@app.route("/hrhome")
@login_required
def hrhome(): 
    emp = Employee.query.get(3)
    print(emp.firstname)
    return render_template('hrhome.html', emp=emp)
    

@app.route("/createpdfnewhire<int:staff_id>", methods = ['GET', 'POST'])
@login_required
def pdf_file(staff_id):
    
    # here we need to get the signatures for each file and pass to html 
    # we alos need the employee name which is stored in gsa variable
    # we also need the list of files which are stored in the hr page varaible
    # and we need to test if a file even exists 
    # if not we need to return with and error message
    
    exists = Empfile.query.filter_by(employee2_id = staff_id).first()
    if exists:
        print("yes")
    else:
        print("no", staff_id)
        flash("no file exists")
        return redirect(url_for("hrlist"))
    
    make_pdf.apply_async(args=[staff_id], countdown=10)
       
    return "working"
    
@app.route("/hrlist", methods =['GET', 'POST'])
@login_required
def hrlist():
   return render_template('hrlist.html')

@app.route("/trainingcompliance", methods=['GET', 'POST'])
@roles_accepted('Admin', 'Manager')
@login_required
def trainingcompliance():
    
    compliance = Grade.query\
            .filter_by(value="n")\
            .join(Employee, Employee.id==Grade.employee_id)\
            .join(Course, Course.id == Grade.course_id)\
            .add_columns(Grade.employee_id, Employee.firstname\
            ,Employee.lastname, Employee.store\
            , Course.name, Grade.value)\
                .order_by(Employee.store)

    
    return render_template('trainingcompliance.html', compliance = compliance)

@app.route("/updategsatraining<int:staff_id>", methods=['GET', 'POST'])
@login_required
def updategsatraining(staff_id):
    
    # get employee information form the database

    gsa = Employee.query.get(staff_id)
    store = Store.query.all()
    course = Course.query.all()
    #for x in course:
    #    print(x.id, x.name)
        
    # get course infomraiton and grade by empployee

    gradelist = Grade.query\
        .filter_by(employee_id=staff_id)\
        .join(Employee, Employee.id == Grade.employee_id)\
        .join(Course, Course.id == Grade.course_id)\
        .add_columns(Course.name, Grade.completed, Grade.completeddate)\
        .order_by(Grade.course_id)
    
    #for x in gradelist:
    #    print(x.name,x.completed, x.completeddate)     
    
    # this is the GET line. Create the dashboard for the employee with the data from 
    # gsa, store, course and gradelist, done up top.
    
    return render_template("updategsatraining.html", gsa=gsa, store=store, course=course, gradelist=gradelist)


@app.route("/updategsatraining2<int:staff_id>", methods=['GET', 'POST'])
@login_required
def updategsatraining2(staff_id):
    
    # get employee information form the database

    gsa = Employee.query.get(staff_id)
    store = Store.query.all()
    course = Course.query.all()
    #for x in course:
    #    print(x.id, x.name)
        
    # get course infomraiton and grade by empployee

    gradelist = Grade.query\
        .filter_by(employee_id=staff_id)\
        .join(Employee, Employee.id == Grade.employee_id)\
        .join(Course, Course.id == Grade.course_id)\
        .add_columns(Course.name, Grade.completed, Grade.completeddate)\
        .order_by(Grade.course_id)
    
    #for x in gradelist:
    #    print(x.name,x.completed, x.completeddate)
    
    # here we are updating the training grade information
    # we get an object that we can alter. Use the .first to do this
    # we need two parameters though, the emp id and the course id
    # that will lead us to one result (assuming only one course per emp by course number)
    # we then loop over the POST values using form.getlist for the variable "completed"
    # then increment course by 1
    # then commit
    
    # We receive the compelted date.
    # We have the id of completeddate.
    # we then loop over the number of courses to enter new competed dates.
    # We need to check the completed date first.
    # then enter this information into the database


    if request.method == "POST":
        r = request.form.getlist('completeddate')
       
        #print(r)
        form = request.form 
        f=staff_id
        yy=0
        y = 1
        z=1
        for x in course:
                
                # here we get the course infomration for the employee.
                # any changes made will over write the exisiting data.
                # we are not creating a duplicate entry.

            t=Grade.query.filter_by(employee_id=staff_id).filter_by(course_id=y).first()
            grade_date = r[yy]
                #print(grade_date,y)
            if grade_date=='None' or grade_date=="" or grade_date==0 or grade_date=="N":
                completeddate = ''
            else:
                    #grade_check = 1
                completeddate = datetime.strptime(grade_date, '%Y-%m-%d')
                    #print(completeddate)
            t.completeddate = r[yy]
            #print(y,x, r[yy])
            y+=1 
            yy +=1
            db.session.commit()

        
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
      
    # this is the GET line. Create the dashboard for the employee with the data from 
    # gsa, store, course and gradelist, done up top.
    
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 


@app.route("/rolesearch", methods = ['POST', "GET"])
@login_required
def rolesearch():

    searchbox = request.form.get("text")
    

    gsa = db.session.query(Employee.mobilephone, Employee.firstname,Employee.lastname,User,Role)\
        .filter((roles_users.c.user_id == User.id) & (roles_users.c.role_id == Role.id))\
            .join(User, Employee.user_id == User.id).order_by(Employee.firstname)\
        .filter(User.active == 1)\
            .filter(Role.id==searchbox)\
        .all()

    #for x in gsa:
    #    print(x.firstname, x.mobilephone)
    results = employee_schema.dump(gsa)
    result = jsonify(results)

   
    return result

@app.route("/existingemployeefile<int:staff_id>", methods = ['GET', 'POST'])
@login_required
def employeefile(staff_id):
    
    # here we need to get the signatures for each file and pass to html 
    # we alos need the employee name which is stored in gsa variable
    # we also need the list of files which are stored in the hr page varaible
    # and we need to test if a file even exists 
    # if not we need to return with and error message
    
    exists = Empfile.query.filter_by(employee2_id = staff_id).first()
    if exists:
        print("yes")
        
    else:
        #print("no", staff_id)
        flash("No file exists. Please create a file. Thank you.")
        return redirect(url_for("hrlist"))
    
    signatures = Empfile.query.filter_by(employee2_id = staff_id)
    
    
    x=signatures
    hrpage = hrfiles.query.all()
    gsa = Employee.query.get(staff_id)
    #for x in signatures:
    #    print (type(x.sig_data))
    #    print(x.file_id, x)
    #    print(x.sig_data)
   
    
    return render_template('employeecompletedfile.html', hrpage = hrpage, signatures=signatures, gsa=gsa)

@app.route("/storesearch", methods = ['POST', "GET"])
@login_required
def storesearch():

    searchbox = request.form.get("text")
    

    site = db.session.query(Store.number,Store.phone).all()

    #for x in gsa:
    #    print(x.firstname, x.mobilephone)
    results = store_schema.dump(site)
    result = jsonify(results)

   
    return result

@app.route("/livesearch", methods = ["POST", "GET"])
@login_required
def livesearch():
    
    # search by first name, last name or store number
    # you need to serialise the result to pass it on as json.

    searchbox = request.form.get("text")
    gsa = Employee.query.filter(or_(Employee.firstname.like('%' + searchbox + '%')\
        ,Employee.lastname.like('%' + searchbox + '%')\
        ,Store.number.like('%' + searchbox + '%')))\
        .join(Store, Store.id == Employee.store_id)\
        .join(User, Employee.user_id == User.id)\
        .filter(User.active == 1).order_by(Store.number)\
        .add_columns(Store.number, Employee.firstname, Employee.lastname, \
        Employee.email, Employee.store_id, Employee.image_file, Employee.id)\
        .all()
    
    for s in gsa:
        print(s.firstname)

    results = employee_schema.dump(gsa)
    result = jsonify(results)
    print(result)
    return result

@app.route("/live_email", methods =['GET', 'POST'])
@login_required
def live_email():
    form=NewRegisterForm()
    return render_template('emailsearch.html', form=form)


@app.route("/email_livesearch", methods = ["POST", "GET"])
def email_livesearch():
    
    # search by first name, last name or store number
    # you need to serialise the result to pass it on as json.

    searchbox = request.form.get("text")
    gsa = User.query.filter(or_(User.email.like('%' + searchbox + '%')))\
        .filter(User.active == 1)\
        .add_columns(User.email, User.id)\
        .all()
    for s in gsa:
        print(s.email)
    results = user_schema.dump(gsa) # need to jsonify results to pass back. 
                                    # done in the User creation model.
    result = jsonify(results)
    
    print(result)
    return result


@app.route("/staff_register", methods=["GET", "POST"])
def staff_register():
    form = NewRegisterForm()
    coursecount = Course.query.all()
    #print(coursecount)
    # the get is for the first load of the page
    if request.method == "GET":
        return render_template('emailsearch.html', form=form)
    if request.method == "POST":
        gsa_register = request.form['hiddenphone']
        if form.validate_on_submit:
            # here we submit a form...which should be valid

            #this is for testing. take out return hello
            #return"hello"
            staff_email = User.query.filter_by(email=form.email.data).first()
            if staff_email:
                flash("email already used")
                return render_template('emailsearch.html', form=form)
            else:
                target=request.form.get('hiddenphone')
                form.mobilephone.data = target
                newuser = request.form.get('hiddenemail')

                print("good stuff")
                print(gsa_register)
                
                newpass = request.form.get('password')
                newpassword = bcrypt.generate_password_hash(newpass)
                
                # now add the user to the database
                
                adduser = User(email=form.email.data,
                    password=newpassword,
                    active=1,
                    firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    phone=form.mobilephone.data)

                db.session.add(adduser)
                print(form.sunavail.data)
                print(form.monavail.data)
                # flush will create an entry in the database that cannot be over written.
                # flush then gives us the user id. 
                # we need the user id to go along with the employee id.

                db.session.flush()
                db.session.commit()

                newid = adduser.id
                
                print(newid)
                picture_file = '3d611379cfdf5a89.jpg'

                # Here we create the new employee in the database.

                emp = Employee(user_id=newid,
                                firstname=form.firstname.data,
                                lastname=form.lastname.data,
                                store_id=1,
                                addressone="tbd",
                                addresstwo="tbd",
                                apt="tbd",
                                city="tbd",
                                province="tbd",
                                country="tbd",
                                postal="tbdtbd",
                                email=form.email.data,
                                mobilephone=form.mobilephone.data,
                                trainingid="tbd",
                                trainingpassword="tbd",
                                image_file=picture_file,
                                iprismcode="tbd",
                                mon_avail=form.monavail.data,
                                tue_avail=form.tueavail.data,
                                wed_avail=form.wedavail.data,
                                thu_avail=form.thuavail.data,
                                fri_avail=form.friavail.data,
                                sat_avail=form.satavail.data,
                                sun_avail=form.sunavail.data)
                                     
                db.session.add(emp)  
                        # flush will get the id of the pending user so that
                        # we can add the raining information     
                db.session.flush()

                # here we are adding the training courses and the compelted dates.
                # adding the dates requires some work.
                # the data has to be in the format that the database can read.

                # need all of this  
            
                #r = request.form.getlist("completeddate")
                #g = request.form.getlist("myCheck2")
                f = emp.id
                
                print(emp.id)
                yy = 0
                y=1
                
                for x in coursecount:
                    empgrade = Grade(
                                employee_id=f,
                                course_id=y,
                                completed = 0
                                )  
                    print(f, y)
                    db.session.add(empgrade)
                    y += 1
                    yy += 1
           
                #print(emp)
                    
                # here we add the defuault role of GSA to new hire
                # you cannot add to the association table 
                # instead you insert
        
                addrole = roles_users.insert().values(user_id = newid, role_id= 5)        
                db.session.execute(addrole)

                db.session.commit()
       
            ''' email = emp.email
                message = Mail(
                from_email=DEFAULT_SENDER,
                to_emails= email,
                subject = 'Welcome to Petro Canada',
                
                )
                
                message.dynamic_template_data = {
                    
                    'name':emp.firstname,
                    'userid':emp.trainingid,
                    'password':emp.trainingpassword,
                    'login':emp.email

                }
            
                message.template_id = SENDGRID_NEWHIRE_ID
            
                response = sg.send(message)
            '''

            message=client.messages\
            .create(
            body="Hello. This is Terry from Petro Canada. Thank you for registering your account. Please go to www.paulfuther.com to log in. We need you to complete your empoloyee file. Please talk to your manager if you have any questions.",
            from_=twilio_from,
            to=target
            )
        flash("Account Created")
        return redirect(url_for('login'))
              
    return redirect('emailsearch.html', form=form)
    
    
@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    
    store_list = Store.query.order_by(Store.number).all()
    form = request.form   
    ugh = form['search_string']
    ugh2 = ugh
    #print(ugh2)
    store_id = Store.query.filter_by(number=ugh2).first()
    storeid = store_id.id
    print(storeid)
    gsa = Employee.query.filter_by(store_id=storeid)
    
   
    return render_template('hrlist.html', gsa=gsa, store_list = store_list, ugh2=ugh2)


def save_hrpicture(form_hrpicture):
    # uses PIL from Pillow
    # saving to two places. thumbnales for the list and mobile for the phone
    # image = form_hrpicture
    # read the miage but then create a new variable to modify size of image
    
    thumb = 30,30
    medium = 150,150
    large = 250,250
    
    random_hex = secrets.token_hex(8)
    
    _, f_ext = os.path.splitext(form_hrpicture.filename)
    hrpicture_fn = random_hex + f_ext 
    
    
    picture_paththumb = os.path.join(
        app.root_path, 'static/empfiles/thumb', hrpicture_fn)
    output_size = (150, 150)
    
    i = Image.open(form_hrpicture)
    #i.thumbnail(output_size, Image.LANCZOS)
    newi = i.resize((150,150))
    newi.save(picture_paththumb)
    print (newi.size)
    
    picture_pathmobile = os.path.join(
        app.root_path, 'static/empfiles/mobile', hrpicture_fn)
    output_size2 = (250, 250)

    i2 = Image.open(form_hrpicture)
    #i2.thumbnail(output_size2, Image.LANCZOS)
    newi2 = i2.resize((250,250))
    newi2.save(picture_pathmobile)
    print(newi2.size)
    
    return hrpicture_fn

@app.route("/updategsa<int:staff_id>", methods=['GET', 'POST'])
@login_required
def updategsa(staff_id):
    # Here we are getting the row of data based on the index, which is staff_id and
    #generatating a query under gsa
    #form is then populated with that data and published

    #when changes are made the form.data attribut is changed also
    #you can then compare the new form data using .data with old data use gsa.data
    #note below that some data is int and some is text. they need to be the same for the compares
    
    
    gsa = Employee.query.get(staff_id)
    print(gsa.dob)
    
    gradelist = Grade.query\
        .filter_by(employee_id = staff_id)\
        .join(Employee, Employee.id == Grade.employee_id)\
        .join(Course, Course.id == Grade.course_id)\
        .add_columns(Course.name, Grade.completed)
  
    
    image_file = url_for(
        'static', filename='empfiles/mobile/' + gsa.image_file)
    
    
    form = EmployeeUpdateForm(obj=gsa)
    
    if request.method == "GET":
        print(form.dob.data)
        return render_template('employeeupdate.html', image_file=image_file, form=form, gsa=gsa)
 
@app.route("/update_gsa_contact<int:staff_id>", methods=['GET','POST'])
@login_required
def update_gsa_contact(staff_id):
    if request.method == "POST":
        r=request.form.to_dict()
        
        gsa = Employee.query.get(staff_id)
    
        form = EmployeeUpdateForm(obj=gsa)
        image_file = url_for('static', filename='empfiles/mobile/' + gsa.image_file)
        if form.hrpicture.data:
           picture_file = save_hrpicture(form.hrpicture.data) 
           print(form.hrpicture.data)
        else:
            picture_file = '3d611379cfdf5a89.jpg'
        gsaphone = gsa.mobilephone
        print(form.addressone.data)
        gsaemail = gsa.email
        gsapostal = gsa.postal
        gsatrainingid = gsa.trainingid
        gsatrainingpassword = gsa.trainingpassword
        gsaiprism = gsa.iprismcode

        phone = form.mobilephone.data        
        postal = form.postal.data
        trainingid = form.trainingid.data
        trainingpassword = form.trainingpassword.data
        iprismcodecheck = form.iprismcode.data

        emp = Employee.query.filter_by(mobilephone=text(phone)).first()
        emailcheck = Employee.query.filter_by(email=form.email.data).first()
        
        postalcheck = Employee.query.filter_by(postal=postal).first()
        trainingidcheck = Employee.query.filter_by(trainingid=trainingid).first()
        trainingpasswordcheck = Employee.query.filter_by(
                trainingpassword=trainingpassword).first()
        iprismcheck = Employee.query.filter_by(iprismcode=iprismcodecheck).first()

        if gsaphone == phone:
            print("same mobile")
        else:
            if emp:
                    flash("mobile already used")
            return render_template('employeeupdate.html', form=form, gsa=gsa)

        if gsa.email == form.email.data:
                print("same email")
        else:
            if emailcheck:
                    flash("email already used")
            return render_template('employeeupdate.html', form=form, gsa=gsa)

        if gsa.trainingid == form.trainingid.data:
                print("same user id ")
        else:
            if trainingidcheck:
                    flash("user id already exists")
            return render_template('employeeupdate.html', form=form, gsa=gsa)

        if gsa.trainingpassword == form.trainingpassword.data:
                print("same training password")
        else:
            if trainingpasswordcheck:
                    flash("training password already exists")
            return render_template('employeeupdate.html', form=form, gsa=gsa)
        
        #print(request.form)
        #for x,y in r.items():
        #    print (x,y)
        gsa.dob=form.dob.data
        gsa.startdate=form.startdate.data
        gsa.addressone=form.addressone.data
        gsa.addresstwo=form.addresstwo.data
        gsa.apt=form.apt.data
        gsa.city=form.city.data
        gsa.province=form.province.data
        gsa.postal=form.postal.data
        gsa.country=form.country.data
        gsa.trainingid=form.trainingid.data
        gsa.trainingpassword=form.trainingpassword.data
        gsa.iprismcode=form.iprismcode.data
        gsa.mon_avail=form.mon_avail.data
        gsa.tue_avail=form.tue_avail.data
        gsa.wed_avail=form.wed_avail.data
        gsa.thu_avail=form.thu_avail.data
        gsa.fri_avail=form.fri_avail.data
        gsa.sat_avail=form.sat_avail.data
        gsa.sun_avail=form.sun_avail.data
        gsa.image_file=picture_file
                                     
        db.session.commit()


        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    return "none"
    
@app.route("/addemployee", methods=['GET', 'POST'])
@login_required
@roles_accepted('Admin', 'Manager')
def addemployee():

    form = EmployeeForm()   
    coursecount = Course.query.all()
    #print(coursecount)
    # the get is for the first load of the page
    
    if request.method=="GET":
        return render_template('employee.html', title='Employee Information',form=form)

    # here we submit a form...which should be valid

    #this is for testing. take out return hello
    #return"hello"
    
    if form.validate_on_submit():
        print("success")
       
        target=request.form.get('hiddenphone')
        form.mobilephone.data = target
        #print(target)
        
        #print("checker",checker)
        teststore = form.store.data
        #print(teststore.id)
        newuser = request.form.get('hiddenemail')

        # generate a randome password

        symbols = ['*', '%', '£'] # Can add more
        password = ""
        for _ in range(9):
            password += secrets.choice(string.ascii_lowercase)
            password += secrets.choice(string.ascii_uppercase)
            password += secrets.choice(string.digits)
            password += secrets.choice(symbols)
            print(password)
        # here we encrypt the password.

        newpass = password
        newpassword = bcrypt.generate_password_hash(newpass)
        
        # now add the user to the database

        adduser = User(email=newuser,
                    password=newpassword,
                    active=1,
                    firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    phone=form.mobilephone.data)

        db.session.add(adduser)
        # flush will create an entry in the database that cannot be over written.
        # flush then gives us the user id. 
        # we need the user id to go along with the employee id.

        db.session.flush()
        db.session.commit()

        newid = adduser.id
        
        print(newid)
        
        if form.hrpicture.data:
           picture_file = save_hrpicture(form.hrpicture.data) 
        else:
            picture_file = '3d611379cfdf5a89.jpg'
       
        #print (form.manager.data.id)
        #print (form.store.data.id)

        # Here we create the new employee in the database.

        emp = Employee(user_id=newid,
                       firstname=form.firstname.data,
                       lastname=form.lastname.data,
                       store=form.store.data,
                       addressone=form.addressone.data,
                       addresstwo=form.addresstwo.data,
                       apt=form.apt.data,
                       city=form.city.data,
                       province=form.province.data,
                       country=form.country.data,
                       postal=form.postal.data,
                       email=form.email.data,
                       mobilephone=form.mobilephone.data,
                       sinexpire=form.sinexpire.data,
                       trainingid=form.trainingid.data,
                       trainingpassword=form.trainingpassword.data,
                       manager=form.manager.data.id,
                       image_file=picture_file,
                       iprismcode=form.iprismcode.data,
                       mon_avail=form.monavail.data,
                       tue_avail=form.tueavail.data,
                       wed_avail=form.wedavail.data,
                       thu_avail=form.thuavail.data,
                       fri_avail=form.friavail.data,
                       sat_avail=form.satavail.data,
                       sun_avail=form.sunavail.data)
                                     
        db.session.add(emp)  
        # flush will get the id of the pending user so that
        # we can add the raining information     
        db.session.flush()
        
        print(emp.store, emp.manager)
        print(type(form.store.data))
        
        # here we are adding the training courses and the compelted dates.
        # adding the dates requires some work.
        # the data has to be in the format that the database can read.

        # need all of this  
    
        #r = request.form.getlist("completeddate")
        #g = request.form.getlist("myCheck2")
        f = emp.id
        
        print(emp.id)
        yy = 0
        y=1
        
        for x in coursecount:
            empgrade = Grade(
                             employee_id=f,
                             course_id=y,
                             completed = 0
                             )  
            print(f, y)
            db.session.add(empgrade)
            y += 1
            yy += 1
           
        #print(emp)
            
        # here we add the defuault role of GSA to new hire
        # you cannot add to the association table 
        # instead you insert
        
        addrole = roles_users.insert().values(user_id = newid, role_id= 5)        
        db.session.execute(addrole)

        db.session.commit()
       
        ''' email = emp.email
        message = Mail(
            from_email=DEFAULT_SENDER,
            to_emails= email,
            subject = 'Welcome to Petro Canada',
            
            )
            
        message.dynamic_template_data = {
                
                'name':emp.firstname,
                'userid':emp.trainingid,
                'password':emp.trainingpassword,
                'login':emp.email

            }
        
        message.template_id = SENDGRID_NEWHIRE_ID
            
        response = sg.send(message)
        '''

        flash('Employee has been added to the database', 'success')

        
        return render_template('newhirehomehr.html',emp=emp)
    return render_template('employee.html', form=form)
   
@app.route("/applications")
@login_required
@roles_required('Admin')
def Applications():
    return render_template('applications.html', title='Applications')

@app.route("/kpiconvert")
@login_required
def Kpiconvert():
    return render_template('kpiconvert.html', title='KPI Converter')

@app.route("/carwashkpiconvert")
@login_required
def CarwashKPIconvert():
    return render_template('carwashkpiconvert.html', title='Carwash KPI Converter')

@app.route("/tpfileconvert")
@login_required
def TPFileconvert():
    return render_template('teamperformanceconvert.html', title='Team Performance File Converter')

@app.route("/tpfileupload", methods=['POST'])
@login_required
def tpfileupload():

    if request.method == "POST":
        try:
            files = request.files.getlist('tpfileinputFile[]')

            newdf = []

            for file in files:
                input_filename = file
                #print(x)
                df_totalsheet = pd.read_excel(input_filename)
                #print(df_totalsheet.head)
                tp_date = (df_totalsheet.iat[8, 0])
                #print(tp_date)
                tp_store = (df_totalsheet.iat[6, 0])
                a, b1, c, d = tp_date.split()
                e, f, g = tp_store.split()
                tp_storefinal = g[:5]
                pd.to_datetime(b1)
                #print(b1)
                b = datetime.strptime(b1, "%m/%d/%Y").strftime("%b-%Y")
                pd.to_numeric(tp_storefinal)
                df = pd.read_excel(input_filename, skiprows=14)
                cols = list(df)
                #print(cols)
                dropcols = [2, 3, 6, 7, 8]
                df.drop(df.columns[dropcols], axis=1, inplace=True)
                df = df.rename(columns={'Performance Measure': 'one'})
                df.set_index('one', inplace=True)
                df = df.T
                df2 = df.index
                df['Gsa'] = df.index
                df['Store'] = tp_storefinal
                df.reset_index(drop=True, inplace=True)
                df.Gsa = df.Gsa.shift(1)
                df['Store'] = tp_storefinal
                df['date'] = b
                df['date'] = pd.to_datetime(df['date'], format="%b-%Y")
                df['date'] = df['date'].dt.date
                df.dropna(subset=['Shift Count'], how='all', inplace=True)
                #print(df)
                df = df[['date', 'Store', 'Gsa', 'Shift Count', 'Average Check',
                        '2 Pack Ratio', 'Season Pass', 'Wash & Go', 'In-Store Premium Ratio',
                        'Crind Ratio', 'Campaign Deals Total', 'Campaign Deals to In-Store Transaction Ratio',
                        'Campaign Deals by Confectionery', 'Campaign Deals by Salty Snacks',
                        'Campaign Deals by Alternative Beverages', 'Campaign Deals by Packaged Soft Drinks',
                        'Hot Beverages', 'FSR Redemptions', '$1 Snack Redemptions']]

                newdf.append(df)
            newdf = pd.concat(newdf)

        except:
            flash('Something went wrong')
            return render_template('applications.html')
            
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    newdf.to_excel(writer)
    writer.save()
    output.seek(0)

    return send_file(output, attachment_filename="sfoutput.xlsx", as_attachment=True)

@app.route("/securityfileconvert")
@login_required
def SecurityFileconvert():
    return render_template('securityfileconvert.html', title='Security File Converter')



@app.route("/securityfileupload", methods=['POST'])
@login_required
def securityfileupload():

    if request.method == "POST":
        try:
            
            start = datetime.strptime('05:15:00', '%H:%M:%S').time()
            end = datetime.strptime('11:45:00', '%H:%M:%S').time()

            files = request.files.getlist('securityfileinputFile[]')
            newdf = []

            for file in files:
                inputfilename = file
                excel_file = inputfilename
                store_number = file
                a = str(store_number)
                b = re.search('\d+', a).group()
                df = pd.read_csv(excel_file, sep='\t', header=None)
                df.columns = ['Text']

                #use regular expresssions re to find character sets in a string of data
                #in a dataframe

                df['Date'] = df['Text'].str.extract(
                    r"([\d]{1,2} [ADJFMNOS]\w* [\d]{2})").copy()


                df2 = df[df['Text'].str.contains('Pump', na=False)].copy()
                if df2.empty:
                    continue
                df2['Store'] = b
                newdf.append(df2)

            newdf = pd.concat(newdf) 
            newdf['Date'] = pd.to_datetime(newdf['Date'], dayfirst=True)
            newdf['Time'] = newdf['Text'].str.extract(r"([\d]{1,2}\:[\d]{1,2}\:[\d]{1,2})")
            newdf['Time'] = pd.to_datetime(newdf['Time'], format='%H:%M:%S').dt.time
            newdf = newdf[newdf['Time'].between(start, end)]
            newdf.set_index('Date', inplace=True) 

        except:
            flash('Something went wrong')
            return render_template('applications.html')

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    newdf.to_excel(writer)
    writer.save()
    output.seek(0)

    return send_file(output, attachment_filename="sfoutput.xlsx", as_attachment=True)

@app.route("/securityfilenegconvert")
@login_required
def SecurityFilenegconvert():
    return render_template('securityfilenegconvert.html', title='Security File Negative Sales Converter')

@app.route("/securityfilenegupload", methods=['POST'])
@login_required
def securityfilenegupload():

    if request.method == "POST":

        try:
            files = request.files.getlist('securityfileneginputFile[]')
            newdf = []

            for file in files:
                inputfilename = file
                print(inputfilename)
                excel_file = inputfilename
                store_number = file
                a = str(store_number)
                b = re.search('\d+', a).group()
                df = pd.read_csv(excel_file, sep='\t', header=None)
                df.columns = ['Text']
                df['Date'] = df['Text'].str.extract('(.. ... ..)', expand=False).copy()
                df2 = df[df['Text'].str.contains('NEGATIVE', na=False)].copy()
                #if df2.empty:
                #    flash('No Negative Sales')
                #    return render_template('applications.html') 

                df2['Store'] = b
                print(df2)
                newdf.append(df2)

                print(newdf)

            newdf = pd.concat(newdf)

            newdf['Date'] = pd.to_datetime(
            newdf['Date'], dayfirst=True)  # .dt.strftime('%d %m %Y')

            newdf['Time'] = newdf['Text'].str.extract(r"([\d]{1,2}\:[\d]{1,2}\:[\d]{1,2})")
            newdf['Time'] = pd.to_datetime(newdf['Time'], format='%H:%M:%S').dt.time
            newdf.set_index('Date', inplace=True)
        except:
            flash('Something went wrong')
            return render_template('applications.html')
        
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    newdf.to_excel(writer)
    writer.save()
    output.seek(0)

    return send_file(output, attachment_filename="sfoutput.xlsx", as_attachment=True)

@app.route("/securityfilevoidconvert")
@login_required
def SecurityFilevoidconvert():
    return render_template('securityfilevoidconvert.html', title='Security File Converter')

@app.route("/securityfilevoidupload", methods=['POST'])
@login_required
def securityfilevoidupload():

    if request.method == "POST":

        try:
            files = request.files.getlist('securityfilevoidinputFile[]')
            newdf = []

            for file in files:
                inputfilename = file
                print(inputfilename)
                excel_file = inputfilename
                store_number = file
                a = str(store_number)
                b = re.search('\d+', a).group()
                df = pd.read_csv(excel_file, sep='\t', header=None)
                df.columns = ['Text']
                df['Date'] = df['Text'].str.extract('(.. ... ..)', expand=False).copy()
                df2 = df[df['Text'].str.contains('Voided', na=False)].copy()
                #if df2.empty:
                #    flash('No Negative Sales')
                #    return render_template('applications.html') 

                df2['Store'] = b
                print(df2)
                newdf.append(df2)

                print(newdf)

            newdf = pd.concat(newdf)

            newdf['Date'] = pd.to_datetime(
            newdf['Date'], dayfirst=True)  # .dt.strftime('%d %m %Y')

            newdf['Time'] = newdf['Text'].str.extract(r"([\d]{1,2}\:[\d]{1,2}\:[\d]{1,2})")
            newdf['Time'] = pd.to_datetime(newdf['Time'], format='%H:%M:%S').dt.time
            newdf.set_index('Date', inplace=True)
        except:
            flash('Something went wrong')
            return render_template('applications.html')
        
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    newdf.to_excel(writer)
    writer.save()
    output.seek(0)

    return send_file(output, attachment_filename="sfoutput.xlsx", as_attachment=True)

@app.route("/carwashkpiupload", methods=['POST'])
@login_required
def carwashkpiupload():

    if request.method == "POST":
        
        try:
        
            file = request.files['cwinputFile']
            print(file)
            filename = secure_filename(file.filename)

            excel_file = file

            df = pd.read_excel(excel_file, skiprows=9, usecols=(3, 4, 5))

            columnheaders = (df.columns.tolist())
            current_cwdate = (columnheaders[1])
            x = datetime.strptime(current_cwdate, "%Y/%b").strftime("%b-%Y")
            previous_cwdate = (columnheaders[2])
            px = datetime.strptime(previous_cwdate, "%Y/%b").strftime("%b-%Y")

            #get list of sheets
            xls = pd.ExcelFile(excel_file)
            res = len(xls.sheet_names)
            nres = res-1

            #get type for the tab names they are a list
            #print(type(res))

            tabs = (xls.sheet_names)
            #print(type(tabs))
            newtabs = (tabs[0:-1])

            dffinal2 = []

            for line in newtabs:

                #first half of spreadsheet

                type = line.split("_")[1]
                df = pd.read_excel(excel_file, sheet_name=line,
                                skiprows=9, usecols=(3, 4, 5))
                df.columns = ['a', x, px]
                df['store'] = type
                df['Date'] = x
                df1 = df.iloc[1:3].copy()
                df1['label'] = 'revenue'
                df2 = df.iloc[4:14].copy()
                df2['label'] = 'expense'
                df3 = df.iloc[17:26].copy()
                df3['label'] = 'operation performnce'
                df4 = df.iloc[30:37].copy()
                df4['label'] = 'sales performance'
                df5 = df.iloc[40:45].copy()
                df5['label'] = 'paid units %'
                df6 = df.iloc[46:52].copy()
                df6['label'] = 'paid units Instore and Crind'
                df7 = df.iloc[54:68].copy()
                df7['label'] = 'total units'
                dfpartone = pd.concat([df1, df2, df3, df4, df5, df6, df7])

                #second half of spreadsheet

                dftwo = pd.read_excel(
                    excel_file, sheet_name=line, skiprows=9, usecols=(3, 8, 9))
                dftwo.columns = ['a', x, px]

                dftwo['store'] = type
                dftwo['Date'] = x

                df8 = dftwo.iloc[1:3].copy()
                df8['label'] = 'revenue per car'
                df9 = dftwo.iloc[4:14].copy()
                df9['label'] = 'expense per car'
                df10 = dftwo.iloc[40:45].copy()
                df10['label'] = '% fullfillment per car'
                df11 = dftwo.iloc[46:52].copy()
                df11['label'] = 'paid fullfillments'
                df12 = dftwo.iloc[54:68].copy()
                df12['label'] = 'total fullfillments'
                dfparttwo = pd.concat([df8, df9, df10, df11, df12])

                dffinal = pd.concat([dfpartone, dfparttwo])

                #final table of data

                dffinal2.append(dffinal)

            #reorganise columns

            dffinal2 = pd.concat(dffinal2)
            dffinal2.columns = ['Item', 'Amount', px,
                'Store', 'Date', 'Classification']

            dffinal2 = dffinal2[['Date', 'Store',
                'Classification', 'Item', 'Amount', px]]
            dffinal2['Amount'] = pd.to_numeric(
                dffinal2['Amount'], errors='coerce')
            dffinal2['Date'] = pd.to_datetime(dffinal2['Date'], format='%b-%Y')
            dffinal2['Date'] = dffinal2['Date'].dt.date

            #save final spreadsheet

            #outputfilename = asksaveasfilename(filetypes=[("Excel files","*.xlsx")])
            #dffinal2.to_excel(outputfilename + ".xlsx", engine='xlsxwriter')

            #dffinal.to_excel("test.xlsx")

        except:
            flash('Something went wrong')
            return render_template('applications.html')

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    dffinal2.to_excel(writer)
    writer.save()
    output.seek(0)

    return send_file(output, attachment_filename="cwoutput.xlsx", as_attachment=True)

    return render_template("applications.html")

# upload had to be changed to upload2 due to ckeditor in admin

@app.route("/upload2", methods=['POST'])
@login_required
def upload2():

    if request.method == "POST":
        
        try:
        
            file = request.files['inputFile']
            print(file)
            filename = secure_filename(file.filename)

            #this will save file to folder in root named Files
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            def convert_amount(val):
                    """
                    Convert the string number value to a float
                    - Remove $
                    - Remove commas
                    - Convert to float type
                    """
                    new_val = val.replace(',', '').replace(
                        '%', '').replace('/0', '')
                    return pd.to_numeric(new_val)

            excel_file = file
            df = pd.read_excel(excel_file, header=3)

                #print (df)

            xls = pd.ExcelFile(excel_file)
            res = len(xls.sheet_names)
            tabs = (xls.sheet_names)
            
            print(tabs)
            newtabs = (tabs)
            columnheaders = (df.columns.tolist())
            print (columnheaders)
            kpidate = (columnheaders[2])

            current_kpidate = datetime.strptime(
            kpidate, "%Y-%m").strftime("%b-%Y")
                    #print (current_kpidate)
            newkpi = []
            finalkpi = []

            print("ready to loop")
            for x in newtabs:
                type = x[:5]
                        #print(type)
                data = pd.read_excel(
                excel_file, sheet_name=x, skiprows=3, usecols=range(8))
                data['store'] = type
                data['Date'] = current_kpidate
                finalkpi.append(data)

            finalkpi = pd.concat(finalkpi)

            print(finalkpi)

                    #name columns

            finalkpi.columns = ['Category1', 'Category2', kpidate, 'Value2', 'value3','value4','value5','Rolling','Store','Date']
                        #reorder columns

            finalkpi = finalkpi[['Date', 'Store', 'Category1', 'Category2',kpidate,'Value2','value3','value4','value5','Rolling']]

            """combine two columns
                """
            finalkpi['Category'] = finalkpi.Category2.combine_first(
            finalkpi.Category1)

            finalkpi = finalkpi[['Date', 'Store', 'Category', kpidate,'Value2','value3','value4','value5','Rolling']]

            finalkpi['Date'] = pd.to_datetime((finalkpi['Date']), format='%b-%Y')

            finalkpi[kpidate] = finalkpi[kpidate].apply(convert_amount)
            finalkpi['Value2'] = finalkpi['Value2'].apply(convert_amount)
            finalkpi['value3'] = finalkpi['value3'].apply(convert_amount)
            finalkpi['value4'] = finalkpi['value4'].apply(convert_amount)
            finalkpi['value5'] = finalkpi['value5'].apply(convert_amount)
            finalkpi['Rolling'] = finalkpi['Rolling'].apply(convert_amount)

            print(finalkpi)

                    #create output stream

        except:
            flash('Something went wrong')
            return render_template('applications.html')

        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        finalkpi.to_excel(writer)
        writer.save()
        output.seek(0)

        return send_file(output, attachment_filename="output.xlsx", as_attachment=True)

        print(finalkpi)

    return render_template("applications.html")

#This route used sql alchemy to access the grwothkpi tables in the MySql database

#@app.route("/newfile")
#@login_required
#def newfile():
#    return render_template('ckfile.html')
    


@app.route('/files/<filename>')
def uploaded_files(filename):
    path = app.config['UPLOADED_PATH']
    return send_from_directory(path, filename)

@app.route('/upload', methods=['POST'])

def upload():
    f = request.files.get('upload')
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    url = url_for('uploaded_files', filename=f.filename)
    return upload_success(url=url)

@app.route("/cstoresales")
@login_required
def data():
    
    metadata = MetaData(engine)
    table = Table('growthkpi', metadata,  autoload=True)
                              
    s = select([table.c.Amount,
                 table.c.Date,
                ])\
        .where(and_(table.c.Store == '48314',
                table.c.Category == 'Total C-Store Sales ($)',
                table.c.Date >= "2017-04-01"))

        
    rs = s.execute()
    
    newdata = []
    content = {}
    for result in rs:
       
       content = {'date': result[1], 'sales': result[0]}
       newdata.append(content)
       content = {}
       #print(newdata)
       
    return jsonify(newdata)

@app.route("/cstoremargin")
@login_required
def thirddata():

    metadata = MetaData(engine)
    table = Table('growthkpi', metadata,  autoload=True)

    s = select([table.c.Amount,
                table.c.Store,
                extract("month", table.c.Date,)])\
                .where(and_(table.c.Category == 'Total C-Store Margin ($)',
                table.c.Date >= "2019-01-01"))
                #.order_by(table.desc(table.c.Store))
                #.all()

    rs3 = s.execute()

    newdata3 = []
    content3 = {}
    for result in rs3:

       content3 = {'date': result[2],'store': result[1], 'margin': result[0]}
       newdata3.append(content3)
       content3 = {}
       print(newdata3)

    return jsonify(newdata3)


        #(table.c.Store == '48314',


@app.route("/data")
@login_required
def seconddata():
    
    metadata = MetaData(engine)
    table = Table('growthkpi', metadata,  autoload=True)

    s = select([table.c.Amount,
        extract("month", table.c.Date,
                )])\
        .where(and_(table.c.Store == '48314',
                table.c.Category == 'Total Fuel Volume',
                table.c.Date >= "2019-01-01"))
   
    rs2=s.execute()
    newdata2 = []
    content2 = {}
    for result in rs2:
       content2 = {'date': result[1], 'volume': result[0]}
       newdata2.append(content2)
       content2 = {}
       #print(newdata2)
    return jsonify(newdata2)

@app.route("/carwashmargin")
@login_required
def carwashmargin():

    metadata = MetaData(engine)
    table = Table('car wash', metadata,  autoload=True)

    s = select([table.c.Amount,
                    table.c.Date,
                        ])\
        .where(and_(table.c.Store == '48314',
                    table.c.Classification == 'revenue',
                    table.c.Item == 'CW Commission Revenue (before crop)',
                    table.c.Date >= "2019-04-01"))

    rs4 = s.execute()
    newdata4 = []
    content4 = {}
    for result in rs4:
       content4 = {'date': result[1], 'commissions': result[0]}
       newdata4.append(content4)
       content4 = {}
       #print(newdata4)
    return jsonify(newdata4)

@app.route("/charts")
@login_required
def charts():
    return render_template('charts.html')

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html')

def save_picture(form_picture):
    thumb = 30, 30
    medium = 150, 150
    large = 250, 250

    random_hex = secrets.token_hex(8)

    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext

    picture_paththumb = os.path.join(
        app.root_path, 'static/profile_pics/thumb', picture_fn)
    output_size = (150, 150)

    i = Image.open(form_picture)
    i.thumbnail(output_size, Image.LANCZOS)
    i.save(picture_paththumb)
    print(i.size)

    picture_pathmobile = os.path.join(
        app.root_path, 'static/profile_pics/mobile', picture_fn)
    output_size2 = (250, 250)

    i2 = Image.open(form_picture)
    i2.thumbnail(output_size2, Image.LANCZOS)

    i2.save(picture_pathmobile)

    return picture_fn
    

def save_inc_picture(form_picture):
    

    random_hex = secrets.token_hex(8)

    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext

    picture_path_inc = os.path.join(
        app.root_path, 'static/incidentpictures', picture_fn)
   
    picture_fn.save(picture_path_inc)
    print(picture_fn.size)

    return picture_fn
    
