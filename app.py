import streamlit as st
import os
from ai_safety.ai_safety_manager import AISafetyManager
from openai import OpenAI
from anthropic import Anthropic

API_KEY = os.getenv('AI_SAFETY_OPENAI_API_KEY')
client = OpenAI(api_key=API_KEY)

ai_safety_manager = AISafetyManager(API_KEY)

# Generate constitution based on the location
constitution = ai_safety_manager.generate_constitution()
st.write("Constitution:" )
st.text(constitution)

# Input for user's prompt
prompt = st.text_input('Enter your prompt:', '')
submit = st.button('Submit')

if submit:
    # Check user's prompt for violations from OpenAI's moderation.
    moderation_warning = ai_safety_manager.check_content_for_moderation(prompt)
    
    if moderation_warning:
        st.error(moderation_warning)
    else:
        # Process the user's prompt if no moderation issues are found
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
        st.write("Response:", model_response)

        # Check for violations against the constitution
        violation_result = ai_safety_manager.screen_output_against_constitution(model_response)

    if violation_result["violation"]:
                st.error("A violation was detected in the model's response.")
                st.write("Violated Rules:", violation_result.get("violated_rules", []))
                st.write("Explanation:", violation_result.get("explanation", "No explanation provided."))
                st.write("Reccomendation, ", violation_result.get("recommendation", "No recommendation provided"))

                revised_output = ai_safety_manager.revise_output(
                    original_output=model_response,
                    explanation=violation_result.get("explanation", ""),
                    recommendation=violation_result.get("recommendation", ""),
                )

                st.header("after improvement has been applied")
                st.write(revised_output)
    else:
        st.success("No violation detected in the model's response.")
