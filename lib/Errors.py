# GENERAL ERROR TYPES -----------------------------------------------------------------------------
class GeneralError(BaseException):
    pass


class GeneralError_WrongInput(GeneralError):
    pass


class GeneralError_NotCallable(GeneralError):
    pass


# HOST ERROR TYPES ---------------------------------------------------------------------------------
class HostError(BaseException):
    pass


class HostError_NotANode(HostError):
    pass


class HostError_Connection(HostError):
    pass


class HostError_CompletenessViolated(HostError):
    pass


class HostError_NotSupported(HostError):
    pass


class HostError_NoSuchNode(HostError):
    pass

