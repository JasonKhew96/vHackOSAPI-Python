class VhackosError(Exception):
    '''Custom exception for vhackOSBot'''
    pass

class CredentialsChangedException(VhackosError):
    '''Credentials have changed.'''

class CredentialsExpiredException(VhackosError):
    '''Android reCAPTCHA forced.'''