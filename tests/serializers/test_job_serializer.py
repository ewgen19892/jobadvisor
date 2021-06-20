"""Test job serializer."""
import pytest
from tests.factories import JobFactory, UserFactory

from jobadvisor.users.serializers import JobSerializer


@pytest.mark.django_db
def test_job_serializer_without_request() -> None:
    job = JobFactory()
    serializer = JobSerializer(instance=job)
    assert serializer.data.get("salary") is None


@pytest.mark.django_db
def test_job_serializer_with_request(rf) -> None:
    user = UserFactory()
    job = JobFactory(owner=user)
    request = rf.get("")
    request.user = user
    serializer = JobSerializer(instance=job, context={"request": request})
    assert serializer.data.get("salary") == job.salary


@pytest.mark.django_db
def test_job_serializer_validate(rf, faker, company, position) -> None:
    job_stub = JobFactory.stub(company=company, position=position)
    data = {
        "company": job_stub.company.pk,
        "position": job_stub.position.pk,
        "salary": job_stub.salary,
        "started_at": job_stub.finished_at,
        "finished_at": job_stub.started_at,
    }
    serializer = JobSerializer(data=data)
    assert not serializer.is_valid()
