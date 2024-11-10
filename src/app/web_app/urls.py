from django.urls import path, include, re_path
from . import views

urlpatterns = [
    re_path(r'^api/v1/persons$', views.web_app),
    re_path(r'^api/v1/persons/([0-9]+)$', views.web_app),
]