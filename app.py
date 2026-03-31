from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from datetime import * 

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'MySqL@maaz3211'
app.config['MYSQL_DB'] = 'my_project_01'
mysql = MySQL(app)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM signup_details WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            return render_template('login.html', success="Login Successful! Welcome " + user[1])
        else:
            return render_template('login.html', error="Invalid email or password. Please try again.")
            
    return render_template('login.html')



@app.route('/signup', methods=['POST', 'GET'])
def signup(): 
    if request.method == 'POST':
        name = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        qualification = request.form['qualification']
        specialization = request.form['myeducation']
        cdate = date.today()
        sql = "INSERT INTO signup_details(name, email, password, qualification, specialization, datetime) VALUES(%s, %s, %s, %s, %s, %s)"
        val = (name, email, password, qualification, specialization, cdate)

        cursor = mysql.connection.cursor()
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()
        return render_template('signup.html')
    return render_template('signup.html')
    

@app.route('/data', methods=['POST', 'GET'])
def show_signup_data():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM signup_details")
    row = cursor.fetchall()
    cursor.close()

    return render_template('data.html', data=row)

if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)