import unittest
from openai import OpenAI
from ai_safety.test.test_data_generators import StandardTestDataGenerator, LocationTestDataGenerator, IndustryTestDataGenerator
from ai_safety.constitution_generator.location_manager import LocationManager
import os

class TestStandardTestDataGenerator(unittest.TestCase):
    def setUp(self):
        self.api_client = OpenAI(api_key=os.getenv('AI_SAFETY_OPENAI_API_KEY'))
        self.generator = StandardTestDataGenerator(api_client=self.api_client)

    def test_generate_standard_data(self):
        user_inputs = self.generator.generate()
        self.assertIsInstance(user_inputs, list)
        self.assertTrue(len(user_inputs) >= 10, "Should generate at least 10 inputs")

class TestLocationTestDataGenerator(unittest.TestCase):
    def setUp(self):
        self.api_client = OpenAI(api_key=os.getenv('AI_SAFETY_OPENAI_API_KEY'))
        self.location_manager = LocationManager()
        self.generator = LocationTestDataGenerator(api_client=self.api_client, location_manager=self.location_manager)

    def test_generate_location_based_data(self):
        prompts = self.generator.generate()
        self.assertIsInstance(prompts, list)
        self.assertTrue(len(prompts) >= 10, "Should generate at least 10 location-based prompts")

class TestIndustryTestDataGenerator(unittest.TestCase):
    def setUp(self):
        self.api_client = OpenAI(api_key=os.getenv('AI_SAFETY_OPENAI_API_KEY'))
        self.location_manager = LocationManager()
        self.generator = IndustryTestDataGenerator(api_client=self.api_client, location_manager=self.location_manager, industry="technology")

    def test_generate_industry_based_data(self):
        prompts = self.generator.generate()
        self.assertIsInstance(prompts, list)
        self.assertTrue(len(prompts) >= 10, "Should generate at least 10 industry-specific prompts")

if __name__ == '__main__':
    unittest.main()
