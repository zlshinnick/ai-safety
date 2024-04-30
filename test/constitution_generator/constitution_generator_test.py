import unittest
from unittest.mock import MagicMock
from ai_safety.constitution_generator.constitution_generator import ConstitutionGenerator

class MockOpenAIClient:
    def __init__(self):
        self.chat = MagicMock()
        self.chat.completions.create = MagicMock()

    def set_response(self, response):
        self.chat.completions.create.return_value = MagicMock(choices=[MagicMock(message=MagicMock(content=response))])

class TestConstitutionGenerator(unittest.TestCase):
    def setUp(self):
        self.mock_client = MockOpenAIClient()
        self.generator = ConstitutionGenerator(api_client=self.mock_client)
        self.industries = ["technology", "healthcare"]
        self.ai_application = "data analysis"

    def test_generate_default_constitution(self):
        # Set the response for the default test
        self.mock_client.set_response('Generated Default Constitution')
        
        # Act
        result = self.generator.generate_default_constitution()

        # Assert
        self.assertEqual(result, 'Generated Default Constitution')
        self.mock_client.chat.completions.create.assert_called_once_with(
            model='gpt-4-turbo', 
            messages=[{'role': 'system', 'content': self.generator.prompt_manager.get_constitution_prompt()}]
        )

    def test_generate_custom_constitution(self):
        # Set the response for the custom test
        self.mock_client.set_response('Generated Custom Constitution')

        # Arrange
        custom_prompt = self.generator.prompt_manager.get_custom_constitution_prompt(self.industries, self.ai_application)
        
        # Act
        result = self.generator.generate_custom_constitution(self.industries, self.ai_application)
        
        # Assert
        self.assertEqual(result, 'Generated Custom Constitution')
        self.mock_client.chat.completions.create.assert_called_once_with(
            model='gpt-4-turbo',
            messages=[{'role': 'system', 'content': custom_prompt}]
        )

if __name__ == '__main__':
    unittest.main()

