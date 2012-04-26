''' A token pair class to appease OAUTH '''

class token_pair(object):
	def __init__(self,key='',secret=''):
		self.key = key
		self.secret = secret 
	
