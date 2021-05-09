from django.db.models.query_utils import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  
from rest_framework import status
from .models import *
from .serializers import *
# Create your views here.
class Category_list(APIView):
     permission_classes = (IsAuthenticated,)  

     def get(self,request):      
        queryset=Category.objects.all()
        serializer = Category_serializer(queryset,many=True)
        return Response(serializer.data)


class Questions(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, category_id):
        category = Category.objects.get(pk=category_id)
        queryset = category.questions.all()
        serializer = Question_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request,category_id):
        category = Category.objects.get(pk=category_id)
        if 'question' in request.data and len(request.data['question']):
            question = Question.objects.create(user = request.user,  question = request.data['question'])
            category.questions.add(question)
            serializer = Question_serializer(question)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error":"No question provided!!"}, status=status.HTTP_400_BAD_REQUEST)
    
        

class Answers(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,question_id, category_id):
        question = Question.objects.get(pk=question_id)
        queryset = question.post.all()
        serializer = Answer_serializer(queryset, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request,question_id,category_id):
        if 'post' in request.data and len(request.data['post']) :
            question = Question.objects.get(pk=question_id)
            post = Post.objects.create(post=request.data['post'],writer = request.user)
            question.post.add(post)
            serializer = Answer_serializer(post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "No post provided!!"}, status=status.HTTP_400_BAD_REQUEST)

class QuestionDetails(APIView):
     permission_classes=(IsAuthenticated,)

     def get(self,request,question_id,category_id):
          question = Question.objects.get(pk=question_id)
          serializer = Question_serializer(question)
          return Response(serializer.data)
     
     def put(self,request,question_id,category_id):
       question=Question.objects.get(pk=question_id)
       if question.user==request.user:         
          if 'question' in request.data and len(request.data['question']):
               question.question=request.data['question']
               question.save()
               serializer=Question_serializer(question)
               return Response(serializer.data,status=status.HTTP_200_OK)
          return Response({"error": "No value provided !!"}, status=status.HTTP_400_BAD_REQUEST)
       else:
            return Response({"error":"Permission Denied!"}, status=status.HTTP_400_BAD_REQUEST)

     def delete(self,request,question_id,category_id):   
      question=Question.objects.get(pk=question_id)
      if question.user==request.user:
          question.delete()
          return Response({"Message":"Successfully Deleted!"}, status=status.HTTP_200_OK)
      else:
          return Response({"error":"Permission Denied!"}, status=status.HTTP_400_BAD_REQUEST)
       

class AnswerDetails(APIView):
     permission_classes=(IsAuthenticated,)

     def get(self,request,answer_id,question_id, category_id):
        answer=Post.objects.get(pk=answer_id)
        serializer = Answer_serializer(answer)
        return Response(serializer.data,status=status.HTTP_200_OK)

     def post(self, request,answer_id,question_id,category_id):
          if 'comment' in request.data and len(request.data['comment']):
               answer=Post.objects.get(pk=answer_id)
               comment=Comment.objects.create(user=request.user,comment=request.data['comment'])
               answer.comment.add(comment)
               serializer=Answer_serializer(answer)
               return Response(serializer.data,status=status.HTTP_201_CREATED)
          return Response({"error":"No value Provided!"},status=status.HTTP_400_BAD_REQUEST)

     def put(self, request,answer_id,question_id,category_id):
        answer=Post.objects.get(pk=answer_id)
        if 'post' in request.data and len(request.data['post']) :
          if answer.writer==request.user:  
            answer.post=request.data['post']
            answer.save()
            serializer = Answer_serializer(answer)
            return Response(serializer.data, status=status.HTTP_200_OK)
          else:
               return Response({"error":"Permission Denied!"}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'like' in request.data:
             user=request.user
             if(user not in answer.like.all()):
                  answer.like.add(user)
                  serializer=Answer_serializer(answer)
                  return Response(serializer.data, status= status.HTTP_200_OK)
             else:
                  return Response({"error":"User has already liked the post once!"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "No value provided!!"}, status=status.HTTP_400_BAD_REQUEST)
     
     def delete(self,request,answer_id,question_id,category_id):
       answer=Post.objects.get(pk=answer_id)   
       if answer.writer==request.user:  
          answer.delete()
          return Response({"Message":"Successfully Deleted!"}, status=status.HTTP_200_OK)
       else:
          return Response({"error":"Permission Denied!"}, status=status.HTTP_400_BAD_REQUEST)
        
  

        
