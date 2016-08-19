import config
import dropbox
from pprint import pprint as pp

class DropboxPictureMover():
    def __init__(self, token, camera_upload_folder, bucket_folder):
        self.client = dropbox.client.DropboxClient(token)
        self.camera_upload_folder = camera_upload_folder
        self.bucket_folder = bucket_folder

    def getCurrentAccount(self):
        return self.client.account_info()

    def getAllPicturesInCameraUploads(self):
        return map(lambda x: x['path'], self.client.metadata(self.camera_upload_folder)['contents'])

    def getCountOfPicturesInCameraUploads(self):
        return len(self.client.metadata(self.camera_upload_folder)['contents'])

    def createPictureBucket(self, start_file, end_file):
        return self.client.file_create_folder('%s/%s-%s'%(self.bucket_folder, start_file, end_file))

if __name__ == '__main__':
    app = DropboxPictureMover(config.app['oauth']['token'], '/Camera Uploads', '/pic_buckets')
    print app.createPictureBucket('a', 'b')
    #print app.getAllPicturesInCameraUploads()
    #print app.getCountOfPicturesInCameraUploads()
    #print app.getCurrentAccount()
