from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from storage.models import Category


URL_CATEGORIES = reverse("storage:category-list")
URL_CATEGORY_CREATE = reverse("storage:category-create")


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
        self.data = {"name": "category_3"}

    def test_retrieve_categories_list(self):
        response = self.client.get(URL_CATEGORIES)
        self.assertEqual(response.status_code, 200)
        categories = Category.objects.all()
        self.assertEqual(
            list(response.context["category_list"]),
            list(categories)
        )
        self.assertTemplateUsed(response, "storage/category_list.html")

    def test_create_category(self):
        self.client.post(URL_CATEGORY_CREATE, data=self.data)
        category = Category.objects.get(name=self.data["name"])
        self.assertEqual(category.name, self.data["name"])

    def test_update_category(self):
        old_category = Category.objects.create(name="name")
        updated_data = {"name": "updated_category"}
        self.client.post(
            reverse(
                "storage:category-update", kwargs={"pk": old_category.id}
            ),
            data=updated_data
        )
        updated_category = Category.objects.get(id=old_category.id)
        self.assertEqual(updated_category.name, updated_data["name"])

    def test_delete_category(self):
        category_to_delete = Category.objects.create(name="name")
        count_categories_before = Category.objects.count()
        url_delete = reverse(
            "storage:category-delete",
            kwargs={"pk": category_to_delete.id}
        )
        self.client.post(url_delete)
        count_categories_after = Category.objects.count()
        self.assertEqual(count_categories_before - 1, count_categories_after)

    def test_search_categories(self):
        response = self.client.get(URL_CATEGORIES, {"search": "1"})
        search_result = response.context["object_list"]
        self.assertEqual(len(search_result), 1)
        self.assertEqual(search_result[0].name, "category_1")
