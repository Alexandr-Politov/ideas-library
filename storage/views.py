from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from storage.forms import SearchForm
from storage.models import Idea, Category


def index(request: HttpRequest) -> HttpResponse:
    num_ideas = Idea.objects.count()
    num_users = get_user_model().objects.count()
    num_categories = Category.objects.count()
    context = {
        "num_ideas": num_ideas,
        "num_users": num_users,
        "num_categories": num_categories
    }
    return render(request, "storage/index.html", context)


class IdeaListView(ListView):
    model = Idea
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IdeaListView, self).get_context_data(**kwargs)
        search = self.request.GET.get("search", "")
        context["search"] = search
        context["search_form"] = SearchForm(initial={"search": search})
        return context

    def get_queryset(self):
        queryset = self.model.objects.all()
        search = self.request.GET.get("search")
        if search:
            return queryset.filter(name__icontains=search)
        return queryset
