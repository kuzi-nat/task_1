import logging
import mysql.connector
import json

create_db_query = 'CREATE DATABASE hostel'
create_rooms_table_query = 'CREATE TABLE rooms (id INT PRIMARY KEY, name VARCHAR(15))'
create_students_table_query = 'CREATE TABLE students (birthday DATETIME, id INT PRIMARY KEY, name VARCHAR(50), room INT, sex CHAR(1), FOREIGN KEY(room) REFERENCES rooms(id))'
select_query_1 = 'SELECT rooms.name, COUNT(students.id) AS count_students FROM rooms LEFT JOIN students ON rooms.id = students.room GROUP BY rooms.id ORDER BY rooms.name;'
select_query_2 = 'SELECT rooms.name, ROUND(AVG((DATEDIFF(NOW(), birthday)) / 365), 2) AS average_age FROM rooms LEFT JOIN students ON rooms.id = students.room GROUP BY rooms.id ORDER BY average_age, rooms.id LIMIT 5;'
select_query_3 = 'SELECT rooms.name, ROUND(MAX((DATEDIFF(NOW(), birthday)) / 365) - MIN((DATEDIFF(NOW(), birthday)) / 365), 2) AS difference_age FROM rooms LEFT JOIN students ON rooms.id = students.room GROUP BY rooms.id ORDER BY difference_age DESC, rooms.id LIMIT 5;'
select_query_4 = 'SELECT rooms.name FROM rooms LEFT JOIN students ON rooms.id = students.room WHERE students.sex IN ("M") AND students.sex IN ('F') GROUP BY rooms.id;'

try:
    mydb = mysql.connector.connect(user='root', password='sql2150', host='127.0.0.1', auth_plugin = 'mysql_native_password')
    logging.debug('Успешное подключение к БД')
except Exception as ex:
    print(ex)
    logging.critical('Не удалось подключиться к БД')

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
except: pass

rooms_file = open(input('Enter rooms file path: '), 'r')
data_rooms_file = json.load(rooms_file)
for i in data_rooms_file:
    insert_rooms_query = 'INSERT INTO rooms VALUES (%s, %s)'
    values = (i['id'], i['name'],)
    cur.execute(insert_rooms_query, values)
mydb.commit()

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


#while True:
#    i=input('[1] Export to json\n[2] Export to XML\nSelect export file type: ')
#    if i == '1':
#        a=[{'id':1, 'name':'1'},{'id':2, 'name':'2'}]
#        with open('output.json', 'w') as file:
#            json.dump(a, file)
#        break