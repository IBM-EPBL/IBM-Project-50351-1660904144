from flask import *
import ibm_db
import mysql.connector
import re

from sqlalchemy.dialects import mysql

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=19af6446-6171-4641-8aba-9dcff8e1b6ff.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30699;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=wbj34020;PWD=Sy0MFttXjE9CVrqI",'','')


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SECRET_KEY'] = 'AJDJRJS24$($(#$$33--'

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/")
def login():
    return render_template("login.html")

# Login
@app.route("/loginmethod", methods = ['GET'])
def loginmethod():
    global userid
    msg = ''

    if request.method == 'GET':
        uname = request.args.get("uname")
        psw = request.args.get("psw")

        sql = "SELECT * FROM accounts WHERE username =? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, uname)
        ibm_db.bind_param(stmt, 2, psw)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)

        if account:
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userid = account['USERNAME']
            session['username'] = account['USERNAME']
            return redirect(url_for("display"))
        else:
            msg = 'Incorrect Username and Password'
            flash(msg)
            return redirect(url_for("login"))

# Signup
@app.route("/signupmethod", methods = ['POST'])
def signupmethod():
    msg = ''
    if request.method == 'POST':
        uname = request.form['uname']
        email = request.form['email']
        name = request.form['name']
        dob = request.form['dob']
        psw = request.form['psw']
        con_psw = request.form['con_psw']

        sql = "SELECT * FROM accounts WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, uname)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)

        if account:
            msg = 'Account already exists !'
            flash(msg)
            return redirect(url_for("signup"))
        elif psw != con_psw:
            msg = "Password and Confirm Password do not match."
            flash(msg)
            return redirect(url_for("signup"))
        else:
            insert_sql = "INSERT INTO accounts VALUES (?, ?, ?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, name)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, dob)
            ibm_db.bind_param(prep_stmt, 4, uname)
            ibm_db.bind_param(prep_stmt, 5, psw)
            ibm_db.execute(prep_stmt)
            return redirect(url_for("login"))

    elif request.method == 'POST':
        msg = 'Please fill out the form !'
        flash(msg)
        return redirect(url_for("signup"))
    
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/home")
def home():
    return render_template("home.html")


@app.route('/display')
def display():
    print(session["username"], session['id'])

    display_sql = "SELECT * FROM accounts WHERE username = ?"
    prep_stmt = ibm_db.prepare(conn, display_sql)
    ibm_db.bind_param(prep_stmt, 1, session['id'])
    ibm_db.execute(prep_stmt)
    account = ibm_db.fetch_assoc(prep_stmt)
    print(account)
    return render_template("home.html", account = account)
    
if __name__ == "__main__":
    app.run(debug=True)