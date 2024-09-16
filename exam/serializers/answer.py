from rest_framework import serializers

from core.apps.mock.models import Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'question', 'answer_text', 'is_right')