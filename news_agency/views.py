from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from news_agency.models import (
    Topic,
    Redactor,
    Newspaper,
)


def index(request: HttpRequest):
    num_topics = Topic.objects.count()
    num_redactors = Redactor.objects.count()
    num_newspapers = Newspaper.objects.count()
    news = Newspaper.objects.all()[:3]

    return render(
        request,
        "news_agency/index.html",
        context={
            "num_topics": num_topics,
            "num_redactors": num_redactors,
            "num_newspapers": num_newspapers,
            "news_list": news
        }
    )


class TopicListView(generic.ListView):
    model = Topic


class NewspaperListView(generic.ListView):
    model = Newspaper


class RedactorListView(generic.ListView):
    model = Redactor


class NewspaperDetailView(generic.DetailView):
    model = Newspaper


class TopicDetailView(generic.DetailView):
    model = Topic


class RedactorDetailView(generic.DetailView):
    model = Redactor


class TopicDeleteView(generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("news_agency:topic-list")
