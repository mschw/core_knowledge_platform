import re

from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from core_web_service.models import Author, Comment, Esteem, PeerReview, PeerReviewTemplate, Publication, Tag, Rating, ReferenceMaterial, User
import business_layer as application_logic

# Create your views here.

nonalpha_re = re.compile('[^A-Z]')
service_url = '127.0.0.1:8000'


class RestView(object):
    """A superclass for RESTlike views.
    
    The class will call the appropriate method of a subclass based on the
    HTTP-request: get, post, put, ...
    
    Subclasses need to set the allowed methods in a tuple *allowed_methods*.
    
    Attributes:
        allowed_methods: lists the HTTP-methods a subclass will respond to.
        OK_STATUS: the HTTP-ok status code (200).
        CREATED_STATUS: the HTTP-created status code (201).
        NO_CONTENT_STATUS: the HTTP-no-content status code (204).
        BAD_REQUEST_STATUS: the HTTP-bad-request status code (400).
        UNAUTHORIZED_STATUS: the HTTP-unauthorized status code (401).
        FORBIDDEN_STATUS: the HTTP-forbidden status code (403).
        METHOD_NOT_ALLOWED_STATUS: the HTTP-method-not-allowed status (405).
        UNSUPPORTED_MEDIA_TYPE_STATUS: the HTTP-unsupported-media type status code (415).
        INTERNAL_SERVER_ERROR_STATUS: the HTTP-internal-server-error status code (500).
    """

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

    def __call__(self, request, *args, **kwargs):
        """Calls the appropriate function corresponding to the HTTP-method."""
        method = nonalpha_re.sub('', request.method.upper())
        if not method in self.allowed_methods:
            return self.method_not_allowed(method)
        return getattr(self, method)(request, *args, **kwargs)

    def method_not_allowed(self, method):
        """Returns a response indicating that the called method is not allowed."""
        response = HttpResponse('The called method is not allowed on this resouce: %s' % (method))
        response.status_code = self.METHOD_NOT_ALLOWED_STATUS
        return response

    def unsupported_format_requested(self, formats):
        """Return a message stating that none of the accepted formats can be returned by the service."""
        response = HttpResponse('The allow response types are not supported by the service: %s' % (formats))
        response.status_code = self.UNSUPPORTED_MEDIA_TYPE_STATUS
        return response

    def render_response(self, request, template_name, dictionary):
        """Render an appropriate template an returns the response object.

        Will determine which template to use based on the HTTP accept header.
        Loads the type of template for the given name and will render it.

        Attributes:
            request: the django request object.
            template_name: the name of the template that needs to be loaded.
            dictionary: a dictionary containing specific values of the subclass that need to be replaced in the template.

        Returns:
            response: the response object with the rendered template.
        """
        response_type = self._get_allowed_response_types(request)
        dictionary['url'] = service_url
        Context(dictionary)
        for response in response_type:
            # TODO: the first that is encountered will be used to render a response.
            if 'xml' in response.lower():
                suffix = 'xml'
                break
            elif 'json' in response.lower():
                suffix = 'json'
                break
        if not suffix:
            return self.unsupported_format_requested(response_type)
        suffix = ".%s" % (suffix)
        template = get_template(template_name + suffix)
        response = template.render(Context(dictionary))
        response.status_code = 200
        return HttpResponse(response)

    def _get_allowed_response_types(self, request):
        """Will return a list of all allowed responses."""
        accept_header = request.META['HTTP_ACCEPT']
        list_of_values = accept_header.split(',')
        return list_of_values


class Authors(RestView):
    """Object to handle requests directed to the Authors resource."""
    allowed_methods = ('GET')

    def GET(self, request):
        """Returns a list of links to all authors in the system."""
        author_list = Author.objects.all()
        values = {'author_list': author_list}
        response = self.render_response(request, 'authors', values)
        return response


class AuthorDetail(RestView):
    """Object to handle requests directet to a particular author resource."""
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')

    def GET(self, request, author_id):
        """Returns the details for a particular author."""
        try:
            author = Author.objects.get(id=author_id)
            values = {'author': author}
            response = self.render_response(request, 'author', values)
        except Author.DoesNotExist:
            response = "The author with ID: %s does not exist." % (author_id)
            response.status_code = self.NOT_FOUND_STATUS
        return response

    def POST(self):
        """Creates a new author and returns the resource-url."""
        pass

    def PUT(self):
        """Modifies an existing author resource."""
        pass

    def DELETE(self):
        """Deletes an existing author resource."""
        pass


class Comments(RestView):
    """Handles request for lists of comments."""
    allowed_methods = ("GET")

    def GET(self, request, publication_id):
        """Return a list of all comments for a given publication."""
        try:
            publication = Publication.objects.get(id=publication_id)
            comment = Comment.objects.get(publication=publication)
            values = {'comment': comment}
            response = self.render_response(request, 'comments', values)
        except Publication.DoesNotExist:
            response = "The publication with ID %s does not exist" % (publication_id)
            response.status_code = self.NOT_FOUND_STATUS
        return response


class CommentDetail(RestView):
    """Handles requests for a specific comment."""
    allowed_methods = ("GET", "POST", "PUT", "DELETE")

    def GET(self, request, comment_id):
        """Return details for a particular comment."""
        try:
            comment = Comment.objects.get(id=comment_id)
            values = {'comment': comment}
            response = self.renders_response(request, 'comment', values)
        except Comment.DoesNotExist:
            response = "The comment with id %s does not exist" % (comment_id)
            response.status_code = self.NOT_FOUND_STATUS
        return response

    def POST(self):
        """docstring for POST"""
        pass

    def PUT(self):
        """docstring for PUT"""
        pass
    
    def DELETE(self):
        """docstring for DELETE"""
        pass


class EsteemDetail(RestView):
    """Handles requests for esteem values of a user."""
    allowed_methods = ("GET", "POST", "PUT")
    
    def GET(self, request, user_id, tag_id=None):
        """Return esteem for a certain user and a certain tag.
        
        Attributes:
            user_id: the id of the user.
            tag_id: the id of the tag.
        """
        try:
            if not tag_id:
                user = User.objects.get(id=user_id)
                esteem = user.esteem_set
                values = {'esteem': esteem}
                response = self.render_response(request, 'esteem', values)
            else:
                esteem = Esteem.objects.filter(user__id=user_id, tag__id=tag_id)
                values = {'esteem': esteem}
                response = self.render_response(request, 'esteem', values)
        except User.DoesNotExist:
            response = "The user with ID %s does not exist" % (user_id)
            response.status_code=self.NOT_FOUND_STATUS
        except Tag.DoesNotExist:
            response = "The tag with ID %s does not exist" % (tag_id)
            response.status_code=self.NOT_FOUND_STATUS
        except Esteem.DoesNotExist:
            response = "No esteem found for user with ID %s and tag with ID %s" % (user_id, tag_id)
            response.status_code=self.NOT_FOUND_STATUS
        return response

    def POST():
        """docstring for POST"""
        pass

    def PUT(self):
        """docstring for PUT"""
        pass


class PeerReviews(RestView):
    """Returns list of peer reviews."""
    allowed_methods = ("GET")

    def GET(self, request, publication_id):
        """Return a list of peer reviews for a certain publication."""
        try:
            peer_reviews = PeerReview.objects.filter(publication__id=publication_id)
            values = {'peerreviews': peer_reviews}
            response = self.render_response(request, 'peerreviews', values)
        except PeerReview.DoesNotExist:
            response = "No peer reviews exist for publicaiton with id %s" % (publication_id)
            response.status_code = self.NOT_FOUND_STATUS
        return response

class PeerReviewDetail(RestView):
    """Handle REST request for a specific peer review."""
    allowed_methods = ("GET", "POST", "PUT", "DELETE")

    def GET(self, request, peer_review_id):
        """Return details for a specific peer review."""
        try:
            peer_review = PeerReview.objects.get(id=peer_review_id)
            values = {'peerreview': peer_review}
            response = self.render_response(request, 'peerreview', values)
        except PeerReview.DoesNotExist:
            response = "Peer review with id %s does not exist" % (peer_review_id)
            response.status_code = self.NOT_FOUND_STATUS
        return response

    def POST(self, request, values):
        """docstring for POST"""
        pass

    def PUT(self, request, values):
        """docstring for PUT"""
        pass

    def DETELE(self, request, peer_review_id):
        """docstring for DETELE"""
        pass


class PeerReviewTemplates(RestView):
    """Handle REST request for lists of templates."""
    allowed_methods = ("GET")

    def GET(self, request):
        """Return a list of peer review templates."""
        peer_review_templates = PeerReviewTemplate.objects.all()
        values = {'peerreviewtemplates': peer_review_templates}
        response = self.render_response(request, 'peerreviewtemplates', values)
        return response


class PeerReviewTemplateDetail(RestView):
    """Handle REST requests for a specific template."""
    allowed_methods = ("GET", "POST", "PUT", "DELETE")

    def GET(self, request, template_id):
        """Return information about a specific template."""
        try:
            template = PeerReviewTemplate.objects.get(id=template_id)
            values = {'template': template}
            response = self.render_response(request, 'peerreviewtemplate', values)
        except PeerReviewTemplate.DoesNotExist:
            response = "Template with ID %s does not exist" % (template_id)
            response.status_code = self.NOT_FOUND_STATUS
        return response

    def POST(self, request, values):
        """"""
        pass

    def PUT(self):
        """docstring for PUT"""
        pass

    def DELETE(self):
        """docstring for DELETE"""
        pass


class Publications(RestView):
    """Class to handle rendering of the publication list view."""
    allowed_methods = ('GET')

    def GET(self, request):
        """Returns all publications stored in the database."""
        publication_list = Publication.objects.all()
        values = {'publication_list': publication_list}
        response = self.render_response(request, 'publications', values)
        return response


class PublicationDetail(RestView):
    """Object to handle rendering of the publication detail view."""
    allowed_methods = ('GET', 'PUT', 'POST', 'DELETE')

    def GET(self, request, publication_id):
        """Returns the information about the publication."""
        try:
            publication = Publication.objects.get(id=publication_id)
            values = {'publication': publication}
            response = self.render_response(request, 'publication', values)
        except Publication.DoesNotExist:
            response = "The publication with ID %s does not exist" % (publication_id)
            response.status_code = self.NOT_FOUND_STATUS
        return response

    def PUT(self, request):
        """Creates a new resource from provided values.
        Accepts key, value encoded pairs or bibtex."""
        content_type = request.META.HTTP_CONTENT_TYPE
        # TODO: use the user object to set the owner of the publication.
        publication_data = request.raw_post_data
        owner = request.user
        if 'application/x-bibtex' in content_type:
            application_logic.insert_bibtex_publication(publication_data, owner)
        else:
            application_logic.insert_publication(publication_data, owner)
        pass

    def POST(self, request):
        """Creates a new resource of the publication type.

        On successful creation the response Location header will contain the location the resource can be addressed at."""
        publication = Publication()
        publication.save()
        publication = {'publication': publication}
        response = self.render_response(request, 'publication', publication)
        response.status_code = self.CREATED_STATUS 
        response['Location'] = "%s/publication/%s" % (service_url, publication.id)
        return response

    def DELETE(self, request, publication_id):
        """Deletes the referred publication from the database."""
        publication = Publication.objects.get(id=publication_id)
        # TODO: do not allow delete when peer review or comments exist.
        publication.delete()
        response = HttpResponse("Publication with ID = %s successfully deleted." % (publication_id))
        response.status_code = self.OK_STATUS 
        return response


class RatingDetail(RestView):
    """Handle REST requests for ratings."""
    allowed_methods = ("GET", "POST", "PUT", "DELETE")

    def GET(self, rating_id):
        """docstring for GET"""
        rating = Rating.objects.get(id=rating_id)
        pass
    
    def POST(self):
        """docstring for POST"""
        pass

    def PUT(self):
        """docstring for PUT"""
        pass

    def DELETE(self):
        """docstring for DELETE"""
        pass
        


class ReferenceMaterialDetail(RestView):
    """Handle REST requests for reference material."""
    allowed_methods = ("GET", "POST", "PUT", "DELETE")

    def GET(self, material_id):
        """docstring for GET"""
        reference_material = ReferenceMaterial.objects.get(id=material_id)
        pass

    def POST(self):
        """docstring for POST"""
        pass
        
    def PUT(self):
        """docstring for PUT"""
        pass

    def DELETE(self):
        """docstring for DELETE"""
        pass


class Tags(RestView):
    """Handle REST requests for tags."""
    allowed_methods = ("GET")

    def GET(self):
        """docstring for GET"""
        pass


class TagDetail(RestView):
    """Handle REST requests for a specific tag."""
    allowed_methods = ("GET", "POST", "PUT", "DELETE")

    def GET(self):
        """docstring for GET"""
        pass

    def POST(self):
        """docstring for POST"""
        pass

    def PUT(self):
        """docstring for PUT"""
        pass

    def DELETE(self):
        """docstring for DELETE"""
        pass
        
