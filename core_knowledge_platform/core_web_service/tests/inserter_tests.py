from core_web_service.models import Tag
from django.utils import unittest
from core_web_service.models import Vote, Comment, Author
from django.contrib.auth.models import User
from core_web_service.business_logic.insert import XmlInserter
from core_web_service.models import Keyword
from core_web_service.models import ReferenceMaterial

class InserterTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """docstring for SetUpClass"""
        self.xml_inserter = XmlInserter()
        self.vote = Vote.objects.create(vote="up")
        self.vote.save()
        self.user = User.objects.create_user(username="testuser", password="test", email="none@none.none")
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
        
    def test_modify_existing_user(self):
        xml = """<?xml version="1.0" encoding="utf-8"?>
<user xmlns="http://test"
    xmlns:atom="http://www.w3.org/2005/atom">
    <username>
        testuser_new
    </username>
    <first_name>
    </first_name>
    <last_name>
    </last_name>
    <email>
        Scott@scott.scott
    </email>
    <degree>
    </degree>
    <institution>
    </institution>
    <fields>
    </fields>
</user>"""
        user = User.objects.get(username="testuser")
        new_user = self.xml_inserter.modify_user(xml, user_id=user.id)
        self.assertEqual(user.id, new_user.id)

    def test_xml_user_parser(self):
        """Attempts to parse a user from xml."""
        xml = """<?xml version="1.0" encoding="utf-8"?>
<user xmlns="http://test"
    xmlns:atom="http://www.w3.org/2005/atom">
    <username>
        John
    </username>
    <first_name>
        Scott
    </first_name>
    <last_name>
        Pilgrim
    </last_name>
    <password>
        test
    </password>
    <email>
        Scott@scott.scott
    </email>
    <degree>
    </degree>
    <institution>
    </institution>
    <fields>
    </fields>
</user>"""
        user = self.xml_inserter.modify_user(xml)
        self.assertEqual(user.username, "John")
        self.assertEqual(user.email, 'Scott@scott.scott')
        self.assertNotEqual(user.password, 'test')

    def test_insert_comment(self):
        xml = """<?xml version="1.0" encoding="utf-8"?>
<comment xmlns="http://url/"
    xmlns:atom="http://www.w3.org/2005/atom">
    <title>
        A Comment
    </title>
    <text>
        Text
    </text>
    <votes>
        <vote>
            <atom:link rel="vote" type="application/xml" href="http://url/vote/%s"/>
        </vote>
    </votes>
</comment>""" % (self.vote.id)
        comment = self.xml_inserter.modify_comment(xml)
        self.assertEqual(comment.vote, self.vote)

    def test_insert_publication_from_xml(self):
        xml="""
<?xml version="1.0" encoding="utf-8"?>
<publication xmlns="http://test/"
    xmlns:atom="http://www.w3.org/2005/atom">
    <address>
        An address
    </address>
    <booktitle>
        A title
    </booktitle>
    <chapter>
        A chapter
    </chapter>
    <edition>
        1
    </edition>
    <editor>
        An editor
    </editor>
    <howpublished>
        Not at all
    </howpublished>
    <institution>
        Some institute
    </institution>
    <isbn>
        1234-1234-1234
    </isbn>
    <journal>
        Nature
    </journal>
    <number>
        1
    </number>
    <organization>
        None
    </organization>
    <pages>
        234
    </pages>
    <publisher>
        PubCorp
    </publisher>
    <review_status>
        1
    </review_status>
    <series>
        Series
    </series>
    <publicationtype>
        Book
    </publicationtype>
    <volume>
        1
    </volume>
    <title>
        Super publication.
    </title>
    <month>
        Jan
    </month>
    <note>
        Notes notes notes notes.
    </note>
    <year>
        2010
    </year>
    <owner>
        <atom:link rel="owner" type="application/xml" href="http://test/user/%s" />
    </owner>
    <authors>    
        <author>
            <atom:link rel="author" type="application/xml" href="http://test/author/%s" />
        </author>
    </authors>
    <comments>    
        <comment>
            <atom:link rel="comment" type="application/xml" href="http://test/comment/%s" />
        </comment>
    </comments>
    <tags>
        <tag>
            <atom:link rel="tag" type="application/xml" href="http://test/tag/%s" />
        </tag>
    </tags>
    <referencematerials>
        <referencematerial>
        </referencematerial>
    </referencematerials>
    <fields>
            <somefield>
                somevalue
            </somefield>
    </fields>
</publication>""" % (self.user.id, self.author.id, self.comment.id, self.tag.id)
        publication = self.xml_inserter.modify_publication(xml)
        self.assertEqual(publication.authors.get(), self.author)
        self.assertEqual(publication.tags.get(), self.tag)
        self.assertEqual(publication.comments.get(), self.comment)
        self.assertEqual(publication.owner, self.user)
