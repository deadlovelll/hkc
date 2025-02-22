import unittest
from unittest.mock import patch, MagicMock
from fastapi.responses import JSONResponse

from controllers.house_controller.house_controller import HouseController
from modules.database.database_pool_controllers import DatabasePoolControllers
from house_factory.house_factory import HouseFactory

class TestHouseController(unittest.TestCase):
    
    """
    Unit tests for the HouseController class.

    This test suite covers:
    - Fetching house information successfully.
    - Handling cases where the house is not found.
    - Creating a new house successfully.
    - Handling database errors during house creation.
    """
    
    def setUp (
        self,
    ) -> None:
        
        self.controller = HouseController()
        self.controller.db = MagicMock(spec=DatabasePoolControllers)
        self.controller.house_factory = MagicMock(spec=HouseFactory)
        self.controller.logger = MagicMock()
    
    @patch('controllers.house_controller.house_controller.DatabasePoolControllers.get_connection')
    def test_get_house_success (
        self, 
        mock_get_connection,
    ) -> None:
        
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        mock_cursor.fetchall.return_value = [(1, 2, '101', 2, 50.0, 3, 'Electric', 100, 4, '2024-01-01', 99, 5, 'John Doe', 30, 500.0)]
        self.controller.house_factory.create_house.return_value = {'id': 1, 'street': 'Main St'}
        
        response = self.controller.get('Main St')
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body, b'{"STATUS":"SUCCESS","HOUSE INFO":{"id":1,"street":"Main St"}}')
    
    @patch('controllers.house_controller.house_controller.DatabasePoolControllers.get_connection')
    def test_get_house_not_found (
        self, 
        mock_get_connection,
    ) -> None:
        
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        mock_cursor.fetchall.return_value = []
        
        response = self.controller.get('Unknown St')
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body, b'{"STATUS":"FAILED","MESSAGE":"House not found"}')
    
    @patch('controllers.house_controller.house_controller.DatabasePoolControllers.get_connection')
    def test_create_house_success (
        self, 
        mock_get_connection,
    ) -> None:
        
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        mock_cursor.fetchone.return_value = [1]
        
        response = self.controller.create('New St')
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body, b'{"STATUS":"SUCCESS","HOUSE_ID":1}')
    
    @patch('controllers.house_controller.house_controller.DatabasePoolControllers.get_connection')
    def test_create_house_database_error (
        self, 
        mock_get_connection
    ) -> None:
        
        mock_get_connection.side_effect = Exception('Database error')
        
        response = self.controller.create('Error St')
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body, b'{"STATUS":"FAILED","MESSAGE":"Internal Server Error"}')

if __name__ == "__main__":
    unittest.main()