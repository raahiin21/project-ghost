#built-in SQLLite DB which will be used to store things as a single file only
#tool will create a new session after running the watch command each session will stores:
#start time + directory being watched + all error caught during that session

import sqlite3 #actual library for db
import os # for the os related commands and functions
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "logs", "ghost.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    #session table to track session and when it started along with which direcory
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   started_at TEXT,
                   directory TEXT
                   )     
   """)
    
    #error table to track all the errors within that particular session(s) with their type, timestamp, msg and the file to which the error belong
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS errors(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            timestamp TEXT,
            error_type TEXT,
            message TEXT,
            file_name TEXT,
            FOREIGN KEY (session_id) REFERENCES sessions(id)   
            )
""")
    conn.commit()
    conn.close()

def create_session(directory):
    conn = get_connection()
    cursor = conn.cursor()
    current_time = datetime.now().isoformat()

    cursor.execute("INSERT INTO sessions (started_at, directory) VALUES (?, ?)",(current_time, directory))
    session_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return session_id