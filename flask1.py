from flask import Flask, render_template, request,redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL connection
#config database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crime management'

mysql = MySQL(app)

@app.route('/', methods=['GET','POST'])
def login(): 
    if request.method == 'POST':

        #get data from form
        userDetails=request.form
        username=userDetails['username']
        password=userDetails['password']
        mobile_no=userDetails['mobile_no']
        aadhar_no=userDetails['aadhar_no']

        cur = mysql.connection.cursor()
      #  cur.execute("CREATE DATABASE IF NOT EXISTS crime_management")
        cur.execute("INSERT INTO citizen(username,password,mobile_no,aadhar_no) VALUES(%s, %s, %s, %s) ",(username,password,mobile_no,aadhar_no))
        mysql.connection.commit()
        cur.close()
        return redirect(profile.html)
 
    return render_template('login.html')

@app.route('/citizen')
def profile():
     cur = mysql.connection.cursor()
     profileValue=cur.execute("SELECT username,mobile_no,aadhar_no FROM citizen WHERE aadhar_no=12345")
     if profileValue>0:
         userDetails=cur.fetchall()
         return render_template('profile.html',userDetails=userDetails)



if __name__ == '__main__':
    app.run(debug=True)