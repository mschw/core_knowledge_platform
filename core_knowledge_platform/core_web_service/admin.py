from django.contrib import admin
from core_web_service.models import Author, Vote, Tag, Comment, Esteem, Keyword, Publication, FurtherField, PeerReviewTemplate, PeerReview, ProfileField, Rating, ReferenceMaterial, ResearchArea, UserProfile

admin.site.register(Author)
admin.site.register(Vote)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Esteem)
admin.site.register(Keyword)
admin.site.register(Publication)
admin.site.register(FurtherField)
admin.site.register(ProfileField)
admin.site.register(PeerReviewTemplate)
admin.site.register(PeerReview)
admin.site.register(Rating)
admin.site.register(ReferenceMaterial)
admin.site.register(ResearchArea)
admin.site.register(UserProfile)
