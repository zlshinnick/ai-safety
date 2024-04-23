from ai_safety.test.test_factory import TestFactory
class AITestSuite:
    def __init__(self, api_key):
        self.test_factory = TestFactory(api_key)
        self.tests = {}  # Keeps track of already created test instances

    def run_test(self, test_type, **kwargs):
        # Fetch the test from stored or create a new one
        if test_type not in self.tests:
            self.tests[test_type] = self.test_factory.get_test(test_type, **kwargs)
        test = self.tests[test_type]
        print(f"Running test {test_type}")
        return test.run()

    def run_all_tests(self):
        pass