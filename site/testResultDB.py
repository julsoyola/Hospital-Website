import sqlite3

# Test Result DB - Primary Key will be the same as the UserName in the PatientDB

# create a new db
conn = sqlite3.connect('TestResultsDB.db')

# create Cursor to execute queries
cur = conn.cursor()

# drop table from database
try:
    conn.execute('''Drop table Results''')
    # save changes
    conn.commit()
    print('Results table dropped.')
except:
    print('Results table did not exist')

# create table in database
cur.execute('''CREATE TABLE Results(
Name TEXT NOT NULL,
TestResultId INTEGER NOT NULL,
UserId INTEGER NOT NULL,
TestName TEXT NOT NULL, 
TestResult TEXT NOT NULL);
''')

# save changes
conn.commit()
print('Results Table created.')

results = [('Juliana Oyola', 111, 3052001, 'Flu', 'Negative'),
           ('Juliana Oyola', 112, 3052001, 'ADHD', 'Negative'),
           ('John Summit', 113, 11223344, 'Chicken Pox', 'Positive'),
           ('John Summit', 114, 11223344, 'Flu', 'Positive'),
           ('Estefan Gonz', 115, 11271996, 'Chicken Pox', 'Positive'),
           ('Estefan Gonz', 116, 11271996, 'Flu', 'Negative'),
           ]

# for each row add the information into the table
for row in results:
    name = row[0]
    test_result_id = row[1]
    user_id = row[2]
    test_name = row[3]
    test_result = row[4]

    cur.execute('''
        SELECT * FROM Results
        WHERE Name=?
    ''', (name,))

    # existing_record = cur.fetchone()
    #
    # if existing_record:
    #     cur.execute('''
    #         UPDATE Results
    #         SET TestResultId=?, UserId=?, TestName=?, TestResult=?
    #         WHERE Name=?
    #     ''', (test_result_id, user_id, test_name, test_result, name))
    # else:
    cur.execute('''
        INSERT INTO Results (Name, TestResultId, UserId, TestName, TestResult)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, test_result_id, user_id, test_name, test_result))

    userId = 30520011

    cur.execute('SELECT Name FROM Results WHERE UserID = ?', (userId,))
    name_result = cur.fetchone()

    print(name_result)
    testResultId = 112
    testname = "COVID"
    result = "Positive"


    cur.execute('''
                                    UPDATE Results
                                   SET TestResultId=?, TestName=?, TestResult=?
                                   WHERE TestResultId=? 
                               ''', (testResultId, testname, result, testResultId))

# commit and save changes to database
conn.commit()

# iterate over the rows
for row in cur.execute('SELECT * FROM Results;'):
    print(row)

# close database connection
conn.close()
print('Connection closed.')
