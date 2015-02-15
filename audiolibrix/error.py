class AudiolibrixError(Exception):
    def __init__(self, message=None, http_body=None, http_status=None):
        super(AudiolibrixError, self).__init__(message)

        self.http_body = http_body
        self.http_status = http_status


class InvalidAuthorizationError(AudiolibrixError):
    pass


class InvalidRequestError(AudiolibrixError):
    pass


class APIError(AudiolibrixError):
    pass


class APIConnectionError(APIError):
    pass


class NotFoundError(APIError):
    pass
