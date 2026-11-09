from django.test import TestCase

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Project
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import Group, User


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experiences")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        # Halaman kini memuat data lewat API (client-side), jadi cek struktur
        # halaman di sini dan konten data lewat endpoint API.
        response = self.client.get(reverse("main:show_experiences"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, f'href="{reverse("main:show_main")}#hero"')

    def test_experience_data_is_available_from_api(self):
        response = self.client.get(reverse("api:experience-list"))

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data[0]["title"], self.experience.title)
        self.assertEqual(data[0]["description"], self.experience.description)
        self.assertEqual(data[0]["category_display"], "Part-Time")
        self.assertTrue(data[0]["is_current"])

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("api:experience-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("api:experience-list"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertFalse(response.json()[0]["is_current"])

    def test_project_url_is_accessible(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")

    def test_project_data_is_available_from_api(self):
        project = Project.objects.create(
            title="Fisiomate",
            description="Aplikasi untuk membantu Rehabilitasi Fisioterapi",
            image="/static/img/project-fisiomate.webp",
            url_link="https://fisiomate.leficullen.xyz"
        )

        response = self.client.get(reverse("api:project-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["id"], str(project.id))
        self.assertEqual(response.json()[0]["title"], project.title)
        self.assertEqual(response.json()[0]["description"], project.description)
        self.assertEqual(response.json()[0]["image"], project.image)
        self.assertEqual(response.json()[0]["url_link"], project.url_link)

    def test_project_data_empty(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response,"Belum ada proyek yang ditambahkan")

class ExperienceAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(username="owner", password="pass12345")
        self.editor = User.objects.create_user(username="editor", password="pass12345")
        self.user = User.objects.create_user(username="user", password="pass12345")

        editor_group = Group.objects.create(name="Editor")
        self.editor.groups.add(editor_group)

        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP", description="Membantu mahasiswa.", category="part-time",
        )
        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse("api:experience-detail", args=[self.experience.id])
        self.star_url = reverse("api:experience-star", args=[self.experience.id])
        self.payload = {"title": "Magang Backend", "description": "Bangun API.", "category": "internship"}

    def test_visitor_can_read(self):
        self.assertEqual(self.client.get(self.list_url).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_visitor_cannot_create(self):
        response = self.client.post(self.list_url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)

    def test_regular_user_cannot_create(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.list_url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)

    def test_regular_user_cannot_delete(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())

    # EDITOR: boleh PATCH, tidak boleh create & delete
    def test_editor_can_patch(self):
        self.client.force_authenticate(self.editor)
        response = self.client.patch(self.detail_url, {"title": "Judul Baru"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Judul Baru")

    def test_editor_cannot_create(self):
        self.client.force_authenticate(self.editor)
        response = self.client.post(self.list_url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)

    def test_editor_cannot_delete(self):
        self.client.force_authenticate(self.editor)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())

    # OWNER: boleh create & delete
    def test_owner_can_create(self):
        self.client.force_authenticate(self.owner)
        response = self.client.post(self.list_url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Experience.objects.count(), 2)

    def test_owner_can_delete(self):
        self.client.force_authenticate(self.owner)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Experience.objects.filter(pk=self.experience.pk).exists())

    def test_create_invalid_input(self):
        self.client.force_authenticate(self.owner)
        response = self.client.post(self.list_url, {**self.payload, "title": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Experience.objects.count(), 1)

    def test_visitor_cannot_star(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_toggle_star(self):
        self.client.force_authenticate(self.user)
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_200_OK)
        self.assertIn(self.user, self.experience.starred_by.all())
        self.client.post(self.star_url)   # toggle lagi
        self.assertNotIn(self.user, self.experience.starred_by.all())


class ExperienceCSRFTest(APITestCase):
    def setUp(self):
        User.objects.create_superuser(username="owner", password="pass12345")
        self.experience = Experience.objects.create(
            title="Exp", description="desc", category="part-time",
        )
        self.detail_url = reverse("api:experience-detail", args=[self.experience.id])

    def test_login_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="pass12345")
        response = client.patch(self.detail_url, {"title": "Tanpa CSRF"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
