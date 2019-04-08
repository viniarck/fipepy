from django.urls import path
from rest_framework_swagger.views import get_swagger_view
from . import views

schema_view = get_swagger_view(title='Fipepy API')

urlpatterns = [
    # swagger docs
    path('', schema_view),
    # makers/
    path("makers/", views.MakersList.as_view()),
    # makers/<maker_name>
    path("makers/<str:maker_name>/cars/", views.CarsList.as_view()),
    # makers/<maker_name>/cars/<fipe_id>
    path("makers/<str:maker_name>/cars/<str:fipe_id>", views.CarDetail.as_view()),
    # makers/<maker_name>/cars/<fipe_id>/chart
    path("makers/<str:maker_name>/cars/<str:fipe_id>/chart", views.IndexView.as_view()),
]
