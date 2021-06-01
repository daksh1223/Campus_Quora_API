from django.urls import path
from .views import *
urlpatterns = [
    path('question',QuestionView.as_view(),name="question"),

]
