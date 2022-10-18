from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import config

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = config.db_connection()
app.config['MYSQL_DB'] = 'flaskapp'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # store the form data
        userDetails = request.form
        first_name = userDetails['first_name']
        last_name = userDetails['last_name']
        email = userDetails['email']
        phone_no = userDetails['phone_no']
        password = userDetails['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(first_name,last_name,email,phone_no,password) VALUES(%s,%s,%s,%s,%s)",
                    (first_name, last_name, email, phone_no, password))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')






if __name__ == '__main__':
    # debug=True --> any change we make can get updated on web without re-running the code
    app.run(debug=True)
