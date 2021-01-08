import audiolibrix

from decimal import Decimal
from datetime import datetime

from .error import APIError, InvalidRequestError


class Book:
    def __init__(self, data={}):
        if data.get("forSale", False):
            self.status = "active"
        else:
            self.status = "inactive"

        self.id = int(data.get("id"))
        self.ean = data.get("ean")
        self.title = data.get("name")
        self.abstract = data.get("info", "")
        self.description = data.get("detail", "")
        self.language = data["language"]["id"] if data.get("language") else []
        self.is_abridged = data.get("abridged", False)

        self.image = data.get("image", None)

        try:
            self.published_on = datetime.strptime(
                data.get("issueDate", None), "%Y-%m-%dT%H:%M:%S"
            )
        except ValueError:
            self.published_on = None

        self.narrators = []

        for narrator in data.get("narrators", []):
            self.narrators.append(narrator["fullName"].strip())

        self.authors = []

        for author in data.get("authors", []):
            self.authors.append(author["fullName"].strip())

        if data.get("price"):
            self.price = {
                "amount": Decimal(data["price"].get("amount", 0.0)).quantize(
                    Decimal("0.01")
                ),
                "currency": data["price"].get("code"),
            }
        else:
            self.price = {}

        if data.get("publisher"):
            self.publisher = {
                "id": data["publisher"].get("id"),
                "name": data["publisher"].get("name"),
            }
        else:
            self.publisher = {}

        if data.get("length"):
            self.length_in_minutes = int(data["length"].get("minutes", 0))

        self.samples = {}

        for sample in data.get("samples", []):
            self.samples[sample.get("id", "mp3").lower()] = {
                "format": sample.get("id", "MP3"),
                "mime_type": sample.get("mimeType", "audio/mpeg"),
                "links": sample.get("links", []),
            }

    @classmethod
    def get(cls, book_id):
        if not isinstance(book_id, int):
            raise InvalidRequestError(
                "Invalid value '%s' for book identifier. "
                "It has to be of type 'int'.",
                book_id,
            )

        client = audiolibrix.http_client.Requestor()
        response = client.request(url="item/" + str(book_id))

        try:
            item = response["item"]
        except (KeyError, TypeError):
            raise APIError(
                "Invalid response object from API, 'item' key missing",
                response.text,
            )

        return Book(item)


class Catalogue:
    ALLOWED_LISTING_TYPES = ["full", "simple", "price"]

    @classmethod
    def all(cls, start=None, max=None, listing_type="full"):
        if listing_type not in cls.ALLOWED_LISTING_TYPES:
            raise InvalidRequestError(
                "Invalid value '%s' for request attribute 'type'. "
                "Alowed values are %s.",
                listing_type,
                ", ".join(cls.ALLOWED_LISTING_TYPES),
            )

        params = {}

        if isinstance(start, int) and start >= 0:
            params["start"] = start

        if isinstance(max, int) and max > 0:
            params["max"] = max

        client = audiolibrix.http_client.Requestor()
        response = client.request(url="items/" + listing_type, params=params)

        try:
            items = response["items"]
        except (KeyError, TypeError):
            raise APIError(
                "Invalid response object from API, 'items' key missing",
                response.text,
            )

        books = {}

        for book in items:
            books[int(book["id"])] = Book(book)

        return books


class Order:
    def __init__(self, data={}):
        self.user_email = data.get("buyerEmail")
        self.order_id = data.get("merchantOrderId")
        self.books = [int(book_id) for book_id in data.get("items", [])]

    @classmethod
    def create(cls, books, order_id, user_email):
        data = {
            "BuyerEmail": user_email,
            "MerchantOrderId": order_id,
            "Items": [
                book_id for book_id in books if isinstance(book_id, int)
            ],
        }

        signature_base = "%s|%s|%s" % (
            user_email,
            order_id,
            ",".join(str(book_id) for book_id in sorted(data["Items"])),
        )

        client = audiolibrix.http_client.Requestor()
        response = client.request(
            url="order",
            method="POST",
            data=data,
            signature_base=signature_base,
        )

        try:
            order = response["order"]
        except (KeyError, TypeError):
            raise APIError(
                "Invalid response object from API, 'order' key missing",
                response.text,
            )

        return Order(order)

    @classmethod
    def get(cls, order_id):
        client = audiolibrix.http_client.Requestor()
        response = client.request(
            url="orderdetails",
            method="GET",
            params={"merchantOrderId": order_id},
            signature_base=str(order_id),
        )

        try:
            order = response["order"]
        except (KeyError, TypeError):
            raise APIError(
                "Invalid response object from API, 'order' key missing",
                response.text,
            )

        items = order.get("downloadLinks", [])
        download_links = {}

        for book in items:
            formats = book.get("formats", [])

            if len(formats) == 0:
                continue

            download_links[book["itemId"]] = []

            for format in book["formats"]:
                links = []
                for link in format["links"]:
                    links.append(
                        {"file_name": link["name"], "url": link["url"]}
                    )

                if format["mimeType"] == "application/mpeg":
                    mime_type = "audio/mpeg"
                else:
                    mime_type = format["mimeType"]

                download_links[book["itemId"]].append(
                    {
                        "format": format["id"].lower(),
                        "mime_type": mime_type,
                        "links": links,
                    }
                )

        return download_links
