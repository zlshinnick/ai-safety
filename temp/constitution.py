import geocoder
from ai_safety.constitution_generator.constitution_prompt_manager import get_constitution_prompt, get_custom_constitution_prompt
from temp.haiku_prompts import get_constitution_prompt_haiku
from temp.mistral_prompts import get_constitution_prompt_mistral

def get_location(manual_location=None):
    """Get the users location based on their IP Adress. For testing can use the manual location text field to manually change location."""
    if manual_location:
        return manual_location.split(', ')
    else:
        g = geocoder.ip('me')
        return g.city, g.country

def generate_standard_constitution(client, location):
    """Generates standard constitution based on the users location. Used to flag any racial, faux pas or legal violations produced by the LLM. """
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

def generate_haiku_constitution(client, location):
    """Generates haiku constitution based on the users location. Used to flag any racial, faux pas or legal violations produced by the LLM. """
    request_data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": get_constitution_prompt_haiku(location)}
        ]
    }
    response = client.chat.completions.create(**request_data)
    return response.choices[0].message.content

def generate_mistral_constitution(client, location):
    """Generates haiku constitution based on the users location. Used to flag any racial, faux pas or legal violations produced by the LLM. """
    request_data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": get_constitution_prompt_mistral(location)}
        ]
    }
    response = client.chat.completions.create(**request_data)
    return response.choices[0].message.content

def generate_custom_constitution(client, location, industries, ai_application):

    # Request data setup for API call
    request_data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": get_custom_constitution_prompt(location, industries, ai_application)}
        ]
    }

    # Call the OpenAI API
    response = client.chat.completions.create(**request_data)
    constitution_text = response.choices[0].message.content
    return constitution_text