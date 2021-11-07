from flask import *
from flask_mail import *
from random import *
import numpy
import sqlite3
import pandas as pd
import re

conn = sqlite3.connect('Customer.db')
df = pd.read_sql_query("SELECT * FROM customers", conn)
reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
pattern = re.compile(reg)
app = Flask(__name__)
mail = Mail(app)
conn = sqlite3.connect('sample.db',check_same_thread=False)
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'teckspeaks@gmail.com'
app.config['MAIL_PASSWORD'] = 'teck@3055'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)



otp = randint(000000, 999999)
details = {}

def CheckCredentials(email,pwd):
  val = df[df['Mail_Id']==email]
  return True if val.shape[0]>0 and (val['Password'].values)[0] == pwd else False
  


@app.route('/')
def index():
    return render_template("login.html")

@app.route('/logincheck',methods=["POST","GET"])
def login():
    email = request.form["email"]
    pwd   = request.form["password"]
    if df[df['Mail_Id']==email.strip().lower()].shape[0] == 0:
       return render_template('login.html',error = "   User doesn't exist :)")
    if CheckCredentials(email.strip().lower(),pwd.strip()):
      return render_template('index.html')
    return render_template('login.html',error = '   Invalid credentials :)')

@app.route('/signup',methods=["POST","GET"])
def signup():
  return render_template('signup.html')

@app.route('/signupcheck',methods=["POST"])
def signupcheck():
  global details ,df
  details['fname'] = request.form['Fname'].strip()
  details['lname'] = request.form['Lname'].strip()
  details['email'] = request.form['email'].strip().lower()
  details['ph']    = int(request.form['ph'].strip())
  details['pwd']   = request.form['pwd'].strip()
  if df[df['Mail_Id']==details['email'].strip().lower()].shape[0]!=0:
    return render_template('signup.html',error='Email already taken :)')
  elif re.search(pattern, details['pwd']):
    msg = Message('OTP', sender='techspeaks@gmail.com', recipients=[details['email']])
    msg.body = str(otp)
    mail.send(msg)
    return render_template('verify.html')
    
  else:
    return render_template('signup.html',error='Passsword must contain [A-Z][a-z][@$!#%*?&][0-9]')

@app.route('/validate',methods=["POST","GET"])
def validate():
    global df
    user_otp = request.form['otp']
    if str(otp) == str(user_otp):
        conn = sqlite3.connect('Customer.db')
        query="insert into customers (First_Name,Last_Name,Mail_Id,Phone_Number,Password) values (?,?,?,?,?)"
        conn.execute(query,list(details.values()))
        conn.commit()
        df = pd.read_sql_query("SELECT * FROM customers", conn)
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        return render_template('login.html')
    return render_template('verify.html',error = "Invalid OTP :)")
if __name__ == '__main__':
    app.run(host = '0.0.0.0' , port = 8080)
 