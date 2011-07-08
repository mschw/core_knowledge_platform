from bibtex_parser import external_parser 
from core_web_service.models import Author, Publication, FurtherFields, Tag, User

class MissingValueException(Exception):
    """Raise when a publication is missing a required attribute."""
    def __init__(self, message):
        super(MissingValueException, self).__init__()
        self.message = message
    
    def __str__(self):
        return repr(self.message)
        

required_fields_by_publication_type = {
        'article': ['author', 'journal', 'title', 'year'],
        'book': ['author', 'editor', 'publisher', 'title', 'year'],
        'booklet': [],
        'inbook': ['author', 'chapter', 'editor', 'pages', 'publisher', 'year'],
        'incollection': ['author', 'booktitle', 'publisher', 'title', 'year'],
        'manual': ['title'],
        'masterthesis': ['author', 'school', 'title', 'year'],
        'misc': [],
        'phdthesis': ['author', 'school', 'title', 'year'],
        'proceedings': ['title', 'year'],
        'techreport': ['author', 'institution', 'title', 'year'],
        'unpublished': ['author', 'note', 'title'],
        }

def insert_bibtex_publication(bibtex, owner):
    """Will insert a publication from a bibtex string.

    This function will parse the bibtex format and perform the following transformations:
    - Keywords will be transformed into tags.
    - Each fields not suitable for the publication table will be inserted into a
      key-value-pair into the furtherfields table.

    Arguments:
        bibtex: the bibtex for an entry.
        owner: the user object that will insert the publication.
    """
    # TODO: check that owner is a user object.
    parsed_list = external_parser.entry.parseString(bibtex)
    publication_type = parsed_list.entrytype
    fields = []
    tags = []
    publication = Publication()
    publication.publication_type = publication_type
    User.objects.get_or_create(owner)
    publication.owner = owner
    for key, value in values.items():
        try:
            # Set the fields that are present in the publication table.
            if key == "keyword":
                keywords = value.split(',')
                for k in keywords:
                    tag = Tag.objects.get_or_create(name=k)
                    publication.tags.add(tag)
                    tags.append(tag)
            #elif key == "author":
            #    authors = value.split('and')
            # TODO: autoreference an existing author via bibtex.
            #    author = search_authors()
            #    publication.authors.add(author)
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
    try:
        validate_required_fields(publication)
        publication.save()
        for field in fields:
            field.save()
        for tag in tags:
            tag.publication_set.add(publication)
            tag.save()
        return publication
    except MissingValueException:
        # TODO: log
        pass

def validate_required_fields(publication):
    """Check if a publication has all fields that are required according to its type.
    
    The required fields for a publication are based on the BibTeX standard that can
    be found under: amath.colorado.edu/documentation/LaTeX/reference/faq/bibtex.pdf.
    Arguments:
        publication: the publication object to be validated.
    """
    pass

def search_authors(search_value, fields_to_search=None):
    """"""
    if fields_to_search is None:
        fields_to_search = []
    return Author.objects.all(id=1)
