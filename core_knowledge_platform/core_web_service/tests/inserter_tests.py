from core_web_service.models import Tag
from django.utils import unittest
from core_web_service.models import Vote, Comment, Author
from django.contrib.auth.models import User
from core_web_service.business_logic.insert import XmlInserter
from core_web_service.models import Keyword
from core_web_service.models import ReferenceMaterial
from core_web_service.tests.xml_strings import user_xml
from core_web_service.tests.xml_strings import comment_xml
from core_web_service.tests.xml_strings import publication_xml

class InserterTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """docstring for SetUpClass"""
        self.xml_inserter = XmlInserter()
        self.vote = Vote.objects.create(vote="up")
        self.vote.save()
        self.author = Author.objects.create(name="Test", address="123-Stree", affiliation="Heriot-Watt", email="Test@test.test")
        self.author.save()
        self.comment = Comment.objects.create(title="Comment", text="Commento", vote=self.vote)
        self.comment.save()
        self.tag = Tag.objects.create(name="AI", description="Artificial Intelligence")
        self.tag.save()
        self.keyword = Keyword.objects.create(keyword="AI")
        self.keyword.save()
        #self.material = ReferenceMaterial.objects.create(publication=self.publication, name="A keyword", url="http://www.someaddress.com/", notes="Some notes")
        #self.material.save()

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="test", email="none@none.none")

    def tearDown(self):
        User.objects.all().delete()
        
    def test_modify_existing_user(self):
        user = User.objects.get(username="testuser")
        new_user = self.xml_inserter.modify_user(user_xml, user_id=user.id)
        self.assertEqual(user.id, new_user.id)

    def test_xml_user_parser(self):
        """Attempts to parse a user from xml."""
        user = self.xml_inserter.modify_user(user_xml)
        self.assertEqual(user.username, "test")
        self.assertEqual(user.email, 'Scott@scott.scott')
        self.assertNotEqual(user.password, 'test')

    def test_insert_comment(self):
        xml = comment_xml % (self.vote.id)
        comment = self.xml_inserter.modify_comment(xml)
        self.assertEqual(comment.vote, self.vote)

    def test_insert_publication_from_xml(self):
        xml = publication_xml % (self.user.id, self.author.id, self.comment.id, self.tag.id)
        publication = self.xml_inserter.modify_publication(xml)
        self.assertEqual(publication.authors.get(), self.author)
        self.assertEqual(publication.tags.get(), self.tag)
        self.assertEqual(publication.comments.get(), self.comment)
        self.assertEqual(publication.owner, self.user)
