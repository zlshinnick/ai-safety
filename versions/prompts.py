def get_constitution_prompt(country_name):
    return f"""
Generate a comprehensive set of guidelines for a language model in a structured format to ensure its outputs are in compliance with the laws, social norms, cultural expectations, and ethical standards of {country_name}. The guidelines should be organized into the following categories, each with a list of specific rules:

Category 1: Legal Restrictions
    - Rule 1: [Description of Rule 1]
    - Rule 2: [Description of Rule 2]
    ...

Category 2: Social Etiquette
    - Rule 1: [Description of Rule 1]
    - Rule 2: [Description of Rule 2]
    ...

Category 3: Cultural Sensitivities
    - Rule 1: [Description of Rule 1]
    - Rule 2: [Description of Rule 2]
    ...

Category 4: Privacy and Confidentiality
    - Rule 1: [Description of Rule 1]
    - Rule 2: [Description of Rule 2]
    ...

Category 5: Intellectual Property Rights
    - Rule 1: [Description of Rule 1]
    - Rule 2: [Description of Rule 2]
    ...

Category 6: Bias and Discrimination
    - Rule 1: [Description of Rule 1]
    - Rule 2: [Description of Rule 2]
    ...

Category 7: Misinformation
    - Rule 1: [Description of Rule 1]
    - Rule 2: [Description of Rule 2]
    ...

Category 8: Incitement and Harm
    - Rule 1: [Description of Rule 1]
    - Rule 2: [Description of Rule 2]
    ...

Category 9: Professional Ethics
    - Rule 1: [Description of Rule 1]
    - Rule 2: [Description of Rule 2]
    ...

Category 10: Psychological Harm
    - Rule 1: [Description of Rule 1]
    - Rule 2: [Description of Rule 2]
    ...

The aim is to provide a clear, organized, and easily interpretable set of guidelines that the language model can use to detect any violations in its outputs within the context of {country_name}.
"""