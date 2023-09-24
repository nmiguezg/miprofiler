class NotSupportedAlgorithmException(Exception):
    def __init__(self, algoritmo):
        mensaje = f"El algoritmo de perfilado seleccionado no está disponible: {algoritmo}"
        super().__init__(mensaje)


class InvalidFileException(Exception):
    def __init__(self, msg, *args: object) -> None:
        self.msg = msg
        super().__init__(msg, *args)


class ServerNotAvailableException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ServerTimeoutException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InstanceNotFoundException(Exception):
    def __init__(self, msg, *args: object) -> None:
        self.msg = msg
        super().__init__(msg, *args)