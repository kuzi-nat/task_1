import unittest
from unittest.mock import patch, MagicMock, mock_open
import main
import json
import xml.etree.ElementTree as ET


class TestMainFunctions(unittest.TestCase):

    @patch('main.mysql.connector.connect')
    def test_connection(self, mock_connect):
        # Настройка mock
        mock_db = MagicMock()
        mock_connect.return_value = mock_db

        # Тест успешного подключения
        result = main.connection('host', 'user', 'password')
        self.assertEqual(result, mock_db)
        self.assertTrue(mock_connect.called)

        # Тест ошибки подключения
        mock_connect.side_effect = Exception('Connection error')
        result = main.connection('host', 'user', 'password')
        self.assertIsInstance(result, Exception)
        self.assertTrue(mock_connect.called)

    def test_create_database(self):
        mock_db = MagicMock()
        mock_cursor = mock_db.cursor.return_value.__enter__.return_value

        # Тест успешного создания базы данных
        result = main.create_database(mock_db, 'test_db')
        mock_cursor.execute.assert_called_with(main.create_db_query.format('test_db'))
        self.assertEqual(result, 0)

        # Тест ошибки при создании базы данных
        mock_cursor.execute.side_effect = Exception('Create DB error')
        result = main.create_database(mock_db, 'test_db')
        self.assertIsInstance(result, Exception)

    def test_create_tables(self):
        mock_db = MagicMock()
        mock_cursor = mock_db.cursor.return_value.__enter__.return_value

        # Тест успешного создания таблиц
        result = main.create_tables(mock_db, 'test_db')
        self.assertEqual(result, 0)
        self.assertTrue(mock_cursor.execute.called)

        # Тест ошибки при создании таблиц
        mock_cursor.execute.side_effect = Exception('Create Tables error')
        result = main.create_tables(mock_db, 'test_db')
        self.assertEqual(result, 0)  # так как ошибка заглушается

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='[{"id": 1, "name": "Room1"}]')
    @patch('json.load')
    def test_insert_tables(self, mock_json_load, mock_open):
        mock_db = MagicMock()
        mock_cursor = mock_db.cursor.return_value.__enter__.return_value

        mock_json_load.side_effect = [
            [{"id": 1, "name": "Room1"}],
            [{"birthday": "2000-01-01", "id": 1, "name": "Student1", "room": 1, "sex": "M"}]
        ]

        result = main.insert_tables(mock_db, 'test_db', 'rooms.json', 'students.json')
        self.assertEqual(result, 0)
        self.assertTrue(mock_cursor.execute.called)

        # Тест ошибки при вставке данных
        mock_cursor.execute.side_effect = Exception('Insert error')
        result = main.insert_tables(mock_db, 'test_db', 'rooms.json', 'students.json')
        self.assertEqual(result, 0)  # так как ошибка заглушается

    def test_execution_queries(self):
        mock_db = MagicMock()
        mock_cursor = mock_db.cursor.return_value.__enter__.return_value

        main.select_queries = ['SELECT * FROM rooms', 'SELECT * FROM students']
        mock_cursor.fetchall.side_effect = [
            [{'id': 1, 'name': 'Room1'}],
            [{'birthday': '2000-01-01', 'id': 1, 'name': 'Student1', 'room': 1, 'sex': 'M'}]
        ]

        result = main.execution_queries(mock_db, 'test_db')
        expected_output = [
            {'task_1': [{'id': 1, 'name': 'Room1'}]},
            {'task_2': [{'birthday': '2000-01-01', 'id': 1, 'name': 'Student1', 'room': 1, 'sex': 'M'}]}
        ]
        self.assertEqual(result, expected_output)

        mock_cursor.execute.side_effect = Exception('Query error')
        result = main.execution_queries(mock_db, 'test_db')
        self.assertIsInstance(result, Exception)




if __name__ == '__main__':
    unittest.main()