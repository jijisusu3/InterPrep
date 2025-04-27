
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Application, PracticeRecord

User = get_user_model()

class PracticeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticeRecord
        fields = [
            "id",
            "application",
            "question_text",
            "batch_number",
            "answer_text",
            "score",
            "is_scored",
            "feedback",
            "created_at",
            "answered_at",
        ]
        read_only_fields = [
            "id",
            "application",
            "created_at",
            "answered_at",
        ]


class ApplicationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    practice_records = PracticeRecordSerializer(
        source="practicerecord_set",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Application
        fields = [
            "id",
            "user",
            "desired_role",
            "created_at",
            "practice_records",
        ]
        read_only_fields = [
            "id",
            "user",
            "created_at",
            "practice_records",
        ]