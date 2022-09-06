import time
from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from users.models import User
from flashcards import LANGUAGES
from flashcards.models import Collection, Flashcard, Log


class ExploreViewTest(TestCase):
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
        for i in range(number_of_collections):
            Collection.objects.create(
                title=f'Testuser1 collection {i + 1}',
                author=testuser1,
                public=True,
                language1=LANGUAGES[i].lower(),
                language2=LANGUAGES[i+1].lower()
            )
        Collection.objects.create(
            author=testuser2,
            title='Testuser2 collection',
            public=True,
            language1='arabic',
            language2='albanian'
        )

        # Add one non-public collection per user
        Collection.objects.create(
            author=testuser1,
            title='Testuser1 private collection',
        )
        Collection.objects.create(
            author=testuser2,
            title='Testuser2 private collection',
        )

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

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('explore'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['collections']), 10)

    def test_lists_all_collections(self):
        response = self.client.get(reverse('explore') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['collections']), 4)

    def test_user_cannot_see_own_collections(self):
        self.client.login(username='testuser1', password='7,a}MXe+oTJL')
        response = self.client.get(reverse('explore'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['collections']), 1)

    def test_collections_default_order_by_reversed_id(self):
        response = self.client.get(reverse('explore'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['collections'][0], Collection.objects.get(id=14))
        self.assertEqual(response.context['collections'][1], Collection.objects.get(id=13))

    def test_filter_by_title(self):
        response = self.client.get(reverse('explore'), {'title': '2'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['collections']), 3)

    def test_filter_sort(self):
        response = self.client.get(reverse('explore'), {'sort': 'oldest'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['collections'][0], Collection.objects.get(id=1))
        self.assertEqual(response.context['collections'][1], Collection.objects.get(id=2))

    def test_filter_languages(self):
        response = self.client.get(reverse('explore'), {'language1': 'albanian'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['collections']), 3)

    def test_filter_both_languages(self):
        response = self.client.get(reverse('explore'), {
            'language1': 'albanian',
            'language2': 'arabic'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['collections']), 2)

    def test_filters_all_together(self):
        response = self.client.get(reverse('explore'), {
            'title': '1',
            'sort': 'oldest',
            'language1': 'albanian',
            'language2': 'arabic',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['collections']), 1)

    def test_pagination_with_filters_is_ten(self):
        response = self.client.get(reverse('explore'), {
            'title': 'collection',
            'sort': 'oldest',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['collections']), 10)


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
                author=testuser1,
                language1='english',
                language2='english'
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

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser', password='7,a}MXe+oTJL')
        response = self.client.get(reverse('add collection'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertTemplateUsed(response, 'flashcards/add.html')


class EditCollectionViewTest(TestCase):
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

        Collection.objects.create(
            author=testuser1,
            title='Testuser1 private collection',
            language1='english',
            language2='english'
        )

        Collection.objects.create(
            author=testuser2,
            title='Testuser2 private collection',
            language1='english',
            language2='english'
        )
        Collection.objects.create(
            author=testuser2,
            title='Testuser2 public collection',
            public=True,
            language1='english',
            language2='english'
        )

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser1', password='7,a}MXe+oTJL')
        response = self.client.get('/edit/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['collection'].id, 1)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser1', password='7,a}MXe+oTJL')
        response = self.client.get(reverse('edit', kwargs={'collection_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['collection'].id, 1)

    def test_view_url_accessible_only_for_author(self):
        self.client.login(username='testuser1', password='7,a}MXe+oTJL')
        response = self.client.get(reverse('edit', kwargs={'collection_id': 2}))
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('edit', kwargs={'collection_id': 3}))
        self.assertEqual(response.status_code, 403)

    def test_incorrect_collection_url(self):
        self.client.login(username='testuser1', password='7,a}MXe+oTJL')
        response = self.client.get(reverse('edit', kwargs={'collection_id': 4}))
        self.assertEqual(response.status_code, 404)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser1', password='7,a}MXe+oTJL')
        response = self.client.get(reverse('edit', kwargs={'collection_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertTemplateUsed(response, 'flashcards/edit.html')


class CollectionViewTest(TestCase):
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

        Collection.objects.create(
            author=testuser1,
            title='Testuser1 private collection',
            language1='english',
            language2='english'
        )
        Collection.objects.create(
            author=testuser2,
            title='Testuser2 private collection',
            language1='english',
            language2='english'
        )
        Collection.objects.create(
            author=testuser2,
            title='Testuser2 public collection',
            public=True,
            language1='english',
            language2='english'
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/collection/3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['collection'].id, 3)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('collection', kwargs={'collection_id': 3}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['collection'].id, 3)

    def test_incorrect_collection_url(self):
        response = self.client.get(reverse('collection', kwargs={'collection_id': 4}))
        self.assertEqual(response.status_code, 404)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('collection', kwargs={'collection_id': 3}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flashcards/collection.html')

    def test_private_collections_are_not_accessible(self):
        response = self.client.get(reverse('collection', kwargs={'collection_id': 1}))
        self.assertEqual(response.status_code, 403)

    def test_user_can_access_own_private_collections(self):
        self.client.login(username='testuser1', password='7,a}MXe+oTJL')
        response = self.client.get(reverse('collection', kwargs={'collection_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['collection'].id, 1)

    def test_user_cannot_access_other_user_private_collection(self):
        self.client.login(username='testuser1', password='7,a}MXe+oTJL')
        response = self.client.get(reverse('collection', kwargs={'collection_id': 2}))
        self.assertEqual(response.status_code, 403)


class ProfileViewTest(TestCase):
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
            Collection.objects.create(
                title=f'Collection {collection_id + 1}',
                author=testuser1,
                language1='english',
                language2='english'
            )
        Collection.objects.create(
            author=testuser1,
            title='Testuser1 public collection',
            public=True,
            language1='english',
            language2='english'
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/profile/testuser1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('profile', kwargs={'username': 'testuser1'}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('profile', kwargs={'username': 'testuser1'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flashcards/profile.html')

    def test_view_shows_only_public_collections(self):
        response = self.client.get(reverse('profile', kwargs={'username': 'testuser1'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['collections']), 1)
        # Test view for logged user
        self.client.login(username='testuser2', password='NqCJAB}N~@Wg')
        response = self.client.get(reverse('profile', kwargs={'username': 'testuser1'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['collections']), 1)

    def test_view_pagination_is_ten(self):
        self.client.login(username='testuser1', password='7,a}MXe+oTJL')
        response = self.client.get(reverse('profile', kwargs={'username': 'testuser1'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['collections']), 10)

    def test_view_lists_all_collections(self):
        self.client.login(username='testuser1', password='7,a}MXe+oTJL')
        response = self.client.get(reverse('profile', kwargs={'username': 'testuser1'}) + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['collections']), 4)


class LearnViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = User.objects.create_user(
            username='testuser1',
            password='7,a}MXe+oTJL'
        )
        User.objects.create_user(
            username='testuser2',
            password='NqCJAB}N~@Wg'
        )
        number_of_flashcards = 3

        collection1 = Collection.objects.create(
            author=testuser1,
            title='Testuser1 private collection',
            public=False,
            language1='english',
            language2='english'
        )
        for i in range(number_of_flashcards):
            Flashcard.objects.create(
                task=f'task{i}',
                solution=f'solution{i}',
                collection=collection1
            )

        collection2 = Collection.objects.create(
            author=testuser1,
            title='Testuser1 public collection',
            public=True,
            language1='english',
            language2='english'
        )
        for i in range(number_of_flashcards):
            Flashcard.objects.create(
                task=f'task{i}',
                solution=f'solution{i}',
                collection=collection2
            )


    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser1', password='7,a}MXe+oTJL')
        response = self.client.get('/learn/1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser1', password='7,a}MXe+oTJL')
        response = self.client.get(reverse('learn', kwargs={'collection_id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser1', password='7,a}MXe+oTJL')
        response = self.client.get(reverse('learn', kwargs={'collection_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flashcards/learn.html')

    def test_view_private_collection_not_accessible_for_others(self):
        self.client.login(username='testuser2', password='NqCJAB}N~@Wg')
        response = self.client.get(reverse('learn', kwargs={'collection_id': 1}))
        self.assertEqual(response.status_code, 403)

    def test_view_user_can_learn_from_public_collections(self):
        self.client.login(username='testuser2', password='NqCJAB}N~@Wg')
        response = self.client.get(reverse('learn', kwargs={'collection_id': 2}))
        self.assertEqual(response.status_code, 200)
        
    def test_view_lists_all_flashcards(self):
        self.client.login(username='testuser1', password='7,a}MXe+oTJL')
        response = self.client.get(reverse('learn', kwargs={'collection_id': 1}))
        self.assertEqual(response.context['collection'].flashcards.count(), 3)
