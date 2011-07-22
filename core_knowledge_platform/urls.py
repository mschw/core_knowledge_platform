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
        (r'^esteem/(?P<esteem_id>\d+)$', 'esteem_detail'),
        (r'^esteem/user/(?P<user_id>\d+)$', 'esteem_detail'),
        (r'^keyword/$', 'keywords'),
        (r'^keyword/(?P<keyword_id>\d+)$', 'keywords'),
        (r'^papergroup/$', 'papergroups'),
        (r'^papergroup/(\d+)$', 'papergroup_detail'),
        (r'^peerreview/(\d+)$', 'peerreview_detail'),
        (r'^peerreview/publication/(\d+)$', 'peerreviews'),
        (r'^peerreviewtemplate/$', 'peerreview_templates'),
        (r'^peerreviewtemplate/(\d+)$', 'peerreview_template_detail'),
        (r'^peerreviewtemplate/peerreview/(\d+)$', 'peerreview_templates'),
        (r'^publication/$', 'publications'),
        (r'^publication/(\d+)$', 'publication_detail'),
        (r'^publication/((?P<pub_search>[\w=&]+))?(/keyword/(?P<key_search>[\w=&]+))?(/author/(?P<auth_search>[\w=&]+))?', 'publications'),
        (r'^rating/(?P<rating_id>\d+)', 'rating_detail'),
        (r'^rating/publication/(?P<publication_id>\d+)$', 'rating_detail'),
        (r'^referencematerial/(\d+)$', 'reference_material_detail'),
        (r'^researcharea/$', 'researchareas'),
        (r'^researcharea/(?P<researcharea_id>\d+)$', 'researchareas'),
        (r'^tag/$', 'tags'),
        (r'^tag/(\d+)$', 'tag_detail'),
        (r'^user/$', 'users'),
        (r'^user/(\d+)$', 'user_detail'),
        (r'^user/((?P<user_search>[\w=&]+))?$', 'users'),
        (r'^user/login/', 'login'),
        (r'^user/logout/', 'logout'),
    # Example:
    # (r'^core_knowledge_platform/', include('core_knowledge_platform.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
