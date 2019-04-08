#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fipepy.client import FipeAPI
import pytest


@pytest.fixture(scope="module")
def fipe_api() -> FipeAPI:
    """Get Fipe API."""
    return FipeAPI()


class TestFipeAPI(object):

    """docstring for TestFilpeAPI. """

    def test_fetch_makers(self, fipe_api: FipeAPI) -> None:
        """Test fetching makers."""
        makers = fipe_api.fetch_makers()
        assert len(makers)
        for maker in ["audi", "subaru", "volkswagen"]:
            assert maker in makers

    def test_fetch_cars(self, fipe_api: FipeAPI) -> None:
        """Test fetching cars from a maker."""
        models = fipe_api.fetch_cars(maker="audi")
        assert len(models)
