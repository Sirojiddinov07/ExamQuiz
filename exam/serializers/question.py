from rest_framework import serializers

from exam.models import Question, Answer
from exam.serializers.answer import AnswerSerializer


class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ('question_number', 'title', 'answers')

    def get_answers(self, obj):
        answers = Answer.objects.filter(question=obj)
        return AnswerSerializer(answers, many=True).data