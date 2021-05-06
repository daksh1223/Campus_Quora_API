from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.MicrosoftView.as_view(), name="msauth"),
]
