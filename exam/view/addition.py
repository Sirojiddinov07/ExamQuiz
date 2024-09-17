from rest_framework import viewsets
from exam.models.addition import Addition
from exam.serializers.addition import AdditionSerializer

class AdditionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Addition.objects.all()
    serializer_class = AdditionSerializer
