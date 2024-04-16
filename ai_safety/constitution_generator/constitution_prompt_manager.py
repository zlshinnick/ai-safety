class ConstitutionPromptManager:
    def __init__(self, country_name):
        self.country_name = country_name

    def get_guideline_categories(self):
        """Generates standard guideline categories with rules."""
        return {
            "Legal Restrictions": [
                "Do not produce any content that violates the country's constitution, laws, or regulations.",
                "Refrain from generating content that infringes on the intellectual property rights of others.",
                "Avoid producing content that is considered obscene, pornographic, or sexually explicit.",
                "Do not generate content that promotes or encourages illegal activities."
            ],
            "Social Etiquette": [
                "Maintain a respectful and polite tone in all outputs.",
                "Refrain from generating content that is considered rude, impolite, or disrespectful."
            ],
            "Cultural Sensitivities": [
                "Respect and accurately represent the country's cultural heritage.",
                "Avoid producing content that trivializes or disrespects the country's indigenous populations."
            ],
            "Privacy and Confidentiality": [
                "Do not disclose or generate content that reveals sensitive personal information without consent.",
                "Avoid generating content that violates the privacy rights of individuals."
            ],
            "Intellectual Property Rights": [
                "Do not reproduce, distribute, or create derivative works from copyrighted material without permission.",
                "Respect and accurately attribute the intellectual property of others."
            ],
            "Bias and Discrimination": [
                "Refrain from producing content that expresses or promotes biases or discrimination.",
                "Ensure that the portrayal of individuals and groups is free from stereotypical representations."
            ],
            "Misinformation": [
                "Do not generate content that contains false, misleading, or unsubstantiated information.",
                "Ensure that all factual claims are supported by reliable and verifiable sources."
            ],
            "Incitement and Harm": [
                "Do not generate content that incites or encourages violence or hatred.",
                "Refrain from producing content that could cause physical, emotional, or psychological harm."
            ],
            "Professional Ethics": [
                "Maintain the highest standards of professional integrity and ethics in all outputs.",
                "Avoid any content that could be considered deceptive, manipulative, or exploitative."
            ],
            "Psychological Harm": [
                "Do not generate content that is likely to cause significant psychological distress or harm.",
                "Avoid generating content that exploits or manipulates human emotions."
            ]
        }


    def formatted_prompt(self, guidelines):
        """Formats guidelines dictionary into a structured string for display."""
        formatted_text = f"Generate a comprehensive set of guidelines for a language model in {self.country_name}. Here are some examples of different categories and rules. Structure your output the same as the example. Make sure to include country specific guidlines and rules.:\n"
        for category, rules in guidelines.items():
            formatted_text += f"\nCategory {list(guidelines.keys()).index(category) + 1}: {category}\n"
            for rule in rules:
                formatted_text += f"    - {rule}\n"
        formatted_text += "\n\nThe aim is to provide a clear, organized, and easily interpretable set of guidelines."
        return formatted_text

    def get_constitution_prompt(self):
        """
        Generates  set of guidelines for a language model formatted for the specified country.
        
        Args:

        Returns:
            str: A formatted string containing the prompt to create the constitution.
        """   
        guidelines = self.get_guideline_categories()
        print("Successfully got standard constitituion prompt")
        return self.formatted_prompt(guidelines)

    def get_custom_constitution_prompt(self, industries, ai_application):
        """
        Generates a custom set of guidelines for a language model that includes
        industry-specific and application-specific rules, formatted for the specified country.
        
        Args:
            industries (list of str): List of industries to tailor the guidelines.
            ai_application (str): Specific AI application to consider in the guidelines.

        Returns:
            str: A formatted string containing the prompt to create the constitution.
        """
        # Retrieve the base guidelines and format them
        guidelines = self.get_guideline_categories()
        formatted_guidelines = self.formatted_prompt(guidelines)
        
        industries_formatted = ', '.join(industries)
        
        return (
            f"Generate a comprehensive set of guidelines for a language model in {self.country_name}:\n"
            f"{formatted_guidelines}\n"
            f"This model is tailored for industries such as {industries_formatted}. The model is primarily used for {ai_application}. "
            f"Use the default rules, but also include additional industry specific ones. Ensure that the new rules are industry-specific and application-specific."
            f"Include all of the rules in the output, including the default and industry specific rules."
            f"Structure the output in a form which a language model will easily be able to follow the guidelines and ensure no violations of the rules."
        )