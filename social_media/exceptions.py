"""
All exceptions used in the app
"""


class ProtectedUserError(Exception):
    """ Indicates attempted access of a protected user """
    pass


class InvalidScreenNameError(Exception):
    """ @Username does not exist """
    pass


class InvalidCredentialsError(Exception):
    """ Raised if the credentials are invalid """
    pass


class UnexpectedError(Exception):
    """ A *VERY* general exception. Raised if anything goes wrong """
    pass
