from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import *
import requests
import json
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
