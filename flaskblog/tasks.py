
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

#works

CLOUDAMQP_URL = os.environ.get('CLOUDAMQP_URL')

celery = Celery('tasks', broker=CLOUDAMQP_URL)

@celery.task(name="print_hello")
def print_hello():
    return print("hello")


@celery.task(name="send_sms_testing")
def send_sms_testing():
    message=client.messages\
        .create(
            body="Hello from Paul",
            from_=twilio_from,
            to='+15196707469'
        )
    
@celery.task(name="call_stores_monthly")
def call_stores_monthly():
    twimlname = 'Monthly Mystershop and Site Evaluation'
    bulk_call = Twimlmessages.query.get(twimlname)
    twil_id = bulk_call.twimlid
        #print(twil_id)
        # this is using twilml machine learning text to speach.
        # this only goes out to stores.
    site = db.session.query(Store.number,Store.phone).all()
    for x in site:
            call = client.calls.create(
                            url=twil_id,
                            to=x.phone,
                            from_=twilio_from
        )              
      

@celery.task
def send_created_email(role_id, filename):
    with app.text_request_context():

        gsa = db.session.query(Employee.email, Employee.firstname, User,Role)\
        .filter((roles_users.c.user_id == User.id) & (roles_users.c.role_id == Role.id))\
            .join(User, Employee.user_id == User.id).order_by(Employee.firstname)\
        .filter(User.active == 1)\
            .filter(Role.id==role_id)\
        .all()

        # cycle through all emails and send the email with attachment if one exists.

        for user in gsa:
      
            message = Mail(
                from_email=DEFAULT_SENDER,
                to_emails=user.email,
                subject=subject,
                html_content=body
            )
        # add attachment if one exists.

            if uploaded_file:
                    with open('flaskblog/static/emailfiles/'+filename, 'rb') as f:
                        data = f.read()
                        f.close()
                    encoded_file = base64.b64encode(data).decode()
                    attachedFile = Attachment(
                            FileContent(encoded_file),
                            FileName(uploaded_file.filename),
                            FileType(uploaded_file.content_type),
                            Disposition('attachment')) 
                    message.attachment = attachedFile
            response=sg.send(message)
       



@celery.task
def send_bulk_email(role_id, templatename, filename):
    with app.test_request_context():    

        
        # this is bulk sms using the notify api from twilio.
        # first we grab all employees who are active users.
        # we need to search specifically for mobile phone
        
        bulkmessage = BulkEmailSendgrid.query.get(templatename)
        bm = bulkmessage.templateid
        gsa = db.session.query(Employee.email, Employee.firstname, User,Role)\
        .filter((roles_users.c.user_id == User.id) & (roles_users.c.role_id == Role.id))\
            .join(User, Employee.user_id == User.id).order_by(Employee.firstname)\
        .filter(User.active == 1)\
            .filter(Role.id==role_id)\
        .all()

        #print(bm)
        
        # gsa returns an object. Although we can serialise the object, we still
        # have issues generating the proper format for twilio rest api.
        # so we do it old school.
    
        ''' with open('flaskblog/static/attachments/siteevaluation.pdf', 'rb') as f:
            data = f.read()
            f.close()
        encoded_file = base64.b64encode(data).decode()
        attachedFile = Attachment(
                    FileContent(encoded_file),
                    FileName(uploaded_file.name),
                    FileType(uploaded_file.content_type),
                    Disposition('attachment')) 
            '''
       
        for user in gsa:
            message = Mail(
            from_email=DEFAULT_SENDER,
            to_emails= user.email)
            message.dynamic_template_data = {
                'subject':templatename,
                'name': user.firstname,

            }
            with open('flaskblog/static/emailfiles/'+filename, 'rb') as f:
                data = f.read()
                f.close()
            encoded_file = base64.b64encode(data).decode()
            attachedFile = Attachment(
                    FileContent(encoded_file),
                    FileName(filename),
                    FileType(filename.content_type),
                    Disposition('attachment')) 
            print(user.email)
            message.template_id = bm
            message.attachment=attachedFile
            response = sg.send(message)

            #print(user.email) 
      

@celery.task
def make_incident_file(file_list):

    form=file_list.get('form')
    file_names=file_list.get('file_names')
    reg_file_names = file_list.get('reg_file_names')

    print(Incident.id)
    # get all of the information from the form

    if form.validate_on_submit():
            pics= request.files.getlist('photos[]')
            hires_pics = request.files.getlist('photoshires[]')
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
            for pic in  reg_file_names:
                if not pic:
                    pass
                else:
                    incimage = incident_files(image=pic,
                                    incident_id = inc.id)
                    db.session.add(incimage)

            for hrpic in  file_names:
                if not hrpic:
                    pass
                else:
                    incimage = incident_files(image=hrpic,
                                    incident_id = inc.id)
                    db.session.add(incimage)
            db.session.commit()

            print(inc.id)
            file_id = int(inc.id)
            
            flash('Your form has been submitted, uploaded to dropbox and sent to the ARL. Thank you', 'success')
            
            # once the data has been written to the database, we create a pdf.
            # we call a task mamanger to do this. That is the apply_async 
            make_incident_pdf.apply_async(args=[file_id], countdown=10)

            #return("good")
            return render_template('layout.html')
           
    return render_template('eventreport.html', form=form)

@celery.task
def make_incident_pdf(file_id):
    with app.test_request_context():
        rol =  User.query.filter(User.roles.any(Role.id == 9)).all()
        print(file_id)
        img = '/Users/paulfuther/arla0061/flaskblog/static/images/SECURITYPERSON.jpg'
        css = "flaskblog/static/main.css"
        file = Incident.query.get(file_id)
        fdate1 = file.eventdate
        #print(fdate1)
        fdate= datetime.strftime(fdate1,'%Y-%m-%d')
        #print(fdate)
        fstore = file.location
        id = file_id
        #print(fdate)
        gsa = Incident.query.get(file_id)
        ident = gsa.id
        print(ident)
        picture = incident_files.query.filter_by(incident_id=file_id)
        rendered = render_template('eventreportpdf.html',gsa=gsa, css=css, picture=picture)
        options = {'enable-local-file-access': None,
            '--keep-relative-links': '',
            '--cache-dir':'/Users/paulfuther/arla0061/flaskblog',
            'encoding' : "UTF-8"
        }
        css = "flaskblog/static/main.css"
        
        pdf = pdfkit.from_string(rendered, False, options=options, css=css)

        file = BytesIO(pdf)
            #print(type(file))
        created_on = datetime.now().strftime('%Y-%m-%d')
        filename = f" {fstore} {fdate}  ID  {id} {created_on}.pdf"

        # need to create a bytes file to use as an attachment for sendgrid

        encoded_file = base64.b64encode(pdf).decode()
        attachedFile = Attachment(
                FileContent(encoded_file),
                FileName(filename),
                FileType('application/pdf'),
                Disposition('attachment')) 

        for x in rol:
                
            email = x.email
            message = Mail(
            from_email = DEFAULT_SENDER,
            to_emails=email,
            subject ='A new incident report has been filed',
            html_content='<strong>An incident report has been filed. {}<strong>'.format(filename))
            message.attachment = attachedFile
            response = sg.send(message)
            print(response.status_code, response.body, response.headers)

            # upload to drop box

        with file as f:    
            dbx.files_upload(f.read(), path=f"/SITEINCDIENTS/{filename}", mode=WriteMode('overwrite'))
    