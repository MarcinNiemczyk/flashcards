from django.test import TestCase
from flashcards.models import Collection, Flashcard
from users.models import User


class CollectionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(
            username='testuser',
            password='7,a}MXe+oTJL'
        )
        Collection.objects.create(
            title='CollectionTestTitle',
            author=test_user,
        )

    def test_title_max_length(self):
        collection = Collection.objects.get(id=1)
        max_length = collection._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)

    def test_default_public_is_false(self):
        collection = Collection.objects.get(id=1)
        self.assertFalse(collection.public)

    def test_default_randomized_is_false(self):
        collection = Collection.objects.get(id=1)
        self.assertFalse(collection.randomized)

    def test_default_reversed_is_false(self):
        collection = Collection.objects.get(id=1)
        self.assertFalse(collection.reversed)

    def test_object_name_is_title(self):
        collection = Collection.objects.get(id=1)
        expected_object_name = collection.title
        self.assertEqual(str(collection), expected_object_name)


class FlashcardModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(
            username='testuser',
            password='7,a}MXe+oTJL'
        )
        collection = Collection.objects.create(
            title='CollectionTestTitle',
            author=test_user,
        )
        Flashcard.objects.create(
            task='FlashcardTestTask',
            solution='FlashcardTestSolution',
            collection=collection
        )

    def test_task_max_length(self):
        flashcard = Flashcard.objects.get(id=1)
        max_length = flashcard._meta.get_field('task').max_length
        self.assertEqual(max_length, 250)

    def test_solution_max_length(self):
        flashcard = Flashcard.objects.get(id=1)
        max_length = flashcard._meta.get_field('solution').max_length
        self.assertEqual(max_length, 250)

    def test_object_name_is_hashtag_id(self):
        flashcard = Flashcard.objects.get(id=1)
        expected_object_name = f'#{flashcard.id}'
        self.assertEqual(str(flashcard), expected_object_name)
