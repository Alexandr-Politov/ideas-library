from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

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