from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from storage.forms import SearchForm, UserCreateForm, CommentForm
from storage.models import Idea, Category, User, Comment


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


class SearchListView(generic.ListView):

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchListView, self).get_context_data(**kwargs)
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


class IdeaListView(LoginRequiredMixin, SearchListView):
    model = Idea
    queryset = Idea.objects.prefetch_related("categories").select_related("author")
    paginate_by = 2


class IdeaDetailView(LoginRequiredMixin, generic.DetailView):
    model = Idea

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.idea = self.object
            comment.author = request.user
            comment.save()
            return redirect("storage:idea-detail", pk=self.object.pk)
        context = self.get_context_data()
        context["comment_form"] = form
        return self.render_to_response(self.get_context_data(form=form))


class IdeaCreateView(LoginRequiredMixin, generic.CreateView):
    model = Idea
    fields = "__all__"
    success_url = reverse_lazy("storage:idea-list")


class IdeaUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Idea
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy(
            "storage:idea-detail",
            kwargs={"pk": self.object.pk}
        )


class IdeaDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Category
    success_url = reverse_lazy("storage:idea-list")


class CategoryListView(LoginRequiredMixin, SearchListView):
    model = Category


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    model = Category
    template_name = "storage/category_detail.html"


class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Category
    fields = "__all__"
    success_url = reverse_lazy("storage:category-list")


class CategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Category
    fields = "__all__"
    success_url = reverse_lazy("storage:category-list")


class CategoryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Category
    success_url = reverse_lazy("storage:category-list")


class UserListView(LoginRequiredMixin, SearchListView):
    model = User

    def get_queryset(self):
        queryset = self.model.objects.all()
        search = self.request.GET.get("search")
        if search:
            return queryset.filter(
                Q(username__icontains=search)
                | Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
            )
        return queryset


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = "storage/user_detail.html"


class UserCreateView(LoginRequiredMixin, generic.CreateView):
    model = User
    form_class = UserCreateForm
    success_url = reverse_lazy("storage:user-list")


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserCreateForm
    success_url = reverse_lazy("storage:user-list")


class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy("storage:user-list")


class CommentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse_lazy(
            "storage:idea-detail",
            kwargs={"pk": self.object.idea.pk}
        )
