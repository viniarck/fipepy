from rest_framework import serializers
from .models import Maker, Car


class MakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maker
        fields = ("name",)


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = (
            "fipe_id",
            "maker",
            "name",
            "year",
            "price",
            "currency",
            "fuel",
            "pub_date",
        )
