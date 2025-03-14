import sqlite3

conn = sqlite3.connect('Class.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY , 
    name TEXT NOT NULL, 
    roll_no INTEGER NOT NULL UNIQUE,
    photo BLOB NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS attendance (
    name TEXT NOT NULL, 
    roll_no INTEGER NOT NULL, 
    timestamp TEXT NOT NULL
);
''')

conn.commit()

conn.close()

print("Tables 'students' and 'attendance' created successfully.")
