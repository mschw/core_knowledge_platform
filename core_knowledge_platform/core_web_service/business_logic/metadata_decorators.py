"""This module holds the metadata decorators that can be used to dynamically add
metadata to objects."""

from oaipmh.client import Client
from oaipmh.error import IdDoesNotExistError
from oaipmh.metadata import MetadataRegistry, oai_dc_reader
import logging

logger = logging.getLogger('myproject.custom')


class OaiPmhDecorator(object):
    """Query a web service and add metadata to an object.
    
    Will query a web service that supports the OAI-PMH protocol and add information
    to the object."""
    
    DOI_PREFIX = 'oai:CiteSeerXPSU:'
    META_DATA_PREFIX = 'oai_dc'

    def __init__(self, url=None, expected_meta_data=None):
        """Create a decorator.

        Arguments:
            url: the endpoint url for the oai call.
            expected_meta_data: a list containing the attributes that shall be
                decorated to the objects.
        """
        super(OaiPmhDecorator, self).__init__()
        if url:
            self.citeseer_url = url
        else:
            self.citeseer_url = 'http://citeseerx.ist.psu.edu/oai2'
        if expected_meta_data:
            self.expected_meta_data = expected_meta_data
        else:
            self.expected_meta_data = ['identifier', 'source']
        registry = MetadataRegistry()
        registry.registerReader(OaiPmhDecorator.META_DATA_PREFIX, oai_dc_reader)
        self.oai_client = Client(self.citeseer_url, registry)

    def decorate_publication(self, publication):
        """Decorate a publication with the metadata for this object."""
        decorated_publication = None
        doi = OaiPmhDecorator.DOI_PREFIX + publication.doi
        if doi:
            metadata = self.query_service(doi, publication)
            self.add_decoration_to_publication(publication, metadata)
        else:
            decorated_publication = publication
        return decorated_publication

    def add_decoration_to_publication(self, publication, metadata):
        publication.decorated = dict()
        for data in self.expected_meta_data:
            try:
                value = metadata[data]
                if len(value) == 1:
                    publication.decorated[data] = value[0]
                else:
                    publication.decorated[data] = value
            except KeyError, e:
                logger.error("Decorator key not found %s for DOI: %s" % (data, doi))

    def query_service(self, doi, publication):
        try:
            citeseer_header, citeseer_body, none_object = self.oai_client.getRecord(
                    identifier=doi, metadataPrefix=OaiPmhDecorator.META_DATA_PREFIX)
            return citeseer_body
        except IdDoesNotExistError, e:
            logger.error("Querying metadata for doi %s failed: %s" % (doi, e))
            # TODO: raise exception?
            raise e

    def decorate_author(self, author):
        """docstring for decorate_author"""
        pass
