from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import User
from core_web_service.models import Author, Vote, Tag, Comment, Esteem, Keyword, Publication, FurtherField, PeerReviewTemplate, PeerReview, ProfileField, Rating, ReferenceMaterial, ResearchArea, UserProfile
from core_web_service.models import PaperGroup
from core_web_service.models import PaperGroup

class AuthorAdmin(admin.ModelAdmin):
    """Defines the administration interface for authors."""
    search_fields = ['name', 'affiliation', 'email']
    list_filter = ['affiliation']

admin.site.register(Author, AuthorAdmin)

class CommentAdmin(admin.ModelAdmin):
    """Defines the administration inteface for comments."""
    search_fields = ['title', 'text']
    list_filter = ['date']
    

admin.site.register(Comment, CommentAdmin)


class UserProfileInline(admin.StackedInline):
    """Defines the user profile as an inline element for the user model."""
    model = UserProfile
    max_num = 1
    can_delete = False
    filter_horizontal = ['research_areas']


class UserAdmin(AuthUserAdmin):
    """Sets the new admin interface for the user model from the auth package."""
    inlines = [UserProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Vote)


class TagAdmin(admin.ModelAdmin):
    """Defines the administration interface for tags."""
    search_fields = ['name', 'description']

admin.site.register(Tag, TagAdmin)


class KeywordAdmin(admin.ModelAdmin):
    """Defines the administration interface for keywords."""
    search_fields = ['keyword']

admin.site.register(Keyword, KeywordAdmin)


class PaperGroupAdmin(admin.ModelAdmin):
    """Defines the administration interface for papergroups.""" 
    search_fields = ['title', 'description']
    filter_horizontal = ['editors', 'referees', 'publications', 'tags']
    list_display = ['title', 'blind_review']

admin.site.register(PaperGroup, PaperGroupAdmin)


class PublicationAdmin(admin.ModelAdmin):
    """Defines the administration interface for publications."""
    search_fields = ['title', 'abstract']
    list_filter = ['review_status']
    filter_horizontal = ['authors', 'tags', 'keywords']
    fieldsets = [
            (None, {'fields': ['title', 'booktitle', 'chapter', 'editor', 'institution', 'isbn', 'journal', 'pages', 'publisher', 'review_status', 'note', 'owner', 'authors', 'tags', 'keywords']},
                ),
                ('More information', {'fields': ['abstract', 'address', 'doi',  'edition', 'how_published', 'month', 'number', 'organization', 'series', 'publication_type', 'volume'], 'classes': ['collapse']},
                )]

admin.site.register(Publication, PublicationAdmin)
admin.site.register(PeerReviewTemplate)
admin.site.register(PeerReview)
admin.site.register(Rating)
admin.site.register(ReferenceMaterial)
admin.site.register(ResearchArea)


class EsteemAdmin(admin.ModelAdmin):
    """Defines the administration interface for esteem."""
    list_display = ['userprofile', 'value']
        
admin.site.register(Esteem, EsteemAdmin)
admin.site.register(FurtherField)
admin.site.register(ProfileField)
