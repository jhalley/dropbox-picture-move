import config
import dropbox
from pprint import pprint as pp

class DropboxPictureMover():
    def __init__(self, token):
        self.client = dropbox.client.DropboxClient(token)

    def getCurrentAccount(self):
        return self.client.account_info()

    def getAllPicturesInCameraUploads(self):
        return map(lambda x: x['path'], self.client.metadata('/Camera Uploads')['contents'])

    def getCountOfPicturesInCameraUploads(self):
        return len(self.client.metadata('/Camera Uploads'))

if __name__ == '__main__':
    app = DropboxPictureMover(config.app['oauth']['token'])
    print app.getAllPicturesInCameraUploads()
    #print app.getCountOfPicturesInCameraUploads()
    #print app.getCurrentAccount()
