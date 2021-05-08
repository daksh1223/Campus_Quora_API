from django.urls import path, include
from . import views

urlpatterns=[
    path('',views.Category_list.as_view(), name="Categories"),
    path('<int:category_id>/questions/',
         views.Questions.as_view(), name="questions"),
    path('<int:category_id>/questions/<int:question_id>/answers/',
         views.Answers.as_view(), name="answers"),
     
]
