import streamlit as st
import os
from openai import OpenAI


client = OpenAI(
    api_key='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',
)

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

    response = chat_completion.choices[0].message.content
    st.write(response)



