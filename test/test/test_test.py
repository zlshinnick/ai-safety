import unittest
from openai import OpenAI
from ai_safety.test.test import StandardTest, LocationTest, IndustryTest
from ai_safety.constitution_generator.constitution_generator import ConstitutionGenerator
from ai_safety.test.test_data_generators import StandardTestDataGenerator, LocationTestDataGenerator, IndustryTestDataGenerator
import os

class TestStandardTest(unittest.TestCase):
    def setUp(self):
        self.api_key = os.getenv('AI_SAFETY_OPENAI_API_KEY')
        self.data_generator = StandardTestDataGenerator(api_client=OpenAI(api_key=self.api_key))
        self.test_instance = StandardTest(data_generator=self.data_generator, api_key=self.api_key)

    def test_run(self):
        # We assume the run method is being tested as a black box.
        # This test will check if it completes without exceptions and returns a structured output.
        try:
            performance, result_details = self.test_instance.run()
            self.assertIsInstance(performance, float)
            self.assertIsInstance(result_details, list)
            print("Test run successfully with performance: {:.2f}%".format(performance * 100))
        except Exception as e:
            self.fail(f"Test run failed due to an error: {str(e)}")

class TestLocationTest(unittest.TestCase):
    def setUp(self):
        self.api_key = os.getenv('AI_SAFETY_OPENAI_API_KEY')
        self.data_generator = LocationTestDataGenerator(api_client=OpenAI(api_key=self.api_key))
        self.test_instance = LocationTest(data_generator=self.data_generator, api_key=self.api_key)

    def test_run(self):
        performance, result_details = self.test_instance.run()
        self.assertIsInstance(performance, float)
        self.assertIsInstance(result_details, list)

class TestIndustryTest(unittest.TestCase):
    def setUp(self):
        self.api_key = os.getenv('AI_SAFETY_OPENAI_API_KEY')
        self.data_generator = IndustryTestDataGenerator(api_client=OpenAI(api_key=self.api_key))
        self.test_instance = IndustryTest(data_generator=self.data_generator, api_key=self.api_key)

    def test_run(self):
        performance, result_details, prompts = self.test_instance.run()
        self.assertIsInstance(performance, float)
        self.assertIsInstance(result_details, list)
        self.assertIsInstance(prompts, list)

if __name__ == '__main__':
    unittest.main()
