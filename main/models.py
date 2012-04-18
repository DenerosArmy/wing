from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.forms import UserCreationForm
from django import forms

	
class Session(models.Model):
	""" An actual wing session, keeps track of users, tokbox session, the subject, and dropbox folder 
	:ivar OneToMany users: all users in this session
	:ivar IntField count: Number of users in this page
	:ivar IntField countCap: Max number of users allowed in this session
	:ivar CharField fileName: Specific dropbox folder name on our server
	:ivar CharField sessionId: TokBox Session ID
	:ivar CharField subject: Subject that this session is studying
	:ivar CharField textEditor: link to Session text editor link 
	:ivar CharField name: name of session
	"""
	subject = models.CharField(max_length = 30) 
	users = models.ManyToManyField(User,related_name="session",blank=True) 
	count = models.FloatField()
	countCap = models.FloatField() 
	fileName = models.CharField(max_length =100) 
	sessionId = models.CharField(max_length= 50) 
	textEditor = models.CharField(max_length = 300) 
	name = models.CharField(max_length=28) 
	def changeCount(self,number): 
			self.count += number
			self.save()

			

		



class User(models.Model): 
	""" The user object, keeps track of their session, and their own personal dropbox folder
	:ivar ManyToOne session: The session that the user is enrolled in 
	:ivar CharField personalFile: Their own specfic dropbox folder 
	:ivar CharField textEditor: link to specfic text editor link 
	"""
	session = models.ForeignKey(Session)
	personalFile = models.CharField(max_length = 30) 
	textEditor = models.CharField(max_length = 300) 

	
