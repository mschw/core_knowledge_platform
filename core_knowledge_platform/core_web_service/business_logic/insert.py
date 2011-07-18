from core_web_service.models import Esteem
from core_web_service.models import Vote
from core_web_service.bibtex_parser.bibtex_parser import BibtexParser
from core_web_service.models import Author, Publication, ProfileField, FurtherField, Keyword, User
from abc import ABCMeta, abstractmethod
from xml.etree.ElementTree import XML
import pdb
from core_web_service.models import Comment
from core_web_service.models import Vote


class MissingValueException(Exception):
    """Raise when a publication is missing a required attribute."""
    def __init__(self, message):
        super(MissingValueException, self).__init__()
        self.message = message
    
    def __str__(self):
        return repr(self.message)


class Inserter(object):
    """Abstracts insertion logic via strategy pattern.
    """
    __metaclass__ = ABCMeta
    def __init__(self):
        super(Inserter, self).__init__()

    @abstractmethod
    def modify_author(self, data, author_id=None):
        """Create or modify an author object according to the specified value."""
        pass

    @abstractmethod
    def modify_comment(self, data, comment_id=None):
        """Create or modify a comment object according to the specified value."""
        pass

    @abstractmethod
    def modify_esteem(self, data, esteem_id=None):
        """Create or modify an esteem object according to the specified value."""
        pass

    @abstractmethod
    def modify_papergroup(self, data, papergroup_id=None):
        """Create or modify a papergroup object according to the specified value."""
        pass

    @abstractmethod
    def modify_peerreview_template(self, data, template_id=None):
        """Create or modify a template object according to the specified value."""
        pass

    @abstractmethod
    def modify_peerreview(self, data, peer_review_id=None):
        """Create or modify a peer review object according to the specified value."""
        pass

    @abstractmethod
    def modify_publication(self, data, publication_id=None):
        """Create or modify a publication object according to the specified value."""
        pass

    @abstractmethod
    def modify_rating(self, data, rating_id=None):
        """Create or modify a rating object according to the specified value."""
        pass

    @abstractmethod
    def modify_reference_material(self, data, material_id=None):
        """Create or modify a reference material object according to the specified value."""
        pass

    @abstractmethod
    def modify_tag(self, data, tag_id=None):
        """Create or modify a tag object according to the specified value."""
        pass

    @abstractmethod
    def modify_user(self, data, user_id=None):
        """Create or modify a user from the provided values."""
        pass


class XmlInserter(Inserter):
    """Used to insert objects based on xml representations."""
    def __init__(self):
        super(XmlInserter, self).__init__()

    def _get_id_from_atom_link(self, link):
        """Return the id of an objects from an atom link."""
        link_text = link[0].attrib['href']
        return link_text.split('/')[-1]

    def _parse_xml_to_dict(self, data):
        """Parses a xml document and returns a dictionary of values.
        
        Only works for a nested depth of 2 levels:
            <a>
                <b>
                </b>
            </a>
        """
        parsed_dict = dict()
        node_tree = XML(data)
        namespace = self._get_namespace(node_tree)
        namespace = "{%s}" % (namespace)
        for node in node_tree:
            tag = node.tag.replace(namespace, "")
            if len(node) > 0:
                parsed_dict[tag] = []
                for subnode in node:
                    parsed_dict[tag].append(subnode)
            else:
                parsed_dict[tag] = node.text.strip()
        return parsed_dict

    def modify_author(self, data, author_id=None):
        """Create or modify an author object according to the specified value."""
        parsed_data = self._parse_xml_to_dict(data)
        if author_id:
            author = Author.objects.get(id=author_id)
        else:
            author = Author()
        author.name = parsed_data['name']
        author.address = parsed_data['address']
        author.affiliation = parsed_data['affiliation']
        author.email = parsed_data['email']
        author.save()
        return author

    def modify_comment(self, data, comment_id=None):
        """Create or modify a comment object according to the specified value."""
        parsed_data = self._parse_xml_to_dict(data)
        if comment_id:
            comment = Comment.objects.get(id=comment_id)
        else:
            comment = Comment()
        comment.title = parsed_data['title']
        comment.text = parsed_data['text']
        for field in parsed_data['votes']:
            vote_id = self._get_id_from_atom_link(field)
            vote = Vote.objects.get(id=vote_id)
            comment.vote = vote
        comment.save()
        return comment

    def modify_esteem(self, data, esteem_id=None):
        """Create or modify an esteem object according to the specified value."""
        # FIXME: fix xml data schema to match parser ?
        parsed_data = self._parse_xml_to_dict(data)
        if esteem_id:
            esteem = Esteem.objects.get(id=esteem_id)
        else:
            esteem = Esteem()
        user = self._get_id_from_atom_link(parsed_data['user'])
        tag = self._get_id_from_atom_link(parsed_data['tag'])
        esteem.user = user
        esteem.tag = tag
        esteem.value = parsed_data['value']
        return esteem

    def modify_papergroup(self, data, papergroup_id=None):
        """Create or modify a papergroup object according to the specified value."""
        pass

    def modify_peerreview_template(self, data, template_id=None):
        """Create or modify a template object according to the specified value."""
        pass

    def modify_peerreview(self, data, peer_review_id=None):
        """Create or modify a peer review object according to the specified value."""
        pass

    def modify_publication(self, data, publication_id=None):
        """Create or modify a publication object according to the specified value."""
        pass

    def modify_rating(self, data, rating_id=None):
        """Create or modify a rating object according to the specified value."""
        pass

    def modify_reference_material(self, data, material_id=None):
        """Create or modify a reference material object according to the specified value."""
        pass

    def modify_tag(self, data, tag_id=None):
        """Create or modify a tag object according to the specified value."""
        pass

    def modify_user(self, data, user_id=None):
        parsed_data = self._parse_xml_to_dict(data)
        if user_id:
            user = User.objects.get(id=user_id)
        else:
            user = User.objects.create_user(parsed_data['username'], parsed_data['email'],
                parsed_data['password'])
        user_profile = user.profile
        user_profile.degree = parsed_data['degree']
        user_profile.institution = parsed_data['institution']
        fields = parsed_data['fields']
        user_profile.save()
        for item in fields:
            field, created = ProfileField.objects.get_or_create(value=item, user_profile=user_profile)
            field.userprofile = user_profile
            field.save()
        user.save()
        user_profile.save()
        return user

    def _get_namespace(self, element):
        """Return the main namespace for a given ElementTree.element."""
        namespace = element.tag[1:].split("}")[0]
        return namespace


class JsonInserter(Inserter):
    """Used to insert objects based on json representations."""
    def __init__(self, arg):
        super(JsonInserter, self).__init__()
        self.arg = arg


def get_inserter(content_type):
    """Returns an inserter based on the provided content-type.
    
    Factory function that returns a fitting parser based on the content-type that
    should be inserted.
    
    Attributes:
        content_type: the content-type the user wants to insert - should be either
            xml or json.
    
    Returns:
        inserter: an inserter that can be used to insert the given format."""
    if 'xml' in content_type:
        return XmlInserter()
    elif 'json' in content_type:
        return JsonInserter()
    else:
        raise AttributeError("No inserter for specified value present.")

def insert_bibtex_publication(bibtex, owner):
    """Will insert a publication from a bibtex string.

    This function will parse the bibtex format and perform the following transformations:
    - Keywords will be transformed into keywords.
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
        keywords = []
        for field in entry.fields.asList():
            key = field[0].lower()
            value = field[1]
            if key == "keywords":
                #create keyword
                kw = value.split(',')
                for k in kw:
                    keyw, created = Keyword.objects.get_or_create(keyword=k)
                    keywords.append(keyw)
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
                    further_field = FurtherField()
                    further_field.key = key
                    further_field.value = value
                    further_fields.append(further_field)
        try:
            validate_required_fields(publication)
            publication.save()
            for field in further_fields:
                field.publication = publication
                field.save()
            for keyword in keywords:
                keyword.publication_set.add(publication)
                keyword.save()
            for author in authors:
                publication.authors.add(author)
                publication.save()
            inserted_publication.append(publication)
        except MissingValueException, e:
            raise e
    return inserted_publication

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
