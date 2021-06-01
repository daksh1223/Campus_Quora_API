from django.shortcuts import render
from rest_framework.views import APIView
from .models import Community,Question
from .serializers import CommunitySerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import datetime
from rest_framework import status

# Create your views here.

class QuestionView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        return Response()

    def post(self,request):
        print("data",request.data)
        print("user",type(request.user),request.user)
        try:
            print(request.data["communities"])
            question = Question.objects.create(
                title = request.data['title'],
                content = request.data['content'],
                date =  datetime.date.today(),
                user = request.user,
            )
        except KeyError:
            return Response({"error": "Incomplete data!!"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(question)

# class TagList(APIView):
#     #  permission_classes = (IsAuthenticated,)  

#      def get(self,request):      
#         tags = Tag.objects.all()
#         serializer = TagSerializer(tags,many=True)
#         print("print -",serializer,type(serializer))
#         return Response(serializer.data)

# class TagDetail(APIView):
#     def get(self,request,tag_id):
#         queryset = Tag.objects.get(pk=tag_id).question_set.all()
#         print(type(queryset),queryset)
#         # questions = Question.objects.filter(tag__id = tag_id)
#         # print(questions)
#         return Response()