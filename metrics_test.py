import streamlit as st
from ai_safety.ai_test_suite import AITestSuite
import os

# Setup the API key and initialize the test suite
API_KEY = os.getenv('AI_SAFETY_OPENAI_API_KEY')
test_suite = AITestSuite(API_KEY)

st.title('Metrics for Standard Test')

# Button to trigger the test
if st.button('Run Standard Test'):
    # Running the 'location' test specifically
    performance, result_details, prompts = test_suite.run_test('standard')
    st.write(f"Test Performance: {performance * 100:.2f}%")

    if result_details:
        st.subheader("Test Details")
        # Iterate through each result and corresponding prompt
        for prompt, detail in zip(prompts, result_details):
            st.write(f"Prompt: {prompt}")
            st.write(f"Model Output: {detail['output']}")
            st.write(f"Response Compliant: {'Yes' if detail['is_compliant'] else 'No'}")
            st.write("---")
    else:
        st.write("No detailed results to display.")
