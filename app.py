import streamlit as st
from openai import OpenAI
import geocoder

def get_location():
    g = geocoder.ip('me')
    return g.city, g.country

def generate_constitution(client, location):
    request_data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "Generate a constitution for the user's country based on the provided template, ensuring that the outputs do not break any laws in that country."
            },
            {
                "role": "user",
                "content": f"User location: {location}"
            },
            {
                "role": "user",
                "content": "Template for constitution:\n1. Preamble\n2. Fundamental Rights\n3. Structure of Government\n4. Judicial System\n5. Amendment Process\n\nI need a constitution for my country that follows this template and respects all legal requirements."
            }
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

client = OpenAI(api_key='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')

city, country = get_location()

constitution = generate_constitution(client, f"{city}, {country}")

prompt = st.text_input('Enter your prompt:', '')
submit = st.button('Submit')

if submit:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    user_output = chat_completion.choices[0].message.content

    final_output = check_violations(client, constitution, user_output)
    st.write(final_output)