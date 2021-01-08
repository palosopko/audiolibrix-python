from .error import (  # noqa: F401
    APIConnectionError,
    APIError,
    AudiolibrixError,
    InvalidAuthorizationError,
    InvalidRequestError,
    NotFoundError,
)
from .http_client import Requestor  # noqa: F401
from .resource import Book, Catalogue, Order  # noqa: F401
from .version import VERSION  # noqa: F401

# Configuration variables
api_credentials = None
user_agent = ""

API_ENDPOINT = "https://www.digiapi.com/api/merchant/v1/"
