from audiolibrix.http_client import Requestor
from audiolibrix.resource import Book, Catalogue, Order
from audiolibrix.error import AudiolibrixError, APIConnectionError, APIError, \
    InvalidAuthorizationError, InvalidRequestError, NotFoundError

# Configuration variables
api_credentials = None
user_agent = ''

VERSION = '0.1.0'

API_ENDPOINT = 'http://test.digiapi.com/api/merchant/v1/'