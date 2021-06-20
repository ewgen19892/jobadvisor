"""Landing URL Configuration."""
from django.urls import path

from jobadvisor.landing.views import (
    AdvantageList,
    CategoryList,
    ContactUs,
    FAQDetail,
    FAQList,
    PageDetail,
    PageList,
)

app_name: str = "landing"

urlpatterns: list = [
    path("advantages/", AdvantageList.as_view(), name="advantage_list"),

    path("contactus/", ContactUs.as_view(), name="contact_us"),

    path("faq/categories/", CategoryList.as_view(), name="category_list"),

    path("faq/", FAQList.as_view(), name="faq_list"),
    path("faq/<int:pk>/", FAQDetail.as_view(), name="faq_detail"),

    path("pages/", PageList.as_view(), name="page_list"),
    path("pages/<slug:slug>/", PageDetail.as_view(), name="page_detail"),

]
