import pytest
from rest_framework.serializers import ValidationError
from tests.factories import CompanyFactory, UserFactory

from jobadvisor.companies.serializers import CompanySerializer


@pytest.mark.django_db
def test_company_serializer_owner_not_employer(industry) -> None:
    user = UserFactory(level=0)
    data = CompanyFactory.stub(owner=user, industry=industry, logo=None)
    data = {
        "owner": data.owner.pk,
        "industry": data.industry.pk,
        "name": data.name,
        "website": data.website,
        "size": data.size,
        "founded": data.founded,
        "description": data.description,
    }
    serializer = CompanySerializer(data=data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_company_serializer_owner_have_company(industry) -> None:
    user = UserFactory(level=2)
    CompanyFactory(owner=user)
    data = CompanyFactory.stub(owner=user, industry=industry, logo=None)
    data = {
        "owner": data.owner.pk,
        "industry": data.industry.pk,
        "name": data.name,
        "website": data.website,
        "size": data.size,
        "founded": data.founded,
        "description": data.description,
    }
    serializer = CompanySerializer(data=data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_company_serializer_owner_have_work(industry) -> None:
    user = UserFactory(level=2)
    company = CompanyFactory()
    company.workers.add(user)
    data = CompanyFactory.stub(owner=user, industry=industry, logo=None)
    data = {
        "owner": data.owner.pk,
        "industry": data.industry.pk,
        "name": data.name,
        "website": data.website,
        "size": data.size,
        "founded": data.founded,
        "description": data.description,
    }
    serializer = CompanySerializer(data=data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_company_serializer_worker_not_employer() -> None:
    user = UserFactory(level=0)
    company = CompanyFactory()
    data = {
        "workers": [user.pk],
    }
    serializer = CompanySerializer(data=data, instance=company, partial=True)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_company_serializer_worker_have_company() -> None:
    user = UserFactory(level=2)
    CompanyFactory(owner=user)
    company = CompanyFactory()
    data = {
        "workers": [user.pk],
    }
    serializer = CompanySerializer(data=data, instance=company)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_company_serializer_worker_have_work() -> None:
    user = UserFactory(level=2)
    other_company = CompanyFactory()
    other_company.workers.add(user)
    company = CompanyFactory()
    data = {
        "workers": [user.pk],
    }
    serializer = CompanySerializer(data=data, instance=company, partial=True)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_company_serializer_worker_success() -> None:
    user = UserFactory(level=2)
    company = CompanyFactory()
    data = {
        "workers": [user.pk],
    }
    serializer = CompanySerializer(data=data, instance=company, partial=True)
    assert serializer.is_valid() is True


@pytest.mark.django_db
def test_company_serializer_clean_workers(industry) -> None:
    user = UserFactory(level=2)
    data = CompanyFactory.stub(owner=user, industry=industry, logo=None)
    data = {
        "owner": data.owner.pk,
        "industry": data.industry.pk,
        "name": data.name,
        "website": data.website,
        "size": data.size,
        "founded": data.founded,
        "description": data.description,
        "workers": [UserFactory(level=2).pk],
    }
    serializer = CompanySerializer(data=data)
    assert serializer.is_valid() is True
    assert serializer.validated_data["workers"] == []


@pytest.mark.django_db
def test_company_serializer_update_owner() -> None:
    user = UserFactory(level=2)
    other_user = UserFactory(level=2)
    company = CompanyFactory(owner=user)
    data = {
        "owner": other_user.pk,
    }
    serializer = CompanySerializer(data=data, instance=company, partial=True)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_company_serializer_get_subscription_without_request() -> None:
    user = UserFactory()
    company = CompanyFactory(owner=user)
    serializer = CompanySerializer(instance=company)
    assert serializer.data.get("subscription") is None


@pytest.mark.django_db
def test_company_serializer_get_subscription(rf) -> None:
    user = UserFactory()
    company = CompanyFactory(owner=user)
    request = rf.get("")
    request.user = user
    serializer = CompanySerializer(instance=company,
                                   context={"request": request})
    assert type(dict(serializer.data.get("subscription"))) is dict
