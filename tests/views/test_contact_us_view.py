from rest_framework import status

from jobadvisor.landing.views import ContactUs


def test_contact_us_success(rf, faker):
    data = {
        "name": faker.name(),
        "phone": faker.msisdn(),
        "email": faker.email(),
        "message": faker.text()
    }
    request = rf.post("", data=data)
    response = ContactUs.as_view()(request)
    assert response.status_code == status.HTTP_200_OK


def test_contact_us_bad_request(rf, faker):
    data = {
        "email": faker.first_name(),
        "password": faker.md5(raw_output=False),
    }
    request = rf.post("", data=data)
    response = ContactUs.as_view()(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
