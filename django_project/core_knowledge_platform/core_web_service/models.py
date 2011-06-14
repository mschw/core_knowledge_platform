from django.db import models
from django.contrib.auth import User

# Publication related classes

class Author(models.Model):
    """Represents an author in the model.
    Authors are not equal to users."""
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
    """Represents the esteem a user can obtain.
    Esteem is tied to a user and a specific tag."""
    user = models.ForeignKey(User)
    tag = models.ForeignKey(Tag)
    value = models.IntegerField()

class PeerReview(models.Model):
    """Represents a peer review."""
    peer_reviewer = models.OneToOneField(User)
    title = models.CharField(max_length=255)
    review = models.TextField()

class Rating(models.Model):
    """Represents a vote cast by a user for a publication of comment."""
    rating = models.DecimalField()

class Publication(models.Model):
    """Abstract base class for concrete publication types."""
    title = models.CharField(max_length=255)
    citation_count = models.IntegerField()
    # TODO: check how to reference integrated user subsystem
    # owner = models.ForeignKey(User)
    authors = models.ManyToManyField(Author)
    comments = models.ManyToManyField(Comment)
    tags = models.ManyToManyField(Tag)
    rating = models.ForeignKey(Rating)
    peer_reviews = models.ForeignKey(PeerReview)
    class Meta(object):
        abstract = True

class ReferenceMaterial(models.Model):
    """Represents a reference to special material associated with a publications.
    This material can be any kind of file that is referenced via a url."""
    publication = models.ForeignKey(Publication)
    name = models.CharField(max_length=75)
    url = models.URLField()
    notes = models.TextField()

        
