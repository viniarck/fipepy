#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fipepy.utils import year_str_to_int


class TestUtils(object):

    """docstring for TestUtils. """

    def test_year_str_to_int(self) -> None:
        """docstring."""
        values = [
            ("R$ 7.345,00", 7_345_00),
            ("R$ 10.000,00", 1_000_000),
            ("R$ 1.123.456,00", 112_345_600),
            ("R$ 999.123.100,00", 99_912_310_000),
        ]
        for args in values:
            price, expected = args[0], args[1]
            assert year_str_to_int(price) == expected
