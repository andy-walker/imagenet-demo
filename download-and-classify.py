"""

Crawler script to download and classify images from Wikimedia Commons,
and save the classification info to a mysql database

"""

from classifier.db.MySQL import Database
from classifier.ImageClassifier import *
from classifier.ImageFinder import *
from classifier.ImageMetadata import *
from classifier.ImageProcurer import *
from classifier.ImageWriter import *

from time import sleep

db = Database()
meta = ImageMetadata(db)

meta.initialize()

while True:

    finder = ImageFinder()
    image = finder.find_random_image()
    exists = meta.image_exists_locally(image.filename)

    if not exists:

        classifier = ImageClassifier()
        procurer = ImageProcurer(image.url)
        writer = ImageWriter()

        image_data = procurer.download_image()
        path_to_image = writer.write_main_image(image_data)
        path_to_thumbnail = writer.write_thumbnail_image(image_data)
        classification = classifier.classify(path_to_image)

        metadata = {
            'filename':       image.filename,
            'image_path':     path_to_image,
            'thumbnail_path': path_to_thumbnail,
            'description':    image.description,
            'classification': classification
        }

        meta.save_metadata(metadata)

    sleep(1)
    break  # for now
