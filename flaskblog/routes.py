from flask import Flask, render_template, jsonify, request, send_file, url_for, redirect, flash, abort
#from flaskblog import app, db, Bcrypt
from flaskblog.forms import LoginForm, EmployeeForm, EmployeeUpdateForm
from flaskblog import app, Employee, User, Role, bcrypt, db, Course
#from flask_user import roles_required
from flask_security import roles_required, login_required
#from flaskblog.models import  User, Role, Employee
from io import BytesIO
import os
from werkzeug.utils import secure_filename
import pandas as pd
import numpy
import openpyxl
import xlrd
import xlwt
import xlsxwriter
from flaskblog import datetime
from flask_moment import Moment
#from flask_login import login_user, current_user, logout_user, login_required
#from flask_user import roles_required
import secrets
from PIL import Image
import re, base64
from sqlalchemy.sql import text, select
from sqlalchemy import *
from sqlalchemy import extract
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

moment = Moment(app)


@app.route("/")
@app.route("/home")
@login_required
def home():
    #return url_for('admin.index')
    
    return render_template('layout.html')
    #return render_template('home.html')


#@app.route("/login", methods=['GET', 'POST'])
#def login():
 #   if current_user.is_authenticated:
 #       return redirect(url_for('home'))

  #  form = LoginForm()

   # if form.validate_on_submit():
   #     user = User.query.filter_by(email=form.email.data).first()

    #    password = bcrypt.checkpw(user.password.encode(), user.passowrd.pwd.encode())
        #print(user.password)
        #print(password)
        #hp = bcrypt.check_password_hash(user.password, password)
        #print(hp)
    #    if user and bcrypt.check_password_hash(user.password, form.password.data):

     #       login_user(user, remember=form.remember.data)
      #      return redirect(url_for('hrhome'))
      #  return '<h1> Invalid Credentials </h1>'

        #return render_template('home.html')

   # return render_template('login.html', form=form)



@app.route("/hrhome")
@login_required
def hrhome(): 
    return render_template('hrhome.html')

@app.route("/hrfile<int:staff_id>")
@login_required
def hrfile(staff_id):
    gsa = Employee.query.get(staff_id)
    return render_template('hrfile.html', gsa=gsa)

@app.route("/hrlist", methods =['GET', 'POST'])
@login_required
def hrlist():
    return render_template('hrlist.html')

@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    form=request.form  
    search_value=form['search_string']
    if search_value == "all":
        gsa = Employee.query.order_by(Employee.store).all()
        
        #for staff in gsa:
         #   print(staff.id)
        return render_template('hrlist.html', gsa=gsa) 
      
    gsa1 = Employee.query.filter_by(store=search_value)
    gsa = gsa1.order_by(Employee.store).all()
        
    #for staff in gsa:
        #print(staff.firstname)
    return render_template('hrlist.html', gsa=gsa)


@app.route("/employeetest", methods=['GET', 'POST'])
def employeetest():
    
    course = Course.query.all()
    
    
    if request.method == "POST":
    
        first_name = request.form['firstname']
        nick_name = request.form['nickname']
        store_number = request.form['store']
        address_one = request.form['addressone']
        address_two = request.form['addresstwo']
        apt_number = request.form['apt']
        city_city = request.form['city']
        province_province = request.form['province']
        country_country = request.form["country"]
        email_email = request.form["email"]
        mobile_phone = request.form["mobilephone"]
        SIN_number = request.form["SIN"]
        
        
        sd = datetime.strptime(request.form["Startdate"] , '%Y-%m-%d')
        start_date = sd.date()
        
        ed = datetime.strptime(request.form["Enddate"], '%Y-%m-%d')
        end_date = ed.date()
        
        
        
        last_name = request.form["lastname"]
        postal_code = request.form["postal"]
        training_id = request.form["trainingid"]
        training_password = request.form["trainingpassword"]
        manager_name = request.form["manager"]
        active_yn = request.form["active"]
        iprism_code = request.form["iprismcode"]
    
        print(first_name)
        print(iprism_code)
        print(start_date)

        #for course in course:
        #print(request.form.getlist("completed[]"))
        #print(request.form.getlist("course"))

        y=1
        for x in request.form.getlist("completed"):
            x2 = int(x)
           # print ((x2))
            id = x2
            #print(id, type(id))
            yy=Course.query.get(y)
            print(yy, x2)
            y +=1
          
            
        #for course in course:
         #   print (type(course.id))
         
    
        picture_file = '3d611379cfdf5a89.jpg'
        #hashed_password = bcrypt.generate_password_hash(form.email.data).decode('utf-8')
        #hashed_SIN = bcrypt.generate_password_hash(form.SIN.data).decode('utf-8')

        emp = Employee(firstname=first_name, \
                        nickname=nick_name,\
                        store=store_number, \
                        addressone= address_one, \
                        addresstwo=address_two, \
                        apt= apt_number, \
                        city= city_city, \
                        province= province_province, \
                        country= country_country, \
                        email= email_email, \
                        mobilephone= mobile_phone, \
                        SIN= SIN_number,\
                        Startdate= start_date,\
                        Enddate= end_date,\
                        lastname= last_name,\
                        postal = postal_code,\
                        trainingid= training_id,\
                        trainingpassword= training_password,\
                        manager= manager_name,\
                        image_file=picture_file,\
                        active= active_yn,\
                        iprismcode= iprism_code)

        print(emp.apt)

        #db.session.add(emp)
        #db.session.commit()

        flash('Employee has been added to the database', 'success')

        return redirect(url_for('hrhome'))
    
    
    return render_template('employeetest.html', course=course)

def save_hrpicture(form_hrpicture):
    
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
    i.thumbnail(output_size, Image.LANCZOS)
    i.save(picture_paththumb)
    print (i.size)
    
    picture_pathmobile = os.path.join(
        app.root_path, 'static/empfiles/mobile', hrpicture_fn)
    output_size2 = (250, 250)

    i2 = Image.open(form_hrpicture)
    i2.thumbnail(output_size2, Image.LANCZOS)
    
    i2.save(picture_pathmobile)
    
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
    
    form = EmployeeUpdateForm(obj=gsa)
    
    #return render_template('employee.html', form=form, gsa=gsa)
    
    image_file = url_for(
        'static', filename='empfiles/mobile/' + gsa.image_file)
    
    
    gsaphone = gsa.mobilephone
    gsasin = gsa.SIN  
    gsaemail = gsa.email
    gsapostal = gsa.postal
    gsatrainingid = gsa.trainingid
    gsatrainingpassword = gsa.trainingpassword
    gsaiprism = gsa.iprismcode
    
    
    
    phone = form.mobilephone.data
    sin = int(form.SIN.data)
    postal = form.postal.data
    trainingid = form.trainingid.data
    trainingpassword = form.trainingpassword.data
    iprismcodecheck = form.iprismcode.data
    
    #add a pciture
    #print(form.hrpicture.data)
    
    emp = Employee.query.filter_by(mobilephone=text(phone)).first()
    emailcheck = Employee.query.filter_by(email=form.email.data).first()
    sincheck = Employee.query.filter_by(SIN=sin).first()
    postalcheck = Employee.query.filter_by(postal=postal).first()
    trainingidcheck = Employee.query.filter_by(trainingid=trainingid).first()
    trainingpasswordcheck = Employee.query.filter_by(trainingpassword=trainingpassword).first()
    iprismcheck = Employee.query.filter_by(iprismcode=iprismcodecheck).first()
    
    if gsaphone == phone:
        print("same mobile")
    else:
        if emp:
            flash("mobile already used")
            return render_template('employeeupdate.html', form=form, gsa=gsa)
        
    if gsaiprism == iprismcodecheck:
            print("same iprism")
    else:
        if iprismcheck:
            flash("iprism code already used")
            return render_template('employeeupdate.html', form=form, gsa=gsa)   
    

    if gsasin == sin:
       print("same sin")
    else:
        if sincheck:
            flash("sin already used")
            return render_template('employeeupdate.html', form=form, gsa=gsa)
        
    if gsa.email == form.email.data:
       print("same email")
    else:
        if emailcheck:
            flash("email already used")
            return render_template('employeeupdate.html', form=form, gsa=gsa)
        
    if gsa.postal == form.postal.data:
        print("same postal code")
    else:
        if postalcheck:
            flash("postal already exists")
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
    
    
    if form.validate_on_submit():
        if form.submit.data:
            form.populate_obj(gsa)
            
            # An updated SIN and or Email Address needs to be hashed before adding to database
            
            #hashed_password = bcrypt.generate_password_hash(
            #    form.email.data).decode('utf-8')
            
            #hashed_SIN = bcrypt.generate_password_hash(
            #form.SIN.data).decode('utf-8')
           
            if form.hrpicture.data:
                picture_file = save_hrpicture(form.hrpicture.data)
                gsa.image_file = picture_file
        
        #add hashed data to database
        
        #gsa.SIN = hashed_SIN
        #gsa.email = hashed_password
           
        db.session.commit()
        
        flash("info updated")
        return render_template('hrhome.html')
    
    elif form.delete.data:
            
            Employee.query.filter_by(id=staff_id).delete()
            db.session.commit()
    return render_template('employeeupdate.html', image_file=image_file, form=form,gsa=gsa)
    
@app.route("/hr", methods=['GET', 'POST'])
@login_required
def hr():
    
    form = EmployeeForm()    
    
    
    if form.validate_on_submit():
        if form.hrpicture.data:
           picture_file = save_hrpicture(form.hrpicture.data) 
        else:
            picture_file = '3d611379cfdf5a89.jpg'
        #hashed_password = bcrypt.generate_password_hash(form.email.data).decode('utf-8')     
        #hashed_SIN = bcrypt.generate_password_hash(form.SIN.data).decode('utf-8')
                
        emp = Employee(firstname=form.firstname.data,
                       nickname=form.nickname.data,
                       store=form.store.data,
                       addressone=form.addressone.data,
                       addresstwo=form.addresstwo.data,
                       apt=form.apt.data,
                       city=form.city.data,
                       province=form.province.data,
                       country=form.country.data,
                       email=form.email.data,
                       mobilephone=form.mobilephone.data,
                       SIN=form.SIN.data,
                       Startdate=form.Startdate.data,
                       Enddate=form.Enddate.data,
                       lastname=form.lastname.data,
                       postal=form.postal.data,
                       trainingid=form.trainingid.data,
                       trainingpassword=form.trainingpassword.data,
                       manager=form.manager.data,
                       image_file=picture_file,
                       active=form.active.data,
                       iprismcode=form.iprismcode.data,
                       tobstartdate=form.tobstartdate.data,
                       tobcompleted=form.tobcompleteddate.data,
                       tobexpireydate=form.tobexpirationdate.data,
                       tobcompliant=form.tobcompliant.data,
                       whmisstartdate=form.whmisstartdate.data,
                       whmiscompleted=form.whmiscompleteddate.data,
                       whmisexpireydate=form.whmisexpirationdate.data,
                       whmiscompliant=form.whmiscompliant.data,
                       ppestartdate=form.ppestartdate.data,
                       ppecompleted=form.ppecompleteddate.data,
                       ppeexpireydate=form.ppeexpirationdate.data,
                       ppecompliant=form.ppecompliant.data,
                       firestartdate=form.firestartdate.data,
                       firecompleted=form.firecompleteddate.data,
                       fireexpireydate=form.fireexpirationdate.data,
                       firecompliant=form.firecompliant.data,
                       emerstartdate=form.emerstartdate.data,
                       emercompleted=form.emercompleteddate.data,
                       emerexpireydate=form.emerexpirationdate.data,
                       emercompliant=form.emercompliant.data,
                       firstaidstartdate=form.firstaidstartdate.data,
                       firstaidcompleted=form.firstaidcompleteddate.data,
                       firstaidexpireydate=form.firstaidexpirationdate.data,
                       firstaidcompliant=form.firstaidcompliant.data,
                       foodstartdate=form.foodstartdate.data,
                       foodcompleted=form.foodcompleteddate.data,
                       foodexpireydate=form.foodexpirationdate.data,
                       foodcompliant=form.foodcompliant.data,
                       propanestartdate=form.propanestartdate.data,
                       propanecompleted=form.propanecompleteddate.data,
                       propaneexpireydate=form.propaneexpirationdate.data,
                       propanecompliant=form.propanecompliant.data,
                       hsstartdate=form.hsstartdate.data,
                       hscompleted=form.hscompleteddate.data,
                       hsexpireydate=form.hsexpirationdate.data,
                       hscompliant=form.hscompliant.data,
                       fuelstartdate=form.fuelstartdate.data,
                       fuelcompleted=form.fuelcompleteddate.data,
                       fuelexpireydate=form.fuelexpirationdate.data,
                       fuelcompliant=form.fuelcompliant.data, 
                       alonestartdate=form.alonestartdate.data,
                       alonecompleted=form.alonecompleteddate.data,
                       aloneexpireydate=form.aloneexpirationdate.data,
                       alonecompliant=form.alonecompliant.data,
                       violencestartdate=form.violencestartdate.data,
                       violencecompleted=form.violencecompleteddate.data,
                       violenceexpireydate=form.violenceexpirationdate.data,
                       violencecompliant=form.violencecompliant.data,
                       jointstartdate=form.jointstartdate.data,
                       jointcompleted=form.jointcompleteddate.data,
                       jointexpireydate=form.jointexpirationdate.data,
                       jointcompliant=form.jointcompliant.data,
                       co2startdate = form.jointstartdate.data,
                       co2completed = form.jointcompleteddate.data,
                       co2expireydate = form.jointexpirationdate.data,
                       co2compliant = form.jointcompliant.data)
                                     
        db.session.add(emp)
        db.session.commit()
        
        
       
        flash('Employee has been added to the database', 'success')
                
        return redirect(url_for('hrhome'))
    
    print(form.errors.items())
    #print("did not work")
    return render_template('employee.html', title='Employee Information', form=form)



@app.route("/applications")
#@login_required
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
                print(df_totalsheet.head)
                tp_date = (df_totalsheet.iat[8, 0])
                print(tp_date)
                tp_store = (df_totalsheet.iat[6, 0])
                a, b1, c, d = tp_date.split()
                e, f, g = tp_store.split()
                tp_storefinal = g[:5]
                pd.to_datetime(b1)
                print(b1)
                b = datetime.strptime(b1, "%m/%d/%Y").strftime("%b-%Y")
                pd.to_numeric(tp_storefinal)
                df = pd.read_excel(input_filename, skiprows=14)
                cols = list(df)
                dropcols = [2, 3, 6, 7, 8, 13, 14]
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
                print(df)
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
                excel_file = inputfilename
                store_number = file
                a = str(store_number)
                b = re.search('\d+', a).group()
                df = pd.read_csv(excel_file, sep='\t', header=None)
                df.columns = ['Text']
                df['Date'] = df['Text'].str.extract('(.. ... ..)', expand=False).copy()

                df2 = df[df['Text'].str.contains('NEGATIVE', na=False)].copy()

                if df2.empty:
                    continue

                df2['Store'] = b
                print(df2)
                newdf.append(df2)


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

@app.route("/upload", methods=['POST'])
@login_required
def upload():

    if request.method == "POST":
        
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
    newtabs = (tabs)
    columnheaders = (df.columns.tolist())
            #print (columnheaders)
    kpidate = (columnheaders[2])

    current_kpidate = datetime.strptime(
    kpidate, "%Y-%m").strftime("%b-%Y")
            #print (current_kpidate)
    newkpi = []
    finalkpi = []

    for x in newtabs:
        type = x[:5]
                  #print(type)
        data = pd.read_excel(
        excel_file, sheet_name=x, skiprows=3, usecols=range(8))
        data['store'] = type
        data['Date'] = current_kpidate
        finalkpi.append(data)

        finalkpi = pd.concat(finalkpi)

            #print(finalkpi)

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

            #create output stream

        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        finalkpi.to_excel(writer)
        writer.save()
        output.seek(0)

        return send_file(output, attachment_filename="output.xlsx", as_attachment=True)

        print(finalkpi)

        return render_template("applications.html")

#This route used sql alchemy to access the grwothkpi tables in the MySql database

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
    


