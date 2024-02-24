"""
Exception classe
"""


class FillMeException(Exception):
    """
    Exception class used for FillMe package.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)