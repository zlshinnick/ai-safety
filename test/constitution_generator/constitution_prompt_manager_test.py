import unittest
from ai_safety.constitution_generator.constitution_prompt_manager import ConstitutionPromptManager

class TestConstitutionPromptManager(unittest.TestCase):

    def setUp(self):
        self.manager = ConstitutionPromptManager("USA")

    def test_get_guideline_categories(self):
        """Test that the guideline categories are correctly fetched based on the country."""
        guidelines = self.manager.get_guideline_categories()
        self.assertIsInstance(guidelines, dict)
        self.assertTrue("Guidelines for country" in guidelines)

    def test_formatted_prompt(self):
        """Test that the prompt formatting correctly structures the guidelines into a readable string."""
        example_guidelines = {
            "Guidelines for country": {
                "Category 1: Test Category": ["Rule 1", "Rule 2"]
            }
        }
        prompt = self.manager.formatted_prompt(example_guidelines)
        self.assertIn("Category 1: Test Category", prompt)
        self.assertIn("- Rule 1", prompt)
        self.assertIn("- Rule 2", prompt)


    def test_get_constitution_prompt(self):
        """Test the function to get a standard constitution prompt for the country."""
        prompt = self.manager.get_constitution_prompt()
        self.assertIn("Generate a comprehensive set of guidelines", prompt)
        self.assertIn("Category 1: Legal Restrictions", prompt)

    def test_get_custom_constitution_prompt(self):
        """Test the function to get a custom constitution prompt for specific industries and AI applications."""
        industries = ["Technology", "Healthcare"]
        ai_application = "data analysis"
        prompt = self.manager.get_custom_constitution_prompt(industries, ai_application)
        self.assertIn("Technology, Healthcare", prompt)
        self.assertIn("data analysis", prompt)
        self.assertIn("Category 1: Legal Restrictions", prompt)

if __name__ == '__main__':
    unittest.main()
