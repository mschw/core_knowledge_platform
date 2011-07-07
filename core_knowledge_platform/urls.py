from django.conf.urls.defaults import *
from core_web_service.views import Authors, AuthorDetail, Comments, CommentDetail, EsteemDetail, PeerReviews, PeerReviewDetail, PeerReviewTemplates, PeerReviewTemplateDetail, Publications, PublicationDetail, RatingDetail, ReferenceMaterialDetail, Tags, TagDetail
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('core_web_service.views',
        # $ at the end will transfer the query string to the view function.
        (r'^/$', 'overview'),
        (r'^author/$', Authors()),
        (r'^author/(\d+)$', AuthorDetail()),
        (r'^comment/(\d+)$', CommentDetail()),
        (r'^comment/publication/(\d+)$', Comments()),
        (r'^esteem/user/(\d+)$', EsteemDetail()),
        (r'^esteem/user/(\d+)/tag/(\d+)$', EsteemDetail()),
        (r'^peerreview/(\d+)$', PeerReviewDetail()),
        (r'^peerreview/publication/(\d+)$', PeerReviews()),
        (r'^peerreviewtemplate/$', PeerReviewTemplates()),
        (r'^peerreviewtemplate/(\d+)$', PeerReviewTemplateDetail()),
        (r'^peerreviewtemplate/peerreview/(\d+)$', PeerReviewTemplates()),
        (r'^publication/$', Publications()),
        (r'^publication/(\d+)$', PublicationDetail()),
        (r'^rating/publication/(\d+)$', RatingDetail()),
        (r'^referencematerial/(\d+)$', ReferenceMaterialDetail()),
        (r'^tag/$', Tags()),
        (r'^tag/(\d+)$', TagDetail()),
    # Example:
    # (r'^core_knowledge_platform/', include('core_knowledge_platform.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
