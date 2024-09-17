from rest_framework import serializers
from exam.models import Quizzes, Addition, Question
from exam.serializers.question import QuestionSerializer
from exam.serializers.addition import AdditionSerializer

class QuizzesSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    additions = serializers.SerializerMethodField()

    class Meta:
        model = Quizzes
        fields = ('id', 'title', 'category', 'date_created', 'duration', 'is_free', 'questions', 'additions')

    def get_questions(self, obj):
        # Get the IDs of the questions in the additions
        addition_question_ids = set(
            Addition.objects.filter(questions__in=obj.questions.all()).values_list('questions__id', flat=True)
        )
        # Filter out questions that are not in the additions
        quiz_questions = obj.questions.exclude(id__in=addition_question_ids)
        return QuestionSerializer(quiz_questions, many=True).data

    def get_additions(self, obj):
        # Get the IDs of the questions in the quiz
        question_ids = obj.questions.values_list('id', flat=True)
        # Find additions that have any of these questions
        additions = Addition.objects.filter(questions__in=question_ids).distinct()
        return AdditionSerializer(additions, many=True).data
