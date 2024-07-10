
from flask import *
import pymysql


# create a Flask app
app = Flask(__name__)
# sessions - used in identify a user after login
# This session is very secure
# you secure by setting a unique key that no one else knows
# above key is used to encrypt use session
app.secret_key = '1_@Ma8vU!_qRb_*A'

# Configure logging
import logging
from logging.handlers import RotatingFileHandler
handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG) 




@app.route('/signin',  methods= ['POST','GET'])
def signin():
    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']

        connection = pymysql.connect(host='localhost', user='root', password='',
                                     database='CyberTestSystem')

        cursor = connection.cursor()

        cursor.execute('select * from users where email = %s and password = %s',
                       (email, password))
        # check if above query found a match or not
        if cursor.rowcount == 0:
            app.logger.error(f'Failed login attempt for email: {email}')
            return render_template('signin.html', error = 'Wrong Credentials')

        else:
            app.logger.info(f'Success login for email: {email}')
            user = cursor.fetchone()
            # Retrieve the user Role
            role = user[3] # role is at position 3 in our table
            # Store the Role and Email in session
            session['userrole'] = role
            
            return redirect('/')

    else:
        return render_template('signin.html')
    


@app.route('/')
def home():
    # Here we check if userole is in session.
    # It will only be inside the session if user is logged in
    if 'userrole' in session:

        return render_template("index.html")
    
    else:
        return redirect('/signin')


# At this point , we need to Know who can add or view messages is it admin or user or both
# Lets make it only users can add a message
@app.route("/add", methods = ['POST', 'GET'])
def add():
    # Is anyone logged in?
    if 'userrole' in session:
        # We retrieve the user who is logged in and the role
        role = session['userrole']
        # If its user, we access Add Page
        if role == "User":
            if request.method =='POST':
                message_title = request.form['message_title']
                message_body = request.form['message_body']
                

                # we now save our message_title, message_body to database
                connection = pymysql.connect(host='localhost', user='root', password='',
                                            database='CyberTestSystem')

                cursor = connection.cursor()
                # create an insert query to insert data to shop_users
                cursor.execute('insert into messages(message_title,message_body)values(%s,%s)',
                            (message_title, message_body))
                connection.commit() # write the record to the table
                return render_template('add.html', success='Thank you for Registering.')
            else:
                 return render_template('add.html') 
        else:
            return render_template("signin.html", message  = "Access Denied, Login in as a User.")
    else:
        return redirect('/signin')



@app.route("/view")
def view():
    # Is anyone logged in?
    if 'userrole' in session:
        # We retrieve the user who is logged in and the role
        role = session['userrole']
        # If its admin, we access View Page
        if role == "Admin":
            connection = pymysql.connect(host='localhost', user='root', password='',
                                     database='cybertestsystem')
            # Step 2: Create a cursor to execute SQL
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM messages')

            # Step 3:  Get the rows from cursor
            messages = cursor.fetchall()
            return render_template("view.html", messages= messages)
        else:
            return render_template("signin.html", message  = "Access Denied, Login in as a Admin.")
        
    else:
        return redirect('/signin')


# Logout
@app.route("/signout")
def signout():
    session.clear()
    return redirect('/')




app.run(debug=True)