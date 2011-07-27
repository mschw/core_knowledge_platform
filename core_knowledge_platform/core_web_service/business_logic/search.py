from core_web_service.models import ResearchArea
from core_web_service.models import UserProfile
from django.db.models import Q
from core_web_service.models import Author, Publication, Keyword
import pdb
import operator
from django.contrib.auth.models import User

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

def search_authors(search_items):
    """Search authors matching the provided arguments."""
    query = build_query(search_items)
    result = Author.objects.filter(reduce(operator.or_, query))
    return result

def _search_publications(search_items):
    """Search publications matching the provided arguments."""
    query = build_query(search_items)
    result = Publication.objects.filter(reduce(operator.or_, query))
    return result

def search_keywords(search_items):
    """Search keywords matching the provided arguements."""
    query = build_query(search_items)
    result = Keyword.objects.filter(reduce(operator.or_, query))
    return result

def search_publications(publication_terms, author_terms, keyword_terms):
    """Return publications that match the provided conditions."""
    publications = None
    authors = None
    keywords = None
    if publication_terms:
        publications = _search_publications(publication_terms)
    else:
        publications = Publication.objects.all()
    if author_terms:
        authors = search_authors(author_terms)
        author_id = [author.id for author in authors]
        publications = publications.filter(authors__id__in=[author_id])
    if keyword_terms:
        keywords = search_keywords(keyword_terms)
        keyword_id = [keyword.id for keyword in keywords]
        publications = publications.filter(keywords__id__in=[keyword_id])
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
    """Return tags that were used when the provided p_tag was used."""
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
    """Return keywords that were used when the provided p_tag was used."""
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

def get_related_publications(publication):
    # TODO
    # FIXME: rank papers higher from the same author.
    # Chack for related papers based on keywords and tags - rate keywords higher than tags.
    # Value keywords higher than tags.
    """docstring for get_related_publications"""
    pass
