from dropbox/dropbox_wrapper import DropboxService

class Session(object):
    users = []

    def __init__(self, code):
        self.session = session
        self.server = DropboxService()

    def addUser(self, user):
        users.append(user)

    def sync(self, user):
        """
        Syncs one user with the rest of the users. Should be called after one
        user uploads a file.
        """
        paths = user.changes()
        self.server.download()
