#!/usr/bin/env python
# -*- coding: utf-8 -*-


class FipeAPIError(Exception):
    def __init__(self, msg) -> None:
        """Constructor of FipeAPIError."""
        super().__init__(msg)
