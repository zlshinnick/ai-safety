from streamlit_app import generate_constitution, check_violations
from metrics.dataset import DatasetProcessor

class TestSuite:
    def __init__(self):
        self.dataset_processor = DatasetProcessor()
        self.constitution = None
        self.dataset = None

    def beginTest(self):
        self.constitution = generate_constitution()
        self.dataset = self.dataset_processor.process_dataset()

    def runEvaluation(self):
        for i in range(1000):
            example = self.dataset[i]
            violation = check_violations(self.constitution, example['user_input'])
            if violation:
                self.violations_counter += 1
            self.generateOutput(example, violation)

    def generateOutput(self, example, violation):
        print(f"Example: {example['user_input']}")
        print(f"Violation: {violation}")

    def assessOutput(self):
        """
        this will be defined elsewhere (in "assessment")
        """
        pass

    def presentMetrics(self):
        # present as a percentage 
        violation_percentage = (self.violations_count / 1000) * 100
        print(f"Percentage of violations: {violation_percentage}%")
        pass

# doubt this will work yet as dataset still has issues but think it is good boiler plate
test_suite = TestSuite()
test_suite.beginTest()
test_suite.runEvaluation()
test_suite.assessOutput()
test_suite.presentMetrics()