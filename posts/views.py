from django.http import response
from django.shortcuts import render
from rest_framework.views import APIView
from .models import Community, Question, Answer, Comment
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import datetime
import json
from rest_framework import status
import django.db.utils

# Create your views here.


class ParticularQuestionView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, question_id):
        try:
            question = Question.objects.get(pk=question_id)
            response = QuestionSerializer(question)
            return Response(response.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": f"question with id : {question_id} does not exist "}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, question_id):
        try:
            question = Question.objects.get(pk=question_id)
            if question.user == request.user:
                question.delete()
                return Response({"message": "succesfully deleted"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({"error": f"question with id : {question_id} does not exist "}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, question_id):
        try:
            user = request.user
            question = Question.objects.get(pk=question_id)
            if question.user == user:
                response = QuestionSerializer(question)
                question.title = request.data['title']
                question.content = request.data['content']
                comm_list = []
                for x in request.data["communities"]:
                    # print("----------------",x)
                    print(Community.objects.all())
                    community = Community.objects.get(name=x)
                    if community.users.filter(username=user.username).exists():
                        comm_list.append(community)
                    else:
                        return Response({"error": f"{user} not present in {community}"}, status=status.HTTP_401_UNAUTHORIZED)
                question.communities.add(*comm_list)
                question.save()
                return Response(response.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({"error": f"question with id : {question_id} does not exist "}, status=status.HTTP_400_BAD_REQUEST)


class ParticularAnswerView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, answer_id):
        try:
            answer = Answer.objects.get(pk=answer_id)
            response = AnswerSerializer(answer)
            return Response(response.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": f"answer with id : {answer_id} does not exist "}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, answer_id):

        try:

            answer = Answer.objects.get(pk=answer_id)
            if request.user == answer.user:
                answer.delete()
                return Response({"message": "succesfully deleted"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED)

        except:
            return Response({"error": f"answer with id : {answer_id} does not exist "}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, answer_id):

        try:

            answer = Answer.objects.get(pk=answer_id)
            if request.user == answer.user:
                answer.content = request.data['content']
                answer.date = datetime.date.today()
                answer.save()
                response = AnswerSerializer(answer)
                return Response(response.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED)

        except:
            return Response({"error": f"answer with id : {answer_id} does not exist "}, status=status.HTTP_400_BAD_REQUEST)


class ParticularCommentView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, reuqest, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
            response = CommentSerializer(comment)
            return Response(response.data,status=status.HTTP_200_OK)
        except:
            return Response({"error": f"comment with id : {comment_id} does not exist "}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
            if comment.user==request.user:
             comment.delete()
             return Response({"message": "succesfully deleted"}, status=status.HTTP_200_OK)
            else :
             return Response({"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        except:
             return Response({"error": f"comment with id : {comment_id} does not exist "}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
            if comment.user == request.user:
             comment.content=request.data['content']
             comment.date = datetime.date.today()
             comment.save()
             response=CommentSerializer(comment)
             return Response(response.data, status=status.HTTP_200_OK)
            else:
             return Response({"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({"error": f"comment with id : {comment_id} does not exist "}, status=status.HTTP_400_BAD_REQUEST)


class ParticularCommunityView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, community_id):
        try:
            community = Community.objects.get(pk=community_id)
            questions = Question.objects.filter(communities=community)
            response = QuestionSerializer(questions, many=True)
            return Response(response.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": f"Community with id : {community_id} does not exist "}, status=status.HTTP_400_BAD_REQUEST)


class QuestionView(APIView):
    permission_classes = (IsAuthenticated,)


    def post(self, request):
        user = request.user
        try:
            question = Question(
                title=request.data['title'],
                content=request.data['content'],
                date=datetime.date.today(),
                user=user,
            )
            comm_list = []
            for x in request.data["communities"]:
                print(Community.objects.all())
                community = Community.objects.get(name=x)
                if community.users.filter(username=user.username).exists():
                    comm_list.append(community)
                else:
                    return Response({"error": f"{user} not present in {community}"}, status=status.HTTP_401_UNAUTHORIZED)
            question.save()
            try:
                question.communities.add(*comm_list)
                serializer = QuestionSerializer(question)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                question.delete()
                return Response({"error": "Unable to add communities to question!!"}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            # print("Exception: ", type(e), e)
            return Response({"error": "Incomplete data!!"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # print("Exception: ", type(e), e)
            return Response({"error": "Question already exists or Server error!!"}, status=status.HTTP_400_BAD_REQUEST)


class AnswerView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, question_id):
        try:
            question = Question.objects.get(pk=question_id)
            print(question)
            answer = Answer.objects.filter(question=question)
            response = AnswerSerializer(answer, many=True)
            return Response(response.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": f"question with id : {question_id} does not exist "}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, question_id):
        try:
            question = Question.objects.get(pk=question_id)
            answer, is_created = Answer.objects.get_or_create(
                content=request.data['content'],
                date=datetime.date.today(),
                question=question,
                user=request.user,
            )
            serializer = AnswerSerializer(answer)
            print(answer, is_created)
            if not is_created:
                return Response({"error": "Already exists", "data": serializer.data}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except KeyError as e:
            print("Exception: ", type(e), e)
            return Response({"error": "Incomplete data!!"}, status=status.HTTP_400_BAD_REQUEST)
        # return Response({"error": ""}, status=status.HTTP_400_BAD_REQUEST)


class CommentView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, answer_id):
        try:
            answer = Answer.objects.get(pk=answer_id)
            comments = Comment.objects.filter(answer=answer)
            response = CommentSerializer(comments, many=True)
            return Response(response.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": f"Answer with id : {answer_id} does not exist "}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request,  answer_id):
        try:
            answer = Answer.objects.get(pk=answer_id)
            comment, is_created = Comment.objects.get_or_create(
                content=request.data['content'],
                date=datetime.date.today(),
                answer=answer,
                user=request.user,
            )
            serializer = CommentSerializer(comment)
            print(comment, is_created)
            if not is_created:
                return Response({"error": "Already exists", "data": serializer.data}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except KeyError as e:
            print("Exception: ", type(e), e)
            return Response({"error": "Incomplete data!!"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": ""}, status=status.HTTP_400_BAD_REQUEST)


class CommunityView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            communities = Community.objects.all()
            response = CommunitySerializer(communities, many=True)
            return Response(response.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Server error"}, status=status.HTTP_400_BAD_REQUEST)
