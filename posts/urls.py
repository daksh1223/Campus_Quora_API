from django.urls import path
from .views import *
urlpatterns = [
    path('question/', QuestionView.as_view(), name="add_question"),
    path('question/<int:question_id>',
         ParticularQuestionView.as_view(), name="question"),
    path('question/<int:question_id>/answer',
         AnswerView.as_view(), name="answer"),
    path('answer/<int:answer_id>/comments/',
         CommentView.as_view(), name="comment"),
    path('community/',
         CommunityView.as_view(), name="category"),
    path('community/<int:community_id>/',
         ParticularCommunityView.as_view(), name="category"),
    path('answer/<int:answer_id>/',
         ParticularAnswerView.as_view(), name="particular_answer"),
    path('comment/<int:comment_id>/',
         ParticularCommentView.as_view(), name="particular_comment"),
   


]
