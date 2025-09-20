import unittest
from unittest.mock import patch, Mock
from web_service import WebService
import requests


class TestWebService(unittest.TestCase):

    @patch("web_service.requests.get")
    def test_get_data_success(self, mock_get):
        # Мокована відповідь з кодом 200
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        mock_get.return_value = mock_response

        service = WebService()
        result = service.get_data("https://example.com/api")
        self.assertEqual(result, {"data": "test"})
        mock_get.assert_called_once_with("https://example.com/api")

    @patch("web_service.requests.get")
    def test_get_data_404_error(self, mock_get):
        # Мокована відповідь з raise_for_status → помилка
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        service = WebService()
        with self.assertRaises(requests.HTTPError):
            service.get_data("https://example.com/not-found")

    @patch("web_service.requests.get")
    def test_get_data_invalid_json(self, mock_get):
        # Мокована відповідь з помилкою при json()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response

        service = WebService()
        with self.assertRaises(ValueError):
            service.get_data("https://example.com/bad-json")


if __name__ == "__main__":
    unittest.main()
