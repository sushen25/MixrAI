from django.urls import path

from mixr import views

urlpatterns = [
    path("", views.index, name="index"),
]