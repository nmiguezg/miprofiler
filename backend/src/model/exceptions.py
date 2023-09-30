class ProfilerException(Exception):
    def __init__(self, msg) -> None:
        self.msg = msg
        super().__init__(msg)
    def json(self) -> dict:
        return {
            "error":{
                "errorType": self.__class__.__name__.removesuffix("Exception"),
                "message": self.msg
            }
        }

class InputValidationException(ProfilerException):
    pass

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
