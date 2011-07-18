from django.utils import unittest
from core_web_service.models import Vote
from django.contrib.auth.models import User
from core_web_service.business_logic.insert import XmlInserter

class InserterTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """docstring for SetUpClass"""
        self.xml_inserter = XmlInserter()
        self.vote = Vote.objects.create(vote="up")
        self.vote.save()
        User.objects.create_user(username="testuser", password="test", email="none@none.none")
        
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
