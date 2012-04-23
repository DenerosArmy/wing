from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django import forms
import generateSessions 
import datetime
import random
from math import log10
from main.models import *
from dbox.dbox_wrapper import DropboxService

sessions=[]

def home(request):
    return render_to_response('home.html',RequestContext(request, {"CS61A":genSession,"EE40":genSession}))


def genSession(request,subject='CS61A'):
    sessionID, token = generateSessions.genSession();
    randomValue = str(int(random.random() *10000000)) 
    mySession = Session.objects.create(name=randomValue, subject=subject,count=1,countCap=6,fileName="/dropbox",sessionId=sessionID,textEditor=randomValue) 
    mySession.save() 
    return redirect('/app/' + randomValue); 

def app(request,randomValue):   
    MySession = Session.objects.filter(name=randomValue)[0]
    sessionId = MySession.sessionId
    changedString = str(int(randomValue) + MySession.count) 
    myText = changedString 
    User.objects.create(session=MySession,personalFile="",textEditor=myText) 
    MySession.changeCount(1)
    return render_to_response('app.html',RequestContext(request,{"name":randomValue,"sessionId":sessionId,"myText":changedString,"groupText":MySession.textEditor})) 

def authenticate(request):
    global session
    sess = DropboxService()
    sessions.append(sess)
    return render_to_response('dbox.html',RequestContext(request,{"url":sessions[-1].url}))

def genList(request):
    f = open('main/templates/files.html','w')
    f.write('<html><body><ul>')
    lst = sessions[0].listFiles('.')
    for pair in lst:
        f.write('<li><a href="{0}" target="freeform"> {1} </li>'.format(pair[1],pair[0]))
    f.write('</ul></body></html>')
    f.close()
    return render_to_response('files.html')

