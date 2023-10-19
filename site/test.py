import sqlite3 as sql
nm = "Juliana Oyola"
pwd = "$PASSWORD123"

with sql.connect("PatientDB.db") as con:
    con.row_factory = sql.Row
    cur = con.cursor()

    sql_select_query = """select * from Patient where Name = ? and Password = ?"""
    cur.execute(sql_select_query, (nm, pwd))

    row = cur.fetchone();
    if (row != None):
        UserLevel = row["UserLevel"]
        print(UserLevel)
    con.close()
con.close()