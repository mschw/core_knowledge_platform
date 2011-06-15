from django.db import models
from django.contrib.auth.models import User

# Publication related classes

class Author(models.Model):
    """Represents an author in the model.
    Authors are not equal to Users."""
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    h_index = models.CharField(max_length=255)

class Vote(models.Model):
    """Represents a vote (either an up or downvote) for a comment."""
    vote = models.CharField(max_length=4)

class Tag(models.Model):
    """Represents a tag that can be added to a publication"""
    name = models.CharField(max_length=75)
    description = models.CharField(max_length=511)

class Comment(models.Model):
    """Represents a comment. Comments can be added to publications and other comments."""
    title = models.CharField(max_length=75)
    text = models.TextField()
    # TODO: Include relationships
    vote = models.ForeignKey(Vote)

class Esteem(models.Model):
    """Represents the esteem a User can obtain.
    Esteem is tied to a User and a specific tag."""
    User = models.ForeignKey(User)
    tag = models.ForeignKey(Tag)
    value = models.IntegerField()

class PeerReview(models.Model):
    """Represents a peer review."""
    peer_reviewer = models.OneToOneField(User)
    title = models.CharField(max_length=255)
    review = models.TextField()

class Rating(models.Model):
    """Represents a vote cast by a User for a publication of comment."""
    rating = models.DecimalField(max_digits=3, decimal_places=2)

class Publication(models.Model):
    """Class to store publication metadata in the system."""
    address          = models.CharField(max_length = 255, blank = True, null = True)
    booktitle        = models.CharField(max_length = 255, blank = True, null = True)
    chapter          = models.CharField(max_length = 255, blank = True, null = True)
    edition          = models.CharField(max_length = 255, blank = True, null = True)
    editor           = models.CharField(max_length = 255, blank = True, null = True)
    how_published    = models.CharField(max_length = 255, blank = True, null = True)
    institution      = models.CharField(max_length = 255, blank = True, null = True)
    isbn             = models.CharField(max_length = 255, blank = True, null = True)
    journal          = models.CharField(max_length = 255, blank = True, null = True)
    number           = models.CharField(max_length = 255, blank = True, null = True)
    organization     = models.CharField(max_length = 255, blank = True, null = True)
    pages            = models.CharField(max_length = 255, blank = True, null = True)
    publisher        = models.CharField(max_length = 255, blank = True, null = True)
    series           = models.CharField(max_length = 255, blank = True, null = True)
    publication_type = models.CharField(max_length = 255, blank = True, null = True)
    volume           = models.CharField(max_length = 255, blank = True, null = True)
    citation_count   = models.IntegerField(blank   = True)
    title            = models.CharField(max_length = 255)
    month            = models.CharField(max_length = 255, blank = True)
    note             = models.TextField(blank      = True)
    year             = models.IntegerField(blank   = True)
    # TODO: check how to reference integrated User subsystem
    owner        = models.ForeignKey(User)
    authors      = models.ManyToManyField(Author)
    comments     = models.ManyToManyField(Comment)
    tags         = models.ManyToManyField(Tag)
    rating       = models.ForeignKey(Rating)
    peer_reviews = models.ForeignKey(PeerReview)

class ReferenceMaterial(models.Model):
    """Represents a reference to special material associated with a publications.
    This material can be any kind of file that is referenced via a url."""
    publication = models.ForeignKey(Publication)
    name = models.CharField(max_length=75)
    url = models.URLField()
    notes = models.TextField()

