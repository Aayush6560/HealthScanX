from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from .models import Report
from .serializers import ReportSerializer


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer

    def get_queryset(self):
        queryset = Report.objects.select_related("patient", "test")
        if not self.request.user.is_staff:
            queryset = queryset.filter(patient=self.request.user)
        return queryset

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            if "patient" not in serializer.validated_data:
                raise ValidationError({"patient_id": "This field is required for staff-created reports."})
            serializer.save()
        else:
            serializer.save(patient=self.request.user)
