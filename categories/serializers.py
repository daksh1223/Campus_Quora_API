from django.db.models import fields
from rest_framework import serializers
from .models import *


class user_serializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields= '__all__'


class Answer_serializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class Question_serializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields='__all__'

class Category_serializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields='__all__'
