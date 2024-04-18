class Test:
    def __init__(self, content_moderator, data_generator, api_key):
        self.content_moderator = content_moderator
        self.data_generator = data_generator
        self.api_key = api_key  

    def run(self):
        raise NotImplementedError("Each test must implement a run method.")

class StandardTest(Test):
    def run(self):
        data = self.data_generator.generate()
        print(f"Running standard test with data: {data}")

class LocationTest(Test):
    def run(self):
        data = self.data_generator.generate()

class IndustryTest(Test):
    def run(self):
        data = self.data_generator.generate()
        print(f"Running industry test with data: {data}")

class ApplicationTest(Test):
    def run(self):
        data = self.data_generator.generate()
        print(f"Running application test with data: {data}")