from django.urls import path

from .views import CarList, CarDetail


urlpatterns = [
    path("api/", CarList.as_view()),
    path("api/<int:pk>/", CarDetail.as_view()),
]