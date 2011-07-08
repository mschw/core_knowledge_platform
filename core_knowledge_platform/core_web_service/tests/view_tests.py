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
        result = self.client.get(reverse('core_web_service.views.publications'), HTTP_ACCEPT='application/xml')
        self.assertEqual(result.status_code, self.OK_STATUS)

    def test_delete_list_of_publications_not_allowed(self):
        result = self.client.delete(reverse('core_web_service.views.publications'))
        self.assertEqual(result.status_code, self.METHOD_NOT_ALLOWED_STATUS)

    def test_put_list_of_publications_not_allowed(self):
        result = self.client.put(reverse('core_web_service.views.publications'))
        self.assertEqual(result.status_code, self.METHOD_NOT_ALLOWED_STATUS)

    def test_post_list_of_publications_returns_201(self):
        result = self.client.post(reverse('core_web_service.views.publications'))
        self.assertEqual(result.status_code, self.CREATED_STATUS)

