from rest_framework import serializers

from core.apps.mock.models.for_read import ForRead


class ForReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForRead
        fields = ('id', 'title', 'text', 'image')