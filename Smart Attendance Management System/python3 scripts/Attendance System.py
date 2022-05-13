# -*- coding: utf-8 -*-
"""
university of Technology jamaica
Major Project 2022
Kert Dixon
Thorn Lewars
Wembley williams
Collie Clarke
Nicholas Grant
"""
import cv2
import face_recognition
import os
import numpy as nump
from datetime import datetime
import databaseScript

path = "Images"
images = []
classNames = []
myList = os.listdir(path)
# print(myList)
for cl in myList:
    curImage = cv2.imread(f'{path}/{cl}')
    images.append(curImage)
    classNames.append(os.path.splitext(cl)[0])


# print(classNames)
def find_encoding_img(images):
    encodelist = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist


def mark_attendance(name):  # save data name attendance into csv file
    with open('Attendance.csv', 'r+') as f:
        my_data_list = f.readlines()
        name_list = []
        for line in my_data_list:
            entry = line.split(',')
            name_list.append(entry[0])
        if name not in name_list:
            now = datetime.now()
        dtstring = now.strftime("%H:%M:%S")
        f.writelines(f'\n{name},{dtstring}')


databaseScript.create_data()


def check_name_state(name_1):
    now = datetime.now()
    d1 = now.strftime("%d/%m/%Y")
    if not databaseScript.exist_name(name_1, d1):
        dtstring = now.strftime("%d/%m/%Y %H:%M:%S")
        databaseScript.insert_data(name_1, dtstring)


known_face_encodings = find_encoding_img(images)
print("Encoding complete.....")
# ----------------------------------------------------------------------
cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(known_face_encodings, encodeFace)
        faceDis = face_recognition.face_distance(known_face_encodings, encodeFace)
        # print(faceDis)
        match_indexes = nump.argmin(faceDis)
        if matches[match_indexes]:
            name = classNames[match_indexes].upper()
            print(name)

            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            # MarkAttendance(name)
            check_name_state(name)

    cv2.putText(img, 'Exit using Q', (10, 18), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)
    cv2.imshow("Attendance System", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
