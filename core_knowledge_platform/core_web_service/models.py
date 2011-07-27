from django.db import models
from django.contrib.auth.models import User

# Publication related classes


class Author(models.Model):
    """Represents an author in the model.
    Authors are not equal to Users."""
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    affiliation = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return u'%s - %s' % (self.id, self.name)


class Tag(models.Model):
    """Represents a tag that can be added to a publication"""
    name = models.SlugField(max_length=75)
    description = models.CharField(max_length=511)

    def __unicode__(self):
        return u'%s - %s' % (self.id, self.name)


class Esteem(models.Model):
    """Represents the esteem a User can obtain."""
    value = models.IntegerField(default=0)

    def __unicode__(self):
        return u'%s - %s' % (self.id, self.value)


class Keyword(models.Model):
    """Stores keywords for a publication that were specified by the author."""
    keyword = models.CharField(max_length=255, blank = True, null = True)

    def __unicode__(self):
        return u'%s - %s' % (self.id, self.keyword)


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
    # TODO: Validate a DOI to be valid.
    doi = models.CharField(max_length = 255, blank = True, null = True)
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
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    keywords = models.ManyToManyField(Keyword, blank=True, null=True)

    def __unicode__(self):
        return u'%s - %s' % (self.id, self.title)


class Comment(models.Model):
    """Represents a comment. Comments can be added to publications and other comments."""
    title = models.CharField(max_length=75)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    publication = models.ForeignKey(Publication)
    user = models.ForeignKey(User, blank=True, null=True)

    def __unicode__(self):
        return u'%s - %s' % (self.id, self.title)


class Vote(models.Model):
    """Represents a vote (either an up or downvote) for a comment."""
    VOTE_CHOICES = (
            (0, 'upvote'),
            (1, 'downvote'),
            )
    votetype = models.IntegerField(max_length=1, choices=VOTE_CHOICES)
    # A vote needs a user, but a user needs no votes
    caster = models.ForeignKey(User, blank=True, null=True)
    comment = models.ForeignKey(Comment)

    def vote_type_string(self):
        if self.votetype == 0:
            return self.VOTE_CHOICES[0][1]
        else:
            return self.VOTE_CHOICES[1][1]

    def __unicode__(self):
        vote = self.vote_type_string()
        return u'%s - %s' % (self.id, vote)


class Rating(models.Model):
    """Represents a vote cast by a User for a publication of comment."""
    CHOICES = [(i, i) for i in range(6)]
    rating = models.IntegerField(max_length=1, choices=CHOICES)
    publication = models.ForeignKey(Publication)

    def __unicode__(self):
        return u'%s - %s' % (self.id, self.rating)


class PaperGroup(models.Model):
    """Store an editor for a certain group."""
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    blind_review = models.BooleanField()
    editors = models.ManyToManyField(User, related_name='papergroup_editors')
    referees = models.ManyToManyField(User, related_name='papergroup_referees', null=True, blank=True)
    publications = models.ManyToManyField(Publication)
    tags = models.ManyToManyField(Tag)

    def __unicode__(self):
        return u'%s - %s' % (self.id, self.title)


class ResearchArea(models.Model):
    """Store research areas for users."""
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u'%s - %s' % (self.id, self.title)


class UserProfile(models.Model):
    """Stores additional information about a user not in the system."""
    user = models.ForeignKey(User, unique=True)
    esteem = models.OneToOneField(Esteem)
    degree = models.CharField(max_length=255, blank=True, null=True)
    authenticated_professional = models.BooleanField()
    institution = models.CharField(max_length=255, blank=True, null=True)
    research_areas = models.ManyToManyField(ResearchArea, blank=True, null=True)


class ProfileField(models.Model):
    """A key-value storage for further fields of the user profile."""
    key = models.CharField(max_length=255)
    value = models.TextField()
    user_profile = models.ForeignKey(UserProfile)

    def __unicode__(self):
        return u'%s - %s' % (self.id, self.key)


class FurtherField(models.Model):
    """A key-value storage that will store values that are not part of the publication table."""
    key = models.CharField(max_length=255)
    value = models.TextField()
    publication = models.ForeignKey(Publication)

    def __unicode__(self):
        return u'%s - %s' % (self.id, self.key)


class PeerReviewTemplate(models.Model):
    """Represent templates for a peer review report."""
    template_text = models.TextField()
    # Storing the path to the binary file containing a template.
    # 4096 - Maximum path length on a UNIX file system: /usr/src/linux-2.4.20-8/include/linux/limits.h.
    template_binary_path = models.CharField(max_length=4096)
    
    def __unicode__(self):
        return u'%s' % (self.id)


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

    def __unicode__(self):
        return u'%s - %s' % (self.id, self.title)


class ReferenceMaterial(models.Model):
    """Represents a reference to special material associated with a publications.
    This material can be any kind of file that is referenced via a url."""
    publication = models.ForeignKey(Publication)
    name = models.CharField(max_length=75)
    url = models.URLField()
    notes = models.TextField()

    def __unicode__(self):
        return u'%s - %s' % (self.id, self.name)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
from core_web_service.business_logic.signals import *
