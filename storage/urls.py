from django.urls import path

from storage.views import (
    index,

    IdeaListView,
    IdeaDetailView,
    IdeaCreateView,
    IdeaUpdateView,
    IdeaDeleteView,

    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,

    UserListView,
    UserDetailView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,

    CommentDeleteView,
)

urlpatterns = [
    path("", index, name="index"),

    path("ideas/", IdeaListView.as_view(), name="idea-list"),
    path("ideas/create/", IdeaCreateView.as_view(), name="idea-create"),
    path("ideas/<int:pk>/", IdeaDetailView.as_view(), name="idea-detail"),
    path("ideas/<int:pk>/update/",
         IdeaUpdateView.as_view(),
         name="idea-update"),
    path("ideas/<int:pk>/delete/",
         IdeaDeleteView.as_view(),
         name="idea-delete"),

    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/create/",
         CategoryCreateView.as_view(),
         name="category-create"),
    path("categories/<int:pk>/update/",
         CategoryUpdateView.as_view(),
         name="category-update"),
    path("categories/<int:pk>/delete/",
         CategoryDeleteView.as_view(),
         name="category-delete"),

    path("users/", UserListView.as_view(), name="user-list"),
    path("users/create/", UserCreateView.as_view(), name="user-create"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("users/<int:pk>/update/",
         UserUpdateView.as_view(),
         name="user-update"),
    path("users/<int:pk>/delete/",
         UserDeleteView.as_view(),
         name="user-delete"),

    path("comments/<int:pk>/delete/",
         CommentDeleteView.as_view(),
         name="comment-delete"),
]

app_name = "storage"
