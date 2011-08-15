import pdb
from django.utils import unittest
from django.contrib.auth.models import User
from core_web_service.models import Publication
from core_web_service.business_logic.metadata_decorators import OaiPmhDecorator
from core_web_service.business_logic.insert import InvalidDataException


class DecoratorTests(unittest.TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(username='testuser',
                email='none@none.none', password='none')
        self.publication = Publication(title='Some Publication')

        self.publication.title = "Some publication"
        self.publication.owner = self.owner
        self.publication.save()

        self.decorator = OaiPmhDecorator()

    def tearDown(self):
        User.objects.all().delete()
        Publication.objects.all().delete()

    @unittest.skip("Takes too long to run - CiteSeer query")
    def test_valid_doi(self):
        self.publication.doi = '10.1.1.119.2204'
        self.decorator.decorate_publication(self.publication)
        self.assertNotEqual(self.publication.decorated, None)

    def test_invalid_doi(self):
        self.publication.doi = 'wrongdoi'
        self.assertRaises(InvalidDataException, self.decorator.decorate_publication, self.publication)
