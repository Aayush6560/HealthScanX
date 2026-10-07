import pytest

from apps.centres.models import DiagnosticTest
from apps.reports.models import Report

pytestmark = pytest.mark.django_db


def test_tests_can_be_filtered_by_category(api, offering):
    offering.test.category = DiagnosticTest.Category.RADIOLOGY
    offering.test.save(update_fields=["category"])

    assert api.get("/tests/?category=RADIOLOGY").json()["results"][0]["category"] == "RADIOLOGY"
    assert api.get("/tests/?category=unknown").status_code == 400


def test_patient_can_create_and_only_view_own_reports(user, user_api, other_api, offering):
    created = user_api.post(
        "/reports/",
        {
            "test_id": offering.test_id,
            "findings": "No abnormality detected.",
            "report_date": "2026-10-07",
            "status": "FINAL",
        },
    )

    assert created.status_code == 201
    assert created.json()["patient_id"] == user.id
    assert user_api.get("/reports/").json()["count"] == 1
    assert other_api.get("/reports/").json()["count"] == 0


def test_staff_can_create_report_for_a_patient(admin_api, user, offering):
    response = admin_api.post(
        "/reports/",
        {
            "patient_id": user.id,
            "test_id": offering.test_id,
            "findings": "Follow-up recommended.",
            "report_date": "2026-10-07",
        },
    )

    assert response.status_code == 201
    assert Report.objects.get().patient_id == user.id
