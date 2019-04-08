from django.db import models


class Maker(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __repr__(self) -> str:
        return self.name


class Car(models.Model):
    fipe_id = models.CharField(max_length=20)
    maker = models.ForeignKey(Maker, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    year = models.CharField(max_length=20)
    price = models.IntegerField(default=0)
    currency = models.CharField(max_length=3)
    fuel = models.CharField(max_length=20)
    pub_date = models.CharField(max_length=20)

    def __repr__(self) -> str:
        return self.name
