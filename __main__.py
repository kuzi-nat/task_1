import logging
import mysql.connector
import json

#while True:
#    i=input('[1] Export to json\n[2] Export to XML\nSelect export file type: ')
#    if i == '1':
#        a=[{'id':1, 'name':'1'},{'id':2, 'name':'2'}]
#        with open('output.json', 'w') as file:
#            json.dump(a, file)
#        break

create_db_query = 'CREATE DATABASE hostel'
create_rooms_table_query = 'CREATE TABLE rooms (id INT PRIMARY KEY, name VARCHAR(15))'
create_students_table_query = 'CREATE TABLE students (birthday DATETIME, id INT PRIMARY KEY, name VARCHAR(50), room INT, sex CHAR(1), FOREIGN KEY(room) REFERENCES rooms(id))'

try:
    mydb = mysql.connector.connect(user='root', password='tptoor-0078', host='127.0.0.1')
    logging.debug('Успешное подключение к БД')
except:
    logging.critical('Не удалось подключиться к дб')

try:
    with mydb.cursor() as cur:
        cur.execute(create_db_query)
except: pass

mydb.database = 'hostel'

try:
    with mydb.cursor() as cur:
        cur.execute(create_rooms_table_query)
        cur.execute(create_students_table_query)
        mydb.commit()
except:pass



#rooms_file = open(input('Enter rooms file path: '), 'r')
#data_rooms_file = json.load(rooms_file)
#for i in data_rooms_file:
#    insert_rooms_query = 'INSERT INTO rooms VALUES (%s, %s)'
#    values = (i['id'], i['name'],)
#    cur.execute(insert_rooms_query, values)
#mydb.commit()

students_file = open(input('Enter students file path: '), 'r')
data_students_file = json.load(students_file)
with mydb.cursor() as cur:
    for i in data_students_file:
        insert_students_query = 'INSERT INTO students VALUES (%s, %s, %s, %s, %s)'
        values = (i['birthday'], i['id'], i['name'], i['room'], i['sex'],)
        cur.execute(insert_students_query, values)
    mydb.commit()

cur.close()
mydb.close()
#