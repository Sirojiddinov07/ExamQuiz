from rest_framework import serializers

from core.apps.mock.models import Question, Answer
from core.apps.mock.serializers.answer import AnswerSerializer


class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ('question_number', 'title', 'answers')

    def get_answers(self, obj):
        answers = Answer.objects.filter(question=obj)
        return AnswerSerializer(answers, many=True).data