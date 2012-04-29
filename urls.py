from django.conf.urls.defaults import *
from django.conf import settings
from main.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^wing/', include('wing.foo.urls')),
    ('^$', home),
    ('^home/$',home),
    ('^gen/$',genSession), 
    ('^gen/([A-Za-z]{0,20})',genSession),
    ('^auth/$',authenticate),
    ('^list/$',genList),
    ('^app/(\d{1,30})' , genDropbox),
    ('^auth/(\d{1,30})/([-\w]+)/$' , auth),
    ('^study/(\d{1,30})/([-\w]+)/$' , study),
    ('^dbox/$', genDropbox),
    ('^rest/', include('wing.rest.urls')),
    ('^sync/(\d{1,30})', syncFromServer),
    

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^%s/Dropbox/Apps/(\d{1,30})/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )

urlpatterns += staticfiles_urlpatterns()
