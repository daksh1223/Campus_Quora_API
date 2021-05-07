from rest_framework import serializers
from .models import *

class category_serializer(serializers.ModelSerializer):
    class Meta:
        model=category
        fields=('category',)