from django.utils import unittest
from core_web_service.models import Publication
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import QueryDict
from core_web_service.business_logic.insert import insert_bibtex_publication
from core_web_service.business_logic.search import build_query
from core_knowledge_platform.core_web_service.models import MissingValueException

class BusinessLogicTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.book_bibtex = """@book{Anderson2007,
    title = {What is Web 2.0?: ideas, technologies and implications for education},
    publisher = {Citeseer},
    year = {2007},
    author = {Andersen, P.},
    booktitle = {Technology},
    file = {:media/datapart/Dokumente/eBooks/master\_thesis/Articles/10.1.1.108.9995.pdf:pdf},
    keywords = {Web 2.0},
    url = {http://www.jisc.ac.uk/media/documents/techwatch/tsw0701b.pdf}
}"""
        self.book = Publication(
                title = "What is Web 2.0?: ideas, technologies and implications for education",
                publisher = "Citeseer",
                year = 2007,
                booktitle = "Technology",
                )
        self.invalid_bibtex = """@book{Anderson2007,
    publisher = {Citeseer},
    year = {2007},
    author = {Andersen, P.},
    booktitle = {Technology},
    file = {:media/datapart/Dokumente/eBooks/master\_thesis/Articles/10.1.1.108.9995.pdf:pdf},
    keywords = {Web 2.0},
    mendeley-tags = {Web 2.0},
    url = {http://www.jisc.ac.uk/media/documents/techwatch/tsw0701b.pdf}
}"""
        self.user = User(username="Tester")

    def test_raise_exception_incomplete_publication(self):
        publication = Publication(publication_type="book")
        self.assertRaises(MissingValueException, publication.validate_required_fields)

    def test_insert_book_bibtex(self):
        publications = insert_bibtex_publication(self.book_bibtex, self.user)
        expected_publications = [self.book]
        self.assertEqual(len(expected_publications), len(publications))

    def test_build_query_one_argument(self):
        dictionary = {'key': 'value'}
        result = build_query(dictionary)
        q = [Q(**({'key__icontains': 'value'}))]
        self.assertEqual(q[0].children, result[0].children)

    def test_build_query_two_arguements(self):
        dictionary = {'key': 'value', 'key2': 'value2'}
        result = build_query(dictionary)
        q = [Q(**({'key__icontains': 'value'})), Q(**({'key2__icontains': 'value2'}))]
        self.assertEqual(q[0].children, result[1].children)
        self.assertEqual(q[1].children, result[0].children)
    
    def test_build_query_from_querydict(self):
        """Testing query building from querydict."""
        dictionairy = QueryDict("key=value")
        result = build_query(dictionairy)
        q = [Q(**{'key__icontains': u'value'})]
        self.assertEqual(q[0].children, result[0].children)

    def test_build_query_from_querydict_two_values(self):
        """docstring for test_build_query_from_querydict_two_values"""
        dictionary = QueryDict("key=value&key2=value2")
        result = build_query(dictionary)
        q = [Q(**({u'key__icontains': u'value'})), Q(**({u'key2__icontains': u'value2'}))]
        self.assertEqual(q[0].children, result[1].children)
        self.assertEqual(q[1].children, result[0].children)

    def test_build_query_without_search_values(self):
        """Raise AttributeError if no arguments are provided."""
        dictionairy = {'key': None}
        self.assertRaises(AttributeError, build_query, dictionairy)

