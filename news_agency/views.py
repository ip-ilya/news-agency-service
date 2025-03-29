from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic

from news_agency.forms import RedactorCreationForm, RedactorUpdateForm
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
    paginate_by = 9


class NewspaperListView(generic.ListView):
    model = Newspaper
    paginate_by = 9


class RedactorListView(generic.ListView):
    model = Redactor


class NewspaperDetailView(generic.DetailView):
    model = Newspaper


class TopicDetailView(generic.DetailView):
    model = Topic


class RedactorDetailView(generic.DetailView):
    model = Redactor


class TopicUpdateView(generic.UpdateView):
    model = Topic
    fields = "__all__"

    def get_success_url(self):
        return reverse("news_agency:topic-detail", kwargs={"pk": self.object.pk})


class TopicDeleteView(generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("news_agency:topic-list")


class TopicCreateView(generic.CreateView):
    model = Topic
    fields = "__all__"

    def get_success_url(self):
        return reverse("news_agency:topic-detail", kwargs={"pk": self.object.pk})


class NewspaperCreateView(generic.CreateView):
    model = Newspaper
    fields = "__all__"

    def get_success_url(self):
        return reverse("news_agency:newspaper-detail", kwargs={"pk": self.object.pk})


class NewspaperUpdateView(generic.UpdateView):
    model = Newspaper
    fields = "__all__"

    def get_success_url(self):
        return reverse("news_agency:newspaper-detail", kwargs={"pk": self.object.pk})


class NewspaperDeleteView(generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("news_agency:newspaper-list")


class RedactorCreateView(generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm

    def get_success_url(self):
        return reverse("news_agency:redactor-create", kwargs={"pk": self.object.pk})


class RedactorUpdateView(generic.UpdateView):
    model = Redactor
    form_class = RedactorUpdateForm

    def get_success_url(self):
        return reverse("news_agency:redactor-detail", kwargs={"pk": self.object.pk})


class RedactorDeleteView(generic.DeleteView):
    model = Redactor
    success_url = reverse_lazy("news_agency:redactor-list")
