import config
import dropbox

class DropboxPictureMover():
    def __init__(self, token):
        self.dbx = dropbox.Dropbox(token)

    def getCurrentAccount(self):
        return self.dbx.users_get_current_account()

if __name__ == '__main__':
    app = DropboxPictureMover(config.app['oauth']['token'])
    print app.getCurrentAccount()
