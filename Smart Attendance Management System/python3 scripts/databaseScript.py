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
import sqlite3

conn = sqlite3.connect('Attendance_db.db')
c = conn.cursor()


def create_data():
    with conn:
        c.execute("""CREATE TABLE if not exists Attendance ("id" INTEGER PRIMARY KEY AUTOINCREMENT,	
        "fullname"TEXT NOT NULL, "datetime"	NUMERIC NOT NULL);""")


def insert_data(name, date_time):
    with conn:
        c.execute(f"INSERT INTO Attendance  (fullname , datetime)values ('{name}','{date_time}');")


def exist_name(name, d1):
    c.execute(f"SELECT fullname FROM Attendance  where datetime between '{d1} 00:00:00' and '{d1} 23:59:59' ")
    row = c.fetchall()
    for ro in row:
        if name == ro[0]:
            return True
    return False
