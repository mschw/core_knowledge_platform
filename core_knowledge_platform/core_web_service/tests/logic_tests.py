from django.utils import unittest
from core_web_service.models import Publication
from django.contrib.auth.models import User
from core_web_service.business_layer import insert_bibtex_publication, MissingValueException, validate_required_fields

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
        with self.assertRaises(MissingValueException):
            validate_required_fields(publication)

    def test_insert_book_bibtex(self):
        publications = insert_bibtex_publication(self.book_bibtex, self.user)
        expected_publications = [self.book]
        self.assertEqual(len(expected_publications), len(publications))
