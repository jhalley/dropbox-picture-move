import config
import dropbox
import time
from pprint import pprint as pp

class DropboxPictureMover():
    def __init__(self, token, camera_upload_folder, bucket_folder, bucket_size, debug_mode = False, move_rate_limit = 0):
        # Init
        self.client = dropbox.client.DropboxClient(token)
        self.camera_upload_folder = camera_upload_folder
        self.bucket_folder = bucket_folder
        self.bucket_size = bucket_size
        self.debug_mode = debug_mode
        self.move_rate_limit = move_rate_limit
        
        # Internal vars
        self.all_pictures = []

    def getCurrentAccount(self):
        return self.client.account_info()

    def getAllPictures(self):
        self.all_pictures = map(lambda x: x['path'], self.client.metadata(self.camera_upload_folder)['contents'])

        # Debug message
        if self.debug_mode:
            print 'Total number of pictures in Camera Uploads: %s'%len(self.all_pictures)

        return self.all_pictures

    # We need to be smarter and check if we've already gotten the list so we don't have to call the api again
    # Actually, this doesn't make sense. Just call it again with getAllPictures and do a count from the return
    #def getCountOfPictures(self):
    #    return len(self.client.metadata(self.camera_upload_folder)['contents'])

    def createPictureBucket(self, start_file, end_file):
        bucket_name = '%s/%s to %s (%s pics)'%(
            self.bucket_folder,
            start_file.split('/')[-1].rsplit('.', 1)[0],
            end_file.split('/')[-1].rsplit('.', 1)[0],
            self.bucket_size
        )

        # Create bucket in dropbox
        self.client.file_create_folder(bucket_name)

        # Debug message
        if self.debug_mode:
            print 'Creating bucket: %s'%(bucket_name)

        # return bucket name
        return bucket_name

    def movePicsToBucket(self):
        # Get all pictures
        self.getAllPictures()

        while len(self.all_pictures) > self.bucket_size:
            curr_bucket = []
            # Get names of pictures to put in bucket
            for i in range(self.bucket_size):
                curr_bucket.append(self.all_pictures.pop(0))

            # Create bucket folder
            bucket_name = self.createPictureBucket(curr_bucket[0], curr_bucket[-1])

            # Move pictures
            while len(curr_bucket) > 0:
                move_pic = curr_bucket.pop(0)

                # Debug message
                if self.debug_mode:
                    print 'Moving: %s (%s remaining)'%(move_pic, len(curr_bucket))

                self.client.file_move(move_pic, '%s/%s'%(bucket_name, move_pic.split('/')[-1]))

                # Apply rate limits if provided
                time.sleep(self.move_rate_limit)


if __name__ == '__main__':
    app = DropboxPictureMover(config.app['oauth']['token'], '/Camera Uploads', '/pic_buckets', 500, debug_mode = True, move_rate_limit = 1)
    print app.movePicsToBucket()
    #print app.createPictureBucket('a', 'b')
    #pp(app.getAllPictures())
    #print app.getCountOfPictures()
    #print app.getCurrentAccount()
