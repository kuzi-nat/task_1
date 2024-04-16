import logging
import mysql.connector
import json
import xml.etree.ElementTree as ET
from dotenv import dotenv_values

from queries import *



def connection(host: str, user: str, password: str):
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password)
        logging.debug('Успешное подключение к БД')
    except Exception as ex:
        logging.critical('Не удалось подключиться к БД')
        return ex
    return mydb


def create_database(mydb, create_db_query = 'CREATE DATABASE hostel'):
    try:
        with mydb.cursor() as cur:
            cur.execute(create_db_query)
    except Exception as ex:
        return ex
    return 0


def create_tables(mydb):
    mydb.database = 'hostel'
    try:
        with mydb.cursor() as cur:
            cur.execute(create_rooms_table_query)
            cur.execute(create_students_table_query)
            cur.execute(create_indexes_query)
            mydb.commit()
    except: pass
    return 0


def insert_tables(mydb, rooms_file_path: str, students_file_path: str):
    mydb.database = 'hostel'
    try:
        rooms_file = open(rooms_file_path, 'r')
        data_rooms_file = json.load(rooms_file)
        with mydb.cursor() as cur:
            for i in data_rooms_file:
                insert_rooms_query = 'INSERT INTO rooms VALUES (%s, %s)'
                values = (i['id'], i['name'],)
                cur.execute(insert_rooms_query, values)
            mydb.commit()

        students_file = open(students_file_path, 'r')
        data_students_file = json.load(students_file)
        with mydb.cursor() as cur:
            for i in data_students_file:
                insert_students_query = 'INSERT INTO students VALUES (%s, %s, %s, %s, %s)'
                values = (i['birthday'], i['id'], i['name'], i['room'], i['sex'],)
                cur.execute(insert_students_query, values)
            mydb.commit()
    except: pass
    return 0


def queries(mydb):
    mydb.database = 'hostel'
    output = []
    try:
        for i in range(len(select_queries)):
            with mydb.cursor(dictionary=True) as cur:
                cur.execute(select_queries[i])
                result = cur.fetchall()
                output.append({f'task_{i+1}': result})
    except Exception as ex:
        return ex
    return output


def export(output, file_name: str, filetype):
    if filetype == 'json':
        with open(f'{file_name}.json', 'w') as file:
            json.dump(output, file)
    elif filetype == 'xml':
        def dict_to_xml(data: list):
            root = ET.Element("data")
            for item in data:
                entry = ET.SubElement(root, "entry")
                for key, value in item.items():
                    sub_element = ET.SubElement(entry, key)
                    sub_element.text = str(value)
            return ET.ElementTree(root)
        tree = dict_to_xml(output)
        tree.write(f"{file_name}.xml", encoding="utf-8", xml_declaration=True)





if __name__ == '__main__':
    config = dotenv_values(".env")
    mydb = connection(config['host'], config['user'], config['password'])
    create_database(mydb)
    create_tables(mydb)
    insert_tables(mydb, input('Enter rooms file path: '), input('Enter students file path: '))
    output = queries(mydb)
    while True:
        choose = int(input('[1] Export to json\n[2] Export to XML\nSelect export file type: '))
        if choose in [1,2]:
            chooses={1:'json', 2:'xml'}
            export(output, input('File name: '), chooses[choose])
            break
        else:
            print('Your input is incorrect')






