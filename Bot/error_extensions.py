# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


class NeverInSameLobbyError(Error):
    """Raised when users never were in the same lobby"""
    pass