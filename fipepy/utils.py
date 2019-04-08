#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import requests
from typing import List
from fipepy.exceptions import FipeAPIError


def _raise_on_failure(
    request: requests.Response, expected_status_code: List[int]
) -> None:
    """Raise FipeAppAPIError if the status code is not as expected."""
    r = request
    exp_code = expected_status_code
    if r.status_code not in expected_status_code:
        raise FipeAPIError(
            f"Status code: {r.status_code} isn't in {exp_code} text: {r.text}"
        )


def year_str_to_int(price: str) -> int:
    """Convert a price in string format to int.

    The format in the online API is R$ XXX.XXX,XX
    """
    if not re.match(r"R\$ (\d{1,3}\.)?\d{1,3}\.\d{3},\d{2}", price):
        raise FipeAPIError(
            f'The price format is supposed to be "R$ XXX.XXX,XX" price:{price}'
        )
    matches = re.findall(r"\d", price)
    if matches:
        return int("".join(matches))
    return 0
