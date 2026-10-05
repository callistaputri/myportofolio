from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Education
from main.views import SECRET_CODE


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Open House Fasilkom UI 2026 - Expert Staff of Public Relations",
            description="Represented Open House Fasilkom UI 2025 during external school visits, delivered presentations and engaged with high school students to promote the event, and coordinated MC requests and assignments across divisions.",
            category="volunteer",
            started_at="2026-01-01"
        )

        self.education = Education.objects.create(
            institution="Universitas Indonesia",
            field_of_study="Information Systems",
            started="2025-08-01",
            ended=None,
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Open House Fasilkom UI 2026 - Expert Staff of Public Relations")
        self.assertEqual(self.experience.category, "volunteer")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, "Experience")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()

        response = self.client.get(
            reverse("main:get_experience_json")
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()

        self.assertFalse(self.experience.is_ongoing)

    def test_education_page(self):
        response = self.client.get(reverse("main:show_education"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")
        self.assertContains(response, "Education")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_education_data_appears(self):
        response = self.client.get(
            reverse("main:get_education_json"),
            HTTP_X_PORTFOLIO_SECRET=SECRET_CODE
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(
            data[0]["fields"]["institution"],
            "Universitas Indonesia"
        )
        self.assertEqual(
            data[0]["fields"]["field_of_study"],
            "Information Systems"
        )

    def test_empty_education_page(self):
        Education.objects.all().delete()

        response = self.client.get(
            reverse("main:get_education_json"),
            HTTP_X_PORTFOLIO_SECRET=SECRET_CODE
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_education_json(self):
        response = self.client.get(reverse("main:get_education_json"), HTTP_X_PORTFOLIO_SECRET=SECRET_CODE)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertContains(response, "Universitas Indonesia")
        self.assertContains(response, "Information Systems")