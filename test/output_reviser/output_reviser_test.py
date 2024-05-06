import unittest
from openai import OpenAI
from ai_safety.output_reviser.output_reviser import OutputReviser
import os

class TestOutputReviserRealAPI(unittest.TestCase):
    def setUp(self):
        # Initialize with a real API key
        self.api_key = os.getenv('AI_SAFETY_OPENAI_API_KEY') 
        self.client = OpenAI(api_key=self.api_key)
        self.reviser = OutputReviser(client=self.client)
        self.original_output = "This is the original output that needs revision."
        self.explanation = "This output is considered disrespectful."
        self.recommendation = "Please revise to be more respectful."

    def test_revise_output_to_comply_with_rules(self):
        # Testing the real API call to revise the output
        result = self.reviser.revise_output_to_comply_with_rules(self.original_output, self.explanation, self.recommendation)
        
        # Assert based on expected response characteristics
        self.assertIsInstance(result, str)  # Check if the output is a string
        self.assertNotEqual(result, self.original_output)  # Ensure the output has been modified


if __name__ == '__main__':
    unittest.main()
