from rest_framework import serializers

from core.apps.mock.models import Commentary


class CommentarySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # Display the username

    class Meta:
        model = Commentary
        fields = ['id', 'quiz', 'user', 'text', 'created_at']
