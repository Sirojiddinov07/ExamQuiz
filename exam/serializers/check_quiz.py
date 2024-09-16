from rest_framework import serializers

class UserAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer_id = serializers.IntegerField()
