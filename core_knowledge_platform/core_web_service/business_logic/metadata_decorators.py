"""This module holds the metadata decorators that can be used to dynamically add
metadata to objects."""

from oaipmh.client import Client
from oaipmh.error import IdDoesNotExistError
from oaipmh.metadata import MetadataRegistry, oai_dc_reader
from core_web_service.business_logic.insert import InvalidDataException
import logging
import pdb

logger = logging.getLogger('myproject.custom')

def built_citeseer_uri(doi):
    """Built a correct uri from the provided doi and base-url."""
    DOI_PREFIX = 'oai:CiteSeerXPSU:'
    if doi:
        return DOI_PREFIX + doi
    else:
        raise InvalidDataException("DOI invalid. Can not query metadata.")

class OaiPmhDecorator(object):
    """Query a web service and add metadata to an object.
    
    Will query a web service that supports the OAI-PMH protocol and add information
    to the object."""
    
    META_DATA_PREFIX = 'oai_dc'

    def __init__(self, url=None, expected_meta_data=None, built_uri=None):
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
        if built_uri:
            self.built_uri = built_uri
        else:
            self.built_uri = built_citeseer_uri
        registry = MetadataRegistry()
        registry.registerReader(OaiPmhDecorator.META_DATA_PREFIX, oai_dc_reader)
        self.oai_client = Client(self.citeseer_url, registry)

    def decorate_publication(self, publication):
        """Decorate a publication with the metadata for this object."""
        doi = self.built_uri(publication.doi)
        if doi:
            metadata = self.query_service(doi, publication)
            publication = self.add_decoration_to_publication(publication, metadata)
        return publication

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
        return publication

    def query_service(self, doi, publication):
        try:
            citeseer_header, citeseer_body, none_object = self.oai_client.getRecord(
                    identifier=doi, metadataPrefix=OaiPmhDecorator.META_DATA_PREFIX)
            return citeseer_body
        except IdDoesNotExistError, e:
            logger.error("Querying metadata for doi %s failed: %s" % (doi, e))
            # TODO: raise exception?
            raise InvalidDataException(e)
