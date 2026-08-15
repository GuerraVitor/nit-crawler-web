from django.urls import path
from .views import ResearcherSearchView

urlpatterns = [
    path("researchers/search/", ResearcherSearchView.as_view(), name="researcher-search"),
]
