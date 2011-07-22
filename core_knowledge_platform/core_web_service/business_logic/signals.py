from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from core_web_service.models import Esteem, Rating, Publication, PaperGroup, UserProfile


"""Module to act upon receiving signals from the django framework."""

@receiver(post_save, sender=PaperGroup)
def handle_assignment_to_papergroup_groups(sender, **kwargs):
    """Assign all editors in a papergroup to the editor group, all referees to the referee group."""
    papergroup = kwargs['instance']
    editors = papergroup.editors
    for editor in editors:
        editor.groups.add('editor')
        editor.save()
    referees = papergroup.referees
    for referee in referees:
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

@receiver(pre_save, sender=Publication)
def automatically_create_rating_for_new_publication(sender, **kwargs):
    """docstring for automatically_create_rating_for_new_publication("""
    publication = kwargs['instance']
    try:
        rating = publication.rating
    except Rating.DoesNotExist:
        rating = Rating()
        rating.save()
        publication.rating = rating
