class Test:
    def __init__(self, content_moderator, data_generator):
        self.content_moderator = content_moderator
        self.data_generator = data_generator

    def run(self):
        raise NotImplementedError("Each test must implement a run method.")

class StandardTest(Test):
    def run(self):
        data = self.data_generator.generate()
        print(f"Running standard test with data: {data}")

class LocationTest(Test):
    def run(self):
        data = self.data_generator.generate()
        print(f"Running location test with data: {data}")

class IndustryTest(Test):
    def run(self):
        data = self.data_generator.generate()
        print(f"Running industry test with data: {data}")

class ApplicationTest(Test):
    def run(self):
        data = self.data_generator.generate()
        print(f"Running application test with data: {data}")