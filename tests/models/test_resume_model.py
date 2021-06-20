from tests.factories import ResumeFactory


def test_resume_name():
    resume = ResumeFactory.build()
    resume_name: str = f"{resume.owner.get_full_name()} {resume.position}"
    assert str(resume) == resume_name
