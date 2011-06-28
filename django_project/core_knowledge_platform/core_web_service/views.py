import re

from django.http import HttpResponse
from django.core import serializers
from core_web_service.models import Publication

# Create your views here.

nonalpha_re = re.compile('[^A-Z]')

class RestView(object):
    """Generic Rest superclass."""
    def __call__(self, request, *args, **kwargs):
        """docstring for __call__"""
        method = nonalpha_re.sub('', request.method.upper())
        if not method in self.allowed_methods:
            return self.method_not_allowed(method)
        return getattr(self, method)(request, *args, **kwargs)

    def method_not_allowed(self, method):
        """Returns a message that the method was not allowed."""
        response = HttpResponse('The called method is not allowed on this resouce: %s' % (method))
        response.status_code = 405
        return response

    def return_json(self, object_to_parse):
        """Returns a json representation of the passed object."""
        json = serializers.serialize('json', object_to_parse)
        response = HttpResponse(json, mimetype='text/json')
        return response

    def return_xml(self, object_to_parse):
        """Returns an xml-representation of the passed object."""
        xml = serializers.serialize('xml', object_to_parse)
        response = HttpResponse(xml, mimetype='text/xml')
        return response

class Publications(RestView):
    """Class to handle rendering of the publication list view."""
    allowed_methods = ('GET')

    def GET(self, request):
        """Returns all publications stored in the database."""
        publication_list = Publication.objects.all()
        response = self.return_xml(publication_list)
        return response

class PublicationDetail(RestView):
    """Object to handle rendering of the publication detail view."""
    allowed_methods = ('GET', 'PUT', 'POST', 'DELETE')

    def GET(self, request, publication_id):
        """Returns the information about the publication."""
        print "Publication ID is %s" % (publication_id)
        publication = [Publication.objects.get(id=publication_id)]
        response = self.return_xml(publication)
        return response

    def PUT(self, request):
        """Creates a new resource from provided values.
        Accepts key, value encoded pairs or bibtex."""
        content_type = request.META.HTTP_CONTENT_TYPE
        # TODO: use the user object to set the owner of the publication.
        publication_data = request.raw_post_data
        owner = request.user
        if 'application/x-bibtex' in content_type:
            logic.insert_bibtex_publication(publication_data, owner)
        else:
            logic.insert_publication(publication_data, owner)
        pass

    def POST(self, request):
        """Creates a new resource of the publication type and returns the url to it."""
        publication = Publication()
        pass

    def DELETE(self, request):
        """docstring for DELETE"""
        pass
