create_db_query = 'CREATE DATABASE {0}'

create_rooms_table_query = '''CREATE TABLE rooms (
id INT PRIMARY KEY, 
name VARCHAR(15))'''

create_students_table_query = '''CREATE TABLE students (
birthday DATETIME, 
id INT PRIMARY KEY, 
name VARCHAR(50), 
room INT, 
sex CHAR(1), 
FOREIGN KEY(room) REFERENCES rooms(id))'''

create_indexes_query = '''CREATE INDEX idx_id ON rooms (id);
CREATE INDEX idx_room ON students (room);'''

select_queries = [
    '''\
SELECT rooms.name, COUNT(students.id) AS count_students
FROM rooms
LEFT JOIN students ON rooms.id = students.room
GROUP BY rooms.id 
ORDER BY rooms.name;
    ''',

    '''\
SELECT rooms.name
FROM rooms
LEFT JOIN students ON rooms.id = students.room
GROUP BY rooms.id 
HAVING AVG((DATEDIFF(NOW(), birthday)) / 365) IS NOT NULL
ORDER BY AVG((DATEDIFF(NOW(), birthday)) / 365), rooms.id
LIMIT 5;
    ''',

'''\
SELECT rooms.name 
FROM rooms 
LEFT JOIN students ON rooms.id = students.room 
GROUP BY rooms.id 
ORDER BY ROUND(MAX((DATEDIFF(NOW(), birthday)) / 365) - MIN((DATEDIFF(NOW(), birthday)) / 365), 2) DESC, rooms.id 
LIMIT 5;
''',

'''\
SELECT DISTINCT r.name AS room_name 
FROM students s 
JOIN rooms r ON s.room = r.id 
JOIN students s2 ON s.room = s2.room AND s.sex <> s2.sex;'''
]
