from core_web_service.models import ResearchArea
from core_web_service.models import UserProfile
from django.db.models import Q
from django.http import QueryDict
from core_web_service.models import Author, Publication, Keyword
import pdb
import operator
from django.contrib.auth.models import User
from core_web_service.models import Tag

import logging

logger = logging.getLogger('myproject.custom')

def build_query(search_query):
    """Build the query for a given dictionary.
    
    Will create a Q object for each query and return a list of these queries.
    
    Attributes:
        search_query: a dictionary with search_term: search_value pairs.

    Returns:
        query: a list of Q-objects containing the query.
    
    Raises:
        AttributeError: when a search_value is not present for a search_term."""
    query = [] 
    for key, value in search_query.items():
        if value:
            # FIXME: should this be always this way?
            # If an id is provided an exact match is required.
            if key == 'id':
                q = Q(**{"%s__iexact" % (key): value})
            else:
                q = Q(**{"%s__icontains" % (key): value})
            query.append(q)
        else:
            raise AttributeError("Invalid value for keyword %s: %s" % (key, value))
    return query

def _get_search_type(search_items):
    """Return the type of search to be performed.

    Attempts to obtain the searchtype key from the dictionary.
    If the key is not present returns an _or_ search.
    Else returns the searchtype and removes it from the searchdict.
    """
    if isinstance(search_items, QueryDict):
        search_items = search_items.copy()
    try:
        search_type = search_items['searchtype']
        del search_items['searchtype']
    except KeyError, e:
        search_type = 'or'
    return (search_type, search_items)

def _perform_search(search_class, search_type, query):
    """Will perform a search on the class with the given search_type."""
    if search_type == 'and':
        result = search_class.objects.filter(reduce(operator.and_, query))
    else:
        result = search_class.objects.filter(reduce(operator.or_, query))
    return result

def search_authors(search_items):
    """Search authors matching the provided arguments."""
    search_type, search_items = _get_search_type(search_items)
    query = build_query(search_items)
    result = _perform_search(Author, search_type, query)
    return result

def _search_publications(search_items):
    """Search publications matching the provided arguments."""
    search_type, search_items = _get_search_type(search_items)
    query = build_query(search_items)
    result = _perform_search(Publication, search_type, query)
    return result

def search_keywords(search_items):
    """Search keywords matching the provided arguements.
    
    Arguments:
        search_items: a dictionary containing the search terms."""
    search_type, search_items = _get_search_type(search_items)
    query = build_query(search_items)
    result = _perform_search(Keyword, search_type, query)
    return result

def search_tags(search_items):
    """Search tags matching the provided arguments."""
    search_type, search_items = _get_search_type(search_items)
    query = build_query(search_items)
    result = _perform_search(Tag, search_type, query)
    return result

def search_publications(publication_terms=None, author_terms=None,
        keyword_terms=None, tag_terms=None):
    """Return publications that match the provided conditions."""
    logger.info('Searching publication with %s %s %s %s' % (publication_terms,
        author_terms, keyword_terms, tag_terms))
    if publication_terms:
        publications = _search_publications(publication_terms)
    else:
        publications = Publication.objects.all()
    if author_terms:
        authors = search_authors(author_terms)
        author_ids = [author.id for author in authors]
        publications = publications.filter(authors__id__in=author_ids)
    if keyword_terms:
        keywords = search_keywords(keyword_terms)
        keyword_ids = [keyword.id for keyword in keywords]
        publications = publications.filter(keywords__id__in=keyword_ids)
    if tag_terms:
        tags = search_tags(tag_terms)
        tag_ids = [tag.id for tag in tags]
        publications = publications.filter(tags__id__in=tag_ids)
    return publications

def search_user(search_items):
    """Return users that match the provided conditions."""
    try:
        search_items['password']
        raise AttributeError('Can not search for password')
    except KeyError:
        pass
    query = build_query(search_items)
    result = User.objects.filter(reduce(operator.or_, query))
    return result

def get_related_tags(tag):
    """Return tags that were used as well, when the provided tag was used."""
    publication_with_tag = Publication.objects.filter(tags__id__in=[tag.id])
    relevance_tags = dict()
    for publication in publication_with_tag:
        for p_tag in publication.tags.all().exclude(id=tag.id):
            if p_tag.name is not tag.name:
                key = p_tag
                if key in relevance_tags:
                    relevance_tags[key] = relevance_tags[key] + 1
                else:
                    relevance_tags[key] = 1
    sorted_list = sorted(relevance_tags, key=lambda p_tag: p_tag)
    return sorted_list

def get_related_keywords(keyword):
    """Return keywords that were used as well, when the provided keyword was used."""
    publication_with_tag = Publication.objects.filter(keywords__id__in=[keyword.id])
    relevance_keywords = dict()
    for publication in publication_with_tag:
        for p_keyword in publication.keywords.all().exclude(id=keyword.id):
            if p_keyword.keyword is not keyword.keyword:
                key = p_keyword
                if key in relevance_keywords:
                    relevance_keywords[key] = relevance_keywords[key] + 1
                else:
                    relevance_keywords[key] = 1
    sorted_list = sorted(relevance_keywords, key=lambda p_keyword: p_keyword)
    return sorted_list

def get_related_users_for_keyword(keyword):
    """Return a list of users that research in the given area."""
    users = User.objects.all()
    related_users = []
    for user in users:
        try:
            research_areas = user.profile.research_areas.all()
            for ra in research_areas:
                if (keyword.keyword in ra.title) or (keyword.keyword in ra.description):
                    related_users.append(user)
        except UserProfile.DoesNotExist:
            pass
        except ResearchArea.DoesNotExist:
            pass
    return related_users

def get_related_users_for_publication(publication):
    """Return a list of users that might be intersted in the paper."""
    interested_users = []
    for keyword in publication.keywords.all():
        users = get_related_users_for_keyword(keyword)
        interested_users.extend(users)
    return interested_users

def get_publications_by_tag(tag):
    """Return all publications with the associated tag."""
    search_dict = {'id': tag.id}
    publications = search_publications(tag_terms=search_dict)
    return publications

def get_publications_by_tags(tags):
    """Return all publications that have one or more of the provided tags."""
    all_publications = Publication.objects.none()
    for tag in tags:
        publications = get_publications_by_tag(tag)
        all_publications = all_publications | publications
    return all_publications

def get_publications_by_keyword(keyword):
    """Return all publications with the associated keyword."""
    search_dict = {'id': keyword.id}
    publications = search_publications(keyword_terms=search_dict)
    return publications

def get_publications_by_keywords(keywords):
    """Return all publications that have one or more of the provided keywords."""
    all_publications = Publication.objects.none()
    for keyword in keywords:
        publications = get_publications_by_keyword(keyword)
        all_publications = all_publications | publications
    return all_publications

def get_publications_by_author(author):
    """Return all publications that were written by the provided author."""
    search_dict = {'id': author.id}
    publications = search_publications(author_terms=search_dict)
    return publications

def get_publications_by_authors(authors):
    """Return all publications that were written by one or more of the provided authors."""
    all_publications = Publication.objects.none()
    for author in authors:
        publications = get_publications_by_author(author)
        all_publications = all_publications | publications
    return all_publications

def get_related_publications(publication):
    # TODO: Implement some kind of rating.
    # FIXME: rank papers higher from the same author.
    # Chack for related papers based on keywords and tags - rate keywords higher than tags.
    # Value keywords higher than tags.
    """Return a set of publications that are related to the argument.
    
    Will search publications that use the same tags, keywords or are written by 
    the same author.
    
    Arguments:
        publication: A publication that is used as base for relations.

    Returns:
        Set: a set of publications that might be related to the current.
    """
    publications = Publication.objects.none()
    tag_publications = get_publications_by_tags(publication.tags.all())
    tag_publications = tag_publications.exclude(id=publication.id)
    keyword_publications = get_publications_by_keywords(publication.keywords.all())
    keyword_publications = keyword_publications.exclude(id=publication.id)
    author_publications = get_publications_by_authors(publication.authors.all())
    author_publications = author_publications.exclude(id=publication.id)
    publications = tag_publications | keyword_publications | author_publications
    return set(publications)
