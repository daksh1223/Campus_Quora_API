from django.urls import path
from .views import *
urlpatterns = [
    path('question',QuestionView.as_view(),name="question"),
    path('question/<int:question_id>/answer',AnswerView.as_view(),name="answer"),
    path('question/<int:question_id>/answer/<int:answer_id>/comment',CommentView.as_view(),name="comment"),
]
