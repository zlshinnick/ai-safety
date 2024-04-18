import os
from openai import OpenAI
from .constitution_prompt_manager import ConstitutionPromptManager
from .location_manager import LocationManager  

class ConstitutionGenerator:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.location_manager = LocationManager()
        country = self.location_manager.get_location() 
        self.prompt_manager = ConstitutionPromptManager(country)

    def generate_default_constitution(self):
        """Generates a default constitution for the specified location."""
        try:
            prompt = self.prompt_manager.get_constitution_prompt()
            print(prompt)
            request_data = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "system", "content": prompt}]
            }
            response = self.client.chat.completions.create(**request_data)
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating standard constitution: {e}")
            return None

    def generate_custom_constitution(self, industries, ai_application):
        """Generates a custom constitution tailored to specific industries and applications for specified location."""
        try:
            prompt = self.prompt_manager.get_custom_constitution_prompt(industries, ai_application)
            print(prompt)
            request_data = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "system", "content": prompt}]
            }
            response = self.client.chat.completions.create(**request_data)
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating custom constitution: {e}")
            return None
