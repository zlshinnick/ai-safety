import geocoder
from versions.prompts import get_constitution_prompt

def get_location(manual_location=None):
    """Get the users location based on their IP Adress. For testing can use the manual location text field to manually change location."""
    if manual_location:
        return manual_location.split(', ')
    else:
        g = geocoder.ip('me')
        return g.city, g.country

def generate_standard_constitution(client, location):
    """Generates constitution based on the users location. Used to flag any racial, faux pas or legal violations produced by the LLM. """
    request_data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": get_constitution_prompt(location)}
        ]
    }
    response = client.chat.completions.create(**request_data)
    return response.choices[0].message.content