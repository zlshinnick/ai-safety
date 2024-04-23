from openai import OpenAI
from ai_safety.test.test_evaluator import TestEvaluator
from ai_safety.constitution_generator.constitution_generator import ConstitutionGenerator

class Test:
    def __init__(self,data_generator, api_key):
        self.data_generator = data_generator
        self.client = OpenAI(api_key=api_key)
        self.test_evaluator = TestEvaluator(client=self.client)

    def run(self):
        raise NotImplementedError("Each test must implement a run method.")

class StandardTest(Test):
    def run(self):
        data = self.data_generator.generate()
        print(f"Running standard test with data: {data}")

class LocationTest(Test):
    def __init__(self, data_generator, api_key):
        super().__init__(data_generator, api_key)  
        self.constitution = ConstitutionGenerator(api_key).generate_default_constitution() 

    def run(self):
        prompts = self.data_generator.generate()
        results = {}
        model_outputs = []

        for prompt in prompts:
            try:
                request_data = {
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": prompt}]
                }

                response = self.client.chat.completions.create(**request_data)
                text = response.choices[0].message.content.strip()
                results[prompt] = text
                model_outputs.append(text)  

            except Exception as e:
                print(f"Error during API call for prompt: {prompt}\n{e}")
                results[prompt] = "Failed to generate response"
        
        performance, result_details = self.test_evaluator.calculate_model_performance(model_outputs, self.constitution)
        return performance, result_details


class IndustryTest(Test):
    def __init__(self, data_generator, api_key):
        super().__init__(data_generator, api_key)  
        self.constitution = ConstitutionGenerator(api_key).generate_default_constitution() 
    def run(self):
        prompts = self.data_generator.generate()
        results = {}
        model_outputs = []

        for prompt in prompts:
            try:
                request_data = {
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": prompt}]
                }

                response = self.client.chat.completions.create(**request_data)
                text = response.choices[0].message.content.strip()
                results[prompt] = text
                model_outputs.append(text)  

            except Exception as e:
                print(f"Error during API call for prompt: {prompt}\n{e}")
                results[prompt] = "Failed to generate response"
        
        performance, result_details = self.test_evaluator.calculate_model_performance(model_outputs, self.constitution)
        return performance, result_details

class ApplicationTest(Test):
    def run(self):
        data = self.data_generator.generate()
        print(f"Running application test with data: {data}")