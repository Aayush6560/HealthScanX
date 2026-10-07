from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.centres.models import DiagnosticTest

from .models import Report

User = get_user_model()


class ReportSerializer(serializers.ModelSerializer):
    patient_id = serializers.PrimaryKeyRelatedField(
        source="patient", queryset=User.objects.all(), required=False
    )
    test_id = serializers.PrimaryKeyRelatedField(source="test", queryset=DiagnosticTest.objects.all())
    test_name = serializers.CharField(source="test.name", read_only=True)

    class Meta:
        model = Report
        fields = [
            "id",
            "patient_id",
            "test_id",
            "test_name",
            "findings",
            "report_date",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "test_name", "created_at", "updated_at"]
