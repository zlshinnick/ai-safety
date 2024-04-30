import os
from openai import OpenAI
from .constitution_prompt_manager import ConstitutionPromptManager
from .location_manager import LocationManager  

class ConstitutionGenerator:
    def __init__(self, api_client):
        self.client = api_client
        self.location_manager = LocationManager()
        self.location = self.location_manager.get_location() 
        self.prompt_manager = ConstitutionPromptManager(self.location)

    def generate_default_constitution(self):
        try:
            prompt = self.prompt_manager.get_constitution_prompt()
            request_data = {
                "model": "gpt-4-turbo",
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
            request_data = {
                "model": "gpt-4-turbo",
                "messages": [{"role": "system", "content": prompt}]
            }
            response = self.client.chat.completions.create(**request_data)
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating custom constitution: {e}")
            return None
