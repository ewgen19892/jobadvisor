import pytest
from rest_framework import status
from tests.factories import FAQFactory

from jobadvisor.landing.serializers import FAQSerializer
from jobadvisor.landing.views import CategoryList, FAQDetail, FAQList


@pytest.mark.django_db
def test_category_list_success(rf, faq_categories):
    request = rf.get("", data={"page_size": 100})
    response = CategoryList.as_view()(request)
    assert response.status_code == status.HTTP_200_OK
    assert int(response["X-Total"]) == len(faq_categories)


@pytest.mark.django_db
def test_faq_list_success(rf, faqs):
    request = rf.get("", data={"page_size": 100})
    response = FAQList.as_view()(request)
    assert response.status_code == status.HTTP_200_OK
    assert int(response["X-Total"]) == len(faqs)


@pytest.mark.django_db
def test_faq_detail_success(rf, faqs):
    faq = FAQFactory()
    request = rf.get("")
    response = FAQDetail.as_view()(request, pk=faq.pk)
    assert response.status_code == status.HTTP_200_OK
    assert FAQSerializer(instance=faq).data == response.data
