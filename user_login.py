# Resource: https://www.youtube.com/watch?v=RHu3mQodroM
# Another resource w/ good explanations https://www.youtube.com/watch?v=gQ6lh3ir2Jw
# Imports to work with urls, html files and sql databases
from flask import Flask, render_template, redirect, session, url_for, request
from flask_mysqldb import MySQL
import MySQLdb

# Create app object and assign secret key
app = Flask(__name__)
app.secret_key = "1234"

# use app.config to inform the app which mysql database to connect to
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'test'
app.config['MYSQL_DB'] = 'login'

# Initialize database as a variable
db = MySQL(app)


# Create a route and function for the first page
@app.route('/', methods=['GET', 'POST'])    # The info in these brackets provides the page address and SQL methods used
def user_login():
    if request.method == 'POST':    # If user clicks on the button...
        return redirect(url_for("index"))   # ... they will be redirected to the "index" method aka log in page
    return render_template("welcome.html")  # HTML display where button is located


# Repeat the above process for the login page
@app.route('/login', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:   # Program checks if text has been entered...
            username = request.form['username']                         # ... in username box...
            password = request.form['password']                         # ... and password box
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)   # Connects with the database & checks validity
            cursor.execute("SELECT * FROM logininfo WHERE email=%s AND password=%s", (username, password))
            info = cursor.fetchone()
            if info is not None:
                if info['email'] == username and info['password'] == password:
                    session['loginsuccess'] = True  # If the log in details match the db, a session is created...
                    return redirect(url_for("profile"))  # ... and user is sent to profile page
            else:
                return redirect(url_for("index"))   # If not they remain on log in page

    return render_template("login.html")    # Display log in page with html


# Route and function for user registration
@app.route('/new', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        if "one" in request.form and "two" in request.form and "three" in request.form:  # Makes sure fields are fill in
            username = request.form['one']  # Assigns field text to appropriate user object variables
            email = request.form['two']
            password = request.form['three']
            cur = db. connection.cursor(MySQLdb.cursors.DictCursor) # Connects and inserts what user wrote in fields
            cur.execute("INSERT INTO login.logininfo(name, password, email) VALUES (%s, %s, %s)",
                        (username, password, email))
            db.connection.commit()
            return redirect(url_for("index"))   # Once added, user is sent back to log in page

    return render_template("register.html")   # Registration page written in HTML


# Route for successful log in
# Will add links to quizzes
@app.route('/new/profile')
def profile():
    if session['loginsuccess']:
        return render_template("profile.html")


# This just ensures that one cannot simply type in the url to get into a persons profile after they have logged out
@app.route('/new/logout')
def logout():
    session.pop('loginsuccess', None)   # .pop() method ends session created by successful log in
    return redirect(url_for("index"))   # Goes back to log in page


if __name__ == '__main__':
    app.run(debug=True)
