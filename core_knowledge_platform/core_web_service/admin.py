from django.contrib import admin
from core_web_service.models import Author, Vote, Tag, Comment, Esteem, Publication, FurtherField, PeerReviewTemplate, PeerReview, ProfileField, Rating, ReferenceMaterial

admin.site.register(Author)
admin.site.register(Vote)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Esteem)
admin.site.register(Publication)
admin.site.register(FurtherField)
admin.site.register(ProfileField)
admin.site.register(PeerReviewTemplate)
admin.site.register(PeerReview)
admin.site.register(Rating)
admin.site.register(ReferenceMaterial)
