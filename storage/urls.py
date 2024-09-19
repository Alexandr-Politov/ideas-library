from django.urls import path

from storage.views import index

urlpatterns = [
    path("", index, name="index"),
]

app_name = "storage"
