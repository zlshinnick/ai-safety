import unittest
from unittest.mock import MagicMock
import json
from ai_safety.output_reviser.output_reviser import OutputReviser
class MockAnthropicClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.chat = MagicMock()

    def set_response(self, response):
        self.chat.completions.create.return_value = {'choices': [{'message': {'content': response}}]}

class TestOutputReviser(unittest.TestCase):
    def setUp(self):
        self.api_key = 'fake_api_key'
        self.mock_client = MockAnthropicClient(api_key=self.api_key)
        self.reviser = OutputReviser(anthropic_client=self.mock_client)
        self.original_output = "This is the original output that needs revision."
        self.explanation = "This output is not respectful."
        self.recommendation = "Please make the output more respectful."

    def test_revise_output_to_comply_with_rules(self):
        # Test revising output successfully
        response = "This is the revised output that is now respectful."
        self.mock_client.set_response(response)
        result = self.reviser.revise_output_to_comply_with_rules(self.original_output, self.explanation, self.recommendation)
        self.assertEqual(result, response)

    def test_handle_api_failure(self):
        # Test handling an API failure 
        self.mock_client.chat.completions.create.side_effect = Exception("API failure")
        with self.assertRaises(Exception):
            self.reviser.revise_output_to_comply_with_rules(self.original_output, self.explanation, self.recommendation)

    def test_malformed_api_response(self):
        # Test handling a malformed response from the API
        self.mock_client.chat.completions.create.return_value = {'malformed': 'response'}
        result = self.reviser.revise_output_to_comply_with_rules(self.original_output, self.explanation, self.recommendation)
        self.assertIsNone(result)  

if __name__ == '__main__':
    unittest.main()