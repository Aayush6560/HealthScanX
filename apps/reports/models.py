from django.conf import settings
from django.db import models

from apps.centres.models import DiagnosticTest


class Report(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        FINAL = "FINAL", "Final"

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="reports")
    test = models.ForeignKey(DiagnosticTest, on_delete=models.PROTECT, related_name="reports")
    findings = models.TextField()
    report_date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.FINAL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-report_date", "-id"]

    def __str__(self):
        return f"{self.test.name} report for {self.patient}"
