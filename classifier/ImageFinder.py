"""
Class to find and retrieve info for random images on Wikimedia Commons
@author: andyw@bbc
"""


class ImageFinder:

    """
    Find and return a random Wikimedia Commons image
    @return: a dictionary containing the filename, url and description of the image
    """
    def find_random_image(self):

        return {
            'filename': '',
            'url': '',
            'description': ''
        }