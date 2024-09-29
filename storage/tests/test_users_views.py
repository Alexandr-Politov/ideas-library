from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


URL_USERS_LIST = reverse("storage:user-list")
URL_USERS_CREATE = reverse("storage:user-create")


class PublicUserTest(TestCase):
    def test_login_required(self):
        response = self.client.get(URL_USERS_LIST)
        self.assertNotEqual(response.status_code, 200)


class PrivateUserTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="test_password",
        )
        self.user2 = get_user_model().objects.create_user(
            username="user2",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)
        self.data = {
            "username": "new_user",
            "password1": "test_password",
            "password2": "test_password",
            "first_name": "First",
            "last_name": "Last",
            "occupation": "City",
        }

    def test_create_user(self):
        self.client.post(URL_USERS_CREATE, data=self.data)
        new_user = get_user_model().objects.get(username=self.data["username"])
        self.assertEqual(new_user.first_name, self.data["first_name"])
        self.assertEqual(new_user.last_name, self.data["last_name"])
        self.assertEqual(new_user.occupation, self.data["occupation"])

    def test_update_user(self):
        updated_data = {
            "username": "updated_user",
            "password1": "new_password",
            "password2": "new_password",
            "first_name": "updated_First",
            "last_name": "updated_Last",
            "occupation": "updated_City",
        }
        self.client.post(
            reverse("storage:user-update", kwargs={"pk": self.user.id}),
            data=updated_data
        )
        updated_user = get_user_model().objects.get(id=self.user.id)
        self.assertEqual(updated_user.username, updated_data["username"])
        self.assertEqual(updated_user.last_name, updated_data["last_name"])
        self.assertEqual(updated_user.occupation, updated_data["occupation"])

    def test_delete_user(self):
        count_users_before = get_user_model().objects.count()
        url_delete = reverse(
            "storage:user-delete",
            kwargs={"pk": self.user2.id}
        )
        self.client.post(url_delete)
        count_users_after = get_user_model().objects.count()
        self.assertEqual(count_users_before - 1, count_users_after)
