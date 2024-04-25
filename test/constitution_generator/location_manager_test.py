import unittest
from unittest.mock import patch
import geocoder
from ai_safety.constitution_generator.location_manager import LocationManager 

class TestLocationManager(unittest.TestCase):

    def setUp(self):
        self.location_manager = LocationManager()

    @patch('geocoder.ip')
    def test_get_location_with_manual_location(self, mock_geocoder):
        # Test the manual location input
        location = "New York, USA"
        result = self.location_manager.get_location(manual_location=location)
        self.assertEqual(result, "USA")
        mock_geocoder.assert_not_called()

    @patch('geocoder.ip')
    def test_get_location_with_ip(self, mock_geocoder):
        # Mocking the geocoder response for IP location
        mock_geocoder.return_value = MockOk({"country": "Canada"})
        result = self.location_manager.get_location()
        self.assertEqual(result, 'Canada')
        mock_geocoder.assert_called_once_with('me')

    @patch('geocoder.ip')
    def test_get_location_with_ip_no_country(self, mock_geocoder):
        # Test when IP location does not provide a country
        mock_geocoder.return_value = MockOk({})
        result = self.location_manager.get_location()
        self.assertEqual(result, 'Default Country')
        mock_geocoder.assert_called_once_with('me')

    @patch('geocoder.ip')
    def test_get_location_with_exception(self, mock_geocoder):
        # Test handling exceptions
        mock_geocoder.side_effect = Exception("An error occurred")
        result = self.location_manager.get_location()
        self.assertEqual(result, 'Default Country')
        mock_geocoder.assert_called_once_with('me')

class MockOk:
    def __init__(self, json_data):
        self.json_data = json_data

    @property
    def country(self):
        return self.json_data.get('country')

if __name__ == '__main__':
    unittest.main()