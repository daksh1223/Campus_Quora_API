from django.urls import path, include
from . import views

urlpatterns=[
    path('',views.Category_list.as_view(), name="Categories"),
    path('<int:category_id>/questions/',
         views.Questions.as_view(), name="questions"),
    path('<int:category_id>/questions/<int:question_id>/answers/',
         views.Answers.as_view(), name="answers"),
    path('<int:category_id>/questions/<int:question_id>/',
         views.QuestionDetails.as_view(), name="question_details"),
    path('<int:category_id>/questions/<int:question_id>/answers/<int:answer_id>/',
          views.AnswerDetails.as_view(), name="answer_details"),
    path('<int:category_id>/questions/<int:question_id>/answers/<int:answer_id>/comments/',
          views.Comments.as_view(), name="comments"),
    path('<int:category_id>/questions/<int:question_id>/answers/<int:answer_id>/comments/<int:comment_id>/',
          views.CommentDetails.as_view(), name="comment_details"),
    path('<int:category_id>/questions/<int:question_id>/answers/<int:answer_id>/likes/',
          views.Likes.as_view(), name="likes"),
    
]
