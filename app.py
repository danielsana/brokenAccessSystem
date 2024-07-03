
from flask import *
import pymysql

# create a Flask app
app = Flask(__name__)

app.secret_key = '1_@Ma8vU!_qRb_*A'

@app.route('/')
def home():
    # here we check wether we have anyone logged in 
    if 'userrole' in session:
        return render_template('index.html')
    else:
        return redirect('/signin')

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
            return render_template('signin.html',error='wrong credentials')
        else:
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
    return render_template('add.html')

app.run(debug=True)