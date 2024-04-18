import streamlit as st
from ai_safety.ai_test_suite import AITestSuite  
import os
API_KEY = os.getenv('AI_SAFETY_OPENAI_API_KEY')
test_suite = AITestSuite(API_KEY)

st.title('AI Test Suite Interface - Location Test')

if st.button('Run Location Test'):
    result = test_suite.run_test("location")

