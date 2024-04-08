from langdetect import detect
from datasets import load_dataset
from langdetect.lang_detect_exception import LangDetectException
from app import generate_constitution, check_violations
from openai import OpenAI

class DatasetProcessor:
    def __init__(self):
        self.dataset = load_dataset('lmsys/toxic-chat', 'toxicchat0124')
        self.language_to_location = {
            'af': 'Pretoria, South Africa',  # Afrikaans
            'sq': 'Tirana, Albania',  # Albanian
            'am': 'Addis Ababa, Ethiopia',  # Amharic
            'ar': 'Riyadh, Saudi Arabia',  # Arabic
            'hy': 'Yerevan, Armenia',  # Armenian
            'az': 'Baku, Azerbaijan',  # Azerbaijani
            'eu': 'Bilbao, Spain',  # Basque
            'be': 'Minsk, Belarus',  # Belarusian
            'bn': 'Dhaka, Bangladesh',  # Bengali
            'bs': 'Sarajevo, Bosnia and Herzegovina',  # Bosnian
            'bg': 'Sofia, Bulgaria',  # Bulgarian
            'ca': 'Barcelona, Spain',  # Catalan
            'ceb': 'Cebu, Philippines',  # Cebuano
            'ny': 'Lilongwe, Malawi',  # Chichewa
            'zh-cn': 'Beijing, China',  # Chinese (Simplified)
            'zh-tw': 'Taipei, Taiwan',  # Chinese (Traditional)
            'co': 'Ajaccio, France',  # Corsican
            'hr': 'Zagreb, Croatia',  # Croatian
            'cs': 'Prague, Czech Republic',  # Czech
            'da': 'Copenhagen, Denmark',  # Danish
            'nl': 'Amsterdam, Netherlands',  # Dutch
            'en': 'Washington, USA',  # English
            'eo': 'Worldwide',  # Esperanto
            'et': 'Tallinn, Estonia',  # Estonian
            'tl': 'Manila, Philippines',  # Filipino
            'fi': 'Helsinki, Finland',  # Finnish
            'fr': 'Paris, France',  # French
            'fy': 'Leeuwarden, Netherlands',  # Frisian
            'gl': 'Santiago de Compostela, Spain',  # Galician
            'ka': 'Tbilisi, Georgia',  # Georgian
            'de': 'Berlin, Germany',  # German
            'el': 'Athens, Greece',  # Greek
            'gu': 'Gandhinagar, India',  # Gujarati
            'ht': 'Port-au-Prince, Haiti',  # Haitian Creole
            'ha': 'Kano, Nigeria',  # Hausa
            'haw': 'Honolulu, USA',  # Hawaiian
            'iw': 'Jerusalem, Israel',  # Hebrew
            'hi': 'New Delhi, India',  # Hindi
            'hmn': 'St. Paul, USA',  # Hmong
            'hu': 'Budapest, Hungary',  # Hungarian
            'is': 'Reykjavik, Iceland',  # Icelandic
            'ig': 'Enugu, Nigeria',  # Igbo
            'id': 'Jakarta, Indonesia',  # Indonesian
            'ga': 'Dublin, Ireland',  # Irish
            'it': 'Rome, Italy',  # Italian
            'ja': 'Tokyo, Japan',  # Japanese
            'jw': 'Yogyakarta, Indonesia',  # Javanese
            'kn': 'Bengaluru, India',  # Kannada
            'kk': 'Nur-Sultan, Kazakhstan',  # Kazakh
            'km': 'Phnom Penh, Cambodia',  # Khmer
            'ko': 'Seoul, South Korea',  # Korean
            'ku': 'Erbil, Iraq',  # Kurdish (Kurmanji)
            'ky': 'Bishkek, Kyrgyzstan',  # Kyrgyz
            'lo': 'Vientiane, Laos',  # Lao
            'la': 'Vatican City',  # Latin
            'lv': 'Riga, Latvia',  # Latvian
            'lt': 'Vilnius, Lithuania',  # Lithuanian
            'lb': 'Luxembourg City, Luxembourg',  # Luxembourgish
            'mk': 'Skopje, North Macedonia',  # Macedonian
            'mg': 'Antananarivo, Madagascar',  # Malagasy
            'ms': 'Kuala Lumpur, Malaysia',  # Malay
            'ml': 'Thiruvananthapuram, India',  # Malayalam
            'mt': 'Valletta, Malta',  # Maltese
            'mi': 'Wellington, New Zealand',  # Maori
            'mr': 'Mumbai, India',  # Marathi
            'mn': 'Ulaanbaatar, Mongolia',  # Mongolian
            'my': 'Naypyidaw, Myanmar (Burma)',  # Burmese
            'ne': 'Kathmandu, Nepal',  # Nepali
            'no': 'Oslo, Norway',  # Norwegian
            'ps': 'Kabul, Afghanistan',  # Pashto
            'fa': 'Tehran, Iran',  # Persian
            'pl': 'Warsaw, Poland',  # Polish
            'pt': 'Lisbon, Portugal',  # Portuguese
            'pa': 'Chandigarh, India',  # Punjabi
            'ro': 'Bucharest, Romania',  # Romanian
            'ru': 'Moscow, Russia',  # Russian
            'sm': 'Apia, Samoa',  # Samoan
            'gd': 'Edinburgh, Scotland',  # Scots Gaelic
            'sr': 'Belgrade, Serbia',  # Serbian
            'st': 'Maseru, Lesotho',  # Sesotho
            'sn': 'Harare, Zimbabwe',  # Shona
            'sd': 'Karachi, Pakistan',  # Sindhi
            'si': 'Colombo, Sri Lanka',  # Sinhala
            'sk': 'Bratislava, Slovakia',  # Slovak
            'sl': 'Ljubljana, Slovenia',  # Slovenian
            'so': 'Mogadishu, Somalia',  # Somali
            'es': 'Madrid, Spain',  # Spanish
            'su': 'Bandung, Indonesia',  # Sundanese
            'sw': 'Nairobi, Kenya',  # Swahili
            'sv': 'Stockholm, Sweden',  # Swedish
            'tg': 'Dushanbe, Tajikistan',  # Tajik
            'ta': 'Chennai, India',  # Tamil
            'te': 'Hyderabad, India',  # Telugu
            'th': 'Bangkok, Thailand',  # Thai
            'tr': 'Ankara, Turkey',  # Turkish
            'uk': 'Kyiv, Ukraine',  # Ukrainian
            'ur': 'Islamabad, Pakistan',  # Urdu
            'uz': 'Tashkent, Uzbekistan',  # Uzbek
            'vi': 'Hanoi, Vietnam',  # Vietnamese
            'cy': 'Cardiff, Wales',  # Welsh
            'xh': 'Cape Town, South Africa',  # Xhosa
            'yi': 'Worldwide',  # Yiddish
            'yo': 'Lagos, Nigeria',  # Yoruba
            'zu': 'Durban, South Africa',  # Zulu
        }
    
    def add_columns(self, example):
        text = example['user_input']
        text = self.clean_text(text)

        try:
            language = detect(text)
        except LangDetectException:
            language = 'unknown'

        location = self.language_to_location.get(language, 'Unknown')
        constitution = generate_constitution(self.client, location)
        violation = check_violations(self.client, constitution, text)

        example['location'] = location
        example['constitution'] = constitution
        example['violation'] = violation

        return example

    def process_dataset(self):
        # add new columns to the dataset based on the user's input
        self.dataset = self.dataset.map(self.add_columns)
        return self.dataset

    def get_example(self, index):
        # function to return an example 
        return self.dataset[index]

    def get_size(self):
        # unaware if this is needed but added it to validate the size of the dataset
        return len(self.dataset)

    def filter_dataset(self, condition):
        # this will likely need fleshing out, but it would allow us to filter the dataset based on a condition
        """
        for example:
        - if the condition function returns True for an example, the example is included in the filtered dataset
        - if the condition function returns False for an example, the example is excluded from the filtered dataset
        """
        self.dataset = self.dataset.filter(condition)
        return self.dataset

    def shuffle_dataset(self):
        # shuffling the data set to ensure that the model is not biased by the order of the examples (limits overfitting)
        self.dataset = self.dataset.shuffle()
        return self.dataset
