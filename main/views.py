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
import appkeys
from tokenPair import * 
from dropbox import client, rest, session
import oauth.oauth

mySession = 0
serverToken = '1c69a9p4n1lli6z'
serverSecret = 'l0p08hfa4kgn7n7'

def home(request):
    return render_to_response('home.html',RequestContext(request, {"CS61A":genSession,"EE40":genSession}))


def genSession(request,subject='CS61A'):
    sessionID, token = generateSessions.genSession();
    randomValue = str(int(random.random() *10000000)) 
    mySession = Session.objects.create(name=randomValue, subject=subject,count=1,countCap=6,fileName="/dropbox",sessionId=sessionID,textEditor=randomValue) 
    mySession.save() 
    return redirect('/app/' + randomValue); 

def genDropbox(request, code):
    dbox = DropboxService()
    sess = session.DropboxSession(appkeys.DROPBOX['key'], appkeys.DROPBOX['secret'], 'app_folder')
    oauth_token = sess.obtain_request_token()
    #url = 'https://www.dropbox.com/1/oauth/authorize?oauth_token={0}&oauth_callback={1}'.format(dbox.parseToken(oauth_token)[0],'http%3A%2F%2F169.229.99.129:1338/auth/'+ code + '/' + oauth_token.secret)
    url = 'https://www.dropbox.com/1/oauth/authorize?oauth_token={0}&oauth_callback={1}'.format(dbox.parseToken(oauth_token)[0],'http%3A%2F%2F127.0.0.1:8000/auth/'+ code + '/' + oauth_token.secret)
    return redirect(url)

def auth(request, randomValue, secret):
    requestId = request.GET[u'oauth_token']
    print(request.GET)
    #sess.set_token('wjxql0pdnuu9yqn','t2gmb966i7l5wpd')
    sess = session.DropboxSession(appkeys.DROPBOX['key'], appkeys.DROPBOX['secret'], 'app_folder')
    tokens = oauth.oauth.OAuthToken(requestId,secret)  
    access_token = sess.obtain_access_token(tokens)
    MySession = Session.objects.filter(name=randomValue)[0] 
    sessionId = MySession.sessionId
    changedString = str(int(randomValue) + MySession.count) 
    myText = changedString
    User.objects.create(session=MySession,personalFile="",textEditor=myText,accessToken = access_token.key,accessSecret = access_token.secret) 
    print("ACCESS TOKEN IS" + access_token.key)
    return redirect('/study/' + randomValue + '/' + requestId) 

def study(request, randomValue, identifier): 
    server = serverSession()
    fileList = {}
    try:
        server.newFolder('/{0}'.format(randomValue))
    except:
        pass
    fileList = server.listFiles('/{0}'.format(randomValue))
    MySession = Session.objects.filter(name=randomValue)[0]
    sessionId = MySession.sessionId
    changedString = str(int(randomValue) + MySession.count) 
    myText = changedString
    return render_to_response('app.html',RequestContext(request,{"name":randomValue,"sessionId":sessionId,"myText":changedString,"groupText":MySession.textEditor,"files":fileList})) 

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

def serverSession():
    dbox = DropboxService(serverToken, serverSecret)
    return dbox
