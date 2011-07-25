from core_web_service.models import ResearchArea
from django.utils import unittest
from django.contrib.auth.models import User
from core_web_service.models import Author, Publication, Tag, Keyword
from core_web_service.business_logic.search import get_related_tags, get_related_users_for_publication

class SearchLogicTests(unittest.TestCase):

    def setUp(self):
        """Create some publications with tags."""
        self.owner =  User.objects.create_user(username='User', password='unit', email='unit@test.test')
        research_area = ResearchArea(title='AI', description='Artificial Intelligence')
        research_area.save()
        self.owner.profile.research_areas.add(research_area)
        self.author = Author(name='An author', email="author@author.author")
        self.author.save()
        self.tag1 = Tag(name = 'AI', description = "Artificial Intelligence")
        self.tag1.save()
        self.tag2 = Tag(name = 'Parallel Programming', description = "Parallel Programming")
        self.tag2.save()
        self.keyword = Keyword(keyword="AI")
        self.keyword.save()
        self.pub1 = Publication(title='Pub1')
        self.pub1.owner = self.owner
        self.pub1.save()
        self.pub1.authors.add(self.author)
        self.pub1.keywords.add(self.keyword)
        self.pub1.tags.add(self.tag1)
        self.pub2 = Publication(title='Pub2')
        self.pub2.owner = self.owner
        self.pub2.save()
        self.pub2.authors.add(self.author)
        self.pub2.tags.add(self.tag1)
        self.pub2.tags.add(self.tag2)

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

    def test_related_users(self):
        """docstring for test_related_users"""
        users = get_related_users_for_publication(self.pub1)
        self.assertEqual([self.owner], users)
