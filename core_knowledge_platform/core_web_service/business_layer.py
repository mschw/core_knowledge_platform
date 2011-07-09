from bibtex_parser.bibtex_parser import BibtexParser
from core_web_service.models import Author, Publication, FurtherFields, Tag, User
import pdb

class MissingValueException(Exception):
    """Raise when a publication is missing a required attribute."""
    def __init__(self, message):
        super(MissingValueException, self).__init__()
        self.message = message
    
    def __str__(self):
        return repr(self.message)
        

required_fields_by_publication_type = {
        'article': ['title', 'year'],
        'book': ['publisher', 'title', 'year'],
        'booklet': [],
        'inbook': ['chapter', 'editor', 'pages', 'publisher', 'year'],
        'incollection': ['booktitle', 'publisher', 'title', 'year'],
        'manual': ['title'],
        'masterthesis': ['school', 'title', 'year'],
        'misc': [],
        'phdthesis': ['school', 'title', 'year'],
        'proceedings': ['title', 'year'],
        'techreport': ['institution', 'title', 'year'],
        'unpublished': ['note', 'title'],
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
    inserted_publication = []
    parser = BibtexParser()
    entries = parser.bib_entry.searchString(bibtex)
    for entry in entries:
        #insert_publication_from_list(entry)
        publication = Publication()
        publication.publication_type = entry.entry_type
        owner, created = User.objects.get_or_create(username=owner.username)
        publication.owner = owner
        authors = []
        further_fields = []
        tags = []
        for field in entry.fields.asList():
            key = field[0].lower()
            value = field[1].lower()
            if key == "keyword":
                #create tag
                keywords = value.split(',')
                for k in keywords:
                    tag = Tag.objects.get_or_create(name=k)
                    publication.tags.add(tag)
                    tags.append(tag)
            elif key == "author":
                #create author
                parsed_authors = [author.strip() for author in value.split('and')]
                for author in parsed_authors:
                    #a, created = Author.objects.get_or_create(name__icontains=author)
                    #if created:
                    a = Author()
                    a.name = author
                    a.save()
                    authors.append(a)
            else:
                #insert into publication or furtherfield
                try:
                    getattr(publication, key)
                    setattr(publication, key, value)
                except AttributeError:
                    further_field = FurtherFields()
                    further_field.key = key
                    further_field.value = value
                    further_fields.append(further_field)
        try:
            validate_required_fields(publication)
            publication.save()
            for field in further_fields:
                field.publication = publication
                field.save()
            for tag in tags:
                tag.publication_set.add(publication)
                tag.save()
            for author in authors:
                publication.authors.add(author)
                publication.save()
            inserted_publication.append(publication)
        except MissingValueException, e:
            raise e
    return inserted_publication

def validate_required_fields(publication):
    """Check if a publication has all fields that are required according to its type.
    
    The required fields for a publication are based on the BibTeX standard that can
    be found under: amath.colorado.edu/documentation/LaTeX/reference/faq/bibtex.pdf.
    Arguments:
        publication: the publication object to be validated.
    """
    publication_type = publication.publication_type.lower()
    try:
        fields = required_fields_by_publication_type[publication_type]
    except KeyError:
        return True
    all_fields_present = True
    errors = []
    for field in fields:
        try:
            attribute = getattr(publication, field)
            if (attribute is None) or (len(attribute) == 0):
                all_fields_present = False
                errors.append('Publication of type %s is missing field %s' % (publication_type, field))
        except AttributeError:
            all_fields_present = False
            errors.append('Publication of type %s is missing field %s' % (publication_type, field))
    errors = "".join(errors)
    if all_fields_present:
        return True
    else:
        raise MissingValueException(errors)

def search_authors(search_value, fields_to_search=None):
    """"""
    if fields_to_search is None:
        fields_to_search = []
