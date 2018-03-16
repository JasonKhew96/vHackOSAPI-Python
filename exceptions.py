class VhackosError(Exception):
    '''Custom exception for vhackOSBot'''
    pass

class CredentialsChangedException(VhackosError):
    '''Credentials have changed.'''
