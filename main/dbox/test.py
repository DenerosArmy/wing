from dbox_wrapper import DropboxService
from dropbox import client, rest, session
import appkeys

def main():
    """
    sess = session.DropboxSession(appkeys.DROPBOX['key'], appkeys.DROPBOX['secret'], 'app_folder')
    request_token = sess.obtain_request_token()
    url = sess.build_authorize_url(request_token)
    print(url)
    raw_input()
    access_token = sess.obtain_access_token(request_token)
    user = client.DropboxClient(sess)
    access_token = access_token.__str__()
    access_token = access_token.split('&')
    token = [access_token[0].split('=')[1]]
    token += [access_token[1].split('=')[1]]
    print(token)
    """
    
    dbox = DropboxService()
    print(dbox.url)
    raw_input()

    dbox.genToken()
    
    dbox.upload('test/wing.gif')
    print("File uploaded")
    dbox.download('test/testfile_downloaded.gif', 'wing.gif')
    print("File downloaded")

    ref = dbox.shareRef('wing.gif')
    print(ref)
    print(dbox.listFiles('.'))

    print("Testing new session based on access token")
    
    dbox2 = DropboxService(dbox.oauth)
    print("New session intialized")
    print(dbox2.listFiles('.'))



main()
