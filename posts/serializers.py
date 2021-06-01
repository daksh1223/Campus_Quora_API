from rest_framework import serializers
from .models import Question,Community

class CommunitySerializer(serializers.ModelSerializer):
    class Meta :
        model = Community
        fields = "__all__"