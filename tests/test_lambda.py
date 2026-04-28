import json
import unittest
from unittest.mock import patch, MagicMock
from lambda_function import lambda_handler, generate_short_code

class TestURLShortener(unittest.TestCase):

    def test_generate_short_code_length(self):
        code = generate_short_code()
        self.assertEqual(len(code), 6)

    def test_generate_short_code_unique(self):
        code1 = generate_short_code()
        code2 = generate_short_code()
        self.assertNotEqual(code1, code2)

    @patch('lambda_function.get_table')
    def test_create_short_url(self, mock_get_table):
        mock_table = MagicMock()
        mock_get_table.return_value = mock_table
        
        event = {
            'httpMethod': 'POST',
            'body': json.dumps({'url': 'https://google.com'})
        }
        
        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 201)

    @patch('lambda_function.get_table')
    def test_invalid_url(self, mock_get_table):
        mock_table = MagicMock()
        mock_get_table.return_value = mock_table
        
        event = {
            'httpMethod': 'POST',
            'body': json.dumps({'url': 'not-a-url'})
        }
        
        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 400)

    @patch('lambda_function.get_table')
    def test_url_not_found(self, mock_get_table):
        mock_table = MagicMock()
        mock_table.get_item = MagicMock(return_value={})
        mock_get_table.return_value = mock_table
        
        event = {
            'httpMethod': 'GET',
            'pathParameters': {'code': 'XXXXXX'}
        }
        
        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 404)

if __name__ == '__main__':
    unittest.main()