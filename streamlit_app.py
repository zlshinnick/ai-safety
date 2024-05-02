import streamlit as st
import os
import json
from ai_safety.ai_safety_manager import AISafetyManager
from openai import OpenAI
from anthropic import Anthropic

# Get the API key from environment variables
API_KEY = os.getenv('AI_SAFETY_OPENAI_API_KEY')
client = OpenAI(api_key=API_KEY)
ai_safety_manager = AISafetyManager(API_KEY)

# Generate constitution based on the location
constitution = ai_safety_manager.generate_constitution()

# Title for prompt input
st.markdown(
    "<h3 style='color: white; font-family: \"DM Mono\", monospace;'>Enter prompt:</h3>",
    unsafe_allow_html=True
)
prompt = st.text_input('', '')
submit = st.button('Submit')

if submit:
    moderation_warning = ai_safety_manager.check_content_for_moderation(prompt)
    
    if moderation_warning:
        st.error(moderation_warning)
    else:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-3.5-turbo",
        )
        model_response = chat_completion.choices[0].message.content
        st.markdown("<p style='color: white; font-family: \"DM Mono\", monospace; font-weight: bold;'>Response:</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: white; font-family: \"DM Mono\", monospace;'>{model_response}</p>", unsafe_allow_html=True)

        violation_result = ai_safety_manager.screen_output_against_constitution(model_response)

        # Check if violation_result is not None before accessing "violation"
        if violation_result and violation_result.get("violation"):
            st.error("A violation was detected in the model's response.")
            violated_rules = violation_result.get("violated_rules", [])
            st.write("Violated Rules:", ', '.join(violated_rules) if violated_rules else "No rules violated.")
            st.markdown("<p style='color: white; font-family: \"DM Mono\", monospace; font-weight: bold;'>Explanation:</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: white; font-family: \"DM Mono\", monospace;'>{violation_result.get('explanation', 'No explanation provided.')}</p>", unsafe_allow_html=True)
            st.markdown("<p style='color: white; font-family: \"DM Mono\", monospace; font-weight: bold;'>Recommendation:</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: white; font-family: \"DM Mono\", monospace;'>{violation_result.get('recommendation', 'No recommendation provided.')}</p>", unsafe_allow_html=True)

            revised_output = ai_safety_manager.revise_output(
                original_output=model_response,
                explanation=violation_result.get("explanation", ""),
                recommendation=violation_result.get("recommendation", "")
            )
            st.markdown(f"<p style='color: white; font-family: \"DM Mono\", monospace; font-weight: bold;'>After improvement:</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: white; font-family: \"DM Mono\", monospace;'>{revised_output}</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='color: white; font-family: \"DM Mono\", monospace; font-weight: bold;'>No violation detected in the model's response.</p>", unsafe_allow_html=True)
