
from flask import *
import pymysql

# create a Flask app
app = Flask(__name__)

app.secret_key = '1_@Ma8vU!_qRb_*A'

# create a python logger
import logging
from logging.handlers import RotatingFileHandler
# create a logger
handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)

@app.route('/')
def home():
    # here we check wether we have anyone logged in 
    if 'userrole' in session:
        return render_template('index.html')
    else:
        return redirect('/signin')
    
# signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # get the form data
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        connection = pymysql.connect(host='localhost',user='root',password='',database='cybertestsystem')

        cursor = connection.cursor()

        sql ='insert into users (email,password,role) values (%s,%s,%s)'

        cursor.execute(sql,(email,password,role))

        connection.commit()

        return redirect('/')
    else:
        return render_template('addUser.html')


@app.route('/signin', methods=['POST','GET'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = pymysql.connect(host='localhost',user='root',password='',database='cybertestsystem')

        cursor = connection.cursor()

        sql ='select * from users where email = %s and password = %s'

        cursor.execute(sql,(email,password))

        if cursor.rowcount == 0:
            app.logger.error(f'Failed login for email: {email}')

            return render_template('signin.html',error='wrong credentials')
        else:

            app.logger.info(f'Success login for : {email}')
            
            user = cursor.fetchone()
            # capture the role
            role = user[3]
            # store the role and email in session 
            session['userrole'] = role 

            return redirect('/')
    else:
        return render_template('signin.html')

# signout
@app.route('/signout')
def signout():
    session.clear()
    return redirect('/')

# add message 
@app.route('/add', methods= ['POST','GET'])
def add():
    #  is anyuser logged in?
    if 'userrole' in session:
        # we check if the loggedin user is a user not admin
        role = session['userrole']

        if role == 'User or Admin':
            if request.method == 'POST':
                message_title = request.form['message_title']
                message_body = request.form['message_body']
                # connect to databse
                connection = pymysql.connect(host='localhost',user='root',password='',database='cybertestsystem')
                # cursor
                cursor = connection.cursor()
                sql ='insert into messages (message_title,message_body) values (%s,%s)'
                cursor.execute(sql,(message_title,message_body))
                connection.commit()
                return render_template('add.html', success = 'message added successfully')
            else:
                return render_template('add.html')  
        else:
            return render_template('signin.html', message = 'Access Denied, login as a User')
    else:
        return redirect('/signin')

# view messages as admin
@app.route('/view')
def view():
    #  is anyuser logged in?
    if 'userrole' in session:
        # we check if the loggedin user is a admin not user
        role = session['userrole']
        if role == 'Admin':
            # connect to databse
            connection = pymysql.connect(host='localhost',user='root',password='',database='cybertestsystem')
            # cursor
            cursor = connection.cursor()
            sql = 'select * from messages'
            cursor.execute(sql)
            messages = cursor.fetchall()
            return render_template('view.html', messages = messages)
        else:
            return render_template('signin.html', message = 'Access Denied, login as a Admin')
    else:
        return redirect('/signin')



app.run(debug=True)