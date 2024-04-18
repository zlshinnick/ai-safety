from ai_safety.content_moderator.content_moderator import ContentModerator
from ai_safety.test.test_factory import TestFactory

class AITestSuite:
    def __init__(self, api_key):
        self.content_moderator = ContentModerator(api_key)
        self.test_factory = TestFactory(self.content_moderator, api_key)  

        self.tests = {
            "standard": self.test_factory.get_test("standard"),
            "location": self.test_factory.get_test("location"),
            "industry": self.test_factory.get_test("industry"),
            "application": self.test_factory.get_test("application"),
        }

        print("Made all Test Classes")

    def run_test(self, test_type):
        """Run a single test."""
        test = self.tests.get(test_type)
        print(f"Running test {test_type}")
        if test:
            return test.run()
        else:
            raise ValueError(f"Test type {test_type} not recognized.")

    def run_all_tests(self):
        pass
