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
        if len(request.data['question']):
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
        return Response(serializer.data)

    def post(self, request,question_id,category_id):
        if len(request.data['post']) :
            question = Question.objects.get(pk=question_id)
            post = Post.objects.create(post=request.data['post'],writer = request.user)
            question.post.add(post)
            serializer = Answer_serializer(post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "No post provided!!"}, status=status.HTTP_400_BAD_REQUEST)
    
        
