from django.conf.urls.defaults import *
from main.views import home,app,genSession,authenticate,genList,genDropbox
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
    ('^dbox/$', genDropbox),


    

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
