from django.urls import path

from storage.views import (
    index,
    IdeaListView,
    IdeaDetailView,
    IdeaCreateView,
    IdeaUpdateView,
    IdeaDeleteView,
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
]

app_name = "storage"
