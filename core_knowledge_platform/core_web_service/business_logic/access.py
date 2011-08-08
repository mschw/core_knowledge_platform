"""This module is used to perform access verification based on user objects that need
certain priviledges."""

import pdb
from core_web_service.models import PaperGroup
from django.contrib.auth.models import User


def check_priviledges_for_editor(user):
    """Validate if a user still fulfills the requirements to be an editor."""
    papergroups = PaperGroup.objects.filter(editors__id__in=[user.id])
    if not papergroups:
        # TODO: remove editor role
        user.groups.remove('editor')

def check_priviledges_for_referee(user):
    """Validate if a user still fulfills the requirements to be a referee."""
    papergroups = PaperGroup.objects.filter(referees__id__in=[user.id])
    if not papergroups:
        user.groups.remove('referee')
        # TODO: make sure the group exists?

def validate_referee_or_editor(user, papergroup_id):
    """Return true if a user is an editor/referee in a special group, false otherwise."""
    papergroup = PaperGroup.objects.get(id=papergroup_id)
    valid = False
    if user in papergroup.referees.all():
        valid = True
    if user in papergroup.editors.all():
        valid = True
    return valid
