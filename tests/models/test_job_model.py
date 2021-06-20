from tests.factories import JobFactory


def test_job_name():
    job = JobFactory.build()
    job_name: str = f"{job.company.name} {job.position}"
    assert str(job_name) == str(job)
