from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt


import config



app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = config.db_connection()
app.config['MYSQL_DB'] = 'bank_data'

mysql = MySQL(app)

bcrypt = Bcrypt()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # store the form data
        userDetails = request.form
        first_name = userDetails['first_name']
        last_name = userDetails['last_name']
        email = userDetails['email']
        phone_no = userDetails['phone_no']
        password=userDetails['password']
        password = bcrypt.generate_password_hash(password)


        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM users WHERE email LIKE %s", [email])

        rows = cur.fetchone()
        if rows:
            return 'email already exists'
        else:
            cur.execute("INSERT INTO users(first_name,last_name,email,phone_no,password) VALUES(%s,%s,%s,%s,%s)",(first_name, last_name, email, phone_no, password))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('index.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # store the form data
        userDetails = request.form
        email = userDetails['email']
        password = userDetails['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email LIKE %s", [email])


        rows = cur.fetchone()
        if rows:
            auth=bcrypt.check_password_hash( rows[-1],password)
            if auth:
                return render_template('homepage.html')
        else:
            return "wrong credentials"
    return render_template('login.html')





@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    return render_template('homepage.html')




if __name__ == '__main__':
    # debug=True --> any change we make can get updated on web without re-running the code
    app.run(debug=True)
