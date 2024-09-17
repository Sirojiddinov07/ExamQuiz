from rest_framework import serializers

from exam.models.commentary import Commentary


class CommentarySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # Display the username

    class Meta:
        model = Commentary
        fields = ['id', 'quiz', 'user', 'text', 'created_at']
