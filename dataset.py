from langdetect import detect
from datasets import load_dataset
from langdetect.lang_detect_exception import LangDetectException

dataset = load_dataset('lmsys/toxic-chat', 'toxicchat0124') 

language_to_location = {
    'en': 'Washington, USA',
    'fr': 'Paris, France',
    'es': 'Madrid, Spain',
    'de': 'Berlin, Germany',
    'it': 'Rome, Italy',
    'pt': 'Lisbon, Portugal',
    'ru': 'Moscow, Russia',
    'ja': 'Tokyo, Japan',
    'zh-cn': 'Beijing, China',
    'ar': 'Riyadh, Saudi Arabia',
    'hi': 'New Delhi, India',
    'ko': 'Seoul, South Korea',
}

def add_columns(example):
    text = example['user_input']  

    try:
        language = detect(text)
    except LangDetectException:
        language = 'unknown'

    location = language_to_location.get(language, 'Unknown')
    example['role'] = ['system', 'user', 'user']
    example['content'] = [
        "Generate a constitution for the user's country based on the provided template, ensuring that the outputs do not break any laws in that country.",
        f"User location: {location}",
        "Template for constitution:\n1. Preamble\n2. Fundamental Rights\n3. Structure of Government\n4. Judicial System\n5. Amendment Process\n\nI need a constitution for my country that follows this template and respects all legal requirements."
    ]
    return example

dataset = dataset.map(add_columns)