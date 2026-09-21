from django.urls import path
from .views import (
    ResearcherSearchView,
    LattesReportTriggerView,
    LattesReportStatusView,
)

urlpatterns = [
    path("researchers/search/", ResearcherSearchView.as_view(), name="researcher-search"),
    path(
        "researchers/lattes-report/",
        LattesReportTriggerView.as_view(),
        name="lattes-report-trigger",
    ),
    path(
        "researchers/lattes-report/status/",
        LattesReportStatusView.as_view(),
        name="lattes-report-status",
    ),
]
