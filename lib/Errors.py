class GeneralError(BaseException):
    pass


class GeneralError_WrongInput(GeneralError):
    pass


class HostError(BaseException):
    pass


class HostError_NotANode(HostError):
    pass


class HostError_Connection(HostError):
    pass


class HostError_CompletenessViolated(HostError):
    pass

