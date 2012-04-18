import appkeys
from dropbox import client, rest, session
from oauth.oauth import OAuthToken
import os
import time

class DropboxService(object):

    lastIndexMetadata = {'modified':''}
    cursor = None

    def __init__(self):
        self.client = None
        self.sess = session.DropboxSession(appkeys.DROPBOX['key'], \
                appkeys.DROPBOX['secret'], 'app_folder')
        self.request_token = self.sess.obtain_request_token()
        self.url = self.sess.build_authorize_url(self.request_token)
        #print "url:", url
        #print "Please visit this website and press the 'Allow' button, then hit 'Enter' here."
        #os.system("xdg-open {0}".format(url))
        #print("Press enter when authentication has completed")
    
    def getToken(self):
        access_token = self.sess.obtain_access_token(self.request_token)
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
        url = self.client.share(path)['url']
        return url

    def shareRef(self, path):
        ref = self.client.create_copy_ref(path)
        return ref['copy_ref']

    def getRef(self, ref, path):
        ref = self.client.add_copy_ref(ref, path)

    def listFiles(self, path):
        lst=[]
        if self.client==None:
            self.getToken()
        metaList = self.client.metadata(path)['contents']
        for data in metaList:
            pair = [None,None]
            pair[0]=data['path'][1:]
            pair[1]=self.getURL(path)
            lst.append(pair)
        return lst

