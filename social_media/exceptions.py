class ProtectedUserError(Exception):
    """ Indicates attempted access of a protected user """
    pass


class InvalidScreenNameError(Exception):
    """ @Username does not exist """
    pass


class InvalidUserError(Exception):
    """ User doesn't exist """
    pass


class InvalidCredentialsError(Exception):
    """ Raised if the credentials are invalid """
    pass


class SuspendedBannedAccountError(Exception):
    """ Raised if the account is suspended or banned """
    pass


class GeneralError(Exception):
    """ A *VERY* general exception. Raised if anything goes wrong """
    pass
