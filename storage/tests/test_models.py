from django.contrib.auth import get_user_model
from django.test import TestCase

from storage.models import Category


class ModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_name",
            password="test_password",
            first_name="first",
            last_name="last",
            occupation="city",
        )

    def test_category_str(self):
        test_category = Category.objects.create(name="test_category")
        self.assertEqual(str(test_category), "test_category")

    def test_create_user_with_occupation(self):
        self.assertEqual(self.user.username, "test_name")
        self.assertTrue(self.user.check_password("test_password"))
        self.assertEqual(self.user.occupation, "city")

    def test_user_str(self):
        self.assertEqual(
            str(self.user),
            f"{self.user.username}: ({self.user.first_name} "
                f"{self.user.last_name} from {self.user.occupation})"
        )
