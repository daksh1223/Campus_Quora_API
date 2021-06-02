from django.shortcuts import render
from rest_framework.views import APIView
from .models import Community,Question
from .serializers import CommunitySerializer
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
            print(request.data["communities"])

            print(user.community_set.all())
            question = Question(
                title = request.data['title'],
                content = request.data['content'],
                date =  datetime.date.today(),
                user = user,
            )
            for x in request.data["communities"]:
                community = Community.objects.get(name= x)
                print(community)
                print(community.users.all())
                if community.users.filter(username = user.username).exists():
                    print("Exists")
                    question.communities.add(user.id)
                else:
                    return Response({"error": f"{user} not present in {community}"})
            question.save()
            return Response(question)
        except KeyError as e:
            print("Exception: ",type(e),e)
            return Response({"error": "Incomplete data!!"}, status=status.HTTP_400_BAD_REQUEST)
        # except Exception as e:
        #     print("Exception: ",type(e),e)
        #     return Response({"error": "Question already exists or Server error!!"}, status=status.HTTP_400_BAD_REQUEST)


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