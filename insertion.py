import sqlite3
from datetime import datetime

conn = sqlite3.connect('Class.db')

cursor = conn.cursor()

def insertStudent(id,name, roll_no, photo_path=None):
    photo_data = None
    if photo_path:
        with open(photo_path, 'rb') as f:
            photo_data = f.read() 

    cursor.execute('''
    INSERT INTO students (id,name, roll_no, photo)
    VALUES (?,?, ?, ?)
    ''', (id,name, roll_no, sqlite3.Binary(photo_data) if photo_data else None))
    
    conn.commit()
    print(f"Student {name} with Roll No: {roll_no} inserted.")

insertStudent(101,'Priyanshu',4,'students/priyanshu.jpg')
insertStudent(102,'Bill',1,'students/bill.jpg')
insertStudent(103,'Elon',2,'students/elon.jpg')
insertStudent(104,'Jack',3,'students/jack.jpg')
