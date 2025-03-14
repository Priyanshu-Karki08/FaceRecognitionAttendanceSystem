import cv2
import numpy as np
import face_recognition
import sqlite3
import pandas as pd
import streamlit as st
from datetime import datetime


st.title("Face Recognition Attendance System")

db = 'Class.db'

conn = sqlite3.connect(db)
cursor = conn.cursor()

def extractInfo():
    images = []
    idList = []
    names = []

    cursor.execute("SELECT  id, photo,name FROM students")
    rows = cursor.fetchall()

    for row in rows:
        studentId, photo,studentName = row

        nparr = np.frombuffer(photo, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        images.append(img)
        idList.append(studentId)
        names.append(studentName)

    return images, idList,names

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(roll_no,name):
    cursor.execute("SELECT * FROM attendance WHERE roll_no = ? ", (roll_no,))

    record = cursor.fetchone()
    
    if record :
        return

    time = datetime.now()
    dtString = time.strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
    INSERT INTO attendance (name, roll_no, timestamp) VALUES (?, ?, ?)
    ''', (name, roll_no, dtString))

    conn.commit()

images, idList,names = extractInfo()

encodeList = findEncodings(images)
st.write("MARK YOUR ATTENDANCE!")

stframe = st.empty()

run = st.button("Start Webcam")
stop = st.button("Stop Webcam")

if run:
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeList, encodeFace)
            facedis = face_recognition.face_distance(encodeList, encodeFace)
            matchIndex = np.argmin(facedis)

            if matches[matchIndex] and facedis[matchIndex] < 0.6:
                id = idList[matchIndex]
                name = names[matchIndex]
                cursor.execute('SELECT roll_no FROM students WHERE id = ?', (id,))
                result = cursor.fetchone()
                result_id = result[0]
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                markAttendance(result_id,name)
            else:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        stframe.image(imgRGB, channels="RGB", use_container_width=True)

        if stop:
            cap.release()
            stframe.empty()
            break

if st.button("View Attendance Records"):
    cursor.execute('SELECT * FROM attendance')
    records = cursor.fetchall()

    df = pd.DataFrame(records, columns=["Student Name", "Roll No", "Timestamp"])
    st.dataframe(df)

conn.close()
