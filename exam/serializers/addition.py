from rest_framework import serializers

from exam.models import Addition
from exam.serializers import QuestionSerializer, ForReadSerializer


class AdditionSerializer(serializers.ModelSerializer):
    text = ForReadSerializer()
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Addition
        fields = ('id', 'image', 'text', 'questions')