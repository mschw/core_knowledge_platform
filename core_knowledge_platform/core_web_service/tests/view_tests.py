from django.utils import unittest
from django.test.client import Client
from django.core.urlresolvers import reverse

class ViewTests(unittest.TestCase):

    OK_STATUS = 200
    CREATED_STATUS = 201
    NO_CONTENT_STATUS = 204
    BAD_REQUEST_STATUS = 400
    UNAUTHORIZED_STATUS = 401
    FORBIDDEN_STATUS = 403
    NOT_FOUND_STATUS = 404
    METHOD_NOT_ALLOWED_STATUS = 405
    UNSUPPORTED_MEDIA_TYPE_STATUS = 415
    INTERNAL_SERVER_ERROR_STATUS = 500

    def setUp(self):
        self.client = Client()

    def test_get_publications_returns_200(self):
        result = self.client.get(reverse('core_web_service.views.publications'), HTTP_ACCEPT='application/xml', CONTENT_TYPE='application/xml')
        self.assertEqual(result.status_code, self.OK_STATUS)

    def test_delete_list_of_publications_not_allowed(self):
        result = self.client.delete(reverse('core_web_service.views.publications'))
        self.assertEqual(result.status_code, self.METHOD_NOT_ALLOWED_STATUS)

    def test_put_list_of_publications_not_allowed(self):
        result = self.client.put(reverse('core_web_service.views.publications'))
        self.assertEqual(result.status_code, self.METHOD_NOT_ALLOWED_STATUS)

    def test_post_list_of_publications_returns_201(self):
        result = self.client.post('/publication', HTTP_ACCEPT='application/xml', CONTENT_TYPE='application/xml')
        self.assertEqual(result.status_code, self.CREATED_STATUS)

    def test_request_with_invalid_content_type_returns_415(self):
        result = self.client.get(reverse('core_web_service.views.publications'), HTTP_ACCEPT='application/xml', CONTENT_TYPE='invalid')
        pass
        self.assertEqual(result.status_code, self.UNSUPPORTED_MEDIA_TYPE_STATUS)

    def test_request_with_invalid_accept_header_returns_415(self):
        result = self.client.get(reverse('core_web_service.views.publications'), HTTP_ACCEPT='invalid', CONTENT_TYPE='application/xml')
        self.assertEqual(result.status_code, self.UNSUPPORTED_MEDIA_TYPE_STATUS)

    def test_request_without_content_type_returns_415(self):
        result = self.client.get(reverse('core_web_service.views.publications'), HTTP_ACCEPT='application/xml')
        self.assertEqual(result.status_code, self.UNSUPPORTED_MEDIA_TYPE_STATUS)

    def test_request_without_accept_header_returns_415(self):
        result = self.client.get(reverse('core_web_service.views.publications'), CONTENT_TYPE='application/xml')
        pass
        self.assertEqual(result.status_code, self.UNSUPPORTED_MEDIA_TYPE_STATUS)

    def test_insert_user_from_view_returns_200(self):
        xml = """<?xml version="1.0" encoding="utf-8"?>
<user xmlns="http://test/"
    xmlns:atom="http://www.w3.org/2005/atom">
    <username>
        View_Test
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
       <field>
       test
       </field>
       <field>
       test2
       </field>
    </fields>
</user>"""
        result = self.client.post(reverse('core_web_service.views.users'), xml, content_type='application/xml', HTTP_ACCEPT='application/xml')
        self.assertEqual(result.status_code, self.CREATED_STATUS)

    def test_login_valid_credential(self):
        xml = """<?xml version="1.0" encoding="utf-8"?>
<user xmlns="http://test"
    xmlns:atom="http://www.w3.org/2005/atom">
    <username>
        test
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
        result = self.client.post(reverse('core_web_service.views.users'), xml, content_type='application/xml', HTTP_ACCEPT='application/xml')
        result = self.client.post(reverse('core_web_service.views.login'), {'username': 'test', 'password': 'test'}, HTTP_ACCEPT='application/xml')
        self.assertEqual(result.status_code, self.OK_STATUS)

    def test_login_invalid_credential(self):
        result = self.client.post(reverse('core_web_service.views.login'), {'username': 'invalid', 'password': 'test'}, HTTP_ACCEPT='application/xml')
        self.assertEqual(result.status_code, self.BAD_REQUEST_STATUS)
