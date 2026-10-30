import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Profile, Report
from main.forms import ProfileForm, ReportForm


class MainViewsAndModelsTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Akun utama untuk testing
        self.user1 = User.objects.create_user(
            username="testuser1",
            password="Password123!"
        )
        self.profile1 = Profile.objects.create(
            user=self.user1,
            avatar="https://example.com/avatar1.png",
            bio="Bio user 1"
        )

        # Akun kedua untuk interaksi/laporan
        self.user2 = User.objects.create_user(
            username="testuser2",
            password="Password123!"
        )
        self.profile2 = Profile.objects.create(
            user=self.user2,
            avatar="https://example.com/avatar2.png",
            bio="Bio user 2"
        )

        # Akun superuser
        self.superuser = User.objects.create_superuser(
            username="adminuser",
            password="AdminPassword123!"
        )
        self.super_profile = Profile.objects.create(
            user=self.superuser,
            avatar="",
            bio="Admin Bio"
        )

    def test_profile_creation(self):
        """Memastikan Profile terhubung ke User dan atribut tersimpan dengan benar"""
        self.assertEqual(self.profile1.user.username, "testuser1")
        self.assertEqual(self.profile1.bio, "Bio user 1")

    def test_report_model_and_str(self):
        """Memastikan Report model dan metode __str__ bekerja sesuai format"""
        report = Report.objects.create(
            reporter=self.user1,
            reported_user=self.user2,
            description="Perilaku mencurigakan"
        )
        self.assertEqual(str(report), "testuser1 -> testuser2")
        self.assertEqual(Report.objects.count(), 1)

    # ==================== 2. TEST FORMS ====================
    def test_profile_form_clean_bio_strips_tags(self):
        """Memastikan clean_bio membersihkan tag HTML (strip_tags)"""
        form = ProfileForm(data={
            "avatar": "https://example.com/avatar.jpg",
            "bio": "<script>alert('xss')</script>Halo Dunia!"
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["bio"], "alert('xss')Halo Dunia!")

    def test_report_form_empty_description_invalid(self):
        """Memastikan clean_description menolak teks kosong atau hanya spasi"""
        form = ReportForm(data={"description": "   "})
        self.assertFalse(form.is_valid())
        self.assertIn("description", form.errors)

    def test_show_main_accessible(self):
        """Memastikan halaman utama dapat diakses dan merender index.html"""
        response = self.client.get(reverse("main:show_main"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_register_get_and_post(self):
        """Memastikan alur pendaftaran membuat User baru beserta Profile-nya"""
        # GET request
        response_get = self.client.get(reverse("main:register"))
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "register.html")

        # POST request pendaftaran
        data = {
            "username": "newuser",
            "password": "ValidPassword123!",
            "password_confirm": "ValidPassword123!",
        }
        response_post = self.client.post(reverse("main:register"), {
            "username": "newuser",
            "password1": "ValidPassword123!",
            "password2": "ValidPassword123!",
        })
        self.assertEqual(response_post.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())
        new_user = User.objects.get(username="newuser")
        self.assertTrue(Profile.objects.filter(user=new_user).exists())

    def test_login_and_logout_user(self):
        """Memastikan alur login men-set cookie last_login dan logout menghapusnya"""
        response_login = self.client.post(reverse("main:login"), {
            "username": "testuser1",
            "password": "Password123!"
        })
        self.assertEqual(response_login.status_code, 302)
        self.assertIn("last_login", response_login.cookies)

        # Logout
        response_logout = self.client.get(reverse("main:logout"))
        self.assertEqual(response_logout.status_code, 302)
        self.assertEqual(response_logout.cookies["last_login"].value, "")



    def test_show_user_profile_view(self):
        """Memastikan halaman detail profil dapat dibuka dengan context yang tepat"""
        url = reverse("main:show_user_profile", args=[self.profile1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user_profile.html")
        self.assertEqual(response.context["viewed_user"], self.user1)

    def test_edit_user_profile_permission_denied_for_other_user(self):
        """User lain tidak boleh mengakses edit profil milik orang lain (403 PermissionDenied)"""
        self.client.login(username="testuser2", password="Password123!")
        url = reverse("main:edit_user_profile", args=[self.profile1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_edit_user_profile_success_by_owner(self):
        """Pemilik profil berhasil mengedit profil via form standar"""
        self.client.login(username="testuser1", password="Password123!")
        url = reverse("main:edit_user_profile", args=[self.profile1.id])
        data = {
            "avatar": "https://example.com/new_avatar.png",
            "bio": "Bio baru terupdate"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.profile1.refresh_from_db()
        self.assertEqual(self.profile1.bio, "Bio baru terupdate")