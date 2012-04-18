from dropbox/dropbox_wrapper import DropboxService

class User(object):

    def __init__(self, session):
        self.dropbox = DropboxService()
        self.session = session

    def upload(self, path):
        for users in self.session.users:
            user.dropbox.upload(path)

    def delete(self, path):
        for users in self.session.users:
            user.dropbox.delete(path)

