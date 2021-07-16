import requests
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated  


from .models import *
from .serializers import *
from posts.models import *
from posts.serializers import *

# Create your views here.


class MicrosoftView(APIView):
    def post(self, request):
        # "Authorization" : "Bearer navgkskjdlmdl...(office 365 access token)"
        headers = {"Authorization": request.headers['Authorization']}
        r = requests.get(
            'https://graph.microsoft.com/v1.0/me/', headers=headers)
        data = json.loads(r.text)

        if 'error' in data:
            content = {
                'message': 'wrong Microsoft token / this Microsoft token is already expired.'}
            return Response(content, status.HTTP_401_UNAUTHORIZED)

        try:
            user = User.objects.get(email=data['userPrincipalName'])

        except User.DoesNotExist:
            user = User.objects.create(username=data['userPrincipalName'],
                                       first_name=data['displayName'], email=data['userPrincipalName'], last_name=data['surname'])

        token = RefreshToken.for_user(user)
        response = {}
        response['username'] = user.username
        response['access_token'] = str(token.access_token)
        response['refresh_token'] = str(token)
        return Response(response)

class profile(APIView):
     permission_classes=(IsAuthenticated,)
     def get(self,request,user_id):
          user=User.objects.get(pk=user_id)
          questions=Question.objects.all().filter(user=user)
          answers=Post.objects.all().filter(writer=user)
          serialized_user=user_serializer(user)
          serialized_questions=Question_serializer(questions,many=True)
          serialzed_answers=Answer_serializer(answers,many=True)
          
          response={}
          response['user']=serialized_user.data
          response['questions']=serialized_questions.data
          response['answers']=serialzed_answers.data
          return Response(response,status=status.HTTP_200_OK)