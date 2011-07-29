from core_web_service.business_logic.search import get_related_publications
from core_web_service.models import ResearchArea
from django.utils import unittest
from django.contrib.auth.models import User
from core_web_service.models import Author, Publication, Tag, Keyword
from core_web_service.business_logic.search import search_publications, get_related_tags, get_related_users_for_publication
from core_web_service.business_logic.search import get_related_keywords

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
        self.keyword2 = Keyword(keyword="Parallel")
        self.keyword2.save()

        self.pub1 = Publication(title='Pub1', doi='10.1.1.10')
        self.pub1.owner = self.owner
        self.pub1.save()
        self.pub1.authors.add(self.author)
        self.pub1.keywords.add(self.keyword)
        self.pub1.keywords.add(self.keyword2)
        self.pub1.tags.add(self.tag1)
        self.pub2 = Publication(title='Pub2', doi='10.1.1.10')
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

    def test_search_publications_by_keyword(self):
        keyword_query = {'keyword': 'AI'}
        publications = search_publications(keyword_terms=keyword_query)
        self.assertListEqual([self.pub1], list(publications))

    def test_search_publication_by_author(self):
        author_query = {'name': 'author'}
        publications = search_publications(author_terms=author_query)
        self.assertListEqual([self.pub1, self.pub2], list(publications))

    def test_search_publications_by_tag(self):
        tag_query = {'name': 'parallel'}
        publications = search_publications(tag_terms=tag_query)
        self.assertListEqual([self.pub2], list(publications))

    def test_search_publications_by_title(self):
        publication_query = {'title': '1'}
        publications = search_publications(publication_terms=publication_query)
        self.assertListEqual([self.pub1], list(publications))

    def test_search_publications_by_title_and_doi(self):
        publication_query = {'title': '1', 'doi': '10.1.1.10', 'searchtype': 'and'}
        publications = search_publications(publication_terms=publication_query)
        self.assertListEqual([self.pub1], list(publications))

    def test_search_publications_by_title_or_doi(self):
        publication_query = {'title': '1', 'doi': '10.1.1.10', 'searchtype': 'or'}
        publications = search_publications(publication_terms=publication_query)
        self.assertListEqual([self.pub1, self.pub2], list(publications))

    def test_search_without_matching_query(self):
        publication_query = {'title': 'no in database'}
        publications = search_publications(publication_terms=publication_query)
        self.assertListEqual([], list(publications))

    def test_get_recommended_publications(self):
        publications = get_related_publications(self.pub1)
        self.assertListEqual([self.pub2], list(publications))

    def test_recommended_tags(self):
        tags = get_related_tags(self.tag1)
        result = [self.tag2]
        self.assertEqual(result, tags)

    def test_recommended_keyword(self):
        keywords = get_related_keywords(self.keyword)
        result = [self.keyword2]
        self.assertListEqual(result, keywords)

    def test_related_users(self):
        users = get_related_users_for_publication(self.pub1)
        self.assertEqual([self.owner], users)
