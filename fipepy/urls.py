"""fipepy URL Configuration."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # /fipeapp/
    path("fipe/v1/", include("fipeapp.urls")),
]
