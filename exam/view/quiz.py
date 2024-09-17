from rest_framework import generics
from rest_framework.permissions import AllowAny

from exam.models import Quizzes
from exam.serializers import QuizzesSerializer


class QuizzesListView(generics.ListAPIView):
    queryset = Quizzes.objects.all()
    serializer_class = QuizzesSerializer
    permission_classes = [AllowAny]

class QuizzesDetailView(generics.RetrieveAPIView):
    queryset = Quizzes.objects.all()
    serializer_class = QuizzesSerializer
    permission_classes = [AllowAny]
