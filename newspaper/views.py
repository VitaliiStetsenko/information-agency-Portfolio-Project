from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from newspaper.forms import (
    NewspaperForm,
    RedactorCreateForm,
    RedactorUpdateForm,
    NewspaperSearchForm,
    RedactorSearchForm,
    TopicSearchForm
)
from newspaper.models import Topic, Newspaper


def index(request):
    """View function for the home page of the site."""

    num_topics = Topic.objects.count()
    num_redactors = get_user_model().objects.count()
    num_newspaper = Newspaper.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_topics": num_topics,
        "num_redactors": num_redactors,
        "num_newspaper": num_newspaper,
        "num_visits": num_visits
    }

    return render(request, "newspaper/index.html", context)


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    paginate_by = 15

    def get_queryset(self):
        queryset = Newspaper.objects.prefetch_related("publishers", "topics")
        title = self.request.GET.get("title")
        if title:
            return queryset.filter(title__icontains=title)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(NewspaperListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = NewspaperSearchForm(
            initial={
                "title": title,
            }
        )
        return context


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    success_url = reverse_lazy("newspaper:newspaper-list")
    form_class = NewspaperForm


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    success_url = reverse_lazy("newspaper:newspaper-list")
    form_class = NewspaperForm


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("newspaper:newspaper-list")


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    paginate_by = 10

    def get_queryset(self):
        queryset = Topic.objects.all()
        name = self.request.GET.get("name")
        if name:
            return queryset.filter(name__icontains=name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TopicListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TopicSearchForm(
            initial={
                "name": name,
            }
        )
        return context


class TopicDetailView(LoginRequiredMixin, generic.DetailView):
    model = Topic


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    success_url = reverse_lazy("newspaper:topic-list")
    fields = "__all__"


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("newspaper:topic-list")


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("newspaper:topic-list")


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    paginate_by = 10

    def get_queryset(self):
        queryset = get_user_model().objects.prefetch_related("newspapers")
        username = self.request.GET.get("username")
        if username:
            return queryset.filter(username__icontains=username)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(RedactorListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = RedactorSearchForm(
            initial={
                "username": username,
            }
        )
        return context


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()


class RedactorCreateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = RedactorCreateForm
    success_url = reverse_lazy("newspaper:redactor-list")


class RedactorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = RedactorUpdateForm
    success_url = reverse_lazy("newspaper:redactor-list")


class RedactorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("newspaper:redactor-list")
