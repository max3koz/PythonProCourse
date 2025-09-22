class AgeVerifier:
    """Class for verifying the user's age."""

    @staticmethod
    def is_adult(age: int) -> bool:
        """Return True, if the age more or equal 18."""
        return age >= 18
