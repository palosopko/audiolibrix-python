import audiolibrix
import hmac
import requests

from hashlib import sha256


class Auth:
    def __init__(self):
        if (
            not isinstance(audiolibrix.api_credentials, tuple)
            or len(audiolibrix.api_credentials) != 2
        ):
            raise audiolibrix.error.APIError(
                "Invalid credentials to Audiolibrix service provided (expected "
                "two-part tuple with `client_id` and `shared_secret`)."
            )

    def sign(self, message):
        return (
            hmac.new(
                audiolibrix.api_credentials[1].encode("utf-8"),
                message.encode("utf-8"),
                sha256,
            )
            .hexdigest()
            .upper()
        )


class Requestor:
    def request(
        self, url, data=[], params=[], method="GET", signature_base=""
    ):
        headers = {
            "x-merchantapi-merchant": audiolibrix.api_credentials[0],
            "User-Agent": "audiolibrix-python/" + audiolibrix.VERSION,
            "Accept": "application/json",
        }

        if method.upper() == "POST":
            headers["Content-Type"] = "application/json"

            if signature_base != "":
                data["Signature"] = Auth().sign(signature_base)
        elif method.upper() == "GET":
            if signature_base != "":
                params["signature"] = Auth().sign(signature_base)
        try:
            response = requests.request(
                method=method,
                url=audiolibrix.API_ENDPOINT + url,
                headers=headers,
                json=data,
                params=params,
                timeout=60,
            )
        except Exception as e:
            self._handle_request_error(e)

        try:
            data = response.json()
        except ValueError:
            raise audiolibrix.error.APIError(
                "Improperly structured JSON that cannot be read: %s "
                "(HTTP status code %s)"
                % (response.text, response.status_code),
                response.text,
            )

        try:
            items = data["data"]
        except (KeyError, TypeError):
            try:
                error = data["error"]
            except (KeyError):
                raise audiolibrix.error.APIError(
                    "Invalid error response object from API: %s"
                    % response.text,
                    response.text,
                )

            if error["id"] == "InvalidSignature":
                raise audiolibrix.error.InvalidRequestError(
                    "Incorrect signature", response.text
                )
            elif error["id"] == "UnknownMerchant":
                raise audiolibrix.error.InvalidAuthorizationError(
                    "Authorization information incorrect or missing",
                    response.text,
                )
            elif error["id"] == "NotFound":
                raise audiolibrix.error.NotFoundError(
                    "Requested item not found or does not exist", response.text
                )
            elif error["id"] == "NoItems":
                raise audiolibrix.error.InvalidRequestError(
                    "No items to be bought", response.text
                )
            elif error["id"] == "InvalidEmail":
                raise audiolibrix.error.InvalidRequestError(
                    "Buyer's e-mail address invalid or missing", response.text
                )
            elif error["id"] == "InvalidOrderId":
                raise audiolibrix.error.InvalidRequestError(
                    "Merchant's e-mail address invalid or missing",
                    response.text,
                )
            elif error["id"] == "ItemsNotFound":
                raise audiolibrix.error.InvalidRequestError(
                    "Following items are not found: %s"
                    % ", ".join([str(item) for item in error["items"]]),
                    response.text,
                )
            elif error["id"] == "ItemsNotForSale":
                raise audiolibrix.error.InvalidRequestError(
                    "Following items are not for sale: %s"
                    % ", ".join([str(item) for item in error["items"]]),
                    response.text,
                )
            elif error["id"] == "OrderMismatch":
                raise audiolibrix.error.InvalidRequestError(
                    "Order with the same merchant identifier already exists, but "
                    "contains different items: %s"
                    % ", ".join([str(item) for item in error["items"]]),
                    response.text,
                )
            elif error["id"] == "OrderNotFound":
                raise audiolibrix.error.NotFoundError(
                    "Order not found or does not exist", response.text
                )
            else:
                raise audiolibrix.error.APIError(
                    "Unknown error occurred, try again later", response.text
                )

        return items

    def _handle_request_error(self, e):
        if isinstance(e, requests.exceptions.RequestException):
            err = "%s: %s" % (type(e).__name__, str(e))
        else:
            err = "A %s was raised" % (type(e).__name__,)

            if str(e):
                err += " with error message %s" % (str(e),)
            else:
                err += " with no error message"

        msg = "Network error: %s" % (err,)

        raise audiolibrix.error.APIConnectionError(msg)
