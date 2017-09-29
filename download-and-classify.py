"""

Crawler script to download and classify images from Wikimedia Commons
and save the classification info to a mysql database - uses Inception v3 and
code from the TensorFlow imagenet example here:

https://github.com/tensorflow/models

:author andyw@bbc

"""

import sys
from time import sleep
from pathlib import Path
from random import randint

from classifier.db.MySQL import Database
from classifier.ImageClassifier import *
from classifier.ImageFinder import *
from classifier.ImageMetadata import *
from classifier.ImageProcurer import *
from classifier.ImageWriter import *

metadata = ImageMetadata(Database())
metadata.initialize()

while True:

    # sleep at the beginning of the loop as there are a few potential exit points, so it makes
    # more sense to do at the beginning - this is just to throttle the requests slightly, to
    # avoid Wikimedia banning our ip and me having a lot of explaining to do.
    sleep(randint(1, 5))

    finder = ImageFinder()
    image = finder.find_random_image()

    if Path(image['filename']).suffix.lower() not in ('.jpg', '.jpeg'):
        print('Skipping ' + image['filename'] + ' (not a jpeg)')
        continue

    if not metadata.exists_locally(image['filename']):

        classifier = ImageClassifier()
        procurer = ImageProcurer(image['url'])
        writer = ImageWriter('/Users/walkea28/imagenet')

        try:

            image_data = procurer.download_image()

            if not image_data:
                continue

            path_to_image = writer.write_main_image(image_data, image['filename'])

            if not path_to_image:
                continue

            path_to_thumbnail = writer.write_thumbnail_image(path_to_image)

            if not path_to_thumbnail:
                continue

        except BaseException as e:

            print('An error occurred downloading the image: {}'.format(image['url']))
            print(str(e))
            continue

        print('Successfully downloaded ' + image['filename'])

        try:
            classification = classifier.classify(path_to_image)
        except ValueError as e:
            print('An exception was raised while analysing the image:')
            print(str(e))
            continue

        data = {
            'filename':       image['filename'],
            'image_path':     path_to_image,
            'description':    image['description'],
            'classification': classification
        }

        metadata.save(data)
        del classifier

    break  # for now
