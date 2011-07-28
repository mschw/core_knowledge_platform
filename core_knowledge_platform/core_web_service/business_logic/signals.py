import pdb
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from core_web_service.models import Comment, Esteem, PaperGroup, UserProfile
from core_web_service.models import Vote


"""Module to act upon receiving signals from the django framework."""

@receiver(post_save, sender=PaperGroup)
def handle_assignment_to_papergroup_groups(sender, **kwargs):
    """Assign all editors in a papergroup to the editor group, all referees to the referee group."""
    papergroup = kwargs['instance']
    editors = papergroup.editors
    for editor in editors.all():
        editor.groups.add('editor')
        editor.save()
    referees = papergroup.referees
    for referee in referees.all():
        referee.groups.add('referee')
        referee.save()

@receiver(pre_save, sender=UserProfile)
def automatically_create_esteem_for_new_user(sender, **kwargs):
    """docstring for automatically_create_esteem_for_new_user"""
    user_profile = kwargs['instance']
    try:
        esteem = user_profile.esteem
    except Esteem.DoesNotExist:
        esteem = Esteem()
        esteem.save()
        user_profile.esteem = esteem

# TODO: calculate esteem based on comments.
# FIXME: When a user that uploaded the document upvoted it you gain +20 esteem points.
@receiver(post_save, sender=Vote)
def recalculate_esteem_for_user(sender, **kwargs):
    """Use the information from a vote to recalculate the esteem of a user."""
    new_esteem = 0
    vote = kwargs['instance']
    comment = vote.comment
    publication = comment.publication
    user = comment.user
    old_esteem = user.profile.esteem.value
    esteem = user.profile.esteem
    if user:
        publication = comment.publication
        publication_owner = publication.owner
        if vote.votetype == 0:
            m = 1
        else:
            m = -1
        caster = vote.caster
        if caster == publication_owner:
            new_esteem += 20 * m
        else:
            new_esteem += 5 * m
    new_esteem = old_esteem + new_esteem
    esteem.value = new_esteem
    esteem.save()
