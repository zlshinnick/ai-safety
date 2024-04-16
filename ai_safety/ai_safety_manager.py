from ai_safety.constitution_generator.constitution_generator import ConstitutionGenerator
from ai_safety.conent_moderator.content_moderator import ContentModerator
from ai_safety.output_reviser.output_reviser import OutputReviser

class AISafetyManager:
    def __init__(self, api_key, industries=None, ai_application=None):
        self.api_key = api_key
        self.industries = industries
        self.ai_application = ai_application

        self.constitution_generator = ConstitutionGenerator(api_key)
        self.content_moderator = ContentModerator(api_key)
        self.output_reviser = OutputReviser(api_key)

        self.constitution = self.generate_constitution()

    def generate_constitution(self):
        """
        Generate a constitution based on the location and optionally for specific industries and applications.
        """
        if self.industries and self.ai_application:
            return self.constitution_generator.generate_custom_constitution(self.industries, self.ai_application)
        else:
            return self.constitution_generator.generate_standard_constitution()

    def check_content_for_moderation(self, text):
        """
        Check if the given text violates any OpenAI content moderation policies.
        """
        return self.content_moderator.check_openai_moderation(text)

    def screen_output_against_constitution(self, text):
        """
        Check if the given text violates the constitution.
        """
        return self.content_moderator.screen_output_for_violations(text, self.constitution)
    
    def revise_output(self, original_output, explanation, recommendation):
        """
        Revise the given output based on the explanation and recommendation provided.
        """
        return self.output_reviser.revise_output_to_comply_with_rules(original_output, explanation, recommendation)
