# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import pytest
import audiolibrix

from audiolibrix import APIError
from audiolibrix.http_client import Auth


class TestAuth(object):
    def test_invalid_auth_instantiation_with_no_credentials(self):
        with pytest.raises(APIError):
            audiolibrix.api_credentials = None
            Auth()

    def test_invalid_auth_instantiation_with_empty_credentials(self):
        with pytest.raises(APIError):
            audiolibrix.api_credentials = ()
            Auth()

    def test_invalid_auth_instantiation_with_incomplete_credentials(self):
        with pytest.raises(APIError):
            audiolibrix.api_credentials = ("client_id",)
            Auth()

    def test_signing_unicode_message(self):
        audiolibrix.api_credentials = ("client_id", "client_secret")
        auth = Auth()
        signature = auth.sign(u"ORD123/$Čx")
        assert (
            signature
            == "DCC3674794089482A4549BF8A313AF038003267021E7B9D37067B47D000D893C"
        )
