from ai_safety.test.test import StandardTest, LocationTest, IndustryTest, ApplicationTest
from ai_safety.test.test_data_generators import StandardTestDataGenerator, LocationTestDataGenerator, IndustryTestDataGenerator
from openai import OpenAI 

class TestFactory:
    """
    A factory for creating test instances with appropriate data generators based on the specified test type.
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.test_mapping = {
            "standard": (StandardTest, StandardTestDataGenerator),
            "location": (LocationTest, LocationTestDataGenerator),
            "industry": (IndustryTest, IndustryTestDataGenerator),
        }
        self.client = OpenAI(api_key=api_key)  

    def get_test(self, test_type, **kwargs):
        if test_type in self.test_mapping:
            test_class, data_generator_class = self.test_mapping[test_type]
            data_generator = data_generator_class(api_client=self.client, **kwargs) 
            return test_class(data_generator, self.api_key)
        else:
            raise ValueError(f"Unknown test type '{test_type}'. Available types are: {list(self.test_mapping.keys())}")