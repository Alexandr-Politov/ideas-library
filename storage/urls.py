from django.urls import path

from storage.views import index, IdeaListView

urlpatterns = [
    path("", index, name="index"),
    path("ideas/", IdeaListView.as_view(), name="idea-list"),
]

app_name = "storage"
