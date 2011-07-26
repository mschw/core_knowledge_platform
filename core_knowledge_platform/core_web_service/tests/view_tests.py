import pdb
from core_web_service.models import Author
from django.utils import unittest
from django.test.client import Client
from django.core.urlresolvers import reverse
from core_web_service.views import RestView
from core_web_service.tests.xml_strings import author_xml, user_xml, publication_xml
from core_web_service.models import User

class ViewTests(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='unittest', password='unit', email='unit@test.test')
        self.author = Author.objects.create(name="test", address="test", email="test@test.test")
        self.client.login(username="unittest", password="unit")

    def tearDown(self):
        User.objects.all().delete()
        Author.objects.all().delete()

    def test_get_publications_returns_200(self):
        result = self.client.get(reverse('core_web_service.views.publications'), HTTP_ACCEPT='application/xml', CONTENT_TYPE='application/xml')
        self.assertEqual(result.status_code, RestView.OK_STATUS)

    def test_delete_list_of_publications_not_allowed(self):
        result = self.client.delete(reverse('core_web_service.views.publications'))
        self.assertEqual(result.status_code, RestView.METHOD_NOT_ALLOWED_STATUS)

    def test_put_list_of_publications_not_allowed(self):
        result = self.client.put(reverse('core_web_service.views.publications'))
        self.assertEqual(result.status_code, RestView.METHOD_NOT_ALLOWED_STATUS)

    def test_post_list_of_publications_without_data_returns_400(self):
        result = self.client.post('/publication/', HTTP_ACCEPT='application/xml', CONTENT_TYPE='application/xml')
        self.assertEqual(result.status_code, RestView.BAD_REQUEST_STATUS)

    def test_request_with_invalid_content_type_returns_415(self):
        result = self.client.get(reverse('core_web_service.views.publications'), HTTP_ACCEPT='application/xml', CONTENT_TYPE='invalid')
        self.assertEqual(result.status_code, RestView.UNSUPPORTED_MEDIA_TYPE_STATUS)

    def test_request_with_invalid_accept_header_returns_415(self):
        result = self.client.get(reverse('core_web_service.views.publications'), HTTP_ACCEPT='invalid', CONTENT_TYPE='application/xml')
        self.assertEqual(result.status_code, RestView.UNSUPPORTED_MEDIA_TYPE_STATUS)

    def test_request_without_content_type_returns_415(self):
        result = self.client.get(reverse('core_web_service.views.publications'), HTTP_ACCEPT='application/xml')
        self.assertEqual(result.status_code, RestView.UNSUPPORTED_MEDIA_TYPE_STATUS)

    def test_request_without_accept_header_returns_415(self):
        result = self.client.get(reverse('core_web_service.views.publications'), CONTENT_TYPE='application/xml')
        self.assertEqual(result.status_code, RestView.UNSUPPORTED_MEDIA_TYPE_STATUS)

    def test_insert_user_from_view_returns_200(self):
        result = self.client.post('/user/', user_xml, content_type='application/xml', HTTP_ACCEPT='application/xml')
        self.assertEqual(result.status_code, RestView.CREATED_STATUS)

    def test_login_valid_credential(self):
        result = self.client.post(reverse('core_web_service.views.login'), {'username': 'unittest', 'password': 'unit'}, HTTP_ACCEPT='application/xml')
        self.assertEqual(result.status_code, RestView.OK_STATUS)

    def test_login_invalid_credential(self):
        result = self.client.post(reverse('core_web_service.views.login'), {'username': 'invalid', 'password': 'test'}, HTTP_ACCEPT='application/xml')
        self.assertEqual(result.status_code, RestView.BAD_REQUEST_STATUS)

    def test_post_author_returns_200(self):
        result = self.client.post(reverse('core_web_service.views.authors'), author_xml, content_type='application/xml', HTTP_ACCEPT='application/xml')
        self.assertEqual(result.status_code, RestView.CREATED_STATUS)

    def test_post_author_not_logged_in_returns_200(self):
        self.client.logout()
        result = self.client.post(reverse('core_web_service.views.authors'), author_xml, content_type='application/xml', HTTP_ACCEPT='application/xml')
        self.assertEqual(result.status_code, RestView.CREATED_STATUS)

    def test_put_author_to_change_returns_200(self):
        id = self.author.id
        url = '/author/%s' % (id)
        result = self.client.put(url, author_xml, content_type='application/xml', HTTP_ACCEPT='application/xml')
        self.assertEqual(result.status_code, RestView.OK_STATUS)

    def test_restricted_method_without_login(self):
        self.client.logout()
        result = self.client.put('/publication/1', publication_xml, content_type='application/xml', HTTP_ACCEPT='application/xml')
        self.assertEqual(result.status_code, 302)
