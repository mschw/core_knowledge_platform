import pdb
from django.contrib.auth.models import User
from django.utils import unittest

from core_web_service.business_logic.insert import XmlInserter
from core_web_service.models import Tag, Vote, Comment, Author, Keyword, Publication, PeerReviewTemplate
from core_web_service.tests.xml_strings import user_xml, comment_xml, publication_xml, template_xml
from core_web_service.tests.xml_strings import peerreview_xml
from core_web_service.tests.xml_strings import author_xml
from core_web_service.tests.xml_strings import rating_xml
from core_web_service.tests.xml_strings import papergroup_xml
from core_web_service.tests.xml_strings import vote_xml
from core_web_service.tests.xml_strings import downvote_xml
from core_web_service.tests.xml_strings import keyword_xml
from core_web_service.tests.xml_strings import invalid_email_user_xml


class InserterTests(unittest.TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="test", email="none@none.none")
        self.user2 = User.objects.create_user(username="testuser2", password="test", email="none@none.none")
        self.xml_inserter = XmlInserter()

        self.author = Author.objects.create(name="Test", address="123-Stree", affiliation="Heriot-Watt", email="Test@test.test")
        self.author.save()

        self.tag = Tag.objects.create(name="AI", description="Artificial Intelligence")
        self.tag.save()

        self.keyword = Keyword.objects.create(keyword="AI")
        self.keyword.save()

        self.publication = Publication(title="A publication")
        self.publication.owner = self.user
        self.publication.save()
        self.publication.authors.add(self.author)

        self.comment = Comment.objects.create(title="Comment", text="Commento", publication=self.publication)
        self.comment.user = self.user2
        self.comment.save()
        self.vote = Vote(comment=self.comment)
        self.vote.votetype = 0
        self.vote.caster = self.user
        self.vote.save()

        self.template = PeerReviewTemplate()
        self.template.template_text = "Some text"
        self.template.save()

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

    def test_insert_user_invalid_email(self):
        """Attempts to insert a user with an invalid email."""
        user = self.xml_inserter.modify_user(invalid_email_user_xml)

    def test_insert_comment(self):
        xml = comment_xml % (self.publication.id, self.user.id, self.vote.id)
        comment = self.xml_inserter.modify_comment(xml, user_id=self.user.id)
        self.assertNotEqual(comment.vote_set, None)

    def test_insert_publication_from_xml(self):
        xml = publication_xml % (self.user.id, self.author.id, self.comment.id, self.tag.id)
        publication = self.xml_inserter.modify_publication(xml)
        self.assertEqual(publication.authors.get(), self.author)
        self.assertEqual(publication.tags.get(), self.tag)
        self.assertEqual(publication.owner, self.user)

    def test_insert_peer_review_template_from_xml(self):
        xml = template_xml
        text = """A template.

        With linebreaks.

        An stuff like that."""
        template = self.xml_inserter.modify_peerreviewtemplate(xml)
        self.assertEqual(template.template_text, text)

    def test_insert_peer_review_from_xml(self):
        xml = peerreview_xml % (self.user.id, self.publication.id, self.template.id)
        peerreview = self.xml_inserter.modify_peerreview(xml)
        self.assertEqual(peerreview.peer_reviewer, self.user)
        self.assertEqual(peerreview.publication, self.publication)
        self.assertEqual(peerreview.template, self.template)
        self.assertEqual(peerreview.title, 'The reviewing of stuff.')

    def test_insert_author_from_xml(self):
        xml = author_xml
        author = self.xml_inserter.modify_author(xml)
        self.assertEqual(author.name, 'Jack')
        self.assertEqual(author.address, '123 Funroad')

    def test_insert_rating_from_xml(self):
        xml = rating_xml % (self.publication.id)
        rating = self.xml_inserter.modify_rating(xml)
        self.assertEqual(rating.rating, '5')

    def test_insert_papergroup_from_xml(self):
        xml = papergroup_xml % (self.user.id, self.user2.id, self.tag.id, self.publication.id)
        papergroup = self.xml_inserter.modify_papergroup(xml)
        self.assertEqual(papergroup.description, 'Papergroup of nature.')
        self.assertEqual(papergroup.title, 'Nature papergroup.')
        self.assertEqual(papergroup.blind_review, '1')
        self.assertEqual(papergroup.publications.all()[0], self.publication)

    def test_insert_upvote_for_comment(self):
        xml = vote_xml % (self.user.id, self.comment.id)
        vote = self.xml_inserter.modify_vote(xml)
        self.assertEqual('upvote', vote.votetype)
        self.assertEqual(vote.caster, self.user)
        self.assertEqual(self.comment, vote.comment)
        self.assertEqual(self.user2.profile.esteem.value, 20)

    def test_insert_downvote_for_comment(self):
        xml = downvote_xml % (self.user.id, self.comment.id)
        vote = self.xml_inserter.modify_vote(xml)
        self.assertEqual('downvote', vote.votetype)
        self.assertEqual(vote.caster, self.user)
        self.assertEqual(self.comment, vote.comment)

    def test_insert_keyword_from_xml(self):
        xml = keyword_xml
        keyword = self.xml_inserter.modify_keyword(xml)
        self.assertEqual(keyword.keyword, "Some keyword.")

    def test_modify_keyword_from_xml(self):
        xml = keyword_xml
        kw = Keyword.objects.create(keyword='test')
        keyword = self.xml_inserter.modify_keyword(xml, kw.id)
        self.assertEqual(keyword.keyword, 'Some keyword.')
