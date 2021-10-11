"""
addVals adds values to the created sql table.
param msgTxt is the message in it's entirety, action is the action that jarvis
should take ie. WEATHER, TIME etc 
"""
import sqlite3

def addVals(msgTxt, action):
    
    try:
        conn = sqlite3.connect("jarvis.db")
    except:
        print("error connecting")
    c = conn.cursor()
    c.execute("INSERT INTO training_data (txt,action) VALUES (?, ?);", (msgTxt, action))
    conn.commit() # save (commit) the changes
    conn.close
