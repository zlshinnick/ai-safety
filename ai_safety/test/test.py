from openai import OpenAI

class Test:
    def __init__(self, content_moderator, data_generator, api_key):
        self.content_moderator = content_moderator
        self.data_generator = data_generator
        self.client = OpenAI(api_key=api_key)

    def run(self):
        raise NotImplementedError("Each test must implement a run method.")

class StandardTest(Test):
    def run(self):
        data = self.data_generator.generate()
        print(f"Running standard test with data: {data}")

class LocationTest(Test):
   def run(self):
        prompts = self.data_generator.generate()

        results = {}

        for prompt in prompts:
            try:
                request_data = {
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "system", "content": prompt}]
                }

                response = self.client.chat.completions.create(**request_data)
                text = response.choices[0].message.content.strip()
                results[prompt] = text
            except Exception as e:
                print(f"Error during API call for prompt: {prompt}\n{e}")
                results[prompt] = "Failed to generate response"

        return results
class IndustryTest(Test):
    def run(self):
        data = self.data_generator.generate()
        print(f"Running industry test with data: {data}")

class ApplicationTest(Test):
    def run(self):
        data = self.data_generator.generate()
        print(f"Running application test with data: {data}")