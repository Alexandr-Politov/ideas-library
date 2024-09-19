from django.urls import path

from storage.views import index, IdeaListView, IdeaDetailView

urlpatterns = [
    path("", index, name="index"),
    path("ideas/", IdeaListView.as_view(), name="idea-list"),
    path("ideas/<int:pk>", IdeaDetailView.as_view(), name="idea-detail"),
]

app_name = "storage"
