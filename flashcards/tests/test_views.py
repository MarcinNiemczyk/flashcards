import time
from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from users.models import User
from flashcards.models import Collection, Log


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
        testuser1 = User.objects.create_user(
            username='testuser1',
            password='7,a}MXe+oTJL'
        )
        testuser2 = User.objects.create_user(
            username='testuser2',
            password='NqCJAB}N~@Wg'
        )

        number_of_collections = 13
        for collection_id in range(number_of_collections):
            collection = Collection.objects.create(
                title=f'Testuser1 collection {collection_id + 1}',
                author=testuser1
            )
            Log.objects.create(
                visitor=testuser1,
                collection=collection
            )
            # Ensure created logs have different timestamp
            time.sleep(0.05)

        Collection.objects.create(
            author=testuser2,
            title='Testuser2 collection',
        )

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser1', password='7,a}MXe+oTJL')
        response = self.client.get('/library')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser1', password='7,a}MXe+oTJL')
        response = self.client.get(reverse('library'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('library'))
        self.assertRedirects(response, '/login/?next=/library')

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='testuser1', password='7,a}MXe+oTJL')
        response = self.client.get(reverse('library'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertTemplateUsed(response, 'flashcards/library.html')

    def test_pagination_is_ten(self):
        self.client.login(username='testuser1', password='7,a}MXe+oTJL')
        response = self.client.get(reverse('library'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['collections']), 10)

    def test_lists_all_collections(self):
        self.client.login(username='testuser1', password='7,a}MXe+oTJL')
        response = self.client.get(reverse('library')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['collections']), 3)

    def test_lists_following_collections(self):
        collection = Collection.objects.get(id=14)
        collection.followers.add(User.objects.get(id=1))
        Log.objects.create(
            visitor=User.objects.get(id=1),
            collection=collection
        )
        self.client.login(username='testuser1', password='7,a}MXe+oTJL')
        response = self.client.get(reverse('library')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['collections']), 4)

    def test_not_lists_visited_collections(self):
        Log.objects.create(
            visitor=User.objects.get(id=1),
            collection=Collection.objects.get(id=14)
        )
        self.client.login(username='testuser1', password='7,a}MXe+oTJL')
        response = self.client.get(reverse('library') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['collections']), 3)

    def test_collections_order_by_latest_visit(self):
        log = Log.objects.get(id=5)
        log.timestamp = datetime.now()
        log.save()
        self.client.login(username='testuser1', password='7,a}MXe+oTJL')
        response = self.client.get(reverse('library'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['collections'][0], Collection.objects.get(id=5))
        self.assertEqual(response.context['collections'][1], Collection.objects.get(id=13))


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
        self.assertTemplateUsed(response, 'flashcards/add.html')
