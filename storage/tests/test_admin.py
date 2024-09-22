from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            password="<PASSWORD>",
        )
        self.client.force_login(self.admin)
        self.user = get_user_model().objects.create_user(
            username="user",
            password="<PASSWORD>",
            occupation="city"
        )

    def test_users_occupation_listed_on_users_list_display(self):
        url = reverse("admin:storage_user_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.user.occupation)

    def test_user_occupation_listed_on_user_chagne_page(self):
        url = reverse("admin:storage_user_change", args=[self.user.id])
        response = self.client.get(url)
        self.assertContains(response, self.user.occupation)

    def test_user_occupation_available_on_user_add_page(self):
        url = reverse("admin:storage_user_add")
        response = self.client.get(url)
        self.assertContains(response, "occupation")
