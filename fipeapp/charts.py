#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygal
import logging
from logging.config import fileConfig
import os
from .models import Car, Maker
from django.core.exceptions import ObjectDoesNotExist

if os.environ.get("FIPEPY_DEBUG"):
    parent_dir = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-2])
    log_file = f"{parent_dir}{os.path.sep}logging.ini"
    fileConfig(log_file)
log = logging.getLogger("charts")


class PriceChart(object):

    """Pygal PriceChart of a Car. """

    def __init__(self, maker: str, fipe_id: str, **kwargs) -> None:
        """Constructor of PriceChart."""
        self.chart = pygal.Bar(**kwargs)
        self.maker = maker
        self.fipe_id = fipe_id

    def generate(self) -> object:
        """Generate the graph by querying the DB."""
        try:
            maker = Maker.objects.get(name=self.maker)
            cars = Car.objects.filter(maker=maker.id, fipe_id=self.fipe_id).order_by(
                "price"
            )
            x_values, y_values = [], []
            name = ""
            pub_date = ""
            for car in cars:
                name = car.name
                pub_date = car.pub_date
                x_values.append(car.year)
                y_values.append(car.price // 100)
            self.chart.config.title = "Data de publicação: {}".format(
                pub_date.capitalize()
            )
            self.chart.add(name, y_values)
            self.chart.x_labels = x_values
            return self.chart.render(is_unicode=True)
        except ObjectDoesNotExist as e:
            return str(e)
