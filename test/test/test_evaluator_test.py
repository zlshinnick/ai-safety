import unittest
import json
from openai import OpenAI
from ai_safety.test.test_evaluator import TestEvaluator
import os

class TestTestEvaluatorRealAPI(unittest.TestCase):
    def setUp(self):
        # Use a valid API key from your environment variables or a secure location
        self.api_key = os.getenv('AI_SAFETY_OPENAI_API_KEY')
        self.client = OpenAI(api_key=self.api_key)
        self.evaluator = TestEvaluator(client=self.client)
        self.model_outputs = ["This output respects all rules.", "This output violates some rules."]
        self.constitution = "All outputs must be respectful and non-offensive."

    def test_calculate_model_performance(self):
        # Perform the real API call to calculate model performance
        accuracy_percentage, results_details = self.evaluator.calculate_model_performance(self.model_outputs, self.constitution)

        # Assert based on the expected structure of the results
        self.assertIsInstance(accuracy_percentage, float)
        self.assertIsInstance(results_details, list)
        self.assertTrue(all('is_compliant' in detail for detail in results_details), "Each result detail should have an 'is_compliant' key")

    def test_determine_response_result_constitution(self):
        # Perform the real API call to determine if a single output is compliant with the constitution
        for output in self.model_outputs:
            is_compliant = self.evaluator.determine_response_result_constitution(output, self.constitution)
            self.assertIn(is_compliant, [True, False], "is_compliant should be a boolean value indicating compliance status")

if __name__ == '__main__':
    unittest.main()
