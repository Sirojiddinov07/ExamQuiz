from rest_framework import generics

from exam.models.answer import Answer
from exam.serializers.answer import AnswerSerializer


class AnswerListView(generics.ListAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class AnswerDetailView(generics.RetrieveAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer