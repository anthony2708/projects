from flask import Flask, render_template, request
from flaskext.mysql import MySQL
from waitress import serve
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os

application = Flask(__name__)

# Configure DB
load_dotenv()
mysql = MySQL()
application.config['MYSQL_DATABASE_HOST'] = os.getenv('RDS_HOSTNAME')
application.config['MYSQL_DATABASE_USER'] = os.getenv('RDS_USERNAME')
application.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('RDS_PASSWORD')
application.config['MYSQL_DATABASE_DB'] = os.getenv('RDS_DB_NAME')

mysql.init_app(application)

@application.route('/',methods=['GET','POST'])
def index():
        create_query = "CREATE TABLE IF NOT EXISTS users (name VARCHAR(255), email VARCHAR(255), gender VARCHAR(10), country VARCHAR(255), password VARCHAR(255))"
        if request.method == 'POST':
                # FETCH FORM DATA
                userdetails = request.form
                name = userdetails['name']
                email = userdetails['email']
                gender = userdetails['gender']
                country = userdetails['country']
                raw_password = userdetails['password']
                password = generate_password_hash(raw_password)
                # CREATING MYSQL OBJECT
                conn = mysql.connect()
                cur = conn.cursor()

                # Check if the table exists before:
                cur.execute(create_query)
                conn.commit()


                # Execute the insert command
                cur.execute("INSERT INTO users(name, email, gender, country, password) VALUES(%s, %s, %s, %s, %s)", (name, email, gender, country, password))
                conn.commit()
                cur.close()
                return render_template('success.html')
        return render_template('index.html')

@application.route('/users')
def users():
        create_query = "CREATE TABLE IF NOT EXISTS users (name VARCHAR(255), email VARCHAR(255), gender VARCHAR(10), country VARCHAR(255), password VARCHAR(255))"
        
        conn = mysql.connect()
        cur = conn.cursor()

        # Check if the table exists before:
        cur.execute(create_query)
        conn.commit()

        resultValue = cur.execute("SELECT * FROM users")
        if resultValue >= 0:
                userdetails = cur.fetchall()
                return render_template('users.html',userdetails=userdetails)

if __name__ == '__main__':
        serve(application, host='0.0.0.0', port=8000)