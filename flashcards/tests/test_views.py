from django.test import TestCase
from django.urls import reverse
from users.models import User


class ExploreViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('explore'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('explore'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flashcards/explore.html')


class LibraryViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username='testuser',
            password='7,a}MXe+oTJL'
        )

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser', password='7,a}MXe+oTJL')
        response = self.client.get('/library')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser', password='7,a}MXe+oTJL')
        response = self.client.get(reverse('library'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('library'))
        self.assertRedirects(response, '/login/?next=/library')

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='testuser', password='7,a}MXe+oTJL')
        response = self.client.get(reverse('library'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertTemplateUsed(response, 'flashcards/library.html')


class AddCollectionViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username='testuser',
            password='7,a}MXe+oTJL'
        )

    def test_view_url_exists_at_desire_location(self):
        self.client.login(username='testuser', password='7,a}MXe+oTJL')
        response = self.client.get('/add')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser', password='7,a}MXe+oTJL')
        response = self.client.get(reverse('add collection'))
        self.assertEqual(response.status_code, 200)

    def test_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('add collection'))
        self.assertRedirects(response, '/login/?next=/add')

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='testuser', password='7,a}MXe+oTJL')
        response = self.client.get(reverse('add collection'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertTemplateUsed(response, 'flashcards/add_collection.html')
