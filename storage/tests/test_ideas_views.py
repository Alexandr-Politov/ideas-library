from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from storage.models import Idea


URL_IDEAS = reverse("storage:idea-list")
URL_IDEA_CREATE = reverse("storage:idea-create")


class PublicIdeaTest(TestCase):
    def test_login_required(self):
        response = self.client.get(URL_IDEAS)
        self.assertNotEqual(response.status_code, 200)


class PrivateIdeaTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="<PASSWORD>",
        )
        self.idea_1 = Idea.objects.create(
            name="idea_1",
            description="description_1",
            difficulty="Easy",
            author=self.user,
        )
        self.idea_2 = Idea.objects.create(
            name="idea_2",
            description="description_2",
            difficulty="Hard",
            author=self.user,
        )
        self.client.force_login(self.user)
        self.data = {
            "name": "ides_3",
            "description": "description_3",
            "difficulty": "Medium",
        }

    def test_retrieve_ideas_list(self):
        response = self.client.get(URL_IDEAS)
        self.assertEqual(response.status_code, 200)
        categories = Idea.objects.all()
        self.assertEqual(
            list(response.context["idea_list"]),
            list(categories)
        )
        self.assertTemplateUsed(response, "storage/idea_list.html")

    def test_create_idea(self):
        self.client.post(URL_IDEA_CREATE, data=self.data)
        idea = Idea.objects.get(name=self.data["name"])
        self.assertEqual(idea.name, self.data["name"])

    def test_update_idea(self):
        old_idea = self.idea_1
        updated_data = {
            "name": "ides_4",
            "description": "description_4",
            "difficulty": "Hard",
        }
        self.client.post(
            reverse("storage:idea-update", kwargs={"pk": old_idea.id}),
            data=updated_data
        )
        updated_idea = Idea.objects.get(id=old_idea.id)
        self.assertEqual(updated_idea.name, updated_data["name"])

    def test_delete_idea(self):
        idea_to_delete = self.idea_1
        count_ideas_before = Idea.objects.count()
        url_delete = reverse(
            "storage:idea-delete",
            kwargs={"pk": idea_to_delete.id}
        )
        self.client.post(url_delete)
        count_ideas_after = Idea.objects.count()
        self.assertEqual(count_ideas_before - 1, count_ideas_after)

    def test_search_ideas(self):
        response = self.client.get(URL_IDEAS, {"search": "1"})
        search_result = response.context["object_list"]
        self.assertEqual(len(search_result), 1)
        self.assertEqual(search_result[0].name, "idea_1")
