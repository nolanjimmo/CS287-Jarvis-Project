import sqlite3

from sqlite3 import Error

"""
connectToDataBase connects the file to the sqlite data base server.
param name of data base file.
"""
def connectToDataBase(dbFile):
    
    conn = None
    
    try: 
        
        conn = sqlite3.connect(dbFile)
        return conn
    
    except Error as e:
        print(e)
    
    return conn 

"""
createTable uses sqlite3 cursor object to create a table with povided sql
code.
param sql connection, and string of sql code to create table.
"""
def createTable(conn, sql):
    
    try:
        c = conn.cursor()
        c.execute(sql)
    
    except Error as e:
        print(e)


def main():
    # Name of database.
    dataBase = "jarvis.db"
    
    # Sql code to create a table. 
    createTableSql = """ CREATE TABLE IF NOT EXISTS training_data (
                                        id integer PRIMARY KEY,
                                        txt text NOT NULL,
                                        action text
                                    ); """
    conn = connectToDataBase(dataBase)
    
    if conn is not None:
        
        createTable(conn, createTableSql)
        
    else: 
        print("Error")
    
main()
