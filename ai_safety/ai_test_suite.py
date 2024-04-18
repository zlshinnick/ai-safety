from ai_safety.content_moderator.content_moderator import ContentModerator

class AITestSuite:
    def __init__(self, api_key, industries=None, ai_application=None):
        self.content_moderator = ContentModerator(api_key)

    def standard_test():
        """
        Runs standard test against toxic chat dataset.
        """

    def location_test():
        """
        Runs standard test against location specific dataset.
        """

    def indsutry_test():
        """
        Runs standard test against indsutry spefic dataset.
        """

    def application_test():
        """
        Runs standard test against application spefic dataset.
        """