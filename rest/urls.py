from django.conf.urls.defaults import *
from piston.resource import Resource
from wing.rest.handlers import SessionHandler

sessionHandler = Resource(SessionHandler)

urlpatterns = patterns('',
    url('^(\d{1,30})' ,sessionHandler , {'emitter_format': 'json'}),
)
