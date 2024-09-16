from rest_framework import serializers

from core.apps.mock.models import News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'image', 'title', 'text']