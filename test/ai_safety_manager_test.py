import unittest
from unittest.mock import MagicMock, patch
from ai_safety.ai_safety_manager import AISafetyManager

class TestAISafetyManager(unittest.TestCase):
    def setUp(self):
        self.mock_openai_client = MagicMock()
        self.mock_anthropic_client = MagicMock()
        self.mock_constitution_generator = MagicMock()
        self.mock_content_moderator = MagicMock()
        self.mock_output_reviser = MagicMock()

        # Patch the constructors of the components to return the mocks
        self.patches = [
            patch('ai_safety.ai_safety_manager.ConstitutionGenerator', return_value=self.mock_constitution_generator),
            patch('ai_safety.ai_safety_manager.ContentModerator', return_value=self.mock_content_moderator),
            patch('ai_safety.ai_safety_manager.OutputReviser', return_value=self.mock_output_reviser),
            patch('openai.OpenAI', return_value=self.mock_openai_client),
            patch('anthropic.Anthropic', return_value=self.mock_anthropic_client)
        ]
        for p in self.patches:
            p.start()
            self.addCleanup(p.stop)

        self.manager = AISafetyManager(api_key='fake_api_key')

    def test_generate_constitution_standard(self):
        # Set return value for the default constitution generation method
        self.mock_constitution_generator.generate_default_constitution.return_value = 'Standard'
        result = self.manager.generate_constitution()
        self.assertEqual(result, 'Standard')

    def test_generate_constitution_custom(self):
        # Set manager to use custom settings
        self.manager.industries = ['technology']
        self.manager.ai_application = 'data analysis'
        # Set return value for the custom constitution generation method
        self.mock_constitution_generator.generate_custom_constitution.return_value = 'Custom'
        result = self.manager.generate_constitution()
        self.assertEqual(result, 'Custom')

    def test_check_content_for_moderation(self):
        # Setup the mock to return a specific moderation result
        self.mock_content_moderator.check_openai_moderation.return_value = "Moderation Alert"
        result = self.manager.check_content_for_moderation("sample text")
        self.assertEqual(result, "Moderation Alert")
        self.mock_content_moderator.check_openai_moderation.assert_called_once_with("sample text")

    def test_screen_output_against_constitution(self):
        # Setup the mock to return a violation
        self.mock_content_moderator.screen_output_for_violations.return_value = {'violation': True, 'details': 'Violation found'}
        result = self.manager.screen_output_against_constitution("sample output")
        self.assertTrue(result['violation'])
        self.mock_content_moderator.screen_output_for_violations.assert_called_once_with("sample output", self.manager.constitution)

    def test_revise_output(self):
        # Setup the mock to return a revised output
        self.mock_output_reviser.revise_output_to_comply_with_rules.return_value = "Revised output based on recommendation"
        result = self.manager.revise_output("original output", "some explanation", "some recommendation")
        self.assertEqual(result, "Revised output based on recommendation")
        self.mock_output_reviser.revise_output_to_comply_with_rules.assert_called_once_with("original output", "some explanation", "some recommendation")

if __name__ == '__main__':
    unittest.main()
