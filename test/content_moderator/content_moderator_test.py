import unittest
from unittest.mock import MagicMock, patch
import json
from ai_safety.content_moderator.content_moderator import ContentModerator

class MockOpenAIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.chat = MagicMock()

    def set_response(self, response):
        response_content = json.dumps(response)
        self.chat.completions.create.return_value = {'choices': [{'message': {'content': response_content}}]}

class TestContentModerator(unittest.TestCase):
    def setUp(self):
        # Set up test environment; initialize a mock API client with a fake API key.
        self.api_key = 'fake_api_key'
        self.mock_client = MockOpenAIClient(api_key=self.api_key)
        self.moderator = ContentModerator(client=self.mock_client)
        self.sample_text = "This is a sample text for moderation."
        self.constitution = "All outputs must be respectful and non-offensive."
        self.model_output = "This output is somewhat disrespectful."

    def test_screen_output_for_violations(self):
        # Test that the moderator correctly identifies violations and provides appropriate feedback.
        response = {
            "violation": True, 
            "violated_rules": ["Respect", "Courtesy"], 
            "explanation": "Output is disrespectful.", 
            "recommendation": "Revise to be more respectful."
        }
        self.mock_client.set_response(response)
        result = self.moderator.screen_output_for_violations(self.model_output, self.constitution)
        self.assertTrue(result['violation'])
        self.assertIn("Respect", result['violated_rules'])
        self.assertIn("Output is disrespectful.", result['explanation'])

    def test_no_violation_detected(self):
        # Test that the moderator correctly identifies when there are no violations.
        response = {"violation": False}
        self.mock_client.set_response(response)
        result = self.moderator.screen_output_for_violations(self.model_output, self.constitution)
        self.assertFalse(result['violation'])

    def test_error_handling(self):
        # Test the system's error handling when an external network error occurs.
        error_response = {"error": "Network Error"}
        self.mock_client.set_response(error_response)
        result = self.moderator.screen_output_for_violations(self.model_output, self.constitution)
        self.assertIn("error", result)
        self.assertEqual("Network Error", result['error'])

    def test_api_failure(self):
        # Simulate an API failure by raising an Exception from the mock
        self.mock_client.chat.completions.create.side_effect = Exception("API failure")
        result = self.moderator.screen_output_for_violations(self.model_output, self.constitution)
        # Expect the method to handle the error and return None instead of raising an exception
        self.assertIsNone(result)

    def test_malformed_api_response(self):
        # Test the system's response to receiving a malformed API response.
        # Checks that the system does not crash and handles the error ok.
        self.mock_client.chat.completions.create.return_value = {'malformed': 'response'}
        result = self.moderator.screen_output_for_violations(self.model_output, self.constitution)
        self.assertIsNone(result)  

if __name__ == '__main__':
    unittest.main()
