"""Module to act upon receiving signals from the django framework."""
from django.db.models.signals import post_save
from django.dispatch import receiver
from core_web_service.models import PaperGroup

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
