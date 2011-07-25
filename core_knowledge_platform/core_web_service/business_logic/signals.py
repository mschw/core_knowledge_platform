import pdb
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from core_web_service.models import Comment, Esteem, Rating, Publication, PaperGroup, UserProfile
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

@receiver(pre_save, sender=Comment)
def automatically_create_votes_for_new_comment(sender, **kwargs):
    """docstring for automatically_create_votes_for_new_comment"""
    comment = kwargs['instance']
    try:
        vote = comment.vote
    except Vote.DoesNotExist:
        vote = Vote()
        vote.save()
        comment.vote = vote

# TODO: calculate esteem based on comments.
# FIXME: When a user that uploaded the document upvoted it you gain +20 esteem points.
