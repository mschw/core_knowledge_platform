from django.db import models
from django.contrib.auth.models import User

# Publication related classes


class Author(models.Model):
    """Represents an author in the model.
    Authors are not equal to Users."""
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    affiliation = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)


class Vote(models.Model):
    """Represents a vote (either an up or downvote) for a comment."""
    vote = models.CharField(max_length=4)


class Tag(models.Model):
    """Represents a tag that can be added to a publication"""
    name = models.SlugField(max_length=75)
    description = models.CharField(max_length=511)


class Comment(models.Model):
    """Represents a comment. Comments can be added to publications and other comments."""
    # FIXME: only one vote per comment?
    title = models.CharField(max_length=75)
    text = models.TextField()
    vote = models.ForeignKey(Vote)


class Esteem(models.Model):
    """Represents the esteem a User can obtain.
    Esteem is tied to a User and a specific tag."""
    user = models.ForeignKey(User)
    tag = models.ForeignKey(Tag)
    value = models.IntegerField()


class Keyword(models.Model):
    """Stores keywords for a publication that were specified by the author."""
    keyword = models.CharField(max_length=255, blank = True, null = True)


class Publication(models.Model):
    """Class to store publication metadata in the system."""
    PUBLIC_STATUS = 1
    REVIEWED_STATUS = 2
    IN_REVIEW_STATUS = 3
    STATUS_CHOICES = (
            (PUBLIC_STATUS, 'Public'),
            (REVIEWED_STATUS, 'Reviewed'),
            (IN_REVIEW_STATUS, 'Being reviewed'),
            )
    abstract = models.TextField(blank=True)
    address = models.CharField(max_length = 255, blank = True, null = True)
    booktitle = models.CharField(max_length = 255, blank = True, null = True)
    chapter = models.CharField(max_length = 255, blank = True, null = True)
    edition = models.CharField(max_length = 255, blank = True, null = True)
    editor = models.CharField(max_length = 255, blank = True, null = True)
    how_published = models.CharField(max_length = 255, blank = True, null = True)
    institution = models.CharField(max_length = 255, blank = True, null = True)
    isbn = models.CharField(max_length = 255, blank = True, null = True)
    journal = models.CharField(max_length = 255, blank = True, null = True)
    number = models.CharField(max_length = 255, blank = True, null = True)
    organization = models.CharField(max_length = 255, blank = True, null = True)
    pages = models.CharField(max_length = 255, blank = True, null = True)
    publisher = models.CharField(max_length = 255, blank = True, null = True)
    review_status = models.IntegerField(choices=STATUS_CHOICES, default=PUBLIC_STATUS)
    series = models.CharField(max_length = 255, blank = True, null = True)
    publication_type = models.CharField(max_length = 255, blank = True, null = True)
    volume = models.CharField(max_length = 255, blank = True, null = True)
    title = models.CharField(max_length = 255)
    month = models.CharField(max_length = 255, blank = True, null = True)
    note = models.TextField(blank = True, null = True)
    year = models.IntegerField(blank = True, null = True)
    # TODO: check how to reference integrated User subsystem
    owner = models.ForeignKey(User)
    authors = models.ManyToManyField(Author)
    comments = models.ManyToManyField(Comment)
    tags = models.ManyToManyField(Tag)
    keywords = models.ManyToManyField(Keyword)


class PaperGroup(models.Model):
    """Store an editor for a certain group."""
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    blind_review = models.BooleanField()
    editors = models.ManyToManyField(User, related_name='papergroup_editors')
    referees = models.ManyToManyField(User, related_name='papergroup_referees')
    publications = models.ManyToManyField(Publication)
    tags = models.ManyToManyField(Tag)


class UserProfile(models.Model):
    """Stores additional information about a user not in the system."""
    user = models.ForeignKey(User, unique=True)
    degree = models.CharField(max_length=255, blank=True, null=True)
    authenticated_professional = models.BooleanField()
    institution = models.CharField(max_length=255, blank=True, null=True)


class ProfileField(models.Model):
    """A key-value storage for further fields of the user profile."""
    key = models.CharField(max_length=255)
    value = models.TextField()
    user_profile = models.ForeignKey(UserProfile)


class FurtherField(models.Model):
    """A key-value storage that will store values that are not part of the publication table."""
    key = models.CharField(max_length=255)
    value = models.TextField()
    publication = models.ForeignKey(Publication)


class PeerReviewTemplate(models.Model):
    """Represent templates for a peer review report."""
    template_text = models.TextField()
    # Storing the path to the binary file containing a template.
    # 4096 - Maximum path length on a UNIX file system: /usr/src/linux-2.4.20-8/include/linux/limits.h.
    template_binary_path = models.CharField(max_length=4096)


class PeerReview(models.Model):
    """Represents a peer review."""
    peer_reviewer = models.OneToOneField(User)
    publication = models.ForeignKey(Publication)
    template = models.ForeignKey(PeerReviewTemplate)
    title = models.CharField(max_length=255)
    review = models.TextField()
    class Meta:
        permissions = (
                ("can_view", "Can see the available peer reviews."),
                )


class Rating(models.Model):
    """Represents a vote cast by a User for a publication of comment."""
    publication = models.ForeignKey(Publication)
    rating = models.DecimalField(max_digits=4, decimal_places=2)


class ReferenceMaterial(models.Model):
    """Represents a reference to special material associated with a publications.
    This material can be any kind of file that is referenced via a url."""
    publication = models.ForeignKey(Publication)
    name = models.CharField(max_length=75)
    url = models.URLField()
    notes = models.TextField()

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
