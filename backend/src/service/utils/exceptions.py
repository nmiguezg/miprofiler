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