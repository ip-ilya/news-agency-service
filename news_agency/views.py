from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.core.exceptions import PermissionDenied

from news_agency.forms import (
    RedactorCreationForm,
    RedactorUpdateForm,
    TopicNameSearchForm,
    RedactorUsernameSearchForm,
    NewspaperTitleSearchForm,
    NewspaperCreateForm,
    NewspaperUpdateForm,
)
from news_agency.models import (
    Topic,
    Redactor,
    Newspaper,
)


class AdminRequiredMixin(LoginRequiredMixin):
    """Mixin to restrict access to admin users only."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.is_staff:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


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
            "news_list": news,
        },
    )


class TopicListView(generic.ListView):
    model = Topic
    paginate_by = 9

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TopicNameSearchForm(initial={"name": name})

        return context

    def get_queryset(self):
        queryset = Topic.objects.all()
        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class NewspaperListView(generic.ListView):
    model = Newspaper
    paginate_by = 9

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get("title", "")

        context["search_form"] = NewspaperTitleSearchForm(
            initial={
                "title": title
            }
        )

        return context

    def get_queryset(self):
        queryset = Newspaper.objects.all()
        title = self.request.GET.get("title")
        if title:
            queryset = queryset.filter(title__contains=title)

        return queryset


class RedactorListView(generic.ListView):
    model = Redactor

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = RedactorUsernameSearchForm(
            initial={"username": username}
        )

        return context

    def get_queryset(self):
        queryset = get_user_model().objects.all()
        username = self.request.GET.get("username")

        if username:
            queryset = queryset.filter(username__icontains=username)

        return queryset


class NewspaperDetailView(generic.DetailView):
    model = Newspaper


class TopicDetailView(generic.DetailView):
    model = Topic


class RedactorDetailView(generic.DetailView):
    model = Redactor


class TopicUpdateView(AdminRequiredMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"

    def get_success_url(self):
        return reverse(
            "news_agency:topic-detail",
            kwargs={"pk": self.object.pk}
        )


class TopicDeleteView(AdminRequiredMixin, generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("news_agency:topic-list")


class TopicCreateView(AdminRequiredMixin, generic.CreateView):
    model = Topic
    fields = "__all__"

    def get_success_url(self):
        return reverse(
            "news_agency:topic-detail",
            kwargs={"pk": self.object.pk}
        )


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperCreateForm

    def get_success_url(self):
        return reverse(
            "news_agency:newspaper-detail",
            kwargs={"pk": self.object.pk}
        )

    def form_valid(self, form):
        newspaper = form.save(commit=False)
        newspaper.save()
        newspaper.publishers.add(self.request.user)
        return super().form_valid(form)


class NewspaperUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.UpdateView
):
    model = Newspaper
    form_class = NewspaperUpdateForm

    def get_success_url(self):
        return reverse(
            "news_agency:newspaper-detail",
            kwargs={"pk": self.object.pk}
        )

    def test_func(self):
        newspaper = self.get_object()
        user = self.request.user
        return user.is_staff or (user in newspaper.publishers.all())


class NewspaperDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DeleteView
):
    model = Newspaper
    success_url = reverse_lazy("news_agency:newspaper-list")

    def test_func(self):
        newspaper = self.get_object()
        user = self.request.user
        return user.is_staff or (user in newspaper.publishers.all())


class RedactorCreateView(AdminRequiredMixin, generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm

    def get_success_url(self):
        return reverse(
            "news_agency:redactor-detail",
            kwargs={"pk": self.object.pk}
        )


class RedactorUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.UpdateView
):
    model = Redactor
    form_class = RedactorUpdateForm

    def get_success_url(self):
        return reverse(
            "news_agency:redactor-detail",
            kwargs={"pk": self.object.pk}
        )

    def test_func(self):
        redactor = self.get_object()
        user = self.request.user
        return user.is_staff or (user.pk == redactor.pk)


class RedactorDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DeleteView
):
    model = Redactor
    success_url = reverse_lazy("news_agency:redactor-list")

    def test_func(self):
        redactor = self.get_object()
        user = self.request.user
        return user.is_staff or (user.pk == redactor.pk)


class CustomLoginView(LoginView):
    redirect_authenticated_user = True
