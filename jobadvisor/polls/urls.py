"""Polls URL Configuration."""
from django.urls import path

from jobadvisor.polls.views import (
    AnswerDetail,
    AnswerList,
    CategoryDetail,
    CategoryList,
    QuestionDetail,
    QuestionList,
    VariantDetail,
    VariantList,
)

app_name: str = "polls"

urlpatterns: list = [
    path("categories/", CategoryList.as_view(), name="category_list"),
    path("categories/<slug:pk>/", CategoryDetail.as_view(),
         name="category_detail"),

    path("variants/", VariantList.as_view(), name="variant_list"),
    path("variants/<slug:pk>/", VariantDetail.as_view(),
         name="variant_detail"),

    path("questions/", QuestionList.as_view(), name="question_list"),
    path("questions/<slug:pk>/", QuestionDetail.as_view(),
         name="question_detail"),

    path("answers/", AnswerList.as_view(), name="answer_list"),
    path("answers/<slug:pk>/", AnswerDetail.as_view(), name="answer_detail")
]
