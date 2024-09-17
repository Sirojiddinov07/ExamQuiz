from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from exam.models import Quizzes, Question, Answer
from exam.serializers import UserAnswerSerializer


class CheckAnswersView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, quiz_id):
        serializer = UserAnswerSerializer(data=request.data, many=True)
        if serializer.is_valid():
            results = []

            try:
                quiz = Quizzes.objects.get(id=quiz_id)
            except Quizzes.DoesNotExist:
                return Response({"detail": "Quiz not found."}, status=status.HTTP_404_NOT_FOUND)

            # Access the related questions via the `questions` ManyToManyField
            questions = quiz.questions.all()

            answered_questions = set(item['question_id'] for item in serializer.validated_data)

            for question in questions:
                if question.id in answered_questions:
                    answer_id = next(
                        item['answer_id'] for item in serializer.validated_data if item['question_id'] == question.id)

                    try:
                        correct_answer = Answer.objects.get(question=question, is_right=True)

                        if correct_answer.id == answer_id:
                            results.append({'question_id': question.id, 'correct': True})
                        else:
                            results.append({'question_id': question.id, 'correct': False})
                    except Answer.DoesNotExist:
                        results.append({'question_id': question.id, 'correct': False})
                else:
                    results.append({'question_id': question.id, 'message': 'answer not found'})

            return Response(results, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
