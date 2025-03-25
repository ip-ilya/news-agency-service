from django.urls import path

from news_agency.views import index, TopicListView, NewspaperListView

app_name = "news_agency"

urlpatterns = [
    path("", index, name="index"),
    path("topics/", TopicListView.as_view(), name="topic-list"),
    path("newspapers/", NewspaperListView.as_view(), name="newspaper-list")
]
