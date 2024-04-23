import streamlit as st
from ai_safety.ai_test_suite import AITestSuite  
import os

API_KEY = os.getenv('AI_SAFETY_OPENAI_API_KEY')
test_suite = AITestSuite(API_KEY)

st.title('AI Test Suite Interface - Location Test')

if st.button('Run Location Test'):
    performance, result_details, prompts = test_suite.run_test('industry', industry='healthcare')
    st.write(f"Test Performance: {performance * 100}%")

    if result_details:
        st.subheader("Test Details")
        for detail in result_details:
            st.text(f"Model Output: {detail['output']}")
            st.text(f"Response Compliant: {'Yes' if detail['is_compliant'] else 'No'}")
            st.write("---")
    else:
        st.write("No detailed results to display.")

    for prompt in prompts:
        st.write(prompt)