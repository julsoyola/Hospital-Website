import sqlite3

"""
Name: Juliana Oyola-Pabon
Date:10/02/2023
Assignment:Module 7:Send Encrypted Message
Due Date:10/15/2023
Solve a simple programming problem based on various approaches to computer security and information management.
Build a small scale real-world application that incorporates the principles of secure computing including cryptography, 
network security, and data protection.
All work below was performed by Juliana Oyola-Pabon """


# this sets up the DB storing the patient information
# Name, Age, PhoneNum, UserHasCovid, SecurityLevel, Password

# create a new db
conn = sqlite3.connect('PatientDB.db')

# create Cursor to execute queries
cur = conn.cursor()

# drop table from database
try:
    conn.execute('''Drop table Patient''')
    # save changes
    conn.commit()
    print('Patient table dropped.')
except:
    print('Patient table did not exist')

# create table in database
cur.execute('''CREATE TABLE Patient(
Name TEXT PRIMARY KEY NOT NULL,
Age INTEGER NOT NULL,
PhoneNum TEXT NOT NULL,
UserHasCOVID TEXT NOT NULL, 
SecurityLevel INTEGER NOT NULL, 
Password TEXT NOT NULL);
''')

# save changes
conn.commit()
print('Patient Table created.')

patients = [('Juliana Oyola', 22, '352-789-2222', 'Positive', 1,
             '$PASSWORD123'),
            ('Sarah Wilson', 23, '910-709-2222', 'Positive', 1,
             '$Sarah123'),
            ('Bobby Smith', 45, '352-799-2242', 'Negative', 3,
             '$Bbby1'),
            ('John Summit', 25, '345-897-0099', 'Positive', 2,
             'JohnSummit3')
            ]

# add into table
cur.executemany('Insert Into Patient Values (?,?,?,?,?, ?)', patients)

# commit and save changes to database
conn.commit()

# iterate over the rows
for row in cur.execute('SELECT * FROM Patient;'):
    print(row)

# close database connection
conn.close()
print('Connection closed.')