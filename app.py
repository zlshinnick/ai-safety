import streamlit as st
from openai import OpenAI
import geocoder
import requests
from prompts import get_constitution_prompt

API_KEY = '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'

def get_location(manual_location=None):
    """Get the users location based on their IP Adress. For testing can use the manual location text field to manually change location."""
    if manual_location:
        return manual_location.split(', ')
    else:
        g = geocoder.ip('me')
        return g.city, g.country
    
def check_moderation(text):
    """Checks if the users prompt violates OpenAI's content policy"""
    url = "https://api.openai.com/v1/moderations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
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

def generate_constitution(client, location):
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

def check_violations(client, constitution, user_output):
    request_data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "Given the following constitution and an output based on a user prompt, determine if the output violates any part of the constitution. If it does, rewrite the output to comply with the constitution by prodviding a warning stating why this prompt is not allowed."
            },
            {
                "role": "user",
                "content": f"Constitution:\n{constitution}"
            },
            {
                "role": "user",
                "content": f"Output:\n{user_output}"
            },
            {
                "role": "user",
                "content": "Check if the above output violates any part of the constitution and rewrite it to comply if necessary. Only output the new output if a violation is detected. Otherwise, keep the output the same as before. I do not want any additional characters apart from the output message."
            }
        ]
    }
    response = client.chat.completions.create(**request_data)
    return response.choices[0].message.content

client = OpenAI(api_key=API_KEY)

manual_location = st.text_input('Enter a manual location (City, Country) for testing:', '')
change_location = st.button('Change Location')

if change_location:
    city, country = get_location(manual_location)
else:
    city, country = get_location()

constitution = generate_constitution(client, f"{city}, {country}")

prompt = st.text_input('Enter your prompt:', '')
submit = st.button('Submit')
st.write(city, country)

if submit:
    # Check users prompt for violations from OpenAI moderation. 
    user_prompt_moderation_warning = check_moderation(prompt)
    
    if user_prompt_moderation_warning:
        st.error(user_prompt_moderation_warning)
    else:
        # Generate chat completion from user input
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
        )
        model_response = chat_completion.choices[0].message.content
        
        # Screen models output against our constitution.
        final_output = check_violations(client, constitution, model_response)

        st.write(final_output)
