class Error(Exception):
    code: int
    message: str # Any, really
    def __init__(self, code: int, message):
        if code: self.code = code
        self.message = message

class Success(Error):
    code = 201
    pass
