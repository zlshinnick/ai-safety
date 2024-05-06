import unittest
from openai import OpenAI
from ai_safety.content_moderator.content_moderator import ContentModerator
import os
class TestContentModeratorRealAPI(unittest.TestCase):
    def setUp(self):
        # Use a valid API key from your environment variables or a secure location
        self.api_key = os.getenv('AI_SAFETY_OPENAI_API_KEY')
        self.client = OpenAI(api_key=self.api_key)
        self.moderator = ContentModerator(client=self.client)
        self.sample_text = "This is a sample text for moderation."
        self.constitution = "All outputs must be respectful and non-offensive."
        self.model_output = "This output is somewhat disrespectful."

    def test_screen_output_for_violations(self):
        # Perform the real API call
        result = self.moderator.screen_output_for_violations(self.model_output, self.constitution)

        # Assert based on the expected structure of the response
        self.assertIsInstance(result, dict)  # Ensure the response is a dictionary
        self.assertIn('violation', result)  # Check for violation in the response

        if result['violation']:
            self.assertIn('violated_rules', result)
            self.assertIn('explanation', result)
            self.assertIn('recommendation', result)


if __name__ == '__main__':
    unittest.main()
