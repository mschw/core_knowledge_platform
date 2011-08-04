from core_web_service.models import Vote
from core_web_service.business_logic.access import check_priviledges_for_referee
from core_web_service.business_logic.access import check_priviledges_for_editor
from abc import ABCMeta, abstractmethod
import pdb
import logging
from xml.etree.ElementTree import XML, ParseError

from core_web_service.bibtex_parser.bibtex_parser import BibtexParser
from core_web_service.models import Rating, PeerReview, PeerReviewTemplate, Tag, Esteem, Vote, Author, Publication, ProfileField, FurtherField, Keyword, User, Comment, PaperGroup, ReferenceMaterial

logger = logging.getLogger('myproject.custom')


class MissingValueException(Exception):
    """Raise when a publication is missing a required attribute."""
    def __init__(self, message):
        super(MissingValueException, self).__init__()
        self.message = message
    
    def __str__(self):
        return repr(self.message)


class InvalidDataException(Exception):
    """Raise when an insert is attempted that has no data."""
    def __init__(self, message):
        super(InvalidDataException, self).__init__()
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
    def modify_comment(self, data, comment_id=None, user_id=None):
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
    def modify_peerreviewtemplate(self, data, template_id=None):
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
    def modify_rating(self, data, rating_id):
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

    @abstractmethod
    def modify_vote(self, data, vote_id=None):
        """docstring for modify_vote"""
        pass

class XmlInserter(Inserter):
    """Used to insert objects based on xml representations."""
    def __init__(self):
        super(XmlInserter, self).__init__()

    def _get_id_from_atom_link(self, link):
        """Return the id of an objects from an atom link."""
        if (link) and ("link" in link[0].tag):
            link_text = link[0].attrib['href']
            return link_text.split('/')[-1]
        else:
            # TODO: Decide if exception should be raised.
            return None

    def _parse_xml_to_dict(self, data):
        """Parses a xml document and returns a dictionary of values.
        
        Only works for a nested depth of 2 levels:
            <a>
                <b>
                </b>
            </a>
        """
        parsed_dict = dict()
        try:
            node_tree = XML(data.strip())
            namespace = self._get_namespace(node_tree)
            namespace = "{%s}" % (namespace)
            for node in node_tree:
                tag = node.tag.replace(namespace, "")
                if len(node) > 0:
                    parsed_dict[tag] = []
                    for subnode in node:
                        parsed_dict[tag].append(subnode)
                else:
                    text = node.text
                    if text:
                        parsed_dict[tag] = text.strip()
                    else:
                        parsed_dict[tag] = ""
            return parsed_dict
        except ParseError, e:
            logger.error(e)
            logger.error(e.message)
            raise InvalidDataException("The data provided was not a valid XML\
                    document. Please validate your xml and try again.")

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

    def modify_comment(self, data, comment_id=None, user_id=None):
        """Create or modify a comment object according to the specified value."""
        parsed_data = self._parse_xml_to_dict(data)
        if comment_id:
            comment = Comment.objects.get(id=comment_id)
        else:
            comment = Comment()
        if not user_id:
            user_id = self._get_id_from_atom_link(parsed_data['user'])
        try:
            user = User.objects.get(id=user_id)
            publication_id = self._get_id_from_atom_link(parsed_data['publication'])
            comment.publication = Publication.objects.get(id=publication_id)
            comment.user = user
            comment.title = parsed_data['title']
            comment.text = parsed_data['text']
            comment.save()
            return comment
        except User.DoesNotExist:
            raise InvalidDataException("The user provided does not exist (id: %s)" %
                    (user_id))
        except Publication.DoesNotExist:
            raise InvalidDataException("The publication provided does not exist (id: %s)" 
                    % publication_id)
        except KeyError, e:
            raise InvalidDataException("The data sent was missing an attribute!")

    def modify_esteem(self, data, esteem_id=None):
        """Create or modify an esteem object according to the specified value."""
        parsed_data = self._parse_xml_to_dict(data)
        if esteem_id:
            esteem = Esteem.objects.get(id=esteem_id)
        else:
            esteem = Esteem()
        try:
            user_id = self._get_id_from_atom_link(parsed_data['user'])
            user = User.objects.get(id=user_id)
            esteem.user = user
            esteem.value = parsed_data['value']
            esteem.save()
            return esteem
        except User.DoesNotExist:
            raise InvalidDataException("The user provided does not exist (id: %s)"
                    % (user_id))
        except KeyError, e:
            raise InvalidDataException("The data sent was missing an attribute!")

    def modify_keyword(self, data, keyword_id=None):
        """Create or modify a keyword object according to the specified values."""
        try:
            parsed_data = self._parse_xml_to_dict(data)
            if keyword_id:
                keyword = Keyword.objects.get(id=keyword_id)
            else:
                keyword = Keyword()
            keyword.keyword = parsed_data['keyword']
            keyword.save()
            return keyword
        except KeyError, e:
            raise InvalidDataException("The data sent was missing an attribute!")

    def modify_papergroup(self, data, papergroup_id=None):
        """Create or modify a papergroup object according to the specified value."""
        # TODO: check if editors are added / removed.
        try:
            parsed_data = self._parse_xml_to_dict(data)
            if papergroup_id:
                papergroup = PaperGroup.objects.get(id=papergroup_id)
                editors = papergroup.editors.all()
                referees = papergroup.editors.all()
            else:
                papergroup = PaperGroup()
            papergroup.title = parsed_data['title']
            papergroup.description = parsed_data['description']
            papergroup.blind_review = parsed_data['blind_review']
            papergroup.save()
            for e in parsed_data['editors']:
                try:
                    editor_id = self._get_id_from_atom_link(e)
                    editor = User.objects.get(id=editor_id)
                    papergroup.editors.add(editor)
                except User.DoesNotExist:
                    raise InvalidDataException("The user provided does not exist (id: %s)"
                            % (editor_id))
            editors = papergroup.editors
            for r in parsed_data['referees']:
                try:
                    referee_id = self._get_id_from_atom_link(r)
                    referee = User.objects.get(id=referee_id)
                    papergroup.referees.add(referee)
                except User.DoesNotExist:
                    raise InvalidDataException("The user provided does not exist (id: %s)"
                            % (referee_id))
            referees = papergroup.referees
            for p in parsed_data['publications']:
                try:
                    publication_id = self._get_id_from_atom_link(p)
                    publication = Publication.objects.get(id=publication_id)
                    papergroup.publications.add(publication)
                except Publication.DoesNotExist:
                    raise InvalidDataException("The publication provided does not exist (id: %s)"
                            % (publication_id))
            for t in parsed_data['tags']:
                try:
                    tag_id = self._get_id_from_atom_link(t)
                    tag = Tag.objects.get(id=tag_id)
                    papergroup.tags.add(tag)
                except Tag.DoesNotExist:
                    raise InvalidDataException("The tag provided does not exist (id: %s)"
                            % (tag_id))
            if editors:
                for editor in editors.all():
                    check_priviledges_for_editor(editor)
            if referees:
                for referee in referees.all():
                    check_priviledges_for_referee(referee)
            return papergroup
        except KeyError, e:
            raise InvalidDataException('The data you sent was missing an attribute')

    def modify_peerreviewtemplate(self, data, template_id=None):
        """Create or modify a template object according to the specified value."""
        try:
            parsed_data = self._parse_xml_to_dict(data)
            if template_id:
                template = PeerReviewTemplate.objects.get(id=template_id)
            else:
                template = PeerReviewTemplate()
            template.template_text = parsed_data['templatetext']
            template.template_binary_path = parsed_data['binarypath']
            template.save()
            return template
        except KeyError, e:
            raise InvalidDataException('The data sent was missing an attribute')

    def modify_peerreview(self, data, peer_review_id=None):
        """Create or modify a peer review object according to the specified value."""
        parsed_data = self._parse_xml_to_dict(data)
        if peer_review_id:
            peerreview = PeerReview.objects.get(id=peer_review_id)
        else:
            peerreview = PeerReview()
        try:
            peerreviewer_id = self._get_id_from_atom_link(parsed_data['peerreviewer'])
            peerreview.peer_reviewer = User.objects.get(id=peerreviewer_id)
            publication_id = self._get_id_from_atom_link(parsed_data['publication'])
            peerreview.publication = Publication.objects.get(id=publication_id)
            template_id = self._get_id_from_atom_link(parsed_data['template'])
            peerreview.template = PeerReviewTemplate.objects.get(id=template_id)
            peerreview.title = parsed_data['title']
            peerreview.review = parsed_data['review']
            peerreview.save()
            return peerreview
        except User.DoesNotExist:
            raise InvalidDataException("The user provided does not exist (id: %s)"
                    % (peerreviewer_id))
        except Publication.DoesNotExist:
            raise InvalidDataException("The publication provided does not exist (id: %s)"
                    % (publication_id))
        except PeerReviewTemplate.DoesNotExist:
            raise InvalidDataException("The template provided does not exist (id: %s)"
                    % (template_id))
        except KeyError, e:
            raise InvalidDataException("The data sent was missing an attribute!")


    def modify_publication(self, data, publication_id=None, requester=None):
        """Create or modify a publication object according to the specified value."""
        try:
            parsed_data = self._parse_xml_to_dict(data)
            if publication_id:
                publication = Publication.objects.get(id=publication_id)
            else:
                publication = Publication()
            publication.address = parsed_data['address']
            publication.booktitle = parsed_data['booktitle']
            publication.chapter = parsed_data['chapter']
            publication.edition = parsed_data['edition']
            publication.editor = parsed_data['editor']
            publication.how_published = parsed_data['howpublished']
            publication.institution = parsed_data['institution']
            publication.isbn = parsed_data['isbn']
            publication.journal = parsed_data['journal']
            publication.number = parsed_data['number']
            publication.organization = parsed_data['organization']
            publication.pages = parsed_data['pages']
            publication.publisher = parsed_data['publisher']
            publication.review_status = parsed_data['review_status']
            publication.series = parsed_data['series']
            publication.publication_type = parsed_data['publicationtype']
            publication.volume = parsed_data['volume']
            publication.title = parsed_data['title']
            publication.month = parsed_data['month']
            publication.note = parsed_data['note']
            publication.year = parsed_data['year']
            owner_id = self._get_id_from_atom_link(parsed_data['owner'])
            xml_owner = User.objects.get(id=owner_id)
            if publication_id:
                current_owner = User.objects.get(id=publication.owner.id)
                if requester:
                    if current_owner == requester:
                        publication.owner = requester
                    else:
                        raise InvalidDataException("Only the owner can change the publication.")
                else:
                    publication.owner = xml_owner
            else:
                if requester:
                    publication.owner = requester
                elif xml_owner:
                    publication.owner = xml_owner 
            publication.save()
            for a in parsed_data['authors']:
                author_id = self._get_id_from_atom_link(a)
                if author_id:
                    author = Author.objects.get(id=author_id)
                    publication.authors.add(author)
            for t in parsed_data['tags']:
                tag_id = self._get_id_from_atom_link(t)
                if tag_id:
                    tag = Tag.objects.get(id=tag_id)
                    publication.tags.add(tag)
            for r in parsed_data['referencematerials']:
                material_id = self._get_id_from_atom_link(r)
                if material_id:
                    material = ReferenceMaterial.objects.get(id=material_id)
                    publication.referencematerial_set.add(material)
            for f in parsed_data['fields']:
                key = f.tag
                furtherfield, created = FurtherField.objects.get_or_create(key=key, publication=publication)
            publication.save()
            return publication
        except User.DoesNotExist:
            raise InvalidDataException("The user provided does not exist (id: %s)"
                    % (owner_id))
        except Author.DoesNotExist:
            raise InvalidDataException("The author provided does not exist (id: %s)"
                    % (author_id))
        except Tag.DoesNotExist:

            raise InvalidDataException("The tag provided does not exist (id: %s)"
                    % (tag_id))
        except ReferenceMaterial.DoesNotExist:
            raise InvalidDataException("The reference material provided does not exist (id: %s)"
                    % (material_id))
        except KeyError, e:
            raise InvalidDataException("The data sent was missing an attribute!")

    def modify_rating(self, data, rating_id=None):
        """Create or modify a rating object according to the specified value."""
        if rating_id:
            rating = Rating.objects.get(id=rating_id)
        else:
            rating = Rating()
        try:
            parsed_data = self._parse_xml_to_dict(data)
            new_rating = parsed_data['rating']
            publication_id = self._get_id_from_atom_link(parsed_data['publication'])
            publication = Publication.objects.get(id=publication_id)
            rating.rating = new_rating
            rating.publication = publication
            rating.save()
            return rating
        except Publication.DoesNotExist:
            raise InvalidDataException("The publication provided does not exist (id: %s)"
                    % (publication_id))
        except KeyError, e:
            raise InvalidDataException("The data sent was missing an attribute!")

    def modify_reference_material(self, data, material_id=None):
        """Create or modify a reference material object according to the specified value."""
        parsed_data = self._parse_xml_to_dict(data)
        if material_id:
            material = ReferenceMaterial.objects.get(id=material_id)
        else:
            material = ReferenceMaterial()
        try:
            publication_id = self._get_id_from_atom_link(parsed_data['publication'])
            material.publication = Publication.objects.get(id=publication_id)
            material.name = parsed_data['name']
            material.url = parsed_data['url']
            material.notes = parsed_data['notes']
            material.save()
            return material
        except Publication.DoesNotExist:
            raise InvalidDataException("The publication provided does not exist (id: %s)"
                    % (publication_id))
        except KeyError, e:
            raise InvalidDataException("The data sent was missing an attribute!")

    def modify_tag(self, data, tag_id=None):
        """Create or modify a tag object according to the specified value."""
        try:
            parsed_data = self._parse_xml_to_dict(data)
            if tag_id:
                tag = Tag.objects.get(id=tag_id)
            else:
                tag = Tag()
            tag.name = parsed_data['name']
            tag.description = parsed_data['description']
            tag.save()
            return tag
        except KeyError, e:
            raise InvalidDataException('The data sent was missing an attribute!')

    def modify_user(self, data, user_id=None):
        try:
            parsed_data = self._parse_xml_to_dict(data)
            if user_id:
                user = User.objects.get(id=user_id)
            else:
                user = User.objects.create_user(parsed_data['username'],
                        parsed_data['email'], parsed_data['password'])
            user_profile = user.profile
            user_profile.degree = parsed_data['degree']
            user_profile.institution = parsed_data['institution']
            fields = parsed_data['fields']
            user_profile.save()
            for item in fields:
                field, created = ProfileField.objects.get_or_create(value=item,
                        user_profile=user_profile)
                field.userprofile = user_profile
                field.save()
            user.save()
            user_profile.save()
            return user
        except KeyError, e:
            raise InvalidDataException('The data sent was missing an attribute!')

    def modify_vote(self, data, vote_id=None):
        parsed_data = self._parse_xml_to_dict(data)
        if vote_id:
            vote = Vote.objects.get(id=vote_id)
        else:
            vote = Vote()
        try:
            vote.votetype = parsed_data['votetype'].lower()
            comment_id = self._get_id_from_atom_link(parsed_data['comment'])
            comment = Comment.objects.get(id=comment_id)
            vote.comment = comment
            caster_id = self._get_id_from_atom_link(parsed_data['caster'])
            caster = User.objects.get(id=caster_id)
            vote.caster = caster
            return vote
        except Comment.DoesNotExist:
            raise InvalidDataException("The comment provided does not exist (id: %s)"
                    % (comment_id))
        except User.DoesNotExist:
            raise InvalidDataException("The user provided does not exist (id: %s)"
                    % (caster_id))
        except KeyError, e:
            raise InvalidDataException("The data sent was missing an attribute!")

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
        raise AttributeError("No inserter for specified value present: %s." % (content_type))

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
