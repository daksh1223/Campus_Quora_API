from rest_framework import serializers
from .models import Question,Community,Answer

class CommunitySerializer(serializers.ModelSerializer):
    class Meta :
        model = Community
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta :
        model = Question
        fields = "__all__"
        
class AnswerSerializer(serializers.ModelSerializer):
    class Meta :
        model = Answer
        fields = "__all__"