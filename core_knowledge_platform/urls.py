from django.conf.urls.defaults import *
from django.contrib import admin
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('core_web_service.views',
        # $ at the end will transfer the query string to the view function.
        (r'^$', 'overview'),
        (r'^admin/', include(admin.site.urls)),
        (r'^author/$', 'authors'),
        (r'^author/(\d+)$', 'author_detail'),
        (r'^comment/(\d+)$', 'comment_detail'),
        (r'^comment/publication/(\d+)$', 'comments'),
        (r'^esteem/user/(\d+)$', 'esteem_detail'),
        (r'^esteem/user/(\d+)/tag/(\d+)$', 'esteem_detail'),
        (r'^peerreview/(\d+)$', 'peerreview_detail'),
        (r'^peerreview/publication/(\d+)$', 'peerreviews'),
        (r'^peerreviewtemplate/$', 'peerreview_templates'),
        (r'^peerreviewtemplate/(\d+)$', 'peerreview_template_detail'),
        (r'^peerreviewtemplate/peerreview/(\d+)$', 'peerreview_templates'),
        (r'^publication/$', 'publications'),
        (r'^publication/(\d+)$', 'publication_detail'),
        (r'^rating/publication/(\d+)$', 'rating_detail'),
        (r'^referencematerial/(\d+)$', 'reference_material_detail'),
        (r'^tag/$', 'tags'),
        (r'^tag/(\d+)$', 'tag_detail'),
    # Example:
    # (r'^core_knowledge_platform/', include('core_knowledge_platform.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
