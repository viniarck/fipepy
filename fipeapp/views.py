from rest_framework.response import Response
from rest_framework import status
from .models import Maker, Car
from .serializers import MakerSerializer, CarSerializer
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
import json
from django.views.generic import TemplateView
from pygal.style import BlueStyle
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.schemas import SchemaGenerator
from rest_framework_swagger import renderers


from .charts import PriceChart


class MakersList(APIView):
    authentication_classes = (BasicAuthentication,)

    """Makers APIView. """

    def get(self, request, format=None) -> Response:
        makers = Maker.objects.all().order_by("name")
        serializer = MakerSerializer(makers, many=True)
        return Response(serializer.data)

    def put(self, request, format=None) -> Response:
        if str(request.user) == "AnonymousUser":
            return Response(
                {"detail": "AnonymousUser isn't authorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            serializer = MakerSerializer(data=json.loads(request.data))
            name = serializer.initial_data.get("name")
            if Maker.objects.get(name=name):
                return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        if str(request.user) == "AnonymousUser":
            return Response(
                {"detail": "AnonymousUser isn't authorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        makers = Maker.objects.all()
        for maker in makers:
            maker.delete()
        return Response(status=status.HTTP_200_OK)


class CarDetail(APIView):

    """Car Detailed View."""

    def get(self, request, maker_name: str, fipe_id: str) -> Response:
        try:
            maker = Maker.objects.get(name=maker_name)
            cars = Car.objects.filter(maker=maker.id, fipe_id=fipe_id)
            serializer = CarSerializer(cars, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CarsList(APIView):

    """CarsList View. """

    def get(self, request, maker_name, format=None) -> Response:
        try:
            maker = Maker.objects.get(name=maker_name)
            cars = Car.objects.filter(maker=maker.id).order_by("name")
            serializer = CarSerializer(cars, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(json.dumps([]), status=status.HTTP_200_OK)

    def put(self, request, maker_name, format=None) -> Response:
        if str(request.user) == "AnonymousUser":
            return Response(
                {"detail": "AnonymousUser isn't authorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        maker, created = Maker.objects.get_or_create(name=maker_name)
        if created:
            maker.save()
        try:
            data = dict(json.loads(request.data))
            data["maker"] = maker.id
            serializer = CarSerializer(data=data)
            if serializer.is_valid():
                car, car_created = Car.objects.get_or_create(
                    fipe_id=serializer.validated_data["fipe_id"],
                    maker=maker,
                    name=serializer.validated_data["name"],
                    year=serializer.validated_data["year"],
                    price=serializer.validated_data["price"],
                    currency=serializer.validated_data["currency"],
                    fuel=serializer.validated_data["fuel"],
                    pub_date=serializer.validated_data["pub_date"],
                )
                car.save()
                if car_created:
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, maker_name, format=None) -> Response:
        if str(request.user) == "AnonymousUser":
            return Response(
                {"detail": "AnonymousUser isn't authorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            maker = Maker.objects.get(name=maker_name)
            maker.delete()
            cars = Car.objects.filter(maker=maker.id)
            for car in cars:
                car.delete()
            return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response(f"{str(e)}", status=status.HTTP_400_BAD_REQUEST)


class IndexView(TemplateView):
    template_name = "fipeapp/pygal.html"

    def get_context_data(self, maker_name: str, fipe_id: str, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        cht = PriceChart(
            maker_name,
            fipe_id,
            title="Preco em R$ x Ano",
            height=800,
            width=1000,
            x_title="Ano",
            y_title="Preço em R$ (BRL)",
            style=BlueStyle,
            explicit_size=True,
            legend_at_bottom=True,
        )
        res = cht.generate()
        context["cht"] = res
        return context


class SwaggerSchemaView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer]

    def get(self, request):
        generator = SchemaGenerator()
        schema = generator.get_schema(request=request)

        return Response(schema)
