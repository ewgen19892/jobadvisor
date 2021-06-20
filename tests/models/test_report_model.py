import pytest
from tests.factories import ReportedInterviewFactory


@pytest.mark.django_db
def test_report_name() -> None:
    report = ReportedInterviewFactory.build()
    assert str(report) == f"Report: {report.pk}"
