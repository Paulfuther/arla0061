@app.route('/updatephone')
def update_phone():

    #this route copied all 

    newuser =  Employee.query.filter(Employee.firstname).all()
    
    for x in newuser:
        print(x.firstname, x.mobilephone, x.user_id)
        user=User.query.get(x.user_id)
        print (user)
        user.phone = x.mobilephone
        db.session.commit()
        print(user.phone)
    
    return "done"


@app.route('/task2', methods = ['GET', 'POST'])
@login_required
@roles_accepted('Admin', 'Manager')
def new_mail():

    #this is for testing purposed. 
    # testing for HR users.

     email = os.environ.get('MAIL_DEFAULT_SENDER')

     rol =  User.query.filter(User.roles.any(Role.id == 3)).all()

     for x in rol:
        print(x.email)

        email = x.email
        print(email)
        email_data = {
             'subject': 'testing 10',
             'to': email,
             'body': 'testing a loop on delay {} '.format(email)
            }
        send_async_email2.apply_async(args=[email_data], countdown=30)
        print("we did it")
     return 'tasksent'    


@app.route('/twofa', methods = ['GET', 'POST'])
@login_required
@roles_required('Admin')
def two_fa():
    twofa('+15196707469')

    return "hello"


@app.route("/sendgridsend", methods = ['GET', 'POST'])
@login_required
@roles_required('Admin')
def emailme():
    
    gsa = User.query.join(roles_users).join(Role)\
        .filter((roles_users.c.user_id == User.id) & (roles_users.c.role_id == Role.id))\
            .filter(Role.id == 5)\
                .filter(User.active == 1)\
                .order_by(User.user_name).all()

    for user in gsa:

        #message = Mail(
        #from_email='paul.futher@outlook.com',
        #to_emails= user.email,
        #subject='Winter Readiness')
       
        #message.template_id = 'd-d97855409101488ea4432a1baccc7f45'
  
        print(user, user.email, user.roles)
        #print(user.firstname, user.email)
        #response = sg.send(message)
   
   
    return render_template("layout.html")


