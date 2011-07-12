from django.db.models import Q
from core_web_service.models import Author, Publication
import operator

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
            q = Q(**{"%s__icontains" % (key): value})
            query.append(q)
        else:
            raise AttributeError("Invalid value for keyword %s: %s" % (key, value))
    return query

def search_authors(search_items):
    """Search authors matching the provided arguments."""
    query = build_query(search_items)
    result = Author.objects.filter(operator.or_(query))
    return result

def search_publications(search_items):
    """Search publications matching the provided arguments."""
    query = build_query(search_items)
    result = Publication.objects.filter(reduce(operator.or_, query))
    return result
