from django.shortcuts import render
from rest_framework.views import APIView
from .models import Community,Question,Answer,Comment
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import datetime
from rest_framework import status
import django.db.utils

# Create your views here.

class QuestionView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        return Response()

    def post(self,request):
        user = request.user
        try:
            # print(request.data["communities"])
            # print(user.community_set.all())
            question = Question(
                title = request.data['title'],
                content = request.data['content'],
                date =  datetime.date.today(),
                user = user,
            )
            comm_list = []
            for x in request.data["communities"]:
                community = Community.objects.get(name= x)
                print(community)
                print(community.users.all())
                if community.users.filter(username = user.username).exists():
                    comm_list.append(community)
                else:
                    return Response({"error": f"{user} not present in {community}"}, status= status.HTTP_401_UNAUTHORIZED)
            question.save()
            try:
                question.communities.add(*comm_list)
                serializer = QuestionSerializer(question)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                question.delete()
                return Response({"error": "Unable to add communities to question!!"}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            print("Exception: ",type(e),e)
            return Response({"error": "Incomplete data!!"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Exception: ",type(e),e)
            return Response({"error": "Question already exists or Server error!!"}, status=status.HTTP_400_BAD_REQUEST)


class AnswerView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,question_id):
        return Response()
    def post(self,request,question_id):
        try:
            question = Question.objects.get(pk=question_id)
            answer,is_created = Answer.objects.get_or_create(
                content=request.data['content'],
                date = datetime.date.today(),
                question = question,
                user = request.user,
            )
            serializer = AnswerSerializer(answer)
            print(answer,is_created)
            if not is_created:
                return Response({"error":"Already exists","data":serializer.data},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except KeyError as e:
            print("Exception: ",type(e),e)
            return Response({"error": "Incomplete data!!"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": ""}, status=status.HTTP_400_BAD_REQUEST)


class CommentView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,question_id):
        return Response()
    def post(self,request,question_id,answer_id):
        try:
            answer = Answer.objects.get(pk=answer_id)
            comment,is_created = Comment.objects.get_or_create(
                content=request.data['content'],
                date = datetime.date.today(),
                answer = answer,
                user = request.user,
            )
            serializer = CommentSerializer(comment)
            print(comment,is_created)
            if not is_created:
                return Response({"error":"Already exists","data":serializer.data},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except KeyError as e:
            print("Exception: ",type(e),e)
            return Response({"error": "Incomplete data!!"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": ""}, status=status.HTTP_400_BAD_REQUEST)

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