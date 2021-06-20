import pytest
from rest_framework import status

from jobadvisor.landing.views import PageDetail, PageList


@pytest.mark.django_db
def test_page_list_success(rf, pages):
    request = rf.get("", data={"page_size": 100})
    response = PageList.as_view()(request)
    assert response.status_code == status.HTTP_200_OK
    assert int(response["X-Total"]) == len(pages)


@pytest.mark.django_db
def test_page_details_success(rf, pages, page):
    request = rf.get("", data={"page_size": 100})
    response = PageDetail.as_view()(request, slug=page.slug)
    assert response.status_code == status.HTTP_200_OK
    assert page.text == response.data.get("text")
