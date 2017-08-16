from PIL import Image
from io import BytesIO
from resizeimage import resizeimage
from os import path

class ImageWriter:

    def __init__(self, image_dir):
        self.image_dir = image_dir

    def write_main_image(self, image_data, filename):

        path = self.image_dir + '/originals/' + filename
        image = Image.open(BytesIO(image_data))
        image.save(path)
        return path

    def write_thumbnail_image(self, path_to_image):

        thumbnail_path = self.image_dir + '/thumbnails/' + path.basename(path_to_image)

        try:

            with open(path_to_image, 'r+b') as f:
                with Image.open(f) as image:
                    cover = resizeimage.resize_cover(image, [200, 120], validate=False)
                    cover.save(thumbnail_path, image.format)

        except BaseException as e:
            # any problems? just ignore them .. so a bit like my old boss in that respect
            print('Something went a bit wrong saving the thumbnail')
            print(str(e))
            return ''

        return thumbnail_path

