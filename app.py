from flask import Flask, render_template, request, redirect,url_for,session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key="123"

# MySQL connection
#config database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crime management'

mysql = MySQL(app)

#home
@app.route('/home')
def home():
    return render_template('home.html')


#citizen signup
@app.route('/signup', methods=['GET','POST'])
def signup(): 
    if request.method == 'POST':

        #get data from form
        userDetails=request.form
        username=userDetails['username']
        password=userDetails['password']
        mobile_no=userDetails['mobile_no']
        aadhar_no=userDetails['aadhar_no']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO citizen(username,password,mobile_no,aadhar_no) VALUES(%s, %s, %s, %s) ",(username,password,mobile_no,aadhar_no))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))
 
    return render_template('signup.html')

# citizen login
@app.route('/login',methods=['GET','POST'])
def login():
    msg='lol'
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['user']= request.form['username']
        cur = mysql.connection.cursor()
        cur.execute(" SELECT * FROM citizen WHERE username = %s AND password = %s ",(username,password))
        record=cur.fetchone()
        if record:
             return redirect(url_for('citizen'))
        else:
             msg='Incorrect Username/Password'
        
    return render_template('login.html',msg=msg)


 # citizens profile
@app.route('/citizen')
def citizen():
    #user=session['user']
    cur = mysql.connection.cursor()
    resultValue=cur.execute("SELECT username,mobile_no,aadhar_no FROM citizen WHERE username = 'rhys'" )   #(user))
    if resultValue>0:
             userDetails= cur.fetchall()
             cur.close()
        #     SELECT t1.username ,t2.complainant_id
        # from citizen t1
        # join complaint t2 on t1.complainant_id=t2.complainant_id;
    cur = mysql.connection.cursor()    
    cur.execute("SELECT complainant_id FROM citizen WHERE username = 'rhys' ")  #,(user))
    result1=cur.fetchall()
    cid=result1[0]
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT complain_id,type_of_crime,date_of_crime,description FROM complaint WHERE `complainant_id` = '%s' ",(cid))
    complain =cur.fetchall()
    cur.close()
    return render_template('citizen.html',userDetails=userDetails,complain=complain)
    

#logout button
@app.route('/dropsession')
def dropsession():
     session.pop('user',None)
     return render_template('login.html')



# # # Citizen complain
@app.route('/complain', methods=['GET', 'POST'])
def complain():
    if request.method == 'POST':
        crime_type = request.form['crime_type']
        crime_date = request.form['crime_date']
        crime_location = request.form['crime_location']
        crime_description = request.form['crime_description']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO complaint(type_of_crime, date_of_crime, location,description) VALUES (%s, %s, %s,%s)", (crime_type, crime_date, crime_location,crime_description))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('citizen'))

    return render_template('complain.html')
     
# # # admin login
@app.route('/adminlogin',methods=['GET','POST'])
def adminlogin():
    if request.method == 'POST':
        if request.form['password']=='12345' and request.form['username']=='admin' :
            session['admin']= request.form['username']
            return redirect(url_for('police_st'))
        
    return render_template('adminlogin.html')
        

#  # # display all the police stations
@app.route('/police_st')
def police_st():
     
        cur = mysql.connection.cursor()
        stnames=cur.execute("SELECT location FROM police_station ")
        if stnames>0:
             userDetails=cur.fetchall()
             return render_template('police_st.html',userDetails=userDetails)


# # #display police department cases
@app.route('/police_dept')
def police_dept():
     
        cur = mysql.connection.cursor()
        profileValue=cur.execute("SELECT complainant_id,complain_id,type_of_crime,date_of_crime,location,description FROM complaint ")
        if profileValue>0:
             userDetails=cur.fetchall()
             return render_template('police_dept.html',userDetails=userDetails)

# # Display all police officers
@app.route('/officers')
def officers():
        cur = mysql.connection.cursor()
        profileValue=cur.execute("SELECT user_id,Fname,Lname,works_on FROM police")
        if profileValue>0:
             userDetails=cur.fetchall()
             print(userDetails)
             return render_template('officers.html',userDetails=userDetails)


# # Add new police officers
@app.route('/addPolice', methods=['GET','POST'])
def pofficer(): 
    if request.method == 'POST':

        #get data from form
        userDetails=request.form
        fname=userDetails['fname']
        lname=userDetails['lname']
        workson=userDetails['works_on']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO police(fname,lname,works_on) VALUES(%s, %s, %s) ",(fname,lname,workson))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('officers'))
        
    return render_template('addPolice.html')
        

# # Display all police officers for specific pstation
# @app.route('/citizen')
# def officers():
     
#         cur = mysql.connection.cursor()
#         profileValue=cur.execute("SELECT username,mobile_no,aadhar_no FROM citizen WHERE aadhar_no=12345")
#         if profileValue>0:
#              userDetails=cur.fetchall()
#              print(userDetails)
#              return render_template('profile.html',userDetails=userDetails)
        



if __name__ == '__main__':
    app.run(debug=True)