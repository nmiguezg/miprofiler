from service.utils.exceptions import ProfilerException


class NotSupportedAlgorithmException(ProfilerException):
    def __init__(self, algoritmo):
        mensaje = f"El algoritmo de perfilado seleccionado no está disponible: {algoritmo}"
        super().__init__(mensaje)


class InvalidFileException(ProfilerException):
    pass


class ServerNotAvailableException(ProfilerException):
    pass


class ServerTimeoutException(ProfilerException):
    pass


class InstanceNotFoundException(ProfilerException):
    pass
