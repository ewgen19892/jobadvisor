from tests.factories import InterviewFactory


def test_interview_name() -> None:
    interview = InterviewFactory.build()
    assert str(interview) == f"Interview: {interview.pk}"
