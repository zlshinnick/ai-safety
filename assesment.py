
import requests

def check_openai_moderation(text, key):
    """Checks if the users prompt violates OpenAI's content policy"""
    url = "https://api.openai.com/v1/moderations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"
    }
    data = {"input": text}
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        moderation_response = response.json()

        if moderation_response["results"][0]["flagged"]:
            categories = moderation_response["results"][0]["categories"]
            categories_list = ", ".join(categories)
            return f"Your prompt contains content that violates our content policy in the following categories: {categories_list}. Please revise your input and try again."
        else:
            return None
    except requests.exceptions.RequestException as e:
        return f"Error checking moderation: {e}"
