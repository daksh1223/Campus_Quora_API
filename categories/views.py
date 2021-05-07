from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  
from rest_framework import generics
from .models import *
from .serializers import *
# Create your views here.
class Category_list(generics.ListAPIView):
     permission_classes = (IsAuthenticated,)        
     queryset=category.objects.all()
     serializer_class=category_serializer