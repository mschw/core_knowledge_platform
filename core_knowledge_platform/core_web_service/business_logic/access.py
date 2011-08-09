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

def validate_editor_for_publication(user, publication):
    """Return true of the user is an editor and the publication is being
    reviewed by a group the user is an editor of."""
    is_editor = False
    papergroups = PaperGroup.objects.filter(editors__id__in=[user.id])
    for papergroup in papergroups:
        if publication in papergroup.publications.all():
            is_editor = True
            break
    return is_editor

def user_in_group_for_publication(user, publication):
    """Return true if the user is in a group refereeing the publication, false else."""
    allow_access = False
    groups = PaperGroup.objects.filter(publications__id__in=[publication.id])
    for group in groups:
        if user in group.editors.all():
            allow_access = True
        if user in group.referees.all():
            allow_access = True
    return allow_access

def validate_access_to_peer_review_for_user(peerreview, user):
    """Return true if a user may see the peer review, false otherwise.
    
    A user can see a peerreview if the publication is publicly accessible.
    If it is still in review only an editor or the peerreviewer may see the peer review.
    
    Arguments:
        peerreview: a peerreview object.
        user: a user object.

    Returns:
        True if user is editor fo publication, false otherwise.
    """
    allow_access = False
    publication = peerreview.publication
    if publication.review_status == 3:
        if validate_editor_for_publication(user, publication):
            allow_access = True
        elif validate_user_is_peerreviewer(peerreview, user):
            allow_access = True
    else:
        allow_access = True
    return allow_access

def validate_user_is_peerreviewer(peerreview, user):
    """Return true if the user has written the peer review, false otherwise."""
    if peerreview.peer_reviewer == user:
        return True
    else:
        return False
