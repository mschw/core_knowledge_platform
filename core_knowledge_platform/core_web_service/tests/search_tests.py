from django.utils import unittest
from django.contrib.auth.models import User
from core_web_service.models import Author, Publication, Tag
from core_web_service.business_logic.search import get_related_tags

class SearchLogicTests(unittest.TestCase):

    def setUp(self):
        """Create some publications with tags."""
        owner =  User.objects.create_user(username='User', password='unit', email='unit@test.test')
        author = Author(name='An author', email="author@author.author")
        self.tag1 = Tag(name = 'AI', description = "Artificial Intelligence")
        self.tag2 = Tag(name = 'Parallel Programming', description = "Parallel Programming")
        self.pub1 = Publication(title='Pub1', tag=self.tag1, author=author, owner=owner)
        self.pub2 = Publication(title='Pub2', tag=[self.tag1, self.tag2], author=author, owner=owner)

    def tearDown(self):
        """docstring for tearDown"""
        User.objects.all().delete()
        Author.objects.all().delete()
        Tag.objects.all().delete()
        Publication.objects.all().delete()

    def test_recommended_tags(self):
        tags = get_related_tags(self.tag1)
        result = [self.tag2]
        self.assertEqual(result, tags)
