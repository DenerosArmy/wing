import appkeys
from dropbox import client, rest, session
from oauth.oauth import OAuthToken
import os
import time

class DropboxService(object):

    lastIndexMetadata = {'modified':''}
    cursor = None

    def __init__(self, oauth_token=False, oauth_secret=False):
        self.sess = session.DropboxSession(appkeys.DROPBOX['key'], \
                appkeys.DROPBOX['secret'], 'app_folder')
        if not oauth_token:
            self.client = None
            self.sess = session.DropboxSession(appkeys.DROPBOX['key'], \
                    appkeys.DROPBOX['secret'], 'app_folder')
            self.request_token = self.sess.obtain_request_token()
            self.url = self.sess.build_authorize_url(self.request_token)
            print "Url:", self.url
            print "Please visit this website and press the 'Allow' button"
            #os.system("xdg-open {0}".format(url))
            #print("Press enter when authentication has completed")
        else:
            self.token = oauth_token
            self.secret = oauth_secret
            self.sess.set_token(self.token, self.secret)
            self.client = client.DropboxClient(self.sess)
    
    def genToken(self):
        self.oauth = self.sess.obtain_access_token(self.request_token)
        self.client = client.DropboxClient(self.sess)
        print("Linked account")

    def upload(self, path):
        f = open(path)
        metadata = self.client.put_file(os.path.basename(path), f, True)

    def download(self, local_path, name):
        outFile = open(local_path, 'w')
        f, metadata = self.client.get_file_and_metadata(name)
        outFile.write(f.read())

    def newFolder(self, path):
        self.client.file_create_folder(path)

    def delete(self, path):
        self.client.file_delete(path)

    def changes(self):
        delta = self.client.delta(cursor)
        self.cursor = delta[cursor]
        entries = delta[entries]
        paths = [[],[]]
        #paths[0] are files to be added, paths[1] are to be deleted
        for entry in entries:
            if entry[1] != None:
                paths[0].append(entry[0])
            else:
                paths[1].append(entry[0])
        return paths

    def getURL(self, path): 
        #print(path)
        #url = self.client.media(path)['url']
        #url = "https://www.dropbox.com/s"+url[29:46]+url[56:]
        url = '../../../Dropbox/Apps/Wing'+path
        return url

    def shareRef(self, path):
        ref = self.client.create_copy_ref(path)
        return ref['copy_ref']

    def getRef(self, ref, path):
        ref = self.client.add_copy_ref(ref, path)

    def listFiles(self, path):
        dic = {}
        if self.client==None:
            self.getToken()
        #print(self.client.metadata(path))
        metaList = self.client.metadata(path)['contents']
        for data in metaList:
            dic[data['path'][1:]] = self.getURL(data['path'])
        return dic

    def parseToken(self, access_token):
        #print("Parsing {0}".format(access_token))
        access_token = access_token.__str__()
        access_token = access_token.split('&')
        token = [access_token[1].split('=')[1]]
        token += [access_token[0].split('=')[1]]
        #print("Parsed {0}".format(token))
        return token
