from django.db.models import fields
from rest_framework import serializers
from .models import *
from user.serializers import *

class Answer_serializer(serializers.ModelSerializer):
    writer=user_serializer()
    class Meta:
        model = Post
        fields = "__all__"


class Question_serializer(serializers.ModelSerializer):
    user=user_serializer()
    class Meta:
        model=Question
        fields="__all__"

class Category_serializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields='__all__'

class comment_serializer(serializers.ModelSerializer):
    user=user_serializer()
    class Meta:
        model=Comment
        fields='__all__'

