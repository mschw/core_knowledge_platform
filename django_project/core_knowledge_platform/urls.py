from django.conf.urls.defaults import *
from core_web_service.views import Publications, PublicationDetail

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
        # $ at the end will transfer the query string to the view function.
        (r'^publications/$', Publications()),
        (r'^publication/(\d+)$', PublicationDetail()),
        (r'^authors/$', 'authors'),
        (r'^author/(\d+)$', 'author'),
    # Example:
    # (r'^core_knowledge_platform/', include('core_knowledge_platform.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
