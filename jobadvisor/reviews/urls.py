"""Reviews URL Configuration."""
from django.urls import path

from jobadvisor.reviews.views import (
    CommentInterview,
    CommentReview,
    InterviewDetail,
    InterviewHelpful,
    InterviewList,
    InterviewTop,
    QADetail,
    QAList,
    ReportInterview,
    ReportReview,
    ReviewDetail,
    ReviewHelpful,
    ReviewList,
    ReviewTop,
)

app_name: str = "reviews"
urlpatterns: list = [
    path("reviews/", ReviewList.as_view(), name="review_list"),
    path("reviews/<int:pk>/", ReviewDetail.as_view(), name="review_detail"),
    path("reviews/<int:pk>/comment/", CommentReview.as_view(),
         name="review_comment"),
    path("reviews/<int:pk>/report/", ReportReview.as_view(),
         name="review_report"),
    path("reviews/<int:pk>/top/", ReviewTop.as_view(),
         name="review_top"),
    path("reviews/<int:pk>/helpful/", ReviewHelpful.as_view(),
         name="review_helpful"),

    path("interviews/", InterviewList.as_view(), name="interview_list"),
    path("interviews/<int:pk>/", InterviewDetail.as_view(),
         name="interview_detail"),
    path("interviews/<int:pk>/comment/", CommentInterview.as_view(),
         name="interview_comment"),
    path("interviews/<int:pk>/report/", ReportInterview.as_view(),
         name="interview_report"),
    path("interviews/<int:pk>/top/", InterviewTop.as_view(),
         name="interview_top"),
    path("interviews/<int:pk>/helpful/", InterviewHelpful.as_view(),
         name="interview_helpful"),
    path("qas/", QAList.as_view(), name="qas_list"),
    path("qas/<int:pk>/", QADetail.as_view(), name="qas_detail"),
]
