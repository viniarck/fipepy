#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import datetime
from typing import List, Dict, Union, Tuple
from collections import namedtuple
import fire
import json
import os
import time
import logging
from logging.config import fileConfig
from fipepy.utils import _raise_on_failure, year_str_to_int
from fipepy.exceptions import FipeAPIError
from fipepy.version import __version__

if os.environ.get("FIPEPY_DEBUG"):
    parent_dir = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-2])
    log_file = f"{parent_dir}{os.path.sep}logging.ini"
    fileConfig(log_file)
log = logging.getLogger("client")

Car = namedtuple("Car", "fipe_id maker name year price currency fuel pub_date")

Maker = namedtuple("Maker", "name")


class FipeAPI(object):

    """Abstraction to interface with Fipe API over HTTP."""

    def __init__(self) -> None:
        """Constructor of FipeAPI."""
        self._makers: Dict[str, int] = {}
        self._cars: Dict[str, Dict[str, int]] = {}
        self._maker_url = "http://fipeapi.appspot.com/api/1/carros/marcas.json"
        self._cars_url = "http://fipeapi.appspot.com/api/1/carros/veiculos/{}.json"
        self._car_url = "http://fipeapi.appspot.com/api/1/carros/veiculo/{}/{}.json"
        self._car_model_url = (
            "http://fipeapi.appspot.com/api/1/carros/veiculo/{}/{}/{}.json"
        )

    def fetch_makers(self) -> List[str]:
        """Fetch all makers from the API."""
        r = requests.get(self._maker_url)
        _raise_on_failure(r, [200])
        for item in r.json():
            self._makers[item["name"].lower()] = item["id"]
        if not len(self._makers):
            raise FipeAPIError(f"{self._maker_url} didn't return any values.")
        return list(self._makers.keys())

    def fetch_cars(self, maker: str) -> List[str]:
        """Fetch all cars from a maker."""
        if not self._makers:
            self.fetch_makers()
        maker_id = self._makers.get(maker)
        if not maker_id:
            raise FipeAPIError(f"Inexistent maker: {maker}")
        url = self._cars_url.format(maker_id)
        r = requests.get(url)
        _raise_on_failure(r, [200])
        self._cars[maker] = {}
        for item in r.json():
            car_name = item["name"].lower()
            self._cars[maker][car_name] = item["id"]
        if not len(self._cars[maker]):
            raise FipeAPIError(f"{url} didn't return any values.")
        return list(self._cars[maker].keys())

    def fetch_car(self, maker: str, name: str, year: str = "") -> List[Car]:
        """Fetch a car of a maker."""
        if not self._makers:
            self.fetch_cars(maker)
        maker_id = self._makers.get(maker)
        if not maker_id:
            raise FipeAPIError(f"Inexistent maker: {maker}")
        car_id = None
        try:
            car_id = self._cars[maker][name]
        except KeyError:
            raise FipeAPIError(f"Inexistent car: {name}")
        r = requests.get(self._car_url.format(maker_id, car_id))
        _raise_on_failure(r, [200])
        models = {}
        for item in r.json():
            key = item["id"]
            year_ = key.split("-")[0]
            if year_ == "32000":
                year_ = f"{datetime.datetime.now().year} (zero KM)"
            models[year_] = key
        if year:
            models = {year: models[year]}
        list_models = []
        for k, v in models.items():
            url = self._car_model_url.format(maker_id, car_id, v)
            r = requests.get(url)
            log.debug(f"getting url {url}")
            # This sleep is needed due to the limit of requests per sec of the API.
            time.sleep(2)
            _raise_on_failure(r, [200, 201])
            resp = r.json()
            if resp["ano_modelo"] == "32000":
                resp["ano_modelo"] = f"{datetime.datetime.now().year} (zero KM)"
            list_models.append(
                Car(
                    fipe_id=resp["fipe_codigo"],
                    name=resp["name"].lower(),
                    maker=maker,
                    year=resp["ano_modelo"],
                    price=year_str_to_int(resp["preco"]),
                    currency="BRL",
                    fuel=resp["combustivel"],
                    pub_date=resp["referencia"],
                )
            )
        return list_models

    def __getitem__(self, name) -> Union[int, None]:
        return self._makers.get(name)

    def __iter__(self) -> Union[None, Tuple[str, int]]:
        for k, v in self._makers.items():
            yield k, v


class FipepyAPI(FipeAPI):

    """Abastraction to interface with FipeApp API over HTTP"""

    def __init__(self, host="localhost", port="8000") -> None:
        super().__init__()
        """Constructor of FipeAppAPI."""
        self._host = os.environ.get("FIPEPY_HOST") or host
        self._port = os.environ.get("FIPEPY_PORT") or port
        self._endpoint = "fipe/v1/"
        self._url = f"http://{self._host}:{self._port}/{self._endpoint}"
        self._user = os.environ.get("FIPEPY_USER", "AnonymousUser")
        self._password = os.environ.get("FIPEPY_PASSWORD", "")

    def update_makers(self, endpoint="makers/") -> None:
        """Update all makers through the REST API."""
        session = requests.Session()
        session.auth = (self._user, self._password)
        for maker in self.fetch_makers():
            named_maker = Maker(name=maker)
            r = session.put(
                self._url + endpoint, json=json.dumps(named_maker._asdict())
            )
            log.debug(f"Updating maker {maker} status {r.status_code}")
            _raise_on_failure(r, [200, 201])

    def update_cars(self, maker: str = "", endpoint="makers/{}/cars/") -> None:
        makers: List[str] = []
        if maker:
            makers.append(maker)
        else:
            if not self._makers:
                self.fetch_makers()
            makers.extend(self._makers.keys())
        session = requests.Session()
        session.auth = (self._user, self._password)
        for maker in makers:
            cars = self.fetch_cars(maker)
            for car in cars:
                models = self.fetch_car(maker, car)
                for model in models:
                    r = session.put(
                        self._url + endpoint.format(maker),
                        json=json.dumps(model._asdict()),
                    )
                    log.debug(f"posted car {model}, status {r.status_code}")
                    _raise_on_failure(r, [200, 201])
            return


class API(FipepyAPI):

    """Abstraction to interface with both APIs"""

    def __init__(self) -> None:
        """Constructor of API."""
        super().__init__()

    def version(self) -> str:
        """Show current version."""
        return __version__


def main() -> None:
    """Main function."""
    fire.Fire(API())


if __name__ == "__main__":
    main()
