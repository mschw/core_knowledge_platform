import re
import pdb

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, QueryDict
from django.template import Context
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt

import core_web_service.business_logic.access as access
from core_web_service.business_logic import search, insert
from core_web_service.business_logic.insert import InvalidDataException
from core_web_service.business_logic.metadata_decorators import OaiPmhDecorator
from core_web_service.models import Author, Comment, Esteem, PaperGroup, PeerReview, PeerReviewTemplate, Publication, Tag, Rating, ReferenceMaterial, User, Keyword, ResearchArea, Vote

import logging
from django.template.context import RequestContext

logger = logging.getLogger('myproject.custom')

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

    allowed_formats = ('xml', 'json', 'bibtex')

    def __call__(self, request, *args, **kwargs):
        """Calls the appropriate function corresponding to the HTTP-method.
        
        """
        logger.info("Request received: %s" % (request.path))
        logger.info("User of request: %s" % (request.user.username))
        method = nonalpha_re.sub('', request.method.upper())
        if not method in self.allowed_methods:
            return RestView.method_not_allowed(method)
        try:
            accepted_format = request.META['HTTP_ACCEPT']
            valid_accept = False
            for f in RestView.allowed_formats:
                if f in accepted_format:
                    valid_accept = True
                if not valid_accept:
                    return RestView.unsupported_format_requested(accepted_format)
        except KeyError:
            return RestView.unsupported_format_requested('No format specified')
        return getattr(self, method)(request, *args, **kwargs)

    @staticmethod
    def validate_sent_format(request):
        """Determine whether a sent format is accepted by the web service.
        
        Arguments:
            request: the request objects received from Django.
            
        Returns:
            True: The format is accepted.
            False: The format is not accepted.

        """
        sent_format = RestView.get_content_type(request)
        for f in RestView.allowed_formats:
            if f in sent_format:
                return True
        return False

    @staticmethod
    def method_not_allowed(method):
        """Returns a response indicating that the called method is not allowed.
        
        Arguments:
            method: The HTTP method used to call the service.
            
        """
        logger.error("Unsupported method requested: %s" % (method))
        response = HttpResponse('The called method is not allowed on this resouce: %s'
                % (method))
        response.status_code = RestView.METHOD_NOT_ALLOWED_STATUS
        return response

    @staticmethod
    def unsupported_format_requested(formats):
        """Return a message stating that none of the accepted formats can be returned
        by the service.
        
        Arguments:
            formats: the format that was requests to be returned by the service.
        
        Returns:
            HttpResponse: A response indicating that the media type is not supported.
            
        """
        logger.error("Unsupported format requested: %s" % (formats))
        response = HttpResponse('The allowed response type is not supported by the service: %s'
                % (formats))
        response.status_code = RestView.UNSUPPORTED_MEDIA_TYPE_STATUS
        return response

    @staticmethod
    def unsupported_format_sent(sent_format):
        """Return a message stating that the sent format can not be interpreted by 
        the web service.
        
        Arguments:
            sent_format: the format sent by a request.

        Returns:
            response: HttpResponse indicating that the sent format is not supported.

        """
        logger.error("Unsupported format sent: %s" % (sent_format))
        response = HttpResponse('The sent format %s can not be understood by the\
                service - please sent one of the following: %s'
                % (sent_format, RestView.allowed_formats))
        response.status_code = RestView.BAD_REQUEST_STATUS
        return response

    @staticmethod
    def render_response(request, template_name, dictionary=None):
        """Render an appropriate template an returns the response object.

        Will determine which template to use based on the HTTP accept header.
        Loads the type of template for the given name and will render it.

        Attributes:
            request: the django request object.
            template_name: the name of the template that needs to be loaded.
            dictionary: a dictionary containing specific values of the subclass"""\
                    """that need to be replaced in the template.

        Returns:
            response: the response object with the rendered template.
        """
        if dictionary is None:
            dictionary = {}
        response_type = RestView._get_allowed_response_types(request)
        dictionary['url'] = service_url
        Context(dictionary)
        for response in response_type:
            if 'xml' in response.lower():
                suffix = 'xml'
                break
            elif 'json' in response.lower():
                suffix = 'json'
                break
        if not suffix:
            return RestView.unsupported_format_requested(response_type)
        dotted_suffix = ".%s" % (suffix)
        template = get_template(template_name + dotted_suffix)
        response = template.render(RequestContext(request, dictionary))
        return_response = HttpResponse(response)
        return_response.status_code = 200
        return_response['Content-Type'] = 'application/%s' % (suffix)
        return return_response

    @staticmethod
    def _get_allowed_response_types(request):
        """Will return a list of all allowed responses.
        
        """
        accept_header = request.META['HTTP_ACCEPT']
        list_of_values = accept_header.split(',')
        return list_of_values

    @staticmethod
    def get_content_type(request):
        """Returns the content type of a request.
        
        """
        content_type = request.META['CONTENT_TYPE']
        return content_type

    @staticmethod
    def insert_object(request, name, id=None, **kwargs):
        """Insert or update an object of type name into the database.

        Arguemnts:
            request: The django request object.
            name: the name of the object to be inserted.
            id: the id of an existing object that should be updated.
            **kwargs: any further arguments to the modify_<name> function.

        Returns:
            response: A HttpResponse object indicating whether the insertion was
            successful or not.
        
        """
        try:
            content_type = RestView.get_content_type(request)
            data = request.raw_post_data
            logger.info("Attempt to insert %s in table: %s" % (data, name))
            inserted_object = None
            inserter = insert.get_inserter(content_type)
            function = getattr(inserter, 'modify_%s' % (name))
            inserted_object = function(data, id, **kwargs)
            values = {name: inserted_object}
            response = RestView.render_response(request, name, values)
            if id:
                response.status_code = RestView.OK_STATUS
            else:
                response.status_code = RestView.CREATED_STATUS
            response['location'] = '%s/%s/%s' % (service_url, name, inserted_object.id)
        except InvalidDataException, exc:
            logger.error(exc)
            response = HttpResponse(exc.message)
            response.status_code = RestView.BAD_REQUEST_STATUS
        logger.info('Insertion successful.')
        return response


@csrf_exempt
class Authors(RestView):
    """Object to handle requests directed to the Authors resource."""
    allowed_methods = ('GET', 'POST')

    @staticmethod
    def GET(request):
        """Return a list of links to authors in the system.
        
        If queried with parameters, a search will be performed.
        
        """
        get_parameters = request.GET
        if get_parameters:
            author_list = search.search_authors(get_parameters)
        else:
            author_list = Author.objects.all()
        values = {'author_list': author_list}
        response = RestView.render_response(request, 'authors', values)
        return response

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login/')
    def POST(request):
        """Creates a new author and returns the resource-url."""
        return RestView.insert_object(request, 'author')


@csrf_exempt
class AuthorDetail(RestView):
    """Object to handle requests directet to a particular author resource."""
    allowed_methods = ('GET', 'PUT', 'DELETE')

    @staticmethod
    def GET(request, author_id):
        """Returns the details for a particular author."""
        try:
            author = Author.objects.get(id=author_id)
            values = {'author': author}
            response = RestView.render_response(request, 'author', values)
        except Author.DoesNotExist:
            response = HttpResponse("The author with ID: %s does not exist." % (author_id))
            response.status_code = RestView.NOT_FOUND_STATUS
        return response

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login/')
    def PUT(request, author_id):
        """Modifies an existing author resource."""
        return RestView.insert_object(request, 'author', author_id)

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login/')
    def DELETE(request, author_id):
        """Deletes an existing author resource."""
        author = Author.objects.get(id=author_id)
        author.delete()
        response = HttpResponse("Delete %s with id %s" % ('author', author_id))
        response.status_code = RestView.NO_CONTENT_STATUS
        return response


@csrf_exempt
class Comments(RestView):
    """Handles request for lists of comments."""
    allowed_methods = ("GET", "POST")

    @staticmethod
    def GET(request, publication_id=None):
        """Return a list of all comments for a given publication."""
        if publication_id:
            try:
                publication = Publication.objects.get(id=publication_id)
                comment = Comment.objects.get(publication=publication)
                values = {'comment': comment}
                response = RestView.render_response(request, 'comments', values)
            except Publication.DoesNotExist:
                response = HttpResponse("The publication with ID %s does not exist" 
                        % (publication_id))
                response.status_code = RestView.NOT_FOUND_STATUS
        else:
            comment = Comment.objects.all()
            values = {'comment': comment}
            response = RestView.render_response(request, 'comments', values)
        return response

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login')
    def POST(request):
        """Insert a new comment."""
        user = request.user
        return RestView.insert_object(request, 'comment', user_id=user.id)


@csrf_exempt
class CommentDetail(RestView):
    """Handles requests for a specific comment."""
    allowed_methods = ("GET", "PUT", "DELETE")

    @staticmethod
    def GET(request, comment_id):
        """Return details for a particular comment."""
        try:
            comment = Comment.objects.get(id=comment_id)
            values = {'comment': comment}
            response = RestView.render_response(request, 'comment', values)
        except Comment.DoesNotExist:
            response = HttpResponse("The comment with id %s does not exist" % (comment_id))
            response.status_code = RestView.NOT_FOUND_STATUS
        return response

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login/')
    def PUT(request, comment_id):
        """Modify an existing comment."""
        user = request.user
        return RestView.insert_object(request, 'comment', comment_id, user_id=user.id)
    
    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login/')
    def DELETE(request, comment_id):
        """docstring for DELETE"""
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        response = HttpResponse("Delete %s with id %s" % ('comment', comment_id))
        response.status_code = RestView.NO_CONTENT_STATUS
        return response


@csrf_exempt
class EsteemDetail(RestView):
    """Handles requests for esteem values of a user."""
    allowed_methods = ("GET", "PUT")
    
    @staticmethod
    def GET(request, esteem_id=None):
        """Return esteem for a certain user.
        
        Attributes:
            esteem_id: the id of a specific esteem instance.
            user_id: the id of the user.
        """
        try:
            if esteem_id:
                esteem = Esteem.objects.get(id=esteem_id)
                values = {'esteem': esteem}
                response = RestView.render_response(request, 'esteem', values)
        except Esteem.DoesNotExist:
            response = HttpResponse("No esteem found for esteem with ID %s." % (esteem_id))
            response.status_code = RestView.NOT_FOUND_STATUS
        return response

    @staticmethod
    @login_required(login_url='/user/login/')
    def PUT(request, esteem_id=None):
        """Change an existing esteem value."""
        return RestView.insert_object(request, 'esteem', esteem_id)


@csrf_exempt
class Keywords(RestView):
    """Return a list of keywords."""
    allowed_methods = ("GET", "POST")

    @staticmethod
    def GET(request, keyword_id=None):
        """Return a list of all keywords in the system."""
        if keyword_id:
            keywords = Keyword.objects.get(id=keyword_id)
            values = {'keyword': keywords}
        else:
            keywords = Keyword.objects.all()
            values = {'keywords': keywords}
        response = RestView.render_response(request, 'keyword', values)
        return response
    
    @staticmethod
    def related_keywords(request, keyword_id):
        """Return keywords related to the provided one."""
        keyword = Keyword.objects.get(id=keyword_id)
        keywords = search.get_related_keywords(keyword)
        values = {'keyword': keywords}
        response = RestView.render_response(request, 'keyword', values)
        return response

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login/')
    def POST(request):
        """Insert a new keyword and return its location."""
        return RestView.insert_object(request, 'keyword')

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login/')
    def PUT(request, keyword_id):
        """Modify an existing keyword."""
        return RestView.insert_object(request, 'keyword', keyword_id)

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login/')
    def DELETE(request, keyword_id):
        """Delete an existing keyword."""
        keyword = Keyword.objects.get(id=keyword_id)
        keyword.delete()
        response = HttpResponse("Delete %s with id %s" % ('keyword', keyword_id))
        response.status_code = RestView.NO_CONTENT_STATUS
        return response


@csrf_exempt
class PeerReviews(RestView):
    """Returns list of peer reviews."""
    allowed_methods = ("GET", "POST")

    @staticmethod
    @login_required(login_url='/user/login/')
    def GET(request, publication_id):
        """Return a list of peer reviews for a certain publication.
        
        If the publication is still in review only editors may see reviews.
        
        """
        try:
            peer_reviews = PeerReview.objects.filter(publication__id=publication_id)
            values = {'peerreviews': peer_reviews}
            response = RestView.render_response(request, 'peerreviews', values)
        except PeerReview.DoesNotExist:
            response = HttpResponse("No peer reviews exist for publicaiton with id %s"
                    % (publication_id))
            response.status_code = RestView.NOT_FOUND_STATUS
        return response

    @staticmethod
    @csrf_exempt
    @login_required
    def POST(request, publication_id):
        """Creates a new peer review."""
        try:
            publication_id = Publication.objects.get(id=publication_id)
            if access.validate_referee(request.user):
                return RestView.insert_object(request, 'peerreview')
            else:
                response = HttpResponse("Invalid priviledges: user not allowed to add peer review.")
                response.status_code = RestView.FORBIDDEN_STATUS
                return response
        except Publication.DoesNotExist:
            response = HttpResponse("The publication with id %s does not exist" %
                    (publication_id))
            response.status_code = RestView.BAD_REQUEST_STATUS
            return response


@csrf_exempt
class PeerReviewDetail(RestView):
    """Handle REST request for a specific peer review."""
    allowed_methods = ("GET", "PUT", "DELETE")

    @staticmethod
    @login_required(login_url='/user/login/')
    def GET(request, peer_review_id):
        """Return details for a specific peer review.
        
        If the publication is still in review only reviewers can see a review."""
        try:
            peer_review = PeerReview.objects.get(id=peer_review_id)
            if access.validate_access_to_peer_review_for_user(peer_review, request.user):
                values = {'peerreview': peer_review}
                response = RestView.render_response(request, 'peerreview', values)
            else:
                response = HttpResponse('Access denied.')
                response.status_code = RestView.FORBIDDEN_STATUS
        except PeerReview.DoesNotExist:
            response = HttpResponse("Peer review with id %s does not exist" % (peer_review_id))
            response.status_code = RestView.NOT_FOUND_STATUS
        return response

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login/')
    def PUT(request, review_id):
        """Changes a peer review.
        
        Only allowed for the user that created it."""
        try:
            peerreview = PeerReview.objects.get(id=review_id)
            if access.validate_user_is_peerreviewer(peerreview, request.user):
                return RestView.insert_object(request, 'peerreview', review_id)
            else:
                response = HttpResponse("Invalid priviledges: user not allowed to change the peer review.")
                response.status_code = RestView.FORBIDDEN_STATUS
                return response
        except PeerReview.DoesNotExist:
            response = HttpResponse("Peer review with id %s does not exist" % (review_id))
            response.status_code = RestView.NOT_FOUND_STATUS

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login/')
    def DETELE(request, peerreview_id):
        """Delete the peer review from the system."""
        peerreview = PeerReview.objects.get(id=peerreview_id)
        peerreview.delete()
        response = HttpResponse("Delete %s with id %s" % ('peerreview', peerreview_id))
        response.status_code = RestView.NO_CONTENT_STATUS
        return response


@csrf_exempt
class PeerReviewTemplates(RestView):
    """Handle REST request for lists of templates."""
    allowed_methods = ("GET", "POST")

    @staticmethod
    def GET(request):
        """Return a list of peer review templates."""
        peer_review_templates = PeerReviewTemplate.objects.all()
        values = {'peerreviewtemplates': peer_review_templates}
        response = RestView.render_response(request, 'peerreviewtemplates', values)
        return response

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login/')
    def POST(request, values):
        """Create a new peer review template."""
        return RestView.insert_object(request, 'peerreviewtemplate')


@csrf_exempt
class PeerReviewTemplateDetail(RestView):
    """Handle REST requests for a specific template."""
    allowed_methods = ("GET", "PUT", "DELETE")

    @staticmethod
    def GET(request, template_id):
        """Return information about a specific template."""
        try:
            template = PeerReviewTemplate.objects.get(id=template_id)
            values = {'template': template}
            response = RestView.render_response(request, 'peerreviewtemplate', values)
        except PeerReviewTemplate.DoesNotExist:
            response = HttpResponse("Template with ID %s does not exist" % (template_id))
            response.status_code = RestView.NOT_FOUND_STATUS
        return response

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login/')
    def PUT(request, template_id):
        """Modify an existing peer review template."""
        return RestView.insert_object(request, 'peerreviewtemplate', template_id)

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login/')
    def DELETE(request, peerreviewtemplate_id):
        """Delete an existing template."""
        peerreviewtemplate = PeerReviewTemplate.objects.get(id=peerreviewtemplate_id)
        peerreviewtemplate.delete()
        response = HttpResponse("Delete %s with id %s" % ('peerreviewtemplate', peerreviewtemplate_id))
        response.status_code = RestView.NO_CONTENT_STATUS
        return response


@csrf_exempt
class Publications(RestView):
    """Class to handle rendering of the publication list view."""
    allowed_methods = ('GET', 'POST')

    @staticmethod
    def GET(request, pub_search=None, auth_search=None, key_search=None,
            tag_search=None):
        """Returns publications stored in the database.
        
        If called with a query string the publications will be searched,
        otherwise all publications will be returned."""
        pub_parameters = None
        auth_parameters = None
        key_parameters = None
        tag_parameters = None
        if pub_search:
            pub_parameters = QueryDict(pub_search)
        if auth_search:
            auth_parameters = QueryDict(auth_search)
        if key_search:
            key_parameters = QueryDict(key_search)
        if tag_search:
            tag_parameters = QueryDict(tag_search)
        publication_list = search.search_publications(pub_parameters, auth_parameters,
                key_parameters, tag_parameters)
        if not access.validate_user_is_editor(request.user):
            publication_list = publication_list.exclude(review_status=Publication.IN_REVIEW_STATUS)
        values = {'publication_list': publication_list}
        response = RestView.render_response(request, 'publications', values)
        return response

    @staticmethod
    def related_publications(request, publication_id):
        """Returns publications that are related to the current publication."""
        publication = Publication.objects.get(id=publication_id)
        publications = search.get_related_publications(publication)
        values = {'publications': publications}
        response = RestView.render_response(request, 'publications', values)
        return response

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login/')
    def POST(request):
        """Inserts publications via POST request."""
        try:
            content_type = RestView.get_content_type(request)
            data = request.raw_post_data
            logger.info("Attempt to insert publication: %s" % (data))
            requester = request.user
            inserted_publications = None
            if 'application/x-bibtex' in content_type:
                inserted_publications = insert.insert_bibtex_publication(data, requester)
            else:
                inserter = insert.get_inserter(content_type)
                inserted_publications = inserter.modify_publication(data, requester=requester)
            values = {'publication_list': inserted_publications}
            response = RestView.render_response(request, 'publications', values)
            response.status_code = RestView.CREATED_STATUS
            if type(inserted_publications) == type(Publication):
                response['Location'] = "%s/publication/%s" % (service_url, inserted_publications.id)
        except InvalidDataException, e:
            logger.error(e)
            response = HttpResponse(e.message)
            response.status_code = RestView.BAD_REQUEST_STATUS
        return response


@csrf_exempt
class PublicationDetail(RestView):
    """Object to handle rendering of the publication detail view."""
    allowed_methods = ('GET', 'PUT', 'DELETE')

    def _insert_publication(request, publication_id):
        content_type = RestView.get_content_type(request)
        data = request.raw_post_data
        logger.info("Attempt to insert publication: %s" % (data))
        requester = request.user
        if 'application/x-bibtex' in content_type:
            inserted_publication = insert.insert_bibtex_publication(data, requester)
        else:
            inserter = insert.get_inserter(content_type)
            inserted_publication = inserter.modify_publication(data, publication_id, requester=requester)
        return inserted_publication

    @login_required(login_url='/user/login')
    def _get_restricted_publication(request, publication):
        """Return if a user can see an in_review publication."""
        user = request.user
        if access.user_in_group_for_publication(user, publication):
            values = {'publication': publication}
            response = RestView.render_response(request, 'publication', values)
        else:
            response = HttpResponse('Access denied')
            response.status_code = RestView.FORBIDDEN_STATUS
        return response

    @staticmethod
    def GET(request, publication_id, meta=None):
        """Returns the information about the publication.
        
        If a publication is in review only an editor or referee of the reviewing
        group should be allowed to see it."""
        try:
            publication = Publication.objects.get(id=publication_id)
            if publication.review_status == 3:
                return PublicationDetail._get_restricted_publication(request, publication)
            if meta:
                oai = OaiPmhDecorator()
                try:
                    publication = oai.decorate_publication(publication)
                except InvalidDataException, exc:
                    logger.error(exc)
                    response = HttpResponse(exc.message)
                    response.status_code = RestView.BAD_REQUEST_STATUS
                    return response
            values = {'publication': publication}
            response = RestView.render_response(request, 'publication', values)
        except Publication.DoesNotExist:
            response = HttpResponse("The publication with ID %s does not exist" % (publication_id))
            response.status_code = RestView.NOT_FOUND_STATUS
        return response

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login')
    def PUT(request, publication_id):
        """Creates a new resource from provided values.
        Accepts key, value encoded pairs or bibtex."""
        try:
            inserted_publication = PublicationDetail._insert_publication(request, publication_id)
            values = {'publication': inserted_publication}
            response = RestView.render_response(request, 'publication', values)
            response.status_code = RestView.CREATED_STATUS
        except InvalidDataException, e:
            logger.error(e)
            response = HttpResponse(e.message)
            response.status_code = RestView.BAD_REQUEST_STATUS
        return response

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login/')
    def DELETE(request, publication_id):
        user = request.user
        """Deletes the referred publication from the database."""
        publication = Publication.objects.get(id=publication_id)
        # TODO: do not allow delete when peer review or comments exist.
        if publication.owner == user:
            publication.delete()
            response = HttpResponse("Publication with ID = %s successfully deleted." % (publication_id))
            response.status_code = RestView.OK_STATUS 
        else:
            response = HttpResponse("Can not delete publication.")
            response.status_code = RestView.FORBIDDEN_STATUS
        return response


@csrf_exempt
class RatingDetail(RestView):
    """Handle REST requests for ratings."""
    allowed_methods = ("GET", "POST", "PUT", "DELETE")

    @staticmethod
    def GET(request, rating_id=None, publication_id=None):
        """Return a rating for a given id or publication."""
        if rating_id:
            rating = Rating.objects.get(id=rating_id)
            values = {'rating': rating}
        elif publication_id:
            rating = Publication.objects.get(id=publication_id).rating_set.all()
            values = {'ratings': rating}
        else:
            rating = Rating.objects.all()
            values = {'ratings': rating}
        response = RestView.render_response(request, 'rating', values)
        return response

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login/')
    def POST(request):
        """Create a new rating object."""
        return RestView.insert_object(request, 'rating')
    
    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login/')
    def PUT(request, rating_id):
        """Change the value of an existing rating."""
        return RestView.insert_object(request, 'rating', rating_id)

    @staticmethod
    @csrf_exempt
    def DELETE(request, rating_id):
        """Delete an existing rating."""
        rating = Rating.objects.get(id=rating_id)
        rating.delete()
        response = HttpResponse("Delete %s with id %s" % ('rating', rating_id))
        response.status_code = RestView.NO_CONTENT_STATUS
        return response


@csrf_exempt
class ReferenceMaterials(RestView):
    """Handle Rest requests for reference materials."""
    allowed_methods = ("POST")

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login/')
    def POST(request):
        """Insert a new reference material object."""
        return RestView.insert_object(request, 'referencematerial')


@csrf_exempt
class ReferenceMaterialDetail(RestView):
    """Handle REST requests for reference material."""
    allowed_methods = ("GET", "POST", "PUT", "DELETE")

    @staticmethod
    def GET(request, material_id):
        """Return reference material for given id."""
        reference_material = ReferenceMaterial.objects.get(id=material_id)
        values = {'referencematerial': reference_material}
        response = RestView.render_response(request, 'referencematerial', values)
        return response

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login/')
    def PUT(request, material_id):
        """Modify an existing reference material."""
        return RestView.insert_object(request, 'referencematerial', material_id)

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login/')
    def DELETE(request, material_id):
        """docstring for DELETE"""
        material = ReferenceMaterial.objects.get(id=material_id)
        material.delete()
        response = HttpResponse("Delete %s with id %s" % ('referencematerial', material_id))
        response.status_code = RestView.NO_CONTENT_STATUS
        return response


@csrf_exempt
class ResearchAreas(RestView):
    """Rest interface for research areas."""
    allowed_methods = ("GET", "POST", "PUT", "DELETE") 

    @staticmethod
    def GET(request, researcharea_id=None):
        """Return list of details for a research area."""
        if researcharea_id:
            ra = ResearchArea.objects.get(id=researcharea_id)
            values = {'researcharea': ra}
            response = RestView.render_response(request, 'researcharea', values)
        else:
            ra = ResearchArea.objects.all()
            values = {'researchareas': ra}
            response = RestView.render_response(request, 'researchareas', values)
        return response

    @staticmethod
    @csrf_exempt
    @login_required(login_url="/user/login")
    def POST(request):
        """Create a new research area."""
        return RestView.insert_object(request, 'researcharea') 

    @staticmethod
    @csrf_exempt
    @login_required(login_url="/user/login")
    def PUT(request, researcharea_id):
        """Modify an existing research area."""
        return RestView.insert_object(request, 'researcharea', researcharea_id) 

    @staticmethod
    @csrf_exempt
    @login_required(login_url="/user/login")
    def DELETE(request, researcharea_id):
        """Delete an existing research area."""
        ra = ResearchArea.objects.get(id=researcharea_id)
        ra.delete()


@csrf_exempt
class Tags(RestView):
    """Handle REST requests for tags."""
    allowed_methods = ("GET", "POST")

    @staticmethod
    def GET(request):
        """Return a list of all tags."""
        tags = Tag.objects.all()
        values = {'tags': tags}
        response = RestView.render_response(request, 'tags', values)
        return response

    @staticmethod
    def related_tags(request, tag_id):
        """Return tags related to the tag with the given id."""
        tag = Tag.objects.get(id=tag_id)
        tags = search.get_related_tags(tag)
        values = {'tags': tags}
        response = RestView.render_response(request, 'tags', values)
        return response

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login/')
    def POST(request):
        """Insert a new tag."""
        return RestView.insert_object(request, 'tag')


@csrf_exempt
class TagDetail(RestView):
    """Handle REST requests for a specific tag."""
    allowed_methods = ("GET", "PUT", "DELETE")

    @staticmethod
    def GET(request, tag_id):
        """Return information for one tag."""
        tag = Tag.objects.get(id=tag_id)
        values = {'tag': tag}
        response = RestView.render_response(request, 'tag', values)
        return response

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login/')
    def PUT(request, tag_id):
        """Modify an tag."""
        return RestView.insert_object(request, 'tag', tag_id)

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login/')
    def DELETE(request, tag_id):
        """Delete a tag."""
        tag = Tag.objects.get(id=tag_id)
        tag.delete()
        response = HttpResponse("Delete %s with id %s" % ('tag', tag_id))
        response.status_code = RestView.NO_CONTENT_STATUS
        return response


class Overview(RestView):
    """Displays an overview over the webservice."""
    allowed_methods = ("GET")

    @staticmethod
    def GET(request):
        """Return the overview template."""
        response = RestView.render_response(request, 'overview')
        return response


@csrf_exempt
class PaperGroups(RestView):
    """Display an overview over the available papergroups."""
    allowed_methods = ("GET", "POST")

    @staticmethod
    def GET(request):
        """Return a list of all papergroups."""
        papergroups = PaperGroup.objects.all()
        values = {'papergroups': papergroups}
        response = RestView.render_response(request, 'papergroups', values)
        return response

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login/')
    def POST(request):
        """Create a new papergroup from the specified data."""
        return RestView.insert_object(request, 'papergroup')


@csrf_exempt
class PaperGroupDetail(RestView):
    """Display information about a specific papergroup."""
    allowed_methods = ("GET", "PUT", "DELETE")

    @staticmethod
    @login_required(login_url='user/login/')
    def GET(request, papergroup_id):
        # TODO: Only an editor can change a peer review status.
        """Return specific information about one papergroup."""
        user = request.user
        if access.validate_referee_or_editor(user, papergroup_id):
            papergroup = PaperGroup.objects.get(id=papergroup_id)
            values = {'papergroup': papergroup}
            response = RestView.render_response(request, 'papergroup', values)
        else:
            response = HttpResponse('Access denied.')
            response.status_code = RestView.FORBIDDEN_STATUS
        return response

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login/')
    def PUT(request, papergroup_id):
        """Modify an existing papergroup."""
        RestView.insert_object(request, 'papergroup', papergroup_id)


    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login/')
    def DELETE(request, papergroup_id):
        """Delete an existing papergroup."""
        # TODO: Make sure only an editor can delete the group.
        papergroup = PaperGroup.objects.get(id=papergroup_id)
        if request.user in papergroup.editors.all():
            papergroup.delete()
            response = HttpResponse("Delete %s with id %s" % ('papergroup', papergroup_id))
            response.status_code = RestView.NO_CONTENT_STATUS
        else:
            response = HttpResponse("Only an editor can delete a papergroup.")
            response.status_code = RestView.FORBIDDEN_STATUS
        return response


@csrf_exempt
class Users(RestView):
    """Used to create user accounts."""
    allowed_methods = ("GET", "POST")

    @staticmethod
    def GET(request, user_search=None):
        """Search for users."""
        # TODO - order by rating
        if user_search:
            query = QueryDict(user_search)
            users = search.search_user(query)
        else:
            users = User.objects.all()
        users = list(users)
        users = sorted(users, key = lambda user: user.profile.esteem.value, reverse=True)
        values = {'users': users}
        return RestView.render_response(request, 'users', values)

    @staticmethod
    def related_users_for_publication(request, publication_id):
        """Return users related to the user with given id."""
        publication = Publication.objects.get(id=publication_id)
        users = search.get_related_users_for_publication(publication)
        values = {'users': users}
        return RestView.render_response(request, 'users', values)

    @staticmethod
    @csrf_exempt
    def POST(request):
        """Create a new user."""
        if RestView.validate_sent_format(request):
            return RestView.insert_object(request, 'user')
        else:
            return RestView.unsupported_format_sent(RestView.get_content_type(request))


@csrf_exempt
class UserDetail(RestView):
    """Display user details."""
    allowed_methods = ("GET", "PUT", "DELETE")
    
    @staticmethod
    def GET(request, user_id):
        """Return the information for a given user."""
        user = User.objects.get(id=user_id)
        values = {'quser': user}
        return RestView.render_response(request, template_name='user', dictionary=values)

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login/')
    def PUT(request, user_id):
        """Change an existing user."""
        if RestView.validate_sent_format(request):
            return RestView.insert_object(request, 'user', user_id)
        else:
            return RestView.unsupported_format_sent(RestView.get_content_type(request))

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/user/login/')
    def DELETE(request, user_id):
        """Delete an existing user."""
        request_user = request.user
        user = User.objects.get(id=user_id)
        if request_user == user:
            logout(user)
            user.delete()
            response = HttpResponse('User account deleted.')
            response.status_code = RestView.OK_STATUS
        else:
            response = HttpResponse('Can only delete own user account.')
            response.status_code = RestView.FORBIDDEN_STATUS
        return response


@csrf_exempt
class VoteDetail(RestView):
    """Handle REST requests for votes."""
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    
    @staticmethod
    def GET(request, vote_id=None):
        """Return a specific vote."""
        if vote_id:
            vote = Vote.objects.get(id=vote_id)
        values = {'vote': vote}
        return RestView.render_response(request, 'vote', values)

    @staticmethod
    @csrf_exempt
    def POST(request):
        """Create a new vote."""
        return RestView.insert_object(request, 'vote')

    @staticmethod
    @csrf_exempt
    def PUT(request, vote_id):
        """Modify a specific vote."""
        return RestView.insert_object(request, 'vote', vote_id)

    @staticmethod
    @csrf_exempt
    def DELETE(request, vote_id):
        """Delete a specific vote."""
        vote = Vote.objects.get(id=vote_id)
        vote.delete()
        response = HttpResponse("Vote deleted.")
        response.status_code = RestView.OK_STATUS

@csrf_exempt
def login(request):
    """Log a user in."""
    xml = insert.XmlInserter()
    data = request.raw_post_data
    logger.info("Login")
    try:
        data = xml._parse_xml_to_dict(data)
        username = data['username']
        password = data['password']
        logger.info("Attempt to login from %s" % (username))
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            values = {'user': user}
            response = RestView.render_response(request, 'login', values)
            response['Content-Type'] = 'application/xml'
            return response
        else:
            logger.info("Login failed.")
            response = HttpResponse("Invalid credentials.")
            response.status_code = RestView.BAD_REQUEST_STATUS
            return response
    except InvalidDataException, e:
        logger.info("Login failed.")
        logger.error(e)
        logger.error(e.message)
        response = HttpResponse("Data could not be parsed.")
        response.status_code = RestView.BAD_REQUEST_STATUS
        return response

@csrf_exempt
def logout(request):
    """Log a user out."""
    auth.logout(request)
    return HttpResponse("Logged out.")

authors = Authors()
author_detail = AuthorDetail()
comments = Comments()
comment_detail = CommentDetail()
esteem_detail = EsteemDetail()
keywords = Keywords()
overview = Overview()
papergroups = PaperGroups()
papergroup_detail = PaperGroupDetail()
peerreviews = PeerReviews()
peerreview_detail = PeerReviewDetail()
peerreview_templates = PeerReviewTemplates()
peerreview_template_detail = PeerReviewTemplateDetail()
publications = Publications()
publication_detail = PublicationDetail()
rating_detail = RatingDetail()
reference_materials = ReferenceMaterials()
reference_material_detail = ReferenceMaterialDetail()
researchareas = ResearchAreas()
tags = Tags()
tag_detail = TagDetail()
users = Users()
user_detail = UserDetail()
vote_detail = VoteDetail()
