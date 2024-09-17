from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from exam.models import Commentary
from exam.serializers import CommentarySerializer


class CommentaryViewSet(viewsets.ModelViewSet):
    serializer_class = CommentarySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Commentary.objects.filter(quiz=self.kwargs['quiz_pk']).order_by('created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, quiz_id=self.kwargs['quiz_pk'])
