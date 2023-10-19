import hashlib
import hmac
import os
import re
import sqlite3
import random
import socket
import routes as routes

"""
Name: Juliana Oyola-Pabon
Date:10/02/2023
Assignment:Module 8:Send Encrypted Message
Due Date:10/15/2023
Solve a simple programming problem based on various approaches to computer security and information management.
Build a small scale real-world application that incorporates the principles of secure computing including cryptography, 
network security, and data protection.
All work below was performed by Juliana Oyola-Pabon """

from flask import Flask, render_template, request, session, flash, jsonify
import sqlite3 as sql

app = Flask(__name__, template_folder='../templates')

# Register the routes defined in the routes module
app.register_blueprint(routes.bp)
SECRET_KEY = b'12347777'


# allows user once logged in to reach the homepage
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html', name=session['Name'])


# for the encrypted result page
@app.route('/encryptresult')
def add_encrypted_testResults():
    if not session.get('logged_in'):
        return render_template('login.html')
    elif session.get('admin'):
        return render_template('/encryptresult.html')


def authenticate_message(message, received_signature):
    expected_signature = hmac.new(SECRET_KEY, message.encode(), hashlib.sha3_512).hexdigest()
    return hmac.compare_digest(expected_signature, received_signature)


def verify(msg, sig):
    secret = b'1234'
    computed_sha = hmac.new(secret,
                            msg,
                            digestmod=hashlib.sha3_512).digest()
    if sig != computed_sha:
        return False
    else:
        return True


# this opens the socket and sends out the string to check if its been encrypted correctly
def sendResults_checkEncryption(testResultID, result):
    host = 'localhost'
    port = 8888

    # Create a socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        print(f"Server listening on {host}:{port}")
        body = (testResultID + "-" + result).encode('utf-8')
        secret = b'1234'
        computedTag = hmac.new(secret, body, digestmod=hashlib.sha3_512).digest()
        print("Computed tag =", computedTag)

        print("Length of computed tag = ", len(computedTag))

        sentMessage = body + computedTag
        print(sentMessage)

        # Send the message to the server
        s.sendall(sentMessage)

        return sentMessage


# send results using encryption
@app.route('/sendResults_Encrypted', methods=['POST', 'GET'])
def sendResults_Encrypted():
    if not session.get('logged_in'):
        return render_template('login.html')
    elif request.method == 'POST':
        con = None
        try:
            # get the userID , test name and the result they are trying to update
            testResultId = request.form['TestResultId']
            result = request.form['TestResult']

            error_msgs = []  # Create a list to store unique error messages
            # check for id
            if not testResultId.isdigit():
                error_msgs.append("Should be a digit")

            # check for result
            if result not in ["Positive", "Negative"]:
                error_msgs.append("Result status should be either 'positive' or 'negative'.")

            if error_msgs:
                # If there are any error messages, join them into one message
                msg = "\n".join(error_msgs)
            else:

                # opens the port 8888
                encrypt_msg = sendResults_checkEncryption(testResultId, result)

                # check if the encrypted message is valid
                message = encrypt_msg[:len(encrypt_msg) - 64]
                tag = encrypt_msg[-64:]

                print("tag recieved = ", tag)

                if verify(message, tag):
                    print("message received = ", message)
                else:
                    print("Unauthenticated Test Result Update received!"
                          " Be on alert! Watch out for bad guys !!")

                # if valid connect to local host
                with sql.connect("TestResultsDB.db") as con:
                    # create Cursor to execute queries
                    cur = con.cursor()

                    print((testResultId, result))

                    # match the ID to the patient
                    cur.execute('SELECT Name FROM Results WHERE testResultId = ?', (testResultId,))
                    name_result = cur.fetchone()
                    # need to only get the first of the tuple
                    name = name_result[0]

                    print(name)

                    # insert into table checks if the id and name are in the table
                    cur.execute('''
                                     UPDATE Results
                                    SET TestResultId=?, TestResult=?
                                    WHERE TestResultId=? 
                                ''', (testResultId, result, testResultId))

                    con.commit()

                    msg = "Test Result Update successfully sent: Updated For " + name
                    # commit and save changes to DB

        except Exception as e:
            print(str(e))
            if con:
                con.rollback()
                con.close()
            msg = "Unauthenticated Test Result Update received! Be on alert! Watch out for bad guys !!!"

        finally:
            if con:
                con.close()
            return render_template("result.html", msg=msg)

    else:
        return render_template('login.html')


# gets the current users info
# Define a function to get user data based on the current session's username
def get_user_data(username):
    conn = sqlite3.connect('PatientDB.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Patient WHERE Name = ?', (username,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data


# Route to display current user's information
@app.route('/userinfo')
def show_userinfo():
    if session.get('logged_in'):
        username = session['Name']
        user_data = get_user_data(username)
        if user_data:
            return render_template('userInfo.html', user=user_data)
        else:
            return "User not found"
    else:
        return "User not logged in"


# Lists the Patients in the DB
@app.route('/list')
def list():
    if not session.get('logged_in'):
        return render_template('login.html')
    elif session.get('admin'):
        con = sql.connect("PatientDB.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute("select * from Patient")

        rows = cur.fetchall()
        return render_template("list.html", rows=rows)


# checks whether this is a valid login
@app.route('/login', methods=['POST'])
def do_admin_login():
    try:
        nm = request.form['username']
        pwd = request.form['password']
        get_user_data(nm)

        with sql.connect("PatientDB.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()

            sql_select_query = """select * from Patient where Name = ? and Password = ?"""
            cur.execute(sql_select_query, (nm, pwd))

            row = cur.fetchone();
            if row is not None:
                session['logged_in'] = True
                session['Name'] = nm
                if int(row['SecurityLevel']) == 1:
                    session['admin'] = True
                else:
                    session['admin'] = False

            else:
                session['logged_in'] = False
                flash('invalid username and/or password!')
    except:
        con.rollback()
        flash("error in insert operation")
    finally:
        con.close()
    return home()


# show test results
@app.route('/showresults')
def show_testResults():
    username = session['Name']

    print(username)
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        con = sql.connect("TestResultsDB.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        # Execute the query to select all rows for the specific name
        cur.execute('SELECT TestResult, TestName FROM Results WHERE Name = ?', (username,))

        rows = cur.fetchall()
        return render_template("showtestresults.html", rows=rows)


# sending test results
@app.route('/testresults')
def add_testResults():
    if not session.get('logged_in'):
        return render_template('login.html')
    elif session.get('admin'):
        return render_template('testresults.html')


# generate 3 rando numbers for the testresult ID
def generate_random_numbers():
    return random.randint(100, 900)


# this ensures that the information is correct (test results)
@app.route('/addresult', methods=['POST', 'GET'])
def addresult():
    # generate random id
    randomId = generate_random_numbers()
    if not session.get('logged_in'):
        return render_template('login.html')
    elif request.method == 'POST':
        try:
            userId = request.form['UserID']
            testname = request.form['TestName']
            result = request.form['TestResult']

            error_msgs = []  # Create a list to store unique error messages

            # check for id
            if not userId.isdigit():
                error_msgs.append("Should be a digit")

            # check for test name
            if not testname:
                error_msgs.append("Test Name needs to be filled out")

            # check for result
            if result not in ["Positive", "Negative"]:
                error_msgs.append("Result status should be either 'positive' or 'negative'.")

            if error_msgs:
                # If there are any error messages, join them into one message
                msg = "\n".join(error_msgs)
            else:
                with sql.connect("TestResultsDB.db") as con:
                    # create Cursor to execute queries
                    cur = con.cursor()

                    # match the ID to the patient
                    cur.execute('SELECT Name FROM Results WHERE UserID = ?', (userId,))
                    name_result = cur.fetchone()
                    # need to only get the first of the tuple
                    name = name_result[0]

                    print(name)
                    print((name, randomId, userId, testname, result))

                    cur.execute('''
                        SELECT * FROM Results
                        WHERE Name=?
                    ''', (name,))

                    # insert into table
                    cur.execute('''
                            INSERT INTO Results (Name, TestResultId, UserId, TestName, TestResult)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (name, randomId, userId, testname, result))

                    # commit and save changes to DB
                    con.commit()
                    msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            con.close()
            return render_template("result.html", msg=msg)


    else:
        return render_template('login.html')


# adding a new patient
@app.route('/enternew')
def new_patient():
    if not session.get('logged_in'):
        return render_template('login.html')
    elif session.get('admin') == True:
        return render_template('patient.html')


# ensures that the user actually put information in
@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if not session.get('logged_in'):
        return render_template('login.html')
    elif request.method == 'POST':
        try:
            nm = request.form['Name']
            ag = request.form['Age']
            num = request.form['PhoneNum']
            cov = request.form['UserHasCOVID']
            sec = request.form['SecurityLevel']
            pwd = request.form['Password']

            error_msgs = []  # Create a list to store unique error messages

            # Check Name (nm) is alphabet only
            if not nm.isalpha():
                error_msgs.append("Name should only contain alphabetic characters.")

            # Check Age (ag) is a number between 0 and 120
            if not ag.isdigit() or not 0 <= int(ag) <= 120:
                error_msgs.append("Age should be a number between 0 and 120.")

            # Check PhoneNum
            if not re.match(r'^\d{10}$', num):  # Assuming it should be a 10-digit number
                error_msgs.append("Phone number should be a 10-digit numeric value.")

            # Check COVID status (cov) is either "positive" or "negative"
            if cov not in ["positive", "negative"]:
                error_msgs.append("COVID status should be either 'positive' or 'negative'.")

            # Check if any of the required fields are empty
            if not sec.isdigit() or not 1 <= int(sec) <= 3:
                error_msgs.append("Security level is required as a number.")

            # Check for password
            if not pwd:
                error_msgs.append("Password is required.")

            if error_msgs:
                # If there are any error messages, join them into one message
                msg = "\n".join(error_msgs)
            else:
                with sql.connect("PatientDB.db") as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO Patient (Name,Age,PhoneNum,UserHasCovid,SecurityLevel, "
                                "Password) VALUES (?,?,?,?,?,?)", (nm, ag, num, cov, sec, pwd))
                    con.commit()
                    msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("result.html", msg=msg)
            con.close()

    else:
        return render_template('login.html')


@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['admin'] = False
    session['Name'] = ""
    return home()


if __name__ == '__main__':
    # Secret Key used to ensure that the data being requested or distributed is not tampered with
    # os.random(n) returns a string of random bytes (more secure than just standard randomizing
    app.secret_key = os.urandom(12)
    app.run(debug=True)

