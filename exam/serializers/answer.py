from rest_framework import serializers

from exam.models.answer import Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'question', 'answer_text', 'is_right')