from bibtex_parser.bibtex_parser import BibtexParser
from core_web_service.models import Publication, FurtherFields, Tag

def insert_bibtex_publication(bibtex, owner):
    """Will insert a publication from a bibtex string."""
    # TODO: check that owner is a user object.
    parser = BibtexParser()
    bibtex_dictionary = parser.parse_to_bibtex(bibtex)
    publication_type = bibtex_dictionary[1][0]
    values = bibtex_dictionary[1][1]
    fields = []
    tags = []
    publication = Publication()
    publication.publication_type = publication_type
    publication.owner = owner
    for key, value in values:
        try:
            # Set the fields that are present in the publication table.
            if key == "keyword":
                tag = Tag.objects.get_or_create(name=value)
                publication.tag = tag
                tags.append(tag)
            else:
                getattr(publication, key)
                setattr(publication, key, value)
        except AttributeError:
            # TODO: log problem
            # Add remaining fields to the further fields table.
            field = FurtherFields()
            field.key = key
            field.value = value
            field.publication = publication
            fields.append(field)
    publication.save()
    for field in fields:
        field.save()
    for tag in tags:
        tag.publication = publication
        tag.save()
    return publication
