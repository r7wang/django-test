from rest_framework import serializers

from .models import Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id']


class ChoiceSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    choice_text = serializers.CharField(max_length=200)
    votes = serializers.IntegerField(default=0)
    publish_date = serializers.DateTimeField()
    contact_email = serializers.EmailField(allow_null=True)
    enabled = serializers.BooleanField()

