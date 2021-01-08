# Audiolibrix Bindings for Python

A Python library for [Audiolibrix](http://www.publixing.com/)'s API v1 (via JSON format) to work with and order audiobooks from their catalogue.

The bindings allow you to:

1.  Get the catalog of all books
2.  Get single book details with links to previews
3.  Create order for multiple books at once
4.  Get download links for given books previously bought by a user

## Setup

Since the documentation to the Audiolibrix service is marked as confidential there is no immediate plan to release this package as open-source. For now, to install the package using `pip`:

	pip install audiolibrix

To install from source, run:

	python setup.py install

To install via `requirements` file from your project, add the following for the moment before updating dependencies:

	git+https://github.com/palosopko/audiolibrix-python.git#egg=audiolibrix

## Usage

First off, you need to require the library and provide authentication information by providing your user handle and shared secret you got from the provider.

	import audiolibrix
	audiolibrix.api_credentials = ('test', '0000000000000000')

**Getting catalogue** is accomplished by calling `audiolibrix.Catalogue.all()` with optional arguments for listing through catalogue and for type of returned items, which can be either `full` (default), `simple` or `price`. The method returns dictionary with book IDs as keys and `audiolibrix.Book` objects as values.

	audiolibrix.Catalogue.all(start=0, max=1, listing_type='full')

When **getting specific book details** you should use the `audiolibrix.Book.get()` method call with book_id as an argument. The method returns `audiolibrix.Book` object.

	audiolibrix.Book.get(1)

For reference, the beforementioned `audiolibrix.Book` object has the following structure (using the `full` listing type when getting the catalogue or when running the `audiolibrix.Book.get()` method directly).

	{
	    'status': 'active',
	    'publisher': {'id': 1, 'name': 'Tympanum'},
	    'is_abridged': False,
	    'description': '...',
	    'language': 'cs',
	    'title': 'Alenka v kraji div\xfa',
	    'abstract': '...',
	    'ean': '8594072279010',
	    'published_on': datetime.datetime(2006, 10, 31, 0, 0),
	    'price': {'currency': 'EUR', 'amount': Decimal('7.2')},
	    'length_in_minutes': 180,
	    'samples': {
	        'mp3': {
	            'links': [{
	                'url': 'http://test.digiapi.com/Sample/1.mp3',
	                'name': 'Alenka v kraji div\xfa'
	            }],
	            'mime_type': 'audio/mpeg',
	            'format': 'MP3'
	        }},
	    'image': {'url': 'http://test.digiapi.com/Image/1.jpg', 'version': 1},
	    'authors': ['Lewis Carroll'],
	    'narrators': [u'Ji\u0159\xed Ornest'],
	    'id': 1
	}

To **create a new order** you need to run `audiolibrix.Order.create()` with list of Audiolibrix's book IDs, your unique order_id and the email address of the buyer as arguments.

	audiolibrix.Order.create(
	    books=[870, 980],
	    order_id=1,
	    user_email='example@example.com'
	)

The method returns `audiolibrix.Order` object which looks the following:

	{
	    'books': [870, 980],
	    'order_id': 1,
	    'user_email': 'example@example.com'
	}

If you would like **to get order details** you call `audiolibrix.Order.get()` with your order ID as the only argument. The method returns dictionary with book IDs as keys and dictionaries with the following attributes:

- `format` - File extension of download links, e.g. "mp3"
- `mime_type` - Mime type of download links, e.g. "audio/mpeg"
- `links` - List of dictionaries with `url` and `filename` attributes

## Contributing

1.  Check for open issues or open a new issue for a feature request or a bug.
2.  Fork the repository and make your changes to the master branch (or branch off of it).
3.  Send a pull request.

## Changelog

### v0.3.2: 08/01/2021

Move over to GitHub and finally drop Python 2 support.

### v0.3.1: 09/10/2019

Send proper JSON to Audiolibrix service.

### v0.3.0: 05/10/2019

Python 3 compatibility and various project formal changes to make everything better.

### v0.2.2: 14/05/2019

Fix raising exception when response from Audiolibrix's API is not a valid JSON.

### v0.2.1: 17/10/2015

When ordering multiple products always order their IDs in an ascending order so that the client application does not have to (otherwise we get `InvalidSignsature` error).

### v0.2.0: 23/08/2015

Version bump with fixes for incorrect URL creating when listing items and stripping whitespace with author handling. API endpoint URL set to Audiolibrix production servers.

### v0.1.0: 15/02/2015

Initial version with support for main API methods with the omission of getting specific user's orders.
