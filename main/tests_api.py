
import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Education


class EducationAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner",
            password="test-password",
            email="owner@example.com",
        )

        self.visitor = User.objects.create_user(
            username="visitor",
            password="test-password",
        )

        self.education = Education.objects.create(
            institution="Universitas Indonesia",
            field_of_study="Information Systems",
            started="2025-08-01",
            ended=None,
        )

        self.list_url = reverse("api:education-list")
        self.detail_url = reverse(
            "api:education-detail",
            args=[self.education.id],
        )
        self.star_url = reverse(
            "api:education-star",
            args=[self.education.id],
        )

        self.payload = {
            "institution": "Universitas Bismillah",
            "field_of_study": "Computer Science",
            "started": "2026-08-01",
            "ended": None,
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data[0]["id"],
            str(self.education.id),
        )
        self.assertEqual(
            response.data[0]["field_of_study"],
            "Information Systems",
        )
        self.assertNotIn("fields", response.data[0])

        detail_response = self.client.get(self.detail_url)

        self.assertEqual(
            detail_response.status_code,
            status.HTTP_200_OK,
        )

    def test_search_and_empty_results(self):
        response = self.client.get(
            self.list_url,
            {"institution": "UNIVERSITAS"},
        )

        self.assertEqual(len(response.data), 1)

        response = self.client.get(
            self.list_url,
            {"institution": "not-found"},
        )

        self.assertEqual(response.data, [])

    def test_missing_education(self):
        url = reverse(
            "api:education-detail",
            args=[uuid.uuid4()],
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_guest_and_visitor_cannot_manage_education(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)

            post_response = self.client.post(
                self.list_url,
                self.payload,
                format="json",
            )

            patch_response = self.client.patch(
                self.detail_url,
                {"institution": "Changed"},
                format="json",
            )

            delete_response = self.client.delete(
                self.detail_url,
            )

            self.assertEqual(post_response.status_code, 403)
            self.assertEqual(patch_response.status_code, 403)
            self.assertEqual(delete_response.status_code, 403)

        self.assertEqual(Education.objects.count(), 1)

        self.education.refresh_from_db()

        self.assertEqual(
            self.education.institution,
            "Universitas Indonesia",
        )

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Education.objects.filter(
                pk=response.data["id"]
            ).exists()
        )

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)

        for changes, field in [
            ({"institution": "   "}, "institution"),
            (
                {"institution": '<img src="x" onerror="alert(1)">'},
                "institution",
            ),
        ]:
            response = self.client.post(
                self.list_url,
                {**self.payload, **changes},
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST,
            )
            self.assertIn(field, response.data)

        self.assertEqual(Education.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.patch(
            self.detail_url,
            {"institution": "Universitas Indonesia Updated"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.education.refresh_from_db()

        self.assertEqual(
            self.education.field_of_study,
            "Information Systems",
        )

        response = self.client.put(
            self.detail_url,
            {"institution": "Incomplete"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        response = self.client.put(
            self.detail_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertEqual(response.content, b"")

        self.assertFalse(
            Education.objects.filter(
                pk=self.education.id
            ).exists()
        )

    def test_star_requires_login_and_toggles(self):
        response = self.client.post(self.star_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.client.force_authenticate(user=self.visitor)

        response = self.client.post(self.star_url)

        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)

        response = self.client.post(self.star_url)

        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            self.list_url,
            {
                **self.payload,
                "star_count": 99,
                "is_starred": True,
                "starred_by_names": "forged",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.delete(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)

        self.assertTrue(
            client.login(
                username="owner",
                password="test-password",
            )
        )

        response = client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertEqual(Education.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)

        client.login(
            username="owner",
            password="test-password",
        )

        page = client.get(
            self.list_url,
            HTTP_ACCEPT="text/html",
        )

        self.assertEqual(
            page.status_code,
            status.HTTP_200_OK,
        )

        token = client.cookies["csrftoken"].value

        response = client.post(
            self.list_url,
            self.payload,
            format="json",
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_editor_can_update_but_cannot_create_or_delete(self):
        editor = User.objects.create_user(
            username="editor",
            password="test-password",
        )

        editor_group, _ = Group.objects.get_or_create(name="Editor")
        editor.groups.add(editor_group)

        self.client.force_authenticate(user=editor)

        patch_response = self.client.patch(
            self.detail_url,
            {"institution": "Updated by Editor"},
            format="json",
        )

        self.assertEqual(
            patch_response.status_code,
            status.HTTP_200_OK,
        )

        post_response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            post_response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        delete_response = self.client.delete(self.detail_url)

        self.assertEqual(
            delete_response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
