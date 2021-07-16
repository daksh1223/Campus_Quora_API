from django.db.models import fields
from rest_framework import serializers
from posts.models import *

class user_serializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields= '__all__'
