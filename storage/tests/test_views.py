from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from storage.models import Category

URL_CATEGORIES = reverse("storage:category-list")

class PublicCategoryTest(TestCase):
    def test_login_required(self):
        response = self.client.get(URL_CATEGORIES)
        self.assertNotEqual(response.status_code, 200)

class PrivateCategoryTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="<PASSWORD>",
        )
        self.category_1 = Category.objects.create(name="category_1")
        self.category_2 = Category.objects.create(name="category_2")
        self.client.force_login(self.user)

    def test_retrieve_categories_list(self):
        response = self.client.get(URL_CATEGORIES)
        self.assertEqual(response.status_code, 200)
        categories = Category.objects.all()
        self.assertEqual(
            list(response.context["category_list"]),
            list(categories)
        )
        self.assertTemplateUsed(response, "storage/category_list.html")


class PrivateUserTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_create_user(self):
        data = {
            "username": "new_user",
            "password1": "test_password",
            "password2": "test_password",
            "first_name": "First",
            "last_name": "Last",
            "occupation": "City",
        }
        self.client.post(reverse("storage:user-create"), data=data)
        new_user = get_user_model().objects.get(username=data["username"])
        self.assertEqual(new_user.first_name, data["first_name"])
        self.assertEqual(new_user.last_name, data["last_name"])
        self.assertEqual(new_user.occupation, data["occupation"])
