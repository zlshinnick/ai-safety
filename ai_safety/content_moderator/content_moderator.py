import requests
import json
from openai import OpenAI

class ContentModerator:
    def __init__(self, client):
        self.client = client

    def check_openai_moderation(self, text):
        """Checks if the user's prompt violates OpenAI's content policy."""
        url = "https://api.openai.com/v1/moderations"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.client.api_key}"
        }
        data = {"input": text}
        response = self.send_request_to_openai(url, headers, data)
        return self.parse_moderation_response(response)

    def screen_output_for_violations(self, model_output, constitution):
            """ Screen if the model output violates any given constitution."""
            request_data = {
                "model": "gpt-4-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": "Given the following constitution and an output based on a user prompt, identify any violations in the output. If there are no violations, state that the output is compliant. Return the result in JSON format, including the violated rules, an explanation, and a recommendation to improve the output if any."
                    },
                    {
                        "role": "user",
                        "content": f"Constitution:\n{constitution}"
                    },
                    {
                        "role": "user",
                        "content": f"Output:\n{model_output}"
                    },
                    {
                        "role": "user",
                        "content": "Check if the output complies with the constitution. If it violates any rules, return {\"violation\": true, \"violated_rules\": [\"Name of Rule 1\", \"Name of Rule 2\"], \"explanation\": \"Explanation of the violation\", \"recommendation\": \"Please revise the output to address the following issues: [Explanation of the violation]. Ensure the revised output complies with the constitution, specifically adhering to [Name of Rule 1, Name of Rule 2].\"}. If there are no violations, return {\"violation\": false}."
                    }
                ]
            }
            response = self.client.chat.completions.create(**request_data)
            response_content = response.choices[0].message.content

            try:
                result = json.loads(response_content)
                return result
            except json.JSONDecodeError:
                return {"violation": False}

    def send_request_to_openai(self, url, headers, data):
        """Send requests to the OpenAI API."""
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def parse_moderation_response(self, response):
        """Parse the moderation response from OpenAI."""
        if response.get("results", [{}])[0].get("flagged", False):
            categories = response["results"][0]["categories"]
            categories_list = ", ".join(categories)
            return f"Your prompt contains content that violates our content policy in the following categories: {categories_list}. Please revise your input and try again."
        else:
            return None
