from piston.handler import BaseHandler 
from wing.main.models import * 


class SessionHandler(BaseHandler):
	allowedMethods = ('GET', 'PUT') 
	model = Session  

	def read(self, request, session_id):
		base = Session.objects
		session =  base.filter(name = session_id)[0] 
		return session
